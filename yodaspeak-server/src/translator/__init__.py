import spacy
import re

nlp = spacy.load('en_core_web_sm')
punctuation = [u',', u'.', u';', u'?']
comma = nlp(u'Hello, World')[1]

cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expand_contractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)] 
    return c_re.sub(replace, text)

def to_yodish(phrase):
    return yoda(expand_contractions(phrase)).strip()  

def sentify(text):
    output = []
    doc = nlp(text)
    for sent in doc.sents:
        sentence = []
        for clause in clausify(sent):
            sentence.append(yodafy(clause))
        output.append(sentence)
    return output

def clausify(sent):
    output = []
    cur = []
    
    for token in sent: 		
        if token.dep_ == 'cc' or (token.dep_ == 'punct' and token.text in punctuation):
                output.append(cur)
                output.append([token])
                cur = []
        else:
            cur.append(token)
    if cur != []:
        output.append(cur)
    return output

def yodafy(clause):
    new_array = []
    state = False
    
    for token in clause:
        if state:
            new_array.append(token)
        if not state and (token.dep_ == "ROOT" or token.dep_ == "aux"):
            state = True
    if len(new_array) > 0 and new_array[len(new_array)-1].dep_ != u'punct':
        new_array.append(comma)
    for token in clause:
        new_array.append(token)
        if token.dep_ == "ROOT" or token.dep_ == "aux":
            break
    return new_array

def yoda(string_):
    string = []
    yodafied = sentify(string_)
    
    for sentence in yodafied:
        sentence_ = ""
        for clause in sentence:
            for token in clause:                
                if token.dep_ == u'NNP' or token.dep_ == u'NNPS' or token.text == u'I':
                    sentence_ += token.text + " "
                elif sentence_ == "" and token.dep_ == u'neg':
                    sentence_ += "Not" + " "
                elif sentence_ == "":
                    sentence_ += token.text[0].upper() + token.text[1:] + " "
                elif token.dep_ == u'punct':
                    sentence_ = sentence_[:len(sentence_)-1] + token.text + " "
                else:
                    sentence_+=token.text.lower() + " "
        string.append(sentence_ + " ")
    return "".join(string)