import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = ''.join(c for c in text if c.isalpha() or c.isspace())
    # Remove stop words
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def generate_wordcloud(text):
    wordcloud = WordCloud(width=500, height=300, background_color='white', stopwords=STOPWORDS).generate(text)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    return plt

st.title("Word Cloud Generator")

text = st.text_area("Enter text", height=200)
min_word_length = st.slider("Minimum Word Length", min_value=1, max_value=8, value=3)
max_words = st.slider("Maximum Number of Words", min_value=10, max_value=50, value=30)

if st.button("Generate Word Cloud"):
    if text.strip():
        processed_text = preprocess_text(text)
        wordcloud = generate_wordcloud(processed_text)
        wordcloud.min_word_length = min_word_length
        wordcloud.max_words = max_words
        st.pyplot(wordcloud)
    else:
        st.warning("Please enter some text.")
