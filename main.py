#!/usr/bin/env python3
version = "1.0.1"

import urllib3
import json
import itertools
import optparse
import time

parser = optparse.OptionParser(usage="usage: %prog [options] arg", version=version)
http = urllib3.PoolManager() # Instance to make requests.

url = "https://www.reddit.com/api/username_available.json?user={}" # Url to reddit api for check username available
dictionary = "qwertyuiopasdfghjklzxcvbnm1234567890" # Char dictionary for names creating

def Check_Available_Username(username):
    response = http.request("GET", url.format(username)) # Get response from reddit api
    json_result = json.loads(response.data.decode("utf-8"))
    if json_result["message"] == "Too Many Requests":
        print("{}. Too Many Requests, please wait a few seconds.".format(username))
        return
    result = json.dumps(json_result) # Result. Decoding, converting to string from json
    format_print = "Username: {} - {}"
    if result == "true":
        print(format_print.format(username, "Available"))
    else:
        print(format_print.format(username, "Not Available"))

def Check_Available_Username_By_Length(length):
    permutations = list(map(lambda x: "".join(x), itertools.product(dictionary, repeat=length))) # String which contains usernames from itertools.product. Example of itertools.product: product('ABCD', repeat=2) - AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD
    count_all, count_available = 1, 1
    for username in permutations:
        if username[0].isdigit():
            continue
        response = http.request("GET", url.format(username)) # Get response from reddit api
        json_result = json.loads(response.data.decode("utf-8"))
        try:
            if json_result["message"] == "Too Many Requests":
                print("{}. Too Many Requests, please wait a few seconds.".format(username))
                permutations.append(username)
                time.sleep(1)
        except:
            pass
        result = json.dumps(json_result) # Result. Decoding, converting to string from json
        format_print = "{}. Username: {} - {}"
        if result == "true":
            print(format_print.format(count_all, username, "Available\tYES!"))
            file = open("availables.txt", "a") # File for available usernames
            file.write("{}. {}\n".format(count_available, username)) # Add Available result to file
            file.close() # Correctly close the file
            count_all+=1
            count_available+=1
        elif result == "false":
            print(format_print.format(count_all, username, "Not Available"))
            count_all+=1
        time.sleep(0.1)

parser.add_option(
    "-n", "--byname",
    action="store",
    help="Check available username by name.",
    type="string",
    dest="username"
)

parser.add_option(
    "-l", "--bylen",
    action="store",
    help="Check available username by dictionary with declarated length. Result will be logged to file: available.txt",
    type=int,
    dest="usernames_length"
)

options, args = parser.parse_args()

if options.username != None:
    Check_Available_Username(options.username)
if options.usernames_length != None:
    Check_Available_Username_By_Length(options.usernames_length)