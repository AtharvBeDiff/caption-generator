import os
from dotenv import load_dotenv
import openai

load_dotenv()  # loads from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # OpenRouter API Key
client.base_url = ""#put the url here

# Sidebar: Settings
st.sidebar.title("Caption Settings")
language = st.sidebar.selectbox("Select Language", 
    ["English", "Spanish", "French", "German", "Hindi"], key="language")
caption_style = st.sidebar.selectbox("Caption Style", 
    ["Funny", "Inspirational", "Trendy", "Professional", "Minimalist"], key="style")
num_captions = st.sidebar.slider("Number of Captions", 1, 5, 1, key="num_captions")
temperature = st.sidebar.slider("Creativity Level", 0.2, 1.0, 0.8, 0.01, key="temperature")
st.sidebar.markdown("Powered by OpenRouter API")

# Header with logo (top left)
col1, col2 = st.columns([1, 8])
with col1:
    st.image("image-2.png", width=60)  # Adjust width as needed
with col2:
    st.markdown(
        "<h1 style='margin-bottom:0px;'>Social Media Caption Generator</h1>",
        unsafe_allow_html=True
    )
st.caption("Generate catchy, AI-powered captions—choose your language, style, and more!")

# Session state for caption history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Caption generation function
def generate_captions(topic, style, language, num, temp):
    prompt = (
        f"Write {num} {style.lower()} captions for social media in {language} about: {topic}. "
        f"Number each caption."
    )
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative social media caption writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60 * num,
        temperature=temp,
    )
    return response.choices[0].message.content.strip()

# Topic input and generation
topic = st.text_input("Enter your caption topic (e.g., 'Sunset on the beach')", key="topic_input")
generate_btn = st.button("Generate Captions", key="generate_btn")

if generate_btn:
    if topic.strip():
        with st.spinner("Generating your captions..."):
            try:
                captions = generate_captions(topic, caption_style, language, num_captions, temperature)
                st.subheader("Your Captions:")
                st.write(captions)
                st.session_state["history"].append({
                    "topic": topic,
                    "style": caption_style,
                    "language": language,
                    "captions": captions,
                })
            except Exception as e:
                st.error(f"Could not generate captions: {e}")
    else:
        st.warning("Please enter a topic before generating captions.")

# Caption history section
if st.session_state["history"]:
    st.markdown("---")
    st.markdown("### 📜 Caption History")
    for idx, entry in enumerate(reversed(st.session_state["history"]), 1):
        st.markdown(
            f"{idx}. *Topic:* {entry['topic']} &nbsp; | &nbsp; "
            f"*Style:* {entry['style']} &nbsp; | &nbsp; "
            f"*Language:* {entry['language']}",
            unsafe_allow_html=True
        )
        st.write(entry["captions"])
    if st.button("Clear History", key="clear_history"):
        st.session_state["history"] = []
        st.success("Caption history cleared!")