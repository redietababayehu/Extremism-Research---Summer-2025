import pandas as pd
# used to manipulate strings 
import re

# Load data
df = pd.read_csv("youtube_comments_test.csv")

# Print column names to confirm
print(df.head(3))

#Define cleaning function
def clean_comment(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

# Apply it to the correct column 
df['cleanText'] = df['text'].apply(clean_comment)
print(df[['text', 'cleanText']].head(5))