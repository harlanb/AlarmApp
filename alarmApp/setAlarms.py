#!/usr/bin/env python3

import sqlite3
import string
import datetime
import argparse
import subprocess

dateArray=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
alarmArray=[]
todaytomorrow=0
dayofweek=0
#tomorrow=new datetime()

alarmCmd = "/home/pi/alarmApp/alarm.py"

#
# Parameters:
#   Run Today or Tomorrow
def parseParams():

    todaytomorrow=0

    parser = argparse.ArgumentParser(description='Play music at a specified Date/Time')
    parser.add_argument('--today', action="store_true", help="Process using today's date" )
    parser.add_argument('--tomorrow', action="store_true", help="Process using tomorrow's date" )

    args = parser.parse_args()
    if args.today:
        todaytomorrow=0
    if args.tomorrow:
        todaytomorrow=1
    return todaytomorrow

def getDayOfWeek(todaytomorrow):
    # One important thing to note is that in JavaScript 0 = Sunday, Python starts with 0 = Monday. Something that I ran into, front-end vs back-end..
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=todaytomorrow)
    print(tomorrow)
    #datetime_object = datetime.datetime.strptime(string(tomorrow), '%m/%d/%Y')
    weekday=tomorrow.weekday()
    dayofweek=dateArray[weekday]
    print(dayofweek)
    return dayofweek, tomorrow

def getAlarmList(dayofweek, date_object):

    conn = sqlite3.connect('/home/pi/alarmApp/db.sqlite3')

    c = conn.cursor()

    sqlStmt='SELECT alarmtime, duration FROM alarmclock_recurring where ' + dayofweek +'= 1'
    for row in c.execute(sqlStmt):
        alarmDate=date_object + ' ' + row[0]
        alarmArray.append([alarmDate,row[1]])
    print (alarmArray)

    #c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #print(c.fetchall())

    # Save (commit) the changes
    #conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return alarmArray

def scheduleAlarms(alarmArray):


    for alarmRow in alarmArray:
        alarmTime=alarmRow[0]
        duration=str(alarmRow[1])

        # Check to make sure we're not past the alarm start time
        checktime = datetime.datetime.strptime(alarmTime, "%m/%d/%Y %H:%M:%S")
        if (datetime.datetime.today() < checktime):

            commandLine = []
            commandLine.append(alarmCmd)
            commandLine.append(alarmTime)
            commandLine.append(duration)
            print("commandLine = %s" %(commandLine))
            proc = subprocess.Popen(commandLine)

#        try:
#             time.sleep(1)
#             outs, errs = proc.communicate()
#        except TimeoutExpired:
#            proc.kill()
#            outs, errs = proc.communicate()

def main():
    todaytomorrow = parseParams()
    dayofweek, tomorrow = getDayOfWeek(todaytomorrow)
    date_object = tomorrow.strftime('%m/%d/%Y')
    print(date_object)
    alarmList = getAlarmList(dayofweek, date_object)
    print(alarmList)
    scheduleAlarms(alarmList)

if __name__ == "__main__":
    main()

