from llama_index.llms.groq import  Groq as Groqllama
from pinecone import Pinecone, ServerlessSpec
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import get_response_synthesizer
import time
import os
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import PromptTemplate
from groq import Groq
from IPython.display import Markdown, display
from openinference.instrumentation.groq import GroqInstrumentor
from arize_otel import register_otel, Endpoints



class NewPineconeQAModel:
  def __init__(self, groqAPIKey, pineconeAPIKey, documentPath, pineconeIndexName, groqModel="llama3-70b-8192"):
    print("Initializing MyClass...")
    self.groqAPIKey = groqAPIKey
    self.pineconeAPIKey = pineconeAPIKey
    self.groqModel = groqModel
    self.embeddingModelName="multi-qa-mpnet-base-dot-v1"
    self.documentPath = documentPath
    self.pineconeIndexName = pineconeIndexName
    llm = Groqllama(model=groqModel, api_key=groqAPIKey)
    pc = Pinecone(api_key=pineconeAPIKey)
    self.pc = pc
    self.llm = llm

    if(any(ind['name']==pineconeIndexName for ind in pc.list_indexes().indexes)):
      raise ValueError("Pinecone index name is already in use!")
    else:
      pc.create_index(
      name=pineconeIndexName,
      dimension=768,
      metric="cosine",
      spec=ServerlessSpec(cloud="aws", region="us-east-1"),
      )
      pinecone_index = pc.Index(pineconeIndexName)

    embed_model = HuggingFaceEmbedding(model_name="multi-qa-mpnet-base-dot-v1")
    Settings.embed_model = embed_model
    Settings.llm = llm
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = SimpleDirectoryReader(documentPath).load_data()
    index=VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)

    query_engine = index.as_query_engine(similarity_top_k=8)
    retriever = index.as_retriever(similarity_top_k=8)

    self.index = index
    self.default_prompt = query_engine.get_prompts()
    self.query_engine = query_engine
    self.retriever = retriever
    time.sleep(10)

  def queryDefault(self, question):
    response = self.query_engine.query(question)
    return({
    "response": response,
    })

  def queryGroq(self, question, instructions = "None"):
    nodes = self.retriever.retrieve(question)
    contextList=[i.text for i in nodes]
    matched_info = '\n\n'.join(item.text for item in nodes)

    context = f"\n {matched_info}"
    if instructions=="None":

      system_prompt = f"""
      Instructions:
      - Be helpful and answer questions concisely. If you don't know the answer, say 'I don't know'
      - Utilize the context provided for accurate and specific information.
      - Incorporate your preexisting knowledge to enhance the depth and relevance of your response.
      \n
      Context: {context}
      """
    else:

      system_prompt = f"""
      Instructions:
        {instructions}
      \n
      Context: {context}
      """
    groq_api_key=self.groqAPIKey
    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
    messages = [
    {
    "role": "system",
    "content":  system_prompt
    },
    {
    "role": "user",
    "content": "User Question: " + question,
    }
    ],
    model = self.groqModel
    )
    response_custom = chat_completion.choices[0].message.content

    return({
    "response":response_custom,
    "prompt": system_prompt,
    "context": contextList
    })

  def queryCustom(self, question, instruction="a clear, concise, and accurate way"):

    nodes = self.retriever.retrieve(question)
    context=[i.text for i in nodes]
    matched_info = '\n\n'.join(item.text for item in nodes)

    qa_prompt_tmpl_str = """\
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and your prior knowledge, answer the query.
    Please write the answer in {instruction} based on a comprehensive understanding of the given context.
    Query: {query_str}
    Answer: \
    """

    QA_PROMPT_KEY = "response_synthesizer:text_qa_template"

    qa_prompt_tmpl = PromptTemplate(
    qa_prompt_tmpl_str,
    )

    fmt_prompt = qa_prompt_tmpl.format(
    context_str=matched_info,
    query_str=question,
    instruction=instruction
    )

    default_qa_template=self.query_engine.get_prompts()[QA_PROMPT_KEY]
    self.query_engine.update_prompts({QA_PROMPT_KEY: fmt_prompt})
    response = self.query_engine.query(question)
    self.query_engine.update_prompts({QA_PROMPT_KEY: default_qa_template})


    return({
    "response": response,
    "template": fmt_prompt,
    "context": context
    })


  def deletePineconeIndex(self):
    self.pc.delete_index(self.pineconeIndexName)





class ExistingPineconeQAModel:
  def __init__(self, groqAPIKey, pineconeAPIKey, pineconeIndexName, arizeSpaceID, arizeAPIKey, arizeProjectName, arizeModelID, groqModel="llama3-70b-8192"):
    self.groqAPIKey = groqAPIKey
    self.pineconeAPIKey = pineconeAPIKey
    self.groqModel = groqModel
    self.embeddingModelName="multi-qa-mpnet-base-dot-v1"
    self.pineconeIndexName = pineconeIndexName
    self.arizeSpaceID=arizeSpaceID
    self.arizeProjectName=arizeProjectName
    self.arizeAPIKey=arizeAPIKey
    self.arizeModelID=arizeModelID

    llm = Groqllama(model=groqModel, api_key=groqAPIKey)
    pc = Pinecone(api_key=pineconeAPIKey)
    self.pc=pc
    self.llm = llm

    if(any(ind['name']==pineconeIndexName for ind in pc.list_indexes().indexes)):
      pinecone_index = pc.Index(pineconeIndexName)
    else:
      raise ValueError("Pinecone index with inputed name doesn't exist!")

    embed_model = HuggingFaceEmbedding(model_name="multi-qa-mpnet-base-dot-v1")
    Settings.embed_model = embed_model
    Settings.llm = llm

    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store)

    query_engine = index.as_query_engine(similarity_top_k=4)
    retriever = index.as_retriever(similarity_top_k=4)

    self.index = index
    self.default_prompt = query_engine.get_prompts()
    self.query_engine = query_engine
    self.retriever = retriever
    time.sleep(10)


  def queryDefault(self, question):
    response = self.query_engine.query(question)
    return({
    "response": response,
    })

  def queryGroq(self, question, instructions = "None"):
    nodes = self.retriever.retrieve(question)
    matched_info = '\n\n'.join(item.text for item in nodes)
    contextList=[i.text for i in nodes]

    context = f"\n Information:\n {matched_info}"
    if instructions=="None":

      system_prompt = f"""
      Instructions:
      - Be helpful and answer questions concisely. If you don't know the answer, say 'I don't know'
      - Utilize the context provided for accurate and specific information.
      - Incorporate your preexisting knowledge to enhance the depth and relevance of your response.
      \n
      Context: {context}
      """
    else:
      system_prompt = f"""
      Instructions:
        {instructions}
      \n
      Context: {context}
      """

    register_otel(
    endpoints = Endpoints.ARIZE,
    space_id = self.arizeSpaceID, # in app space settings page
    api_key = self.arizeAPIKey, # in app space settings page
    project_name = self.arizeProjectName, # name this to whatever you would like
    model_id=self.arizeModelID
    )

    GroqInstrumentor().instrument()
    os.environ["GROQ_API_KEY"] = self.groqAPIKey

    groq_api_key=self.groqAPIKey
    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
    messages = [
    {
    "role": "system",
    "content":  system_prompt
    },
    {
    "role": "user",
    "content": "User Question: " + question,
    }
    ],
    model = self.groqModel
    )
    response_custom = chat_completion.choices[0].message.content

    return({
    "response":response_custom,
    "prompt": system_prompt,
    "context": contextList
    })

  def queryCustom(self, question, instruction="a clear, concise, and accurate way"):

    nodes = self.retriever.retrieve(question)
    context=[i.text for i in nodes]
    matched_info = '\n\n'.join(item.text for item in nodes)

    qa_prompt_tmpl_str = """\

    Given the information provided in context and your preexisting knowledge answer the query.
    Please write the answer in {instruction}, giving the information in the context priority.
    The response should skip introductory or redundant clarifications unless explicitly requested.

    Query: {query_str}

    Context:
    {context_str}

    Answer: \
    """

    QA_PROMPT_KEY = "response_synthesizer:text_qa_template"

    qa_prompt_tmpl = PromptTemplate(
    qa_prompt_tmpl_str,
    )

    fmt_prompt = qa_prompt_tmpl.partial_format(
    instruction=instruction
    )

    default_qa_template=self.query_engine.get_prompts()[QA_PROMPT_KEY]
    self.query_engine.update_prompts({QA_PROMPT_KEY: fmt_prompt})
    
    response = self.query_engine.query(question)
    self.query_engine.update_prompts({QA_PROMPT_KEY: default_qa_template})


    return({
    "response": response,
    "template": fmt_prompt,
    "context": context
    })

  def deletePineconeIndex(self):
    self.pc.delete_index(self.pineconeIndexName)




# define prompt viewing function
def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
        display(Markdown(text_md))
        print(p.get_template())
        display(Markdown("<br><br>"))