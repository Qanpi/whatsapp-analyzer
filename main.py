from matplotlib import pyplot as plt
import numpy as np

from chat import Chat
from analyzer import Analyzer
from visualizer import Visualizer

chat = Chat(f"Data/WhatsApp Chat with Tiktok.txt")
vis = Visualizer(2, 3)


# 1 - Word frequencies
def word_filter(w):
    blacklist = ["like", "that", "which", "have", "this", "what", "just"]
    return len(w) > 3 and w not in blacklist


word_frequencies = Analyzer.word_frequencies(chat, filter=word_filter)
top_ten_words = zip(*word_frequencies[:10])

vis.bar(*top_ten_words, "Most popular (filtered) words", "occurences")

# 2 - Messages per months
messages_per_month, average = Analyzer.messages_per_month(chat)

ax = vis.line(
    list(messages_per_month.keys()),
    list(messages_per_month.values()),
    average,
    "Messages per month",
)

ax.text(0.98, 0.97, f"Total messages: {Analyzer.total_messages(chat)}", horizontalalignment="right", verticalalignment="top", transform=ax.transAxes, alpha=0.5, size=9)

# 3 - Hourly heatmap
hourly_messages = Analyzer.hourly_messages(chat)

hours = [
    "12 PM",
    "01 PM",
    "02 PM",
    "03 PM",
    "04 PM",
    "05 PM",
    "06 PM",
    "07 PM",
    "08 PM",
    "09 PM",
    "10 PM",
    "11 PM",
    "12 AM",
    "01 AM",
    "02 AM",
    "03 AM",
    "04 AM",
    "05 AM",
    "06 AM",
    "07 AM",
    "08 AM",
    "09 AM",
    "10 AM",
    "11 AM",
]
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

heatmap = [[None] * 24 for _ in range(7)]

for i in range(len(weekdays)):
    for j in range(len(hours)):
        index = weekdays[i] + " " + hours[j]
        heatmap[i][j] = hourly_messages[index]

vis.heatmap(heatmap, "Hourly messages", hours, weekdays)

# 4 - Messages per user
messages_per_user = Analyzer.messages_per_user(chat)

vis.bar(*zip(*messages_per_user), "Messages per user", "messages")

# 5 - Name counts
name_counts, self_name_counts = Analyzer.count_names(chat)

labels, data = zip(*name_counts)
ax = vis.bar(labels, data, "Name counts")

ax.bar(labels, self_name_counts, bottom=data, label="Self-named")

# 6 - Ad
ax = vis._ax()
ax.text(0.5, 0.5, f"Easily add your custom graph here.", horizontalalignment="center", verticalalignment="center", transform=ax.transAxes, alpha=0.5, size=11)

plt.show()
