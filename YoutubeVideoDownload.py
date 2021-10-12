from pytube import YouTube
from pytube.cli import on_progress

url = input("Please paste your URL :  ")

yt=YouTube(url, on_progress_callback=on_progress)
count=0
print("Video Name : ",yt.title)
print("Video Length : ",yt.length/60,"Minute")
for i in yt.streams:
    ll=str(i)
    if 'acodec' in ll:
        res_number=ll.find('res=')
        last_number=ll.find('p',res_number+5)
        total=res_number+5
        resolution=ll[total:last_number]
        try:
            byte=yt.streams.get_by_resolution(resolution=resolution+'p').filesize
            in_kb=byte//1024
            in_mb=in_kb//1024
            size=(str(in_mb)+' MB')
        except AttributeError:
            size='Not Available'

        print(count , ' : ', resolution, " : ", size )
        # print(resolution)
    count+=1
got=int(input("Please enter value : "))
yt=yt.streams[got].download("/home/exotel/Videos/Youtube")


# print(yt.streams.get_highest_resolution().filesize)
# print(yt.streams.get_by_resolution('720').filesize)




