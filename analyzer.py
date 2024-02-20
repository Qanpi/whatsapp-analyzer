import re

from collections import defaultdict
from operator import itemgetter

from chat import Chat

class Analyzer:
    def __longer_than(length: int):
        return lambda w: len(w) > length

    @staticmethod
    def word_frequencies(chat, filter=__longer_than(3)):
        words = [w.lower() for w in chat.words()]
        word_count = defaultdict(
            int
        )  # Storing the most popular messages sent in a dictionary {message: occurences}

        for w in words:
            if filter(w):
                word_count[w] += 1

        return sorted(word_count.items(), key=itemgetter(1), reverse=True)

    @staticmethod
    def total_messages(chat):
        return len(chat.messages)

    @staticmethod
    def messages_per_month(chat):
        months_count = defaultdict(
            int
        )  # Storing the amount of messages sent in a dictionary {month_and_year: messages_sent}

        for date in chat.dates():
            month_and_year = date.strftime("%B %y")
            months_count[month_and_year] += 1  # keep count in the dictionary

        average_mpm = Analyzer.total_messages(chat) / len(months_count)

        return months_count, average_mpm

    @staticmethod
    def hourly_messages(chat):
        active_hours = defaultdict(int)

        for date in chat.dates():
            timestamp = date.strftime("%a %I %p")
            active_hours[timestamp] += 1

        return active_hours

    @staticmethod
    def messages_per_user(chat):
        user_messages = defaultdict(
            int
        )  # Storing the amount of messages sent in a dictionary {user: messages_sent}

        for author in chat.authors():
            user_messages[author] += 1

        # Sorting the dictionary by the amount of messages which converts it into a list with tuples [(user, messages_sent)]
        return sorted(user_messages.items(), key=itemgetter(1), reverse=True)

    @staticmethod
    def count_names(chat: Chat):
        name_count = defaultdict(
            int
        )  # Storing the most popular names sent in a dictionary {name: occurences}
        self_name_count = defaultdict(
            int
        )  # Storing the most popular names sent by users themselves in a dictionary {name: occurences}

        authors = [n.lower() for n in chat.authors()]
        texts = [t.lower() for t in chat.texts()]

        names = [re.escape(n) for n in set(authors)]

        for i, t in enumerate(texts):
            for n in names:
                if re.search(n, t) != None:
                    # Finding the name of the user who sent the message
                    author = authors[i]
                    # Checking if the user is the one who sent the message
                    if author != n:
                        name_count[n] += 1
                    else:
                        self_name_count[n] += 1

        return sorted(name_count.items(), key=itemgetter(1), reverse=True), [self_name_count[l] for l in name_count.keys()] 

