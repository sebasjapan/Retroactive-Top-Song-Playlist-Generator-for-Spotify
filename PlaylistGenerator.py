import json
import requests

# fill in with your user specific information
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/{user}/playlists"
ACCESS_TOKEN = "PASTE YOUR ACCESS TOKEN HERE"

def create_playlist_on_spotify(name, public):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"

        },
        json={
            "name":name,
            "public":public
        }
    )
    json_resp = response.json()

    return json_resp

def add_song_to_playlist(track, playlist):

    ADD_TRACKS = "https://api.spotify.com/v1/playlists/" + playlist + "/" + track

    response = requests.post(
        ADD_TRACKS,
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"

        },
        json={
            "track":track,
            "playlist":playlist
        }
    )
    json_resp = response.json()

    return json_resp

# returns whether a specific time resides within a given time interval
def isBetween(time, start, end):

    isBetween = False

    start_month = int(start[0:2])
    start_day = int(start[3:5])
    start_year = int(start[6:10])

    end_month = int(end[0:2])
    end_day = int(end[3:5])
    end_year = int(end[6:10])

    current_month = int( timeStamp[5:7] )
    current_day = int(timeStamp[8:10])
    current_year = int(timeStamp[0:4])
    time =  str(current_month) + "/" + str(current_day) + "/" + str(current_year)  


    # if timestamp year is greater than start year and less than end year then we know its in range
    if current_year > start_year and current_year < end_year:
        isBetween = True
    
    # likewise if its outside of these ranges for years, we instantly know its in range
    if current_year < start_year or current_year > end_year:
        isBetween = False

    # it gets trickier in all other cases:

    # if the timestamp year is the same as the start year but less than the end
    if current_year == start_year and current_year < end_year:
        # if timestamp month is greater than start month then we instantly know its in range
        if current_month > start_month:
            isBetween = True
        # if ts month is less than start month, we instantly know its not in range (no work needed)
        # if ts month is the same then we compare days
        if current_month == start_month:
            if current_day >= start_day:
                isBetween = True

    # if timestamp year is the same as the end year but greater than the start year
    if current_year > start_year and current_year == end_year:
        # same code as last if block but reversed
        if current_month < start_month:
            isBetween = True
        if current_month == start_month:
            if current_day <= end_day:
                isBetween = True

    # if timestamp year is in the same year as start and end year
    if current_year == start_year and current_year == end_year:
        # if ts month is greater than start month and less than end month we know its in range
        if current_month > start_month and current_month < end_month:
            isBetween = True
        # if ts month outside of the month range, then its obviously not in the range
        if current_month < start_month or current_month > end_month:
            isBetween = False
        # if ts month is the same as the start month but less than the end month then we have to rely on days
        if current_month == start_month and current_month < end_month:
            # if ts day greater than or equal to start day then it must be true
            if current_day >= start_day:
                isBetween = True
        # if ts month is the same as the end month but more than the start month then we have to rely on days
        if current_month > start_month and current_month == end_month:
            # if ts day less than or equal to end day then it must be true
            if current_day <= end_day:
                isBetween = True
        # if ts month is equal to both start and end months (range < 1 month) then we rely on days
        if current_month == start_month and current_month == end_month:
            # if the day is between the range of days given, then we know its in range
            if current_day >= start_day and current_day <= end_day:
                isBetween = True

    return isBetween

# given a number of milliseconds, timeString returns a string in terms of minutes, hours, or days 
def timeString(popped):
    returnStr = ""
    t = popped[1]
    if t < 3600000:
        returnStr = str(t/60000) + " minutes"
    if t > 3600000:
        returnStr = str(t/3600000) + " hours"
    if t > 3600000*24:
        returnStr = str(t/(24*3600000)) + " days"
    if t > 3600000*24*7:
           returnStr = str(t/(24*3600000*7)) + " weeks"
    return returnStr

# for loop that takes json files and makes them into a list of dictionaries 
f = open("CompleteData\endsong_0.json", encoding='utf-8')
data = json.load(f)

i = 0
while True:
    try:
        f0 = open("CompleteData\endsong_" + str(i + 1) + ".json", encoding='utf-8')
        data0 = json.load(f0)
        data = data + data0
        f0.close()
        i = i + 1
    except FileNotFoundError:
        break

dict1 = {}

# Asks user for input
print("Pick a time frame from march 2015 to june 2022:")
print("Start(MM/DD/YYYY): ", end = ' ')
start = input()
print("End: ", end = ' ')
end = input()
print("")

# while loop makes a new list with every play that occured in given time frame
list1 = []
count = 0
while count < len(data):
    timeStamp = data[count]["ts"]

    if isBetween(timeStamp, start, end):
        list1.append(data[count])

    count = count + 1


print("Your Top 50 Songs from " + start + " to " + end)

# for loop that adds up all the listens to find total ms played and makes dictionary with every song listened to and ms played
for i in list1:
    # doesnt include songs that got removed or songs listened to while in private mode
    if not i['master_metadata_track_name'] == None and i["incognito_mode"] == False:
        song = i["spotify_track_uri"] + " " + i['master_metadata_track_name'] + "' by " + i['master_metadata_album_artist_name']
        msPlayed = i['ms_played']
        if song in dict1:
            newVal = dict1.pop(song) + i['ms_played']
            dict1[song] = newVal
        else:
            dict1[song] = msPlayed

# sorts dictionary by ms played and prints to user
from collections import OrderedDict
d_sorted_by_value = OrderedDict(sorted(dict1.items(), key=lambda x: x[1]))

n = 50 # how many songs to generate
pain = min(n, len(d_sorted_by_value))

songlist = []
for i in range(pain):
    popped =  d_sorted_by_value.popitem()
    timeStr = timeString(popped)
    title = popped[0]
    songlist.append(title[0:(title.find(" "))])
    title = title[(title.find(" ") + 1):]


    print(str(i + 1) + ". " + title + ", at " + timeStr) 

# Next part is accessing spotify API to make playlist

print("Would you like to make this into a playlist? (Y/N)", end = ' ')
YN = input()

playlist_id = ""

# If user says yes, a playlist is generated
if YN == "Y":
    playlist = create_playlist_on_spotify(
        name = start + " - " + end,
        public=False
    )
    
    playlist_id = playlist["uri"][17:]

    for i in songlist:
        track = "tracks?uris=" + i
        add_song_to_playlist(track, playlist_id)
    
    
