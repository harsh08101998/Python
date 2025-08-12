import io
import re
import sys
import argparse
import time
import websockets
import asyncio
from google.cloud import speech_v1p1beta1 as speech
import base64
import json
import signal
import logging
import threading

from flask import Flask
from flask_sockets import Sockets
from six.moves import queue
from threading import Thread
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)
# PORT = 3000

def signal_handler(sig, frame):
    sys.exit(0)

def listen_print_loop(responses):
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

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

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
async def echo(websocket, path):
    ws=websocket
    print("A client just connected")
    has_seen_media = False
    # print(ws)
    async for message in websocket:
        data = json.loads(message)
        # print(data)
    # while not ws.closed:
    #     websocket.receive()
    #     message = ws.receive()

    # for message in websocket:
    #     hh=message
        # data = json.loads(message)

        # Using the event type you can determine what type of message you are receiving
        if data['event'] == "connected":
            app.logger.info("Connected Message received: {}".format(message))
        if data['event'] == "start":
            app.logger.info("Start Message received: {}".format(message))
            local_stream = Stream(RATE, CHUNK)
            if args.stream_type == "unidirectional":
                thread_map[data['stream_sid']] = {'thread': threading.Thread(target=stream_transcript, args=(data['stream_sid'], local_stream)), 'stream': local_stream}
            elif args.stream_type == "bidirectional":
                thread_map[data['stream_sid']] = {'thread': threading.Thread(target=stream_playback, args=(ws, data['stream_sid'], local_stream)), 'stream': local_stream}
        if data['event'] == "media":
            payload = data['media']['payload']
            chunk = base64.b64decode(payload)
            hex_payload = chunk.hex()
            # print(hex_payload)   ##  to pring leg1 media event
            # Print the hexadecimal representation
            # app.logger.info("Payload in hex: {}".format(hex_payload))
            local_stream = thread_map[data['stream_sid']]['stream']
            local_stream.fill_buffer(chunk)
            if not has_seen_media and args.stream_type == "bidirectional":
                curr_thread = thread_map[data['stream_sid']]['thread']
                curr_thread.daemon = True
                curr_thread.start()
                app.logger.info("Media message: {}".format(message))
                app.logger.info("Payload is: {}".format(payload))
                app.logger.info("That's {} bytes".format(len(chunk)))
                app.logger.info("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "mark":
            app.logger.info("Mark Message received: {}".format(message))
        if data['event'] == "stop":
            app.logger.info("Stop Message received: {}".format(message))
            break
        # message_count += 1

    # app.logger.info("Connection closed. Received a total of {} messages".format(message_count))

def stream_transcript(ws,stream_sid, stream):
    while True:
        audio_generator = stream.generator()
        print(stream)
        try:
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            responses = client.streaming_recognize(streaming_config, requests)
            # Now, put the transcription responses to use.
            # print(f'Transcript for stream({stream_sid})')
            print(responses)
            listen_print_loop(responses)
        except:
            pass
        time.sleep(5)

def stream_playback(ws, stream_sid, stream):
    print("reached to playback")
    
    while not ws.closed:
        try:
            chunkSize = 32000
            with open(f'output_8k.wav', 'rb') as f:
                file = base64.b64encode(f.read()).decode("ascii")
                # print(file)
                i=0
                count=0
                while count < 6:
                    file1 = file[i:i+chunkSize]
                    d = json.dumps({
                        'event': 'media',
                        'stream_sid': stream_sid,
                        'media': {
                        'payload': file1
                        }
                    })

                    asyncio.run(ws.send(d))
                    # time.sleep(2)
                    # m = json.dumps({
                    #     'event': 'marked',
                    #    'stream_sid': stream_sid,
                    #     'mark': {
                    #     'name': 'played the long sample audio msg',
                    #     'timestamp': str(time.time())
                    #     }
                    # })
                    #print(f'Sent MARK msg on stream: {data["stream_sid"]}')
                    # asyncio.run(ws.send(m))
                    i=i+chunkSize
                 #   time.sleep((chunkSize/(16000))-0.1)
                    if(len(file) <= i):
                        i=0
                        count=count+1
                        # time.sleep(5)
                # break

        # print(stream)
            # audio_generator = stream.generator()
            # try:
            #     for content in audio_generator:
            #         d = json.dumps({
            #             'event': 'media',
            #             'stream_sid': stream_sid,
            #             'media': {
            #                 'payload': base64.b64encode(content).decode("ascii")
            #             }
            #         })
            #         time.sleep(0.20)
            # except:
                # pass
                    # await asyncio.sleep(0.20)
    #             # print(d)
                
    #             asyncio.run(ws.send(d))
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

    language_code = "en-IN"  # a BCP-47 language tag

    client = speech.SpeechClient()
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


    # server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    # print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    # print("Route for media: http://localhost:" + str(HTTP_SERVER_PORT))
    # # server.serve_forever()
    # server =  websockets.serve(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)    
    # # server.run_forever()
    # get_event_loop().run_until_complete(start_server)
    # sockets = Sockets(start_server)
