import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import io
from PIL import Image

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = ''.join(c for c in text if c.isalpha() or c.isspace())
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def generate_wordcloud(text, colormap, prefer_horizontal):
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        stopwords=STOPWORDS,
        colormap=colormap,
        prefer_horizontal=prefer_horizontal
    ).generate(text)
    
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    return plt

def plt_to_jpeg(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='jpeg', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf

st.title("Word Cloud Generator with Download")

text = st.text_area("Enter your text here", height=200)
min_word_length = st.slider("Minimum Word Length", min_value=1, max_value=8, value=3)
max_words = st.slider("Maximum Number of Words", min_value=10, max_value=200, value=100)

# Retained parameters
colormap = st.selectbox("Color Scheme", ["viridis", "plasma", "inferno", "magma", "cividis"])
prefer_horizontal = st.slider("Proportion of Horizontal Words", min_value=0.0, max_value=1.0, value=0.9)

if st.button("Generate Word Cloud"):
    if text.strip():
        processed_text = preprocess_text(text)
        wordcloud_fig = generate_wordcloud(
            processed_text, 
            colormap, 
            prefer_horizontal
        )
        st.pyplot(wordcloud_fig)
        
        # Add JPEG download button
        jpeg_buffer = plt_to_jpeg(wordcloud_fig)
        st.download_button(
            label="Download as JPEG",
            data=jpeg_buffer,
            file_name="wordcloud.jpg",
            mime="image/jpeg"
        )
    else:
        st.warning("Please enter some text.")
