# command :-   python3 echo_bidirectional.py --port 8080 --stream_typ bidirectional
import io
import re
import sys
import argparse
import time
import websockets
import asyncio
from threading import Thread

from google.cloud import speech_v1p1beta1 as speech
import base64
import json
import signal
import logging
import threading
import google_doc_helper

from flask import Flask
from flask_sockets import Sockets
from six.moves import queue
from threading import Thread
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from random import randint

from google.oauth2.service_account import Credentials

credentials = Credentials.from_service_account_file('google_app_creds.json')
app = Flask(__name__)
sockets = Sockets(app)

def signal_handler(sig, frame):
    sys.exit(0)

def listen_print_loop(responses, doc_id):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    print(num_chars_printed)
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript
        print(transcript)

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        service = google_doc_helper.authenticate('DOC')
        #google_doc_helper.write_to_doc(service, doc_id, '\n' + transcript)

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            if randint(0,101) % 2 == 0:
                #google_doc_helper.delete_from_doc(service, doc_id, 1, len(transcript+overwrite_chars))
                google_doc_helper.write_to_doc(service, doc_id, '\n' + transcript + overwrite_chars)
                #google_doc_helper.delete_from_doc(service, doc_id, 1, len(transcript+overwrite_chars))

            num_chars_printed = len(transcript)


        else:
            # print(transcript + overwrite_chars)
            #service = google_doc_helper.authenticate('DOC')
            #google_doc_helper.write_to_doc(service, doc_id, transcript + overwrite_chars)
            #google_doc_helper.delete_from_doc(service, doc_id, len(transcript+overwrite_chars))

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0


class Stream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self.buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self.buff.put(None)

    def fill_buffer(self, in_data):
        """Continuously collect data from the audio stream, into the buffer."""
        self.buff.put(in_data)
        return self

    def generator(self):
        while True:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self.buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

# @sockets.route('/media')
async def echo(websocket):
    print(websocket)
    ws=websocket
# websocket.receive
    app.logger.info("Connection accepted")
    # A lot of messages will be sent rapidly. We'll stop showing after the first one.
    has_seen_media = False
    has_started_uni = False
    message_count = 0
    while not ws.closed:
        message = await ws.recv()

        
        if message is None:
            app.logger.info("No message received...")
            continue

        # Messages are a JSON encoded string
        data = json.loads(message)
        # print(data)
        # Using the event type you can determine what type of message you are receiving
        if data['event'] == "connected":
            app.logger.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            app.logger.info("Start Message received: {}".format(message))

            local_stream = Stream(RATE, CHUNK)
            if args.stream_type == "unidirectional":
                print("UNIDIRECTIONAL STREAM")
                # thread_map[data['stream_sid']] = {'thread': threading.Thread(target=stream_transcript, args=(ws, data['stream_sid'], local_stream)), 'stream': local_stream}
                thread_map[data['stream_sid']] = {'stream': local_stream}
                asyncio.create_task(stream_transcript(ws, data['stream_sid'], local_stream))

            elif args.stream_type == "bidirectional":
                print("BIDIRECTIONAL STREAM")
                # thread_map[data['stream_sid']] = {'thread': threading.Thread(target=stream_playback, args=(ws, data['stream_sid'], local_stream)), 'stream': local_stream}
                thread_map[data['stream_sid']] = {'stream': local_stream}
                asyncio.create_task(stream_playback(ws, data['stream_sid'], local_stream))
        if data['event'] == "media":
            payload = data['media']['payload']
            # print(payload)
            chunk = base64.b64decode(payload)
            local_stream = thread_map[data['stream_sid']]['stream']
            local_stream.fill_buffer(chunk)

            if not has_seen_media and args.stream_type == "bidirectional":
                t2 = threading.Thread(target=stream_playback, args=(ws, data['stream_sid'],local_stream))
                t2.daemon = True
                t2.start()
                app.logger.info("Media message: {}".format(message))
                app.logger.info("Payload is: {}".format(payload))
                app.logger.info("That's {} bytes".format(len(chunk)))
                app.logger.info("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "dtmf":
            app.logger.info("dtmf Message received: {}".format(message))
        if data['event'] == "mark":
            app.logger.info("Mark Message received: {}".format(message))
        if data['event'] == "stop":
            app.logger.info("Stop Message received: {}".format(message))
            break
        message_count += 1

    app.logger.info("Connection closed. Received a total of {} messages".format(message_count))

async def stream_transcript(ws, call_sid, stream):
    print('reached to stream transcript  ',  call_sid)
    service = google_doc_helper.authenticate('DRIVE')
    # print(service)
    doc_id = google_doc_helper.get_google_doc_id(service, call_sid)
    # print(doc_id)
    # if doc_id is None:
    #     return
    while not ws.closed:
        audio_generator = stream.generator()
        print(audio_generator)
        try:
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            responses = client.streaming_recognize(streaming_config, requests)
            print(responses)
            # Now, put the transcription responses to use.
            listen_print_loop(responses, doc_id)
        except:
            pass
        await asyncio.sleep(2)

async def stream_playback(ws, stream_sid, stream):
    print("COMING TO PLAYBACK")
    while not ws.closed:
        audio_generator = stream.generator()
        try:
            for content in audio_generator:
                # print(base64.b64encode(content).decode("ascii"))
                d = json.dumps({
                    'event': 'media',
                    'stream_sid': stream_sid,
                    'media': {
                        'payload': base64.b64encode(content).decode("ascii")
                    }
                })
                await asyncio.sleep(0.25)
                # print(d)
                await ws.send(d)
                # await ws.send('test')

                await asyncio.sleep(0.25)
        except:
            pass

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='ExoWS client to enable WS communication')
    parser.add_argument('--port', type=int, default=5000, help='Specify the port on which WS server should be listening')
    parser.add_argument('--stream_type', type=str, required=True, choices=['unidirectional', 'bidirectional'], help='Specify the type of stream')
    args = parser.parse_args()
    
    # Audio recording parameters
    RATE = 8000
    CHUNK = int(RATE / 10)  # 100ms

    HTTP_SERVER_PORT = args.port

    language_code = "en-US"  # a BCP-47 language tag

    client = speech.SpeechClient(credentials=credentials)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_speaker_diarization=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    thread_map = {}

    signal.signal(signal.SIGINT, signal_handler)

    start_server =  websockets.serve(echo, "localhost", args.port)
# sockets = Sockets(start_server)
    asyncio.get_event_loop().run_until_complete(start_server)   
    asyncio.get_event_loop().run_forever()
