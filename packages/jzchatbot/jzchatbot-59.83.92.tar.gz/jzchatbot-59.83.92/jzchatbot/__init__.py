import random
import re
import json
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

def gencode(pyfilename, jsonfilename, botname):
        with open(pyfilename, "w+") as file:
            file.write(f"""
import jzchatbot as jz
                       
ai = jz.Bot(name='{botname}',jsonfile='{jsonfilename}')
                       
while True:
    cmd = input('You: ')
    jz.usrinput(cmd)
                       """)
        
        with open(jsonfilename, "w+") as file:
            file.write("""
[
    {
        "question": "How are you?",
        "answers": [
            "I'm doing well, thank you.",
            "I'm fine, thanks for asking."
        ]
    },
    {
        "question": "Can you help me?",
        "answers": [
            "Of course, I'll do my best to help you.",
            "Sure, what do you need help with?"
        ]
    },
    {
        "question": "Goodbye",
        "answers": [
            "Goodbye!",
            "See you later!"
        ]
    },
    {
        "question": "Thank you",
        "answers": [
            "You're welcome!",
            "Anytime!"
        ]
    },
    {
        "question": "Hello",
        "answers": [
            "Hi, how can I help?",
            "Hello, how can I help?"
        ]
    },

    {
        "question": "What are you made from?",
        "answers": [
            "I'm made from the programming and coding languages Python and JSON.",
            "I'm made from Python and JSON."
        ]
    },
    {
        "question": "What's your name?",
        "answers": [
                       """
            f'"My name is {botname}"'
                       """
        ]
    }
]
                       
                       """)


class Bot:
    def __init__(self, name, jsonfile):
        self.name = name
        self.conversations = self.load_conversations(jsonfile)
        self.engine = pyttsx3.init()

    def preprocess_text(self, text):
        # Correct spelling mistakes using TextBlob
        corrected_text = str(TextBlob(text).correct())

        # Tokenization
        tokens = word_tokenize(corrected_text)

        # Stopword removal and remove non-alphabetic characters
        stop_words = set(stopwords.words('english'))
        tokens = [re.sub(r'[^a-zA-Z]', '', token).lower() for token in tokens if token.lower() not in stop_words]

        # Remove empty tokens
        tokens = [token for token in tokens if token]

        return tokens

    def generate_response(self, user_input):
        max_similarity = 0
        best_response = None
        try:
            for entry in self.conversations:
                question = entry["question"]
                question_tokens = self.preprocess_text(question)
                user_input_tokens = self.preprocess_text(user_input)
                common_tokens = set(question_tokens) & set(user_input_tokens)
                similarity = len(common_tokens) / max(len(question_tokens), len(user_input_tokens))

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = entry.get("answers", ["I'm sorry, I don't have a response for that."])

            if best_response:
                return random.choice(best_response)
            else:
                return "I'm sorry, I didn't understand your question."
            
        except ZeroDivisionError:
            return "Minimum of 4 characters and/or numbers."
        
        except BaseException as e:
            return f"Error: {e}"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def load_conversations(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def usrinput(self, cmd):
        bot_response = self.generate_response(cmd)
        print(f"{self.name}: {bot_response}")
        self.speak(bot_response)
        