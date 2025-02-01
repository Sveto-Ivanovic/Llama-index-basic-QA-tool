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
  pineconeIndexName = 'championbuildv1'

if "arize_space_id" not in st.session_state:
  arize_space_id = os.getenv('arize_space_id')

if "arize_api_key" not in st.session_state:
  arize_api_key = os.getenv('arize_api_key')

if "project_name" not in st.session_state:
  project_name = os.getenv('project_name')

if "model_id" not in st.session_state:
  model_id = os.getenv('model_id')


if "my_class_instance" not in st.session_state:
  st.session_state.my_class_instance = ExistingPineconeQAModel(
    groqAPIKey=groqAPIKey,
    pineconeAPIKey=pineconeAPIKey,
    pineconeIndexName=pineconeIndexName,
    arizeModelID=model_id,
    arizeProjectName=project_name,
    arizeAPIKey=arize_api_key,
    arizeSpaceID=arize_space_id
    )
  
my_class_instance = st.session_state.my_class_instance


user_question = st.text_input("Question:", "")
pressedExist= st.button("Answer the question")

if pressedExist:
  answer = my_class_instance.queryGroq(user_question)
  st.write("Answer:", answer["response"])







