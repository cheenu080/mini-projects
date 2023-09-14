import bs4 as bs
import urllib.request
import re
import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
import heapq

#-----------------------GETTING THE DATA-----------------------
source = urllib.request.urlopen('https://en.wikipedia.org/wiki/India').read()

# lxml is a parser that beautiful soup uses to parse html document
soup  = bs.BeautifulSoup(source,'lxml')

# getting the string data 
"""" p : the html para tag
we cant use  txt.append(paragraph) as append is for list
wikipedia uses para while others may use div , span etc"""
text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text
    
    
#---------------PREPROCESSING THE TEXT-----------------------
"""doesnot have lower case sentences"""
text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+',' ',text)

"""has lower case sentences"""
clean_text = text.lower()
clean_text = re.sub(r'\W',' ',clean_text)# non word charcters
clean_text = re.sub(r'\d',' ',clean_text)# digits
clean_text = re.sub(r'\s+',' ',clean_text)

"""We need to create histogram from clean_text ,thats why we needed clean_text"""
"""We will use text for creating summary as it has vital information like years"""
    
#---------------TOKENIZING INTO SENTENCES-----------------------
sentences = nltk.sent_tokenize(text)

stop_words = nltk.corpus.stopwords.words('english')
"""
Why we created stop_word?
Because when we create histogram we dont need to consider stop words.
"""  
    
#---------------CREATING THE HISTOGRAM-----------------------
# word2 count : dictionary will contain the histogram
word2count = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stop_words: # excluding stop_words
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1
    
# weighted histogram
"""india appears the maximum time hence it has a value 1"""
for i in word2count.keys():
    word2count[i] = word2count[i]/max(word2count.values())
    
#---------------DICTIONARY CONTAINING SENTENCE SCORES-----------------------
"""Creating new dictionary with sentences as keys """
"""And scores as values"""
sent2score = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        #check
        if len(sentence.split(' '))<20:
            if word in word2count.keys():
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] += word2count[word]
    
"""
What if there are some sentences containing 100+ words but no substantial info
And some sentences with 15-20 words containing important info
So as the task is of summarizing we need only the important bits.
So we select sentences with a fixed length.
if len(sentence.split(' '))<30: safety check for more efficiency
"""
   
#---------------GETTING THE SUMMARY-----------------------
"""How ? 
We select the n largest sentences with max scores.
We use heapq for it.
We currently have 371 sentences.(sent2score)
we select 8 sentences"""

best_sentences = heapq.nlargest(8,sent2score,key=sent2score.get)
    
for i in best_sentences:
    print(i)