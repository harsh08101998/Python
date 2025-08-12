from pydub import AudioSegment
# sound = AudioSegment.from_wav("output.mp3")
# sound = sound.set_channels(1)
# sound.export("path.mp3", format="mp3")

src = "tenderness.mp3"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")