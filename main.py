import re
from os import rename
from pytube import YouTube


# pytubes "get_highest_resolution()"" is not working correctly
def get_best_video_res(available_formats):
    format_list = []

    for i in available_formats:
        f = re.search("res=\".*?\"", str(i))
        match = f[0][5:-2]
        format_list.append(int(match))

    return str(max(format_list)) + "p"


def get_best_audio_abr(available_formats):
    format_list = []

    for i in available_formats:
        f = re.search("abr=\".*?\"", str(i))
        match = f[0][5:-5]
        format_list.append(int(match))

    return str(max(format_list)) + "kbps"


def get_tag_from_entry(entry):
    e = re.search("itag=\".*?\"", str(entry))
    match = e[0][6:-1]
    return match


def rename_audio_file(output_type, stream_title):
    input_filename = stream_title + ".webm"
    output_filename =  stream_title + output_type
    rename(input_filename, output_filename)



if __name__ == "__main__":
    url = input("Please enter YouTube Url: ")
    yt = YouTube(url)

    print("1. export to video (mp4)")
    print("2. export to audio (mp3)")

    while True:
        choice = int(input("Please chose your export type (1 for video, 2 for audio): "))
        break

    while True:
        # video
        if choice == 1:
            available_formats = yt.streams.filter(type="video", mime_type="video/webm")
            best_res = get_best_video_res(available_formats)
            highest_stream = available_formats.filter(res=best_res)
            stream_tag = get_tag_from_entry(highest_stream)
            stream = yt.streams.get_by_itag(stream_tag)
            stream.download()
            rename_audio_file(".mp4", yt.title)
            break

        # audio
        elif choice == 2:
            available_formats = yt.streams.filter(type="audio", mime_type="audio/webm")
            best_abr = get_best_audio_abr(available_formats)
            highest_stream = available_formats.filter(abr=best_abr)
            stream_tag = get_tag_from_entry(highest_stream)
            stream = yt.streams.get_by_itag(stream_tag)
            stream.download()
            rename_audio_file(".mp3", yt.title)
            break

        else:
            print("\nInvalid intput")
