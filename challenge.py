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
import datetime
import requests
from operator import itemgetter


"Part 1: Fetches some data from one of the Rest APIs"
#  the url from where the API is to be consumed
url = "https://api.slangapp.com/challenges/v1/activities"
#url = 'https://gist.githubusercontent.com/mccastanedap/e0231b939a478d65d642680e3ddcc3a6/raw/97f055208a81cefae63fb848e11740e369017cc9/Example.json'
# the authentication header
headers = {
    'Authorization': 'Basic MTEyOmpqclBxQ1dWWWtaS1pxbTg2TjNKamt5dS9wWXNpQ3MwZXYvemUzUzhwdVk9'}

# obtain the user activites response from the API
user_activities = requests.get(url, headers=headers).json()

# the python array containing all activites
activity_arr = user_activities['activities']

# dictionary to store the activities, dictionary to store all activites for a given user
activities_dic = dict()
user_activities_dict = dict()
user_sessions = dict()

# insert all activities


def insert_activites():

    for i in range(len(activity_arr)):

        # We need to obatin the atributes of each activity
        # First we obtain the id, user_id then, first seen at, answered at.
        activity_id = activity_arr[i]['id']
        user_id = activity_arr[i]['user_id']
        start_activity_time = datetime.datetime.fromisoformat(
            activity_arr[i]['first_seen_at'])
        end_activity_time = datetime.datetime.fromisoformat(
            activity_arr[i]['answered_at'])

        # create a list with attributes for a activity_id.
        activity = list(
            [activity_id, user_id, start_activity_time, end_activity_time])

        # store the activity in the dictionary
        activities_dic[str(activity_id)] = activity

        # when a user's id is not a key in the dictionary, create a new array and append the
        # activity onto the list
        if user_activities_dict.get(str(user_id)) is None:
            array = []
            user_activities_dict[str(user_id)] = array
        user_activities_dict[str(user_id)].append([activity[2], activity[0]])

    # sort the activities for each user
    for x in user_activities_dict.items():
        x[1].sort(key=itemgetter(0))

# Part 2 create user sessions


def user_sessions_builder():

    for key in user_activities_dict.keys():

        # We know that a session can have multiple activities so these two are arrays
        # k is the key of the user activities
        k = user_activities_dict[str(key)]

        session = []
        activities = []

        # We take out the activity to obtain info
        first_activity = user_activities_dict[str(key)].pop(0)
        # Activity ID
        activities = new_session(activities, first_activity[1])

        # Time first seen at
        start = activities_dic[str(first_activity[1])][2]

        # Time last seen at
        end = activities_dic[str(first_activity[1])][3]

        print("No ha terminado" + "\n" + str(key))
        i = 0
        while i < len(k):

            # We need to check if there is only one activity for that actual user session
            if len(k) == 0:
                last = session_dictionary(end, start, [first_activity[1]])
                # We add the last activity to the list
                session.append(last)
                # We need to stop the loop in case there is no more information
                user_sessions[str(key)] = session

            # We check is there is another activity if there are more keys we enter
            if len(k) > 0:
                # Here we need to calculate how much time it takes between the activies
                curr_activity = user_activities_dict[str(key)].pop(0)

                # We obtain the start time of the activity
                start_act_2 = activities_dic[str(curr_activity[1])][2]
                # We check the time the second activity began and when the first finish
                gap = start_act_2.timestamp() - end.timestamp()

                # If the gap is bigger than 300 seconds that means 5 minutes they belong to
                # differente sections if is less time they belong to the same section.
            if gap < 300:
                activities.append(curr_activity[1])

            if gap >= 300:
                end = activities_dic[str(first_activity[1])][3]
                # We add to the dictionary a new session
                session_dictionary = new_session_dictionary(
                    end, start, activities)
                # We add to the array of sessions the session dictionary already created
                session.append(session_dictionary)

                # We need to take into account the case in which the last activity was 5 minutes after
                # this activity needs his own section
                if curr_activity[1] not in activities and len(k) == 0:
                    # We take the end time of the activity
                    end = activities_dic[str(curr_activity[1])][3]
                    # Create in the dictionary a new session
                    last = new_session_dictionary(
                        end, start_act_2, [curr_activity[1]])
                    # add the new session to the array
                    session.append(last)
                    user_sessions[str(key)] = session

                # if the current activity has already been added to the session list and we
                    # have already popped off the last activity, do not create a new session.
                if curr_activity[1] in activities and len(k) == 0:
                    user_sessions[str(key)] = session

    return user_sessions

# Create a dictionary of user ids and their groups


def new_session_dictionary(end, start, activities):

    my_dictionary = {
        "ended_at": str(end),
        "started_at": str(start),
        "activity_ids": str(activities),
        "duration_seconds": str(end.timestamp() - start.timestamp())
    }
    return my_dictionary

# Create a list of activities


def new_session(activities_arr, activity_id):
    activities_arr.clear()
    activities_arr.append(activity_id)

    return activities_arr


# inserts the activities into my data structures
insert_activites()

# builds the user sessions
final_user_sessions = {"user_sessions": user_sessions_builder()}
# print(final_user_sessions)

# posts the user_sessions json to the endpoint
req = requests.post("https://api.slangapp.com/challenges/v1/activities/sessions",
                    headers=headers, json=final_user_sessions)
print(req)
