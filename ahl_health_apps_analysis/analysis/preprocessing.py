import string
import re
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
from bs4 import BeautifulSoup
import lxml

df= pd.read_csv('inputs/data/app_ids_list.csv')
app_info_df= pd.read_csv('inputs/data/app_ids_list_5.csv')
app_info_df.update(df)
details = app_info_df

details['description'] = details['description'].astype('string')

details.dropna(subset = 'description', inplace= True)


# step 1 - replace with space
def replace_dash(text):
	update = text.replace("-", " ")

	return update.replace(" \u2003\u2003∘", "")


details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:replace_dash(x))


# step 2 - remove emojis
emoji_pattern = re.compile("["
		u"\u2022" # bullet points
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           "]+", flags=re.UNICODE)

def remove_emojis(text):
	output = emoji_pattern.sub(r'', text)
	return output

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:remove_emojis(x))	                        

#step 3 - replace html tags with space
def remove_html_flags(texts):
	soup = BeautifulSoup(texts, features="lxml")
	return soup.get_text(separator=' ')

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:remove_html_flags(x))

# Step 4 - remove punctuation
def remove_punctuation(text):
	punctuationfree="".join([i for i in text if i not in string.punctuation])
	return punctuationfree

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:remove_punctuation(x))

# step 5 - lower
details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x: x.lower())


# step 6 - tockenization
def tokenization(text):
	tokens = re.split('W+',text)
	return tokens

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x: tokenization(x))


# step 7 - stop word removal
stopwords = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
	output= [i for i in text if i not in stopwords]
	return output

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:remove_stopwords(x))

# step 8 - stemming
porter_stemmer = PorterStemmer()

def stemming(text):
	stem_text = [porter_stemmer.stem(word) for word in text]
	return stem_text

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x: stemming(x))

#step 9 - Lemmitization
wordnet_lemmatizer = WordNetLemmatizer()

def lemmatizer(text):
	lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
	return lemm_text

details['descriptionHTML'] = details['descriptionHTML'].apply(lambda x:lemmatizer(x))

details.drop(df.tail(761).index,inplace=True)
details.to_csv('outputs/data/preprocessed_description.csv')

