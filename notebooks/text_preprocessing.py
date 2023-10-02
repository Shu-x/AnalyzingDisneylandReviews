'''
Text preprocessing script

Steps:
1. Expand contractions
2. Convert numbers to words
3. Convert to lowercase
4. Remove punctuations and special characters
5. Stemming/Lemmatizing
'''

import contractions
from num2words import num2words
# from nltk.corpus import PlaintextCorpusReader, stopwords
# from nltk.stem import WordNetLemmatizer, PorterStemmer
# from nltk.tokenize import word_tokenize, sent_tokenize
import re


def text_preprocessing(text, stemmer = None, lemmatizer = None, stopword_list = None):

    # Expand contractions
    output = contractions.fix(text)

    # Split into words
    output = output.split()
    for i in range(len(output)):

        # Convert to number
        if output[i].isnumeric():
            try:
                output[i] = num2words(output[i])
            except:
                pass

        # Make lowercase
        output[i] = output[i].lower()

    # # Remove punctuation
    # pattern = r"[^\w\s]"
    # output = [re.sub(pattern, '', word) for word in output]

    # Keep tokens with letters only
    pattern = r"^[a-z]+$"
    output = [word for word in output if re.search(pattern, word)]

    # Define stopword list
    # stopword_list = stopwords.words('english')
    if stopword_list != None:
        output = [word for word in output if word not in stopword_list]

    # Stemming
    if stemmer != None:
        output = [stemmer.stem(word) for word in output]

     # Lemmatizing
    if lemmatizer != None:
        output = [lemmatizer.lemmatize(word) for word in output]

    return output