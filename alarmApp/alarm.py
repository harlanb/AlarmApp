#!/usr/bin/env python3

import os
import sys
import pause
import datetime
import random
import argparse
import subprocess
import _thread
import time
#import pygame
import pyglet

#
# Variables
#
#mediaPlayer="/usr/bin/omxplayer"
mediaPlayer="/usr/bin/mpg123"
#songsPath="~/Music"
songsPath="/home/pi/Music"
songsList=[]
alarmDateTime=""
duration=0
commandLine=[]
song=0

#
# Parameters:
#   Date/Time to run alarm
#   Directory to play files from
def parseParams():

    parser = argparse.ArgumentParser(description='Play music at a specified Date/Time')
    parser.add_argument('alarmDateTime', action="store", help="Date/Time to run alarm - Format: mm/dd/yyy hh:mm" )
    parser.add_argument('duration', action="store", help="Amount of time in minutes for alarm to run" )

    args = parser.parse_args()
    duration = int(args.duration)
    print("args = %s" %(args.alarmDateTime))
    return args.alarmDateTime, duration

def getSongsList(songdir):
    #
    # Get list of playable songs and the total count
    #
    #fileExtList = ".ogg"
    fileExtList = ".mp3"
    dirList = [os.path.normcase(f)
        for f in os.listdir(songdir)]
    songsList = [os.path.join(songdir, f) 
        for f in dirList
            if os.path.splitext(f)[1] in fileExtList]
    print("(get)songsList = %s" %(songsList))
    return songsList

def playMusic(endTime):
    # working, messes up command line
    songsList=getSongsList(songsPath)
    songsCount = len(songsList)
    print("songsCount = %s" %(songsCount))
    song = random.randrange(songsCount)
    commandLine=[]
    commandLine.append(mediaPlayer)
#    commandLine.append("--no-keys")
    commandLine.append(songsList[song])
    print("commandLine = %s" %(commandLine))

    song = random.randrange(songsCount)
    print("song = %s" %(song))

    keepPlaying=True

    while(keepPlaying):
        print("play song = %s" %(songsList[song]))

#        #song = pyglet.media.load(songsList[song])
#        song = pyglet.media.load("/home/pi/Music/test01.ogg")
#        song.play()
#        pyglet.app.run()

#        pygame.mixer.init()
#        pygame.mixer.music.load(songsList[song])
#        pygame.mixer.music.play()
#        while pygame.mixer.music.get_busy() == True:
#            continue

        proc = subprocess.Popen(commandLine) 
        try:
             time.sleep(1)
             outs, errs = proc.communicate()
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        song = random.randrange(songsCount)
        commandLine = []
        commandLine.append(mediaPlayer)
        commandLine.append(songsList[song])
        print("commandLine = %s" %(commandLine))

        if (datetime.datetime.today() >= endTime):
            keepPlaying=False

def main():
    alarmDateTime, duration = parseParams()
    print("alarmDateTime = %s" %(alarmDateTime))

    datetime_object = datetime.datetime.strptime(alarmDateTime, '%m/%d/%Y %H:%M:%S')

    waittime = datetime.datetime(datetime_object.year, datetime_object.month, datetime_object.day, datetime_object.hour, datetime_object.minute, 0, 0)
    pause.until(waittime)

    endTime=datetime.datetime.today() + datetime.timedelta(minutes=duration)
    print("duration = " + str(duration) )
    print("endTime = " + endTime.strftime('%m/%d/%Y %H:%M:%S') )
    playMusic(endTime)

#    # Create two threads as follows
#    try:
#       _thread.start_new_thread( playMusic )
#    except:
#       print ("Error: unable to start thread")
#
#    time.sleep(30)
#    sys.exit(1)

if __name__ == "__main__":
    main()

