#Imports --------------------------------------------------------------------------

import re #for regex recognition

from collections import defaultdict #for storing and counting data efficiently
from operator import itemgetter

import matplotlib.pyplot as plt #for graphing and visualizing the data
from matplotlib import rcParams
import numpy as np

import datetime #for converting into needed time formats

import os #for finding text files

import sys #for passing cmd line args

android = None
count_names = False

#Function to decorate the output in console --------------------------------------------------------------------------

def line_break():
    print("\n" + "---" * 20 + "\n")

#File opening --------------------------------------------------------------------------
if "-nc" in sys.argv:
    count_names = True

if len(sys.argv) > 1 and sys.argv[1] != "-nc":
    chat_name = sys.argv[1]
    file_name = f"WhatsApp Chat with {chat_name}.txt"
else:
    for file in os.listdir("Data"):
        if file.endswith(".txt"):
            file_name = file

            i = file_name.find(".")
            chat_name = file_name[19:i]

chat_name = re.sub(r" ", r"", chat_name)
print(chat_name)

with open(f"Data/{file_name}", encoding='UTF-8') as file: #UTF-8 necessary to read emojis without errors
    text = "\n" + file.read() #add the \n to the start

#Determining whether the file is android or ios --------------------------------------------------------------------------
if text[1] == "[":
    android = False
else:
    android = True

#Matplotlib initializaton --------------------------------------------------------------------------

plt.style.use("seaborn") #matplotlib style
# plt.rcParams.update({'figure.autolayout': True}) #autolayout for the graphs

#Lines array preparation --------------------------------------------------------------------------

if android:
    #Clean up of unnecessary messages
    parsed_text = re.sub(r"\d+/\d+/\d+, \d+:\d+ - [^:]+\n", r"", text) #Deletes messages about encryption, group picture updates etc.
    #Remove the remaining line break at the end
    parsed_text = parsed_text[:-1]
    #Separation of individual messages in an array
    parsed_text = re.split(r"\n(\d+/\d+/\d+, \d+:\d+ -(?: [^:]+)+): ", parsed_text) #Separates based on the line break and the prefix (for reliability)
else:
    #Clean up of the mysterious \u200e
    parsed_text = re.sub(r"\u200e", r"", text)
    #Clean up of unnecessary messages
    parsed_text = re.sub(r"\[\d+/\d+/\d+, \d+.\d+.\d+\ \w+] [^:]+\n", r"", parsed_text) #Deletes messages about encryption, group picture updates etc.
    #Clean up of unnecessary messages
    parsed_text = re.sub(r"\[\d+/\d+/\d+, \d+.\d+.\d+\ \w+] Shrezauski:[^:]+\n", r"", parsed_text) #Deletes messages about encryption, group picture updates etc.
    #Remove the remaining line break at the end
    parsed_text = parsed_text[:-1]
    #Separation of individual messages in an array
    parsed_text = re.split(r"\n(\[\d+/\d+/\d+, \d+.\d+.\d+ \w+\](?: [^:]+)+): ", parsed_text) #Separates based on the line break and the prefix (for reliability)

#Separate metadata/prefixes from the messages themselves
metadata = parsed_text[1::2]
messages = parsed_text[::2]


#Words array preparation --------------------------------------------------------------------------

words = " ".join(messages) #A conjucted mess of words separated by spaces 

#Counting messages sent by each user --------------------------------------------------------------------------

user_messages = defaultdict(int) #Storing the amount of messages sent in a dictionary {user: messages_sent}

for prefix in metadata:
    if android:
        i = prefix.find("-") + 2 #finding the index of where the name begins
    else:
        i = prefix.find("]") + 2
    name = prefix[i:] #separating the name itself

    user_messages[name] += 1 #counting all messages sent by the user

#Sorting the dictionary by the amount of messages which converts it into a list with tuples [(user, messages_sent)]
user_messages = sorted(user_messages.items(), key=itemgetter(1), reverse=True) 

#Counting the total amount of messages sent, --------------------------------------------------------------------------
# as well as miscellaneous messages

total_count = len(messages) #Total messages

# #Reserved for future use (perhaps)
# #Media 
# media_messages = re.findall(r"<Media omitted>", words)
# media_count = len(media_messages)
# #Deleted messages
# deleted_messages = re.findall(r"This message was deleted", words)
# deleted_count = len(deleted_messages)

#Counting the amount of messages sent per each month --------------------------------------------------------------------------

months_count = defaultdict(int) #Storing the amount of messages sent in a dictionary {month_and_year: messages_sent}

for prefix in metadata: 

    i = prefix.find(",") #finding the index where the date ends
    if android:
        date = prefix[:i]
        #Parsing the month, date and year
        [m, d, y] = re.split("/", date) #Note: there is a possibility for using days, but i did not find that very useful
    else:
        date = prefix[1:i]
        #Parsing the month, date and year
        [d, m, y] = re.split("/", date) #Note: there is a possibility for using days, but i did not find that very useful
        y = datetime.datetime.strptime(y, "%Y")
        y = y.strftime("%y")

    #Format the date
    m = datetime.datetime.strptime(m, "%m")
    m = m.strftime("%b ")

    months_count[m + y] += 1 #keep count in the dictionary

#Calculating the average MPM 
average_mpm = total_count / len(months_count)

#Counting the heatmap of messages for a day on average--------------------------------------------------------------------------

active_hours = defaultdict(int)

for prefix in metadata:
    if android:
        i = prefix.find("-") - 1 #finding the index where the date ends
        date_str = prefix[:i]

        date = datetime.datetime.strptime(date_str, "%m/%d/%y, %H:%M")
        # am_pm = date.strftime("%p") #to eliminate all the AM results
    else:
        i = prefix.find("]")
        date_str = prefix[1:i]

        date = datetime.datetime.strptime(date_str, "%d/%m/%Y, %I.%M.%S %p")
        # am_pm = date.strftime("%p")
    
    # if am_pm == "AM":
    #     continue

    timestamp = datetime.datetime.strftime(date, "%a %I %p")
    active_hours[timestamp] += 1

#Clean up of unnecessary message 
if android:
    words = re.sub(r"<Media omitted>", r"", words) #Deletes messages saying "<Media omitted>"
    words = re.sub(r"This message was deleted", r"", words) #Deletes messages saying "This message was deleted"
else:
    words = re.sub(r"(\w)+ omitted", r"", words) #Deletes messages saying "<Media omitted>"
    words = re.sub(r"This message was deleted.", r"", words) #Deletes messages saying "This message was deleted"

words = words.lower() # lower  as to not  contaminate future data
words = re.findall(r"[a-z-']+", words) 

#Finding the most popular words --------------------------------------------------------------------------

word_count = defaultdict(int) #Storing the most popular messages sent in a dictionary {message: occurences}

for w in words:
    if len(w) > 3:
        word_count[w] += 1

popular_words = sorted(word_count.items(), key=itemgetter(1), reverse=True)

#Finding the most popular names --------------------------------------------------------------------------

if count_names:
    name_count = defaultdict(int) #Storing the most popular names sent in a dictionary {name: occurences}
    self_name_count = defaultdict(int) #Storing the most popular names sent by users themselves in a dictionary {name: occurences}

    names = [u.lower() for u, mc in user_messages if re.search(r"\W", u) == None]


    for i in range(len(messages)):
        #Checking if the name is mentioned in the messages
        m = messages[i]
        #Checking if the name is part of a spam chain
        if messages[i] == messages[i-1]:
            continue
        for n in names:
            if re.search(n, m.lower()) != None:
                #Finding the name of the user who sent the message
                prefix = metadata[i-1]
                if android:
                    j = prefix.find("-") + 2 #finding the index of where the name begins
                else:
                    j = prefix.find("]") + 2
                user = prefix[j:] #separating the user himself
                #Checking if the user is the one who sent the message
                if user.lower() != n:
                    name_count[n] += 1
                else:
                    self_name_count[n] += 1
                    
    popular_names = sorted(name_count.items(), key=itemgetter(1), reverse=True)

#Visualising the data found --------------------------------------------------------------------------
#Order of graphs reversed to stack them on top when displaying

    #Graph 5 - Most popular names --------------------------------------------------------------------------

    #Matplotlib figure init
    fig, ax = plt.subplots(tight_layout=True)

    #Data
    labels_20 = [name for name, count in popular_names]
    data_20 = [count for name, count in popular_names]

    data_20_1 = [self_name_count[l] for l in labels_20]
    
    #Plotting
    ax.bar(labels_20, data_20, label="Normal")
    ax.bar(labels_20, data_20_1, bottom=data_20, label="Self-named")

    #Additional info
    #Write the count on each bar
    for i, v in enumerate(data_20):
        ax.text(i, v - 20, str(v), va="baseline", ha="center", color="white", family="monospace", size=8)
    #Write the count on each bar of self_names
    for i, v in enumerate([x+y for x, y in zip(data_20, data_20_1)]): #get the values of both bars summed up in one array
        ax.text(i, v, str(data_20_1[i]), va="bottom", ha="center", color="green", family="monospace")
    #Rotate the tick titles if over 10 people mentioned
    if len(labels_20) > 10:
        ax.tick_params(axis='x', rotation=85, labelsize=10)
    #Etc
    ax.set_title("Most popular names")
    ax.grid(False, "major", "x")
    ax.set_ylabel("occurences")
    ax.legend()
    fig.text(0.999,0.001, "Whatsapp Analyzer by Qanpi", ha="right", va="bottom", alpha=0.3, family="monospace", size=9) #watermark

    #Save png
    if chat_name == "fish":
        date = datetime.datetime.now()

        date = date.strftime("%d_%m_%y")
        plt.savefig(f"Output/fish/{chat_name.lower()}_nc_{date}")
    else:
        plt.savefig(f"Output/{chat_name.lower()}_5")


#Graph 4 - 10 most popular words --------------------------------------------------------------------------

#Matplotlib figure init
fig, ax = plt.subplots()

#Data
labels_11 = [word for word, count in popular_words[:10]]
data_11 = [count for word, count in popular_words[:10]]

#Plotting
ax.bar(labels_11, data_11)

#Additional info
ax.set_title("Most popular words (over the length of 3 characters)")
ax.grid(False, "major", "x")
ax.set_ylabel("occurences")
fig.text(0.999,0.001, "Whatsapp Analyzer by Qanpi", horizontalalignment="right", verticalalignment="bottom", alpha=0.3, family="monospace", size=9) #watermark

#Save png
plt.savefig(f"Output/{chat_name.lower()}_4")

#Graph 3 - messages per date and time --------------------------------------------------------------------------

#Matplotlib figure init
fig, ax = plt.subplots()

#Data
labels_10_0 = ["12 PM", "01 PM", "02 PM", "03 PM", "04 PM", "05 PM", "06 PM", "07 PM", "08 PM", "09 PM", "10 PM", "11 PM", "12 AM", "01 AM", "02 AM", "03 AM", "04 AM", "05 AM", "06 AM", "07 AM", "08 AM", "09 AM", "10 AM", "11 AM"]
labels_10_1 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

data_10 = [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None] for i in range(7)]
for i in range(len(labels_10_1)):
    for j in range(len(labels_10_0)):
        index = labels_10_1[i] + " " + labels_10_0[j]
        data_10[i][j] = active_hours[index]

#Plotting
ax.imshow(data_10, cmap="Blues", norm=None)

#Additional info

#Set ticks and their labels
ax.set_xticks(np.arange(len(labels_10_0)))
ax.set_yticks(np.arange(len(labels_10_1)))

ax.set_xticklabels(labels_10_0)
ax.set_yticklabels(labels_10_1)

ax.tick_params(axis='x', rotation=85, labelsize=10)

ax.set_title("Heatmap of messages sent per weekday")
ax.grid()
fig.text(0.999,0.001, "Whatsapp Analyzer by Qanpi", horizontalalignment="right", verticalalignment="bottom", alpha=0.3, family="monospace", size=9) #watermark

#Save png
plt.savefig(f"Output/{chat_name.lower()}_3")

#Graph 2 - the amount of messages sent per month --------------------------------------------------------------------------

#Matplotlib figure init
fig, ax = plt.subplots()

#Data
labels_01 = [m for m in months_count]
labels_01 = [label if i%2==0 else "\n" + label for i,label in enumerate(labels_01)] #so that the months ticks do not overlap
data_01 = [v for v in months_count.values()]

#Plotting
ax.axhline(average_mpm, alpha=0.3, c="r", ls="dashed", label="average") #The average line
ax.plot(labels_01, data_01, label="messages") #The data itself

#Additional info
ax.legend()
ax.set_title("Messages per month")
fig.text(0.999,0.001, "Whatsapp Analyzer by Qanpi", horizontalalignment="right", verticalalignment="bottom", alpha=0.3, family="monospace", size=9) #watermark

#Save png
plt.savefig(f"Output/{chat_name.lower()}_2")

#Graph 1 - the messages sent per user --------------------------------------------------------------------------

#Matplotlib figure init
fig, ax = plt.subplots(tight_layout=True)

#Data 
data_00 = [user[1] for user in user_messages]
labels_00 = [user[0] for user in user_messages]

#Plotting
if len(labels_00) > 3:
    #Present a bar chart if there are more than 4 users (purely for aesthetic reasons)
    ax.tick_params(axis='x', rotation=85, labelsize=10)
    ax.bar(labels_00, data_00)
    ax.grid(False, "major", "x")
else:
    #Present a pie chart if there are <= 4 users (purely for aesthetic reasons)
    explode = (0,) * (len(data_00) - 1) + (0.1,) #Fancy math to make the smallest slice explode (pop out)
    ax.pie(data_00, labels=labels_00, explode=explode, startangle=90, autopct="%1.1f%%")

#Additional info
ax.set_title(f"Messages sent by each member", size="14")
ax.text(0.99, 0.99, f"Total messages: {total_count}", horizontalalignment="right", verticalalignment="top", transform=ax.transAxes, alpha=0.5, size=11)
fig.text(0.999,0.001, "Whatsapp Analyzer by Qanpi", horizontalalignment="right", verticalalignment="bottom", alpha=0.3, family="monospace", size=9) #watermark

#Save png
plt.savefig(f"Output/{chat_name.lower()}_1")

#Show the figures
plt.show()
