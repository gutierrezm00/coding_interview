import sys
import json
from datetime import datetime

# This is a calendar overlap finder that functions in what is essentially N time with regard to number of events. 
# I didn't test performance, but lots can be done to smooth out/polish if this implementation has too much overhead. :D

# for those who need it
def printHelp():
    print('''
    Please provide names as arguments to availability.py consistent with those found in users.json in order to accurately filter events.\n
    \te.g. `python3 availability.py Jane,John,Maggie`
    ''')
    exit()

#params: array, array, date, date
def findOverlap(query_users, events, min_date = None, max_date = None):

    #pass in min and max dates if you don't want the program to determine min max dates on its own. 

    if min_date is None or max_date is None:
        min_date = float('inf')
        max_date = 0
        for event in events:
            #WARNING, MAGIC NUMBERS AHEAD. 
            # but seriously. /100 because no one plans their schedules in anything finer than 15 minute increments, and this results in 100X increase in perforamnce ¯\_(ツ)_/¯
            start_timestamp = datetime.strptime(event['start_time'],'%Y-%m-%dT%H:%M:%S').timestamp()/100
            end_timestamp = datetime.strptime(event['end_time'],'%Y-%m-%dT%H:%M:%S').timestamp()/100

            if(start_timestamp < min_date): min_date = start_timestamp
            if(end_timestamp > max_date): max_date = end_timestamp

    time_arr = [True] * int(max_date-min_date)
    
    for event in events:
        start_time = int(datetime.strptime(event['start_time'],'%Y-%m-%dT%H:%M:%S').timestamp()/100-min_date)
        end_time = int(datetime.strptime(event['end_time'],'%Y-%m-%dT%H:%M:%S').timestamp()/100-min_date)
        for i in range(start_time,end_time):
            time_arr[i] = False

    # If I wanted to exclude non business hours, I could do it here by setting non business hour timestamp sections to False. 
    # However, I play D&D, so the only time I really truly absolutely need good scheduling is off business hours anyways. ¯\_(ツ)_/¯
    #                               ______________                               
    #                         ,===:'.,            `-._                           
    #                              `:.`---.__         `-._                       
    #                                `:.     `--.         `.                     
    #                                  \.        `.         `.                   
    #                          (,,(,    \.         `.   ____,-`.,                
    #                       (,'     `/   \.   ,--.___`.'                         
    #                   ,  ,'  ,--.  `,   \.;'         `                         
    #                    `{D, {    \  :    \;                                    
    #                      V,,'    /  /    //                                    
    #                      j;;    /  ,' ,-//.    ,---.      ,                    
    #                      \;'   /  ,' /  _  \  /  _  \   ,'/                    
    #                            \   `'  / \  `'  / \  `.' /                     
    #                             `.___,'   `.__,'   `.__,'  


    i = 1
    ranges = []
    start = None
    stop = None
    prev = time_arr[0]

    #Magic
    if(prev): start = 0
    while i < len(time_arr):
        if(time_arr[i]):
            if(prev != time_arr[i]):
                start = i
        else: 
            if(prev != time_arr[i]):
                stop = i
                ranges.append([start,stop])

        prev = time_arr[i]
        i+=1

    user_string = ' '.join(query_users[:-1]) + ' and ' + str(query_users[-1])

    overlap_strings = []
    for time_range in ranges:
        overlap_strings.append(f'{user_string} are free from {datetime.fromtimestamp((time_range[0]+min_date)*100)} - {datetime.fromtimestamp((time_range[1]+min_date)*100)}')
    return overlap_strings
#params: array, array
def filterUsers(query_users, users):
    filtered_users = []
    for query_user in query_users:
        for user in users:
            if(user['name'] == query_user):
                filtered_users.append(user)
    return filtered_users

# params: array, array
def filterEvents(filtered_users, events):
    filtered_events= []
    for user in filtered_users:
        for event in events:
            if(user['id'] == event['user_id']):
                filtered_events.append(event)
    return filtered_events

def main():

    # if wrong print help
    if(len(sys.argv) <= 1 or sys.argv[1].lower() == 'help'):
        printHelp()

    # load files
    with open('users.json') as f:
        users = json.load(f)
    with open('events.json') as f:
        events = json.load(f)

    # get users from command line
    query_users = sys.argv[1].split(',')
 
    # filter users, then filter events based on those users
    filtered_users = filterUsers(query_users, users)
    filtered_events = filterEvents(filtered_users, events)

    # get overlaps! 
    overlaps = findOverlap(query_users, filtered_events)


    #... and print them!
    print(overlaps)
    # for overlap in overlaps:
    #     print(overlap)


if __name__ == "__main__":
    main()

