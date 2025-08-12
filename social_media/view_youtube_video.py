import webbrowser
import os 
import time
# YouTube video URL
count=0
for i in range(1,100000):
    list=['https://www.youtube.com/watch?v=cgeQ6VMhjuo','https://www.youtube.com/watch?v=AX4a7OWX3j0','https://www.youtube.com/watch?v=fc6jNXg28TA','https://www.youtube.com/watch?v=eLX8xP7SA9s']
    video_url = ""  # Replace VIDEO_ID with the actual video ID
    for j in list:
        for i in range(1,40):
        # Open the video in the web browser
            media_link =str(j)
            webbrowser.open(media_link)

        print('All video played',' :- ',count)
        time.sleep(30)
        browserExe = "firefox" 
        os.system("pkill "+browserExe) 
    count+=1