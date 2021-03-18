
#Meet Robo: your friend

#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
#print(sent_tokens)
word_tokens = nltk.word_tokenize(raw)# converts to list of words
thisdict=dict()
raw=raw.split("\n")
#print(raw)
for i in range(0,len(raw)-1,2):
    if raw[i] not in thisdict:
        thisdict[raw[i]]=raw[i+1]


#print(word_tokens)
# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("salut", "hei", "buna")
GREETING_RESPONSES = ["Buna!", "Salut!", "Hei!", "Hei! Ma bucur ca vorbesti cu mine"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    #print(user_response)
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    #print(flat)
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"Scuze, dar nu inteleg.Mai spune o data."
        return robo_response
    else:
        for x in thisdict:
            ok=0
            if x in user_response:
                robo_response = robo_response + thisdict[x]
                ok=1
                return robo_response
    if ok==0:
        return ("Scuze, dar nu inteleg.Mai spune o data.")
            #print(x)


flag=True
print("ROBO: Numele meu este Robo. Eu iti voi raspunde la intrebarile legate de Arhitectura Calculatoarelor. Daca vrei sa iesi, scrie 'La revedere'")
while(flag==True):
    user_response = input()
    user_response = user_response.lower()
    if user_response == "":
        ok = 1
    else:
        ok = 0
    if (user_response != 'la revedere'):
        if (user_response == 'mersi' or user_response == 'multumesc'):
            flag = False
            print("ROBO: Cu placere!")
        elif (user_response == 'ce faci?' or user_response == 'ce faci'):
            print("ROBO: ", end="")
            print("Sunt foarte bine! Intreaba-ma ceva legat de Arhitectura Calculatoarelor :)")
        else:
            if (greeting(user_response) != None):
                print("ROBO: " + greeting(user_response))
                k = 1
            else:
                k = 0
            if (ok==1):
                print("ROBO: ",end="")
                print("Vorbeste cu mine!")

            if (k == 0 and user_response != ""):
                print("ROBO: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)

    else:
        flag=False
        print("ROBO: La revedere! Te mai astept sa vorbim")