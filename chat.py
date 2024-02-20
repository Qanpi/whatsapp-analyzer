import re
from typing import NamedTuple
from datetime import datetime

class Message(NamedTuple):
    timestamp: datetime
    author: str
    text: str


class Chat:
    messages: list[Message]

    def __init__(self, filepath, os="android"):
        if os not in ["android", "ios"]:
            raise ValueError("Unrecognized operating system for chat log.")

        self.os = os

        # UTF-8 necessary to read emojis without errors
        with open(filepath, encoding="UTF-8") as file:
            self.text = file.read()  # add the \n to the start

        self.__clean()
        self.__parse()

    def __clean(self):
        if self.os == "android":
            # Clean up of unnecessary messages
            self.text = re.sub(
                r"\d+/\d+/\d+, \d+:\d+ - [^:]+\n", r"", self.text
            )  # Deletes messages about encryption, group picture updates etc.
            
            self.text = re.sub(
                r"(\d+/\d+/\d+, \d+:\d+) - ([^:]+): (This message was deleted)\n", r"", self.text
            )

            self.text = re.sub(
                r"(\d+/\d+/\d+, \d+:\d+) - ([^:]+): (<Media omitted>)\n", r"", self.text
            )
        else:
            # Clean up of the mysterious \u200e
            self.text = re.sub(r"\u200e", r"", self.text)
            # Clean up of unnecessary messages
            self.text = re.sub(
                r"\[\d+/\d+/\d+, \d+.\d+.\d+\ \w+] [^:]+\n", r"", self.text
            )  # Deletes messages about encryption, group picture updates etc.
            # Clean up of unnecessary messages
            self.text = re.sub(
                r"\[\d+/\d+/\d+, \d+.\d+.\d+\ \w+] Shrezauski:[^:]+\n", r"", self.text
            )  # Deletes messages about encryption, group picture updates etc.

    # TODO: proper python docs
    # Separation of individual messages in an array
    def __parse(self):
        if self.os == "android":
            messages = re.findall(r"(\d+/\d+/\d+, \d+:\d+) - ([^:]+): (.+)", self.text)
            self.messages = [
                Message(datetime.strptime(timestamp, f"%m/%d/%y, %H:%M"), author, text)
                for (timestamp, author, text) in messages
            ]
        else:
            # FIXME: findall and timestamp
            messages = re.split(
                r"\n(\[\d+/\d+/\d+, \d+.\d+.\d+ \w+\](?: [^:]+)+): ", self.text
            )
        
    def words(self):
        texts = [t for _, _, t in self.messages] 

        words = " ".join(texts)
        return words.split(" ")
    
    def dates(self): 
        return [d for d, _, _ in self.messages]
    
    def authors(self):
        return [a for _, a, _ in self.messages]

    def texts(self):
        return [t for _, _, t in self.messages]
