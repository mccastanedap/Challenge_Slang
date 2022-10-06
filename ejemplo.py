"""
Slang Coding Challenge 2022
October 03, 2022
author= Melissa Castañeda
email = "mc.castanedap@uniandes.edu.co"
This program fetches data from a REST API at a given enpoint and consumes a list of
activites for an arbitrary amount of users. It then parses the JSON
file to create a dictionary of user ids and their groups their respective sessions from the list of
their activities if the time between activities exceeds 5 minutes the activites are different user sessions.
"""
from heapq import heappush, heappop
from collections import namedtuple
import datetime
import requests





"Part 1: Fetches some data from one of the Rest APIs"
 #  the url from where the API is to be consumed
#url = "https://api.slangapp.com/challenges/v1/activities"
url = 'https://gist.githubusercontent.com/Geisson19/6344e79dd5143d4c9ccb4648a8f8334f/raw/0137962f582d69e588c8b12a8215e84501c4ecb6/slangtest.json'
 # the authentication header
#headers = {'Authorization': 'Basic' 'MTEyOmpqclBxQ1dWWWtaS1pxbTg2TjNKamt5dS9wWXNpQ3MwZXYvemUzUzhwdVk9'}

 # obtain the user activites response from the API
user_activities = requests.get(url).json()

 # the python array containing all activites
activity_arr = user_activities['activities']

 # dictionary to store the activities, dictionary to store all activites for a given user
activities_dic= dict()
user_activities_dict = dict()
user_sessions = dict()
# insert all activities

def insert_activites():
     
    for i in range(len(activity_arr)):

        
        #Activity = namedtuple("activity", "id user_id first_seen_at answered_at")

        # We need to obatin the atributes of each activity
        #First we obtain the id, user_id then, first seen at, answered at.
        activity_id = activity_arr[i]['id']
        user_id = activity_arr[i]['user_id']
        start_activity_time = datetime.datetime.fromisoformat(
            activity_arr[i]['first_seen_at'])
        end_activity_time = datetime.datetime.fromisoformat(
            activity_arr[i]['answered_at'])

        # create a tuple with attributes for a activity_id.
        activity = list({activity_id, user_id, start_activity_time, end_activity_time})

        # store the activity in the dictionary
        activities_dic[f"{activity_id}"]= activity

        # when a user's id is not a key in the dictionary, create a new array and push the
        # activity onto the min-heap for this user which means that the parent would be always
        #  less or equal to the key of the son
        if user_activities_dict.get(f"{user_id}") is None:
            array = []
            user_activities_dict[f"{user_id}"] = array
            heappush(user_activities_dict[f"{user_id}"],
                     (activity.first_seen_at, activity.id))

        # if a user's id is already a key in the dictionary, push the tuple with the activity
        # into the min-heap
        else:
            heappush(user_activities_dict[f"{user_id}"],
                     (activity.first_seen_at, activity.id))

#Part 2 create user sessions

#def user_sessions():
   # print(user_activities_dict)
    #session={}
    #for i, v in user_activities_dict.items():

     #   session[v] =[i] if v not in session.keys() else res[v] + [i]
    #print("Grouped dictionary is : " + str(dict(session)))


def finalize_entry(key, session_arr):
    global user_sessions
    user_sessions[f"{key}"] = session_arr

def new_session_dictionary(end, start, activities):
   
    my_dictionary = {
        "ended_at": f"{end}",
        "started_at": f"{start}",
        "activity_ids": f"{activities}",
        "duration_seconds": f"{end.timestamp() - start.timestamp()}"
    }
    return my_dictionary

def new_session(activities_arr, activity_id):
    activities_arr.clear()
    activities_arr.append(activity_id)

    return activities_arr

# inserts the activities into my data structures
insert_activites()
user_sessions()
# builds the user sessions
#final_user_sessions = {"user_sessions": user_sessions()}

# posts the user_sessions json to the endpoint
#req = requests.post(url, json=final_user_sessions)
#print(final_user_sessions)