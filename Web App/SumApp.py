import streamlit as st
import regex as re
import urllib.request
import bs4 as bs
from paraphraser import paraphrase
from gensim.summarization import summarize 
import file_upload as fu
from transformers import pipeline
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
#from pysummarization.web_scraping import WebScraping
from pysummarization.abstractabledoc.std_abstractor import StdAbstractor
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

def SIDEBAR():
    st.sidebar.header('MENU')
    s = [ 'Extractive Summarizer','Abstractive Summarizer']
    choice = st.sidebar.selectbox('Select a Summarizer',s, key="s")

    if choice == "Extractive Summarizer":
         st.subheader("Extractive Summmarizer")
         EXTRACTIVESUMMARIZER()
    elif choice == "Abstractive Summarizer":
         st.subheader("Abstractive Summarizer")
         ABSTRACTIVESUMMARIZER()
   
    return choice

def DOCUMENTUPLOAD():
    upload_type = ["Paste Text", "Upload Text", "Upload URL"]
    option = st.selectbox("Select text upload method",upload_type)
                        
    uploaded_text = " "                    
    
    if option == "Paste Text":
       txt = st.empty()
       value = " "
       if st.button('Process'):
               value =" "
       uploaded_text=txt.text_area("Enter text here", value, height= 300)
           
    elif option =="Upload Text":
         local_text= fu.main()
         if (local_text != None and local_text != " " and local_text != ""):
            uploaded_text=local_text
         
    elif option == "Upload URL":
        #Enter URL
        variable= st.empty()
        url_value = ""
        if st.button('Process'):
           url_value
        url = variable.text_input('Enter URL link', url_value)
        if (url != ""):
            req = urllib.request.Request(url)
            scraped_data = urllib.request.urlopen(req)
            article = scraped_data.read().decode('utf-8')
     
            #parsing the URL content and storing in a variable
            parsed_article = bs.BeautifulSoup(article,'lxml')
    
            #returning <p> tags
            paragraphs = parsed_article.find_all('p')
    
            uploaded_text = " "
    
            #looping through the paragraphs and adding them to the variable
            for p in paragraphs:
               uploaded_text += p.text
             
            if (url != " "):
               req = urllib.request.Request(url)
               try:feed_xml = urllib.request.urlopen(url).read()
               except urllib.error.URLError as e:
                   print(e.reason)
    else:
          st.write("Wrong option selected")
    
    return uploaded_text   

def TEXT_PREPROCESSING():
    new_text =DOCUMENTUPLOAD()
    contraction_map = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",

                           "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",

                           "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",

                           "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",

                           "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",

                           "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",

                           "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",

                           "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",

                           "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",

                           "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",

                           "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",

                           "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",

                           "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",

                           "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",

                           "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",

                           "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",

                           "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",

                           "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",

                           "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",

                           "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",

                           "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",

                           "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",

                           "you're": "you are", "you've": "you have"}
   
    text = " "
    if (new_text != " " and new_text != "" and new_text != None):
        #for p in new_text:
            #new_text = new_text.translate(string.maketrans('',''), string.punctuation)
            #text = re.sub(r'\([^)]*\)', '', new_text)
            #st.write(text)
            text = re.sub('"','', new_text)
            #text = re.sub(r'\d+', '', text)
            text = ' '.join([contraction_map[t] if t in contraction_map else t for t in text.split(" ")])    
            text = re.sub(r"'s\b","",text)
            #text = re.sub(r'[0-9]', ' ', text)
            
    return text

def EXTRACTIVESUMMARIZER():
    input_sen= TEXT_PREPROCESSING()
    if (input_sen != " " and input_sen != "" and input_sen != None):
        if len(input_sen)>1000:
            summary= summarize(input_sen, ratio=0.15)
        else:
            summary= summarize(input_sen, ratio=0.50)
        st.write("Here is your summary: ")
        st.write(summary)
       
   
def ABSTRACTIVESUMMARIZER():

    input_sen = TEXT_PREPROCESSING()
    document = input_sen
    summarization= pipeline('summarization')
    if (document != " " and document != "" and document != None):
        sentence= summarization(document)
        new = sentence
        st.write("Here is your summary: ")
        st.write(new)


def main():
    st.title('EASESUM')
    st.text(" An easy means to summarize your text with no stress")
    SIDEBAR()

if __name__ == '__main__':
	main()

