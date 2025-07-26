import getpass
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from streamlit_mic_recorder import speech_to_text


load_dotenv('hack.env')
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
prompt = """
Hello everyone! My name is [Your Name], and today I want to talk about the importance of kindness. 
Being kind means treating others the way you want to be treated. Even small acts, 
like saying “thank you” or helping a friend, can make someone's day better. 

"""
st.write(prompt)
state = st.session_state

if 'text_received' not in state:
    state.text_received = []

c1, c2 = st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

def get_evaluation_prompt(reference_text, speech_text):
    return f"""
You are an English teacher grading a 5th-grade student's speech performance.

This is the reference speech for them to read or memorize:
----
{reference_text}
----

Here is the student's actual spoken version:
----
{speech_text}
----

Please compare the student's speech to the reference. Consider:
- Accuracy (did they say the same words/ideas?)
- Content (did they include all main points?)
- Structure (was the order or structure kept?)
- Clarity and grammar
- Confidence and delivery

List differences (things missed, added, or changed) in a few bullet points.
Then, give a friendly, encouraging progress report for a 5th grader with praise and suggestions.
Finish with a total score out of 10.

Use clear, simple language.

also generete the score card in json format with all the evalution matrixs
"""

# ...

if text:
    state.text_received.append(text)
    evaluation_prompt = get_evaluation_prompt(prompt, text)
    with st.spinner("Evaluating your speech..."):
        feedback = llm.invoke(evaluation_prompt)
    st.subheader("Your Speech Evaluation")
    st.markdown(feedback.content)
