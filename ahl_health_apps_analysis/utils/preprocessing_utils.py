import re
from bs4 import BeautifulSoup
import lxml


# step 1 - replace with space
def replace_dash(text):
	update = text.replace("-", " ")
	return update.replace(" \u2003\u2003∘", "")


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


#step 3 - replace html tags with space
def remove_html_flags(texts):
	soup = BeautifulSoup(texts, features="lxml")
	return soup.get_text(separator=' ')