from tinydb import TinyDB, Query
from datetime import date
import time
import matplotlib.pyplot as plt

db_fin = TinyDB('db_production.json')
db_test = TinyDB('db_test.json')
User = Query()

def writeToDb(_db, _date, _activity, _time):
    # skriver till databasen, val av databas och variabler kommer från intro samt registrator
    # skapar en lista med dictionaries, en dictionary för varje registreringstillfälle
    _db.insert({'date': _date, 'activity': _activity, 'time spent': _time})

def registrator(_db):
    # ifyllnad av aktivitet, tid, samt registrerande av datum
    # presenterar även resultatet avseende aktuell aktivitet
    _date = date.today().strftime("%d/%m/%Y")
    activity = input('Enter activity: ')
    time = int(input('Enter time spent: '))
    writeToDb(_db, _date, activity, time)
    print('Registration complete ')
    searcherTime(_db.search(User['activity'] == activity), activity)
    searcherDate(_db.search(User['activity'] == activity))

def searcherTime(_resultTime, _activity):
    # visa tid för aktivitet som eftersökts
    _totalTime = 0
    for i in range(len(_resultTime)):
        _timePerActivity = (_resultTime[i]['time spent'])
        _totalTime = _totalTime + int(_timePerActivity)
    print('You have spent ' + str(_totalTime) + ' minutes doing ' + str(_activity) + ' over ' + str(len(_resultTime)) + ' registrations. ')
    
def searcherDate(_resultDate):
    # visa datum från första tillfället till det senaste för aktivitet som eftersökts
    print('First date: ' + str(_resultDate[0]['date']) + ' last date: ' + str(_resultDate[-1]['date']))

def dateList(_resultDateList):
    # funktion för att se alla datum som registrerats, huvudsakligen för debugging
    dates = []
    for i in range(len(_resultDateList)):
        dates.append(_resultDateList[i]['date'])
    print(dates)
        
def debug(_resultDebug, _debug):
    # funktion för att se all data i databasen
    print(_resultDebug)

def searcherPlot(_resultOfSearch):
    # visa upp resultatet visuellt med hjälp av matplotlib
    dates = []
    time_dates = []
    for i in range(len(_resultOfSearch)):
        if _resultOfSearch[i]['date'] in dates:
            last_time_date = int(time_dates[-1])
            time_dates.append(last_time_date + _resultOfSearch[i]['time spent'])
            time_dates.pop(-2)
            pass
        else:
            dates.append(_resultOfSearch[i]['date'])
            time_dates.append(_resultOfSearch[i]['time spent'])
    print(dates)
    print(time_dates)
    labels = dates
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(labels, time_dates, label='time per day')
    ax.set_ylabel('time')
    ax.set_title('time spent per day')
    ax.legend
    plt.show()

def baseSearch(_db, _term):
    # huvudfunktionen, tar emot sökterm och databas och ger _resultOfSearch som används i andra funktioner
    # styr även valet av visuell presentering av data och avslutar även programmet.
    # om visuell presentering av data väljs stängs programmet ned 1 sek efter att den visuella presentationen avslutats
    _resultOfSearch = _db.search(User['activity'] == _term)
    if len(_resultOfSearch) == 0:
        print('I have got no records of that activity')
        time.sleep(.8)
        newSearch = input('Wanna try again? Press 2 for a doing a new search ')
        if newSearch == '2':
            baseSearch(_db, input('What term do you want to search for? '))
        else:
            print('Killing everything')
            quit
    else:    
        searcherTime(_resultOfSearch, _term)
        searcherDate(_resultOfSearch)
        _viewplot = input('Press 1 to view plot, anything else to pass: ')
        if _viewplot == '1':
            searcherPlot(_resultOfSearch)
            time.sleep(1)
        else:
            print('Alright hombre, see you next time.')
            time.sleep(1)
        #debug(_resultOfSearch, _term)
        #dateList(_resultOfSearch)
    
def intro():
    # inledande funktion, val av databas samt inhämtande av sökord som ges till baseSearch
    _dbChoice = input('Press 1 for product DB, press 2 for test DB: ')
    if _dbChoice == '1':
        _db = db_fin
    if _dbChoice == '2':
        _db = db_test
    _selection = input('Press 1 for new registration, press 2 for search: ')
    if _selection == '1':
        registrator(_db)
    elif _selection == '2':
        baseSearch(_db, input('What term do you want to search for? '))
    else:
        print('Brr brr please wait while killing everything')
        quit

intro()
