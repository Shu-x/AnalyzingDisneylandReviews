'''
Text preprocessing script

Steps:
1. Convert to lowercase
2. Replace ride names with 'ride'
3. Expand contractions
4. Lemmatising
5. Split into tokens
6. Convert numbers to words
7. Keep tokens with letters only
8. Remove stopwords
'''

import contractions
from num2words import num2words
import nltk
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
import re
from collections import Counter

# Define list of rides
ride_name = [
    'tarzan tree house', 'slinky dog spin', 'iron man', 'hyperspace', 'hyper space', 'spaceship',
    'small world', 'star wars', 'dumbo', 'lion king', 'boat ride', 'mystic mansion',
    'honey hunt', 'grizzley gulch', 'carousel', 'teacup', 'tea cup', 'thunder mountain', 'buzz',
    'monsters', 'indiana', 'haunted', 'pirates', 'star tours', "peter pan's flight", 'singing bear',
    'mickey', 'space mountain', 'western river railroad', 'pirates of the caribbean', 'jungle' , 'cruise',
    'tiki', 'riverboat', 'tom sawyer', 'splash mountain', 'beaver brothers', "alice's tea party", 'castle carrousel',
    "snow white's adventure", 'dumbo the flying elephant', 'enchanted tale of beauty and the beast', "pinocchio's daring journey",
    'haunted mansion', 'go coaster', "roger rabbit's car toon spin", 'astro blasters', 'happy ride with baymax', 'ride & go seek',
    'animation academy', 'ant-man and the wasp', 'grizzly mountain', 'geyser gulch', 'hyperspace mountain', 'iron man experience',
    'mad hatter', 'mystic manor', 'orbiton', 'rc racer', 'roaring rapids', "rex's racer", 'mine train', 'crystal grotto', 'jet packs',
    'tron', 'lightcycle', 'space mountain', 'roller coaster', 'grizzly gulch']

lemmatizer = WordNetLemmatizer()

# Part-of-Speech Tagging
def nltk_pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None
    
def lemmatize_sentence(sentence):
    
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
    wordnet_tagged = map(lambda x: (x[0], nltk_pos_tagger(x[1])), nltk_tagged)
    lemmatized_sentence = []
    
    for word, tag in wordnet_tagged:
        if tag is None:
            lemmatized_sentence.append(word)
        else:        
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


def text_preprocessing(text, sub_ride = False, lemmatize = False, stem = False, stopword_list = None):

    # Make lowercase
    output = text.lower()
    
    # Replace ride name with 'ride'
    if sub_ride == True:
        for name in ride_name:
            pattern = re.compile(rf'\b{re.escape(name)}\b', flags=re.IGNORECASE)
            output = pattern.sub('ride', output)
                
    # Expand contractions
    output = contractions.fix(output)
    
    # Lemmatising
    if lemmatize == True:
        output = lemmatize_sentence(output)

    # Split into words
    output = word_tokenize(output)
    # output = output.split()
    
    for i in range(len(output)):

        # Convert to number
        if output[i].isnumeric():
            try:
                output[i] = num2words(output[i])
            except:
                pass

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
    if stem == True:
        stemmer = SnowballStemmer(language='english')
        output = [stemmer.stem(word) for word in output]

    return output