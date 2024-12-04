from llama_index_custom import NewPineconeQAModel, ExistingPineconeQAModel
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if "groqAPIKey" not in st.session_state:
  groqAPIKey = os.getenv('groqAPIKey')

if "pineconeAPIKey" not in st.session_state:
  pineconeAPIKey = os.getenv('pineconeAPIKey')

if "pineconeIndexName" not in st.session_state:
  pineconeIndexName = os.getenv('pineconeIndexName')

if "my_class_instance" not in st.session_state:
  st.session_state.my_class_instance = NewPineconeQAModel(
    groqAPIKey=groqAPIKey,
    pineconeAPIKey=pineconeAPIKey,
    documentPath="./documents",
    pineconeIndexName=pineconeIndexName,
    )
  
my_class_instance = st.session_state.my_class_instance


user_question = st.text_input("Question:", "")
pressedExist= st.button("Answer the question")

if pressedExist:
  answer = my_class_instance.queryGroq(user_question)
  st.write("Answer:", answer["response"])


