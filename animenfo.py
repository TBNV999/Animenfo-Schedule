#The schedule of animeNfo radio

import sys, os, datetime

import requests
from bs4 import BeautifulSoup


def cls():

    #for windows
    if os.name == "nt":
        command = "cls"

    #other os 
    else:
        command = "clear"

    os.system(command)
    

def color(l):

    red = '\033[31m'
    default = '\033[0m'
    l[0] = red + l[0] + default

    return l


def form_data(data):
    
    data = data.replace('\"',"")
    data = data.replace('href',"")
    data = data.replace('amp;',"")

    return data


def form_series_data(series):

    series=series.replace('<div class="span2 seriestag"',"")
    series=series.replace("</div>","")
    series=series.replace("\n","")
    series=series.replace("\t","")
    series=series.replace(">","")
    series=series.replace("href","")
    series=series.replace("\xa0"," ")
    series=series.replace("amp;","")

    return series


def display_time():

    now = datetime.datetime.now()

    hour = now.hour
    minute = now.minute
    second = now.second

    if hour < 10:
        hour = "0" + str(hour)

    if minute < 10:
        minute = "0" + str(minute)

    if second < 10:
        second = "0" + str(second)

    print("now - {}:{}:{} ".format(hour, minute, second), end="\n\n")


def display_coming_up(source):

    schedule= source.find_all(class_="span5")
    raw_series_list = source.find_all(class_="span2 seriestag")

    schedule.pop(0)
    
    songs = []

    for song in schedule:
        splited_data = str(song).split("=")
        songs.append(splited_data[3])

    artist_list = []
    title_list = []

    for song in songs:

        splited_song = song.split(" - ")

        artist = form_data(splited_song[0])

        title = form_data(splited_song[1])
        
        artist_list.append(artist)
        title_list.append(title)


    series_list = []

    for series in raw_series_list:
        series = form_series_data(str(series))
        series_list.append(series)
    
    print("")
    print("Coming up:")
    print("Artist - Title - Series")

    for i in range(5):

        try:

            if series_list[i] == " ":
                series_list[i] = "N/A"

            print("{} - {} - {}".format(artist_list[i],title_list[i],series_list[i]))    

        except IndexError:
            sys.exit()


def main():

    cls()
    display_time()
    
    res = requests.get('https://www.animenfo.com/radio/nowplaying.php')

    if res.status_code != 200:
        print("Connection Error!")
        sys.exit()

    source = BeautifulSoup(res.text, "lxml")
    schedule = source.find(id='schedule_container').get_text()

    schedule = schedule.splitlines()

    #remove needless elements
    schedule.pop(2)
    schedule.pop(4)
    schedule.pop(1)
    schedule.pop(0)

    print("Currently on schedule:")

    for element in schedule:
        print(element)

    print("Now playing:")

    song_data = source.find(class_="span6").get_text().splitlines()
    artist = color(song_data[1].split(":"))

    #exist circle handling 
    #not Title
    if song_data[5][0] != 'T': 
        title = song_data[3].split(':')

    else:
        title  = song_data[2].split(':')

    #exist circle handling
    #not Series
    if song_data[5][0] != "S":
        series = song_data[6].split(':')

    else:
        series = song_data[5].split(':')
    
    title = color(title)
    series = color(series)

    song_data[1] = ':'.join(artist)
    song_data[2] = ':'.join(title)
    song_data[5] = ':'.join(series)

    song_data.pop(0)
    song_data.pop(2)
    song_data.pop(4)

    for data in song_data:
        print(data)

    display_coming_up(source)


if __name__ == "__main__":
    main()
