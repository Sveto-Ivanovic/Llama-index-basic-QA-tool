from bs4 import BeautifulSoup
import os
from llama_index.llms.groq import  Groq as Groqllama
from pinecone import Pinecone, ServerlessSpec
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document

Data=[]

for filename in os.listdir("./ChampionBuildHTMLSelenium/"):
  with open(f'.\ChampionBuildHTMLSelenium\{filename}','r',encoding='utf-8') as f:
    file=f.read()
    soup = BeautifulSoup(file,'html.parser', multi_valued_attributes=None)
    name=filename.split('.')[0]
    main_rune=""
    div_tag_main = soup.find_all('div', attrs={'class': 'm-ku03qt'})

    for img in div_tag_main[0].contents:
      if img["class"]=="m-1iebrlh":
        main_rune=img["alt"]

    first_keystone=""
    for div in div_tag_main[1].contents:
      if div["class"]=="m-kr04v7":
        first_keystone=div.contents[0]["alt"]

    second_keystone=""
    for div in div_tag_main[2].contents:
      if div["class"]=="m-kr04v7":
        second_keystone=div.contents[0]["alt"]

    thrid_keystone=""
    for div in div_tag_main[3].contents:
      if div["class"]=="m-kr04v7":
        third_keystone=div.contents[0]["alt"]

    fourth_keystone=""
    fifth_keystone=""

    for div in div_tag_main[4].contents:
      if div["class"]=="m-kr04v7":
        fourth_keystone=div.contents[0]["alt"]
  
    for div in div_tag_main[5].contents:
      if div["class"]=="m-kr04v7" and fourth_keystone=="":
        fourth_keystone=div.contents[0]["alt"]
      elif div["class"]=="m-kr04v7" and fourth_keystone!="":
        fifth_keystone=div.contents[0]["alt"]

    for div in div_tag_main[6].contents:
      if div["class"]=="m-kr04v7":
        fifth_keystone=div.contents[0]["alt"]

    stats_1=''
    stats_2=''
    stats_3=''
    div_tag_stats = soup.find_all('div', attrs={'class': 'm-1hhp7hd'})

    for stat in div_tag_stats[0].contents:
      if stat['class']== "m-1dj96r2":
        stats_1=stat.contents[0]['alt']

    for stat in div_tag_stats[1].contents:
      if stat['class']== "m-1dj96r2":
        stats_2=stat.contents[0]['alt']

    for stat in div_tag_stats[2].contents:
      if stat['class']== "m-1dj96r2":
        stats_3=stat.contents[0]['alt']

    div_tag_summoners= soup.find_all('div', attrs={'class': 'm-13lqnlo'})
    summoner_1= div_tag_summoners[0].contents[0]['alt']
    summoner_2= div_tag_summoners[0].contents[0]['alt']
  

    div_tag_items = soup.find_all('div', attrs={'class': 'm-1q4a7cx'})

    begg_item_1=div_tag_items[0].contents[0].contents[0].contents[0]['alt']
    begg_item_2=div_tag_items[0].contents[1].contents[0].contents[0]['alt']
    begg_item_3="" if len(div_tag_items[0].contents)==2 else div_tag_items[0].contents[2].contents[0].contents[0]['alt']
    if len(div_tag_items[0].contents[1].contents)==2:
      begg_item_2=div_tag_items[0].contents[1].contents[1].contents[0]+'x'+begg_item_2
    
    core_item_1=div_tag_items[2].contents[0].contents[0].contents[0]['alt']
    core_item_2=div_tag_items[2].contents[1].contents[0].contents[0]['alt']
    core_item_3="" if len(div_tag_items[2].contents)==2 else div_tag_items[2].contents[2].contents[0].contents[0]['alt']


    full_item_1=div_tag_items[3].contents[0].contents[0].contents[0]['alt']
    full_item_2=div_tag_items[3].contents[1].contents[0].contents[0]['alt']
    full_item_3=div_tag_items[3].contents[2].contents[0].contents[0]['alt']
    full_item_4=div_tag_items[3].contents[3].contents[0].contents[0]['alt']
    full_item_5=div_tag_items[3].contents[4].contents[0].contents[0]['alt']
    full_item_6=div_tag_items[3].contents[5].contents[0].contents[0]['alt']
  
    skillOrder=[]
    
    div_tag_skill_order= soup.find_all('div', attrs={'class': 'm-1uv578k'})
    for skill in div_tag_skill_order[0].contents:
      skillOrder.append(skill.contents[1].contents[0].contents[0])


    champ_weak=[]
    champ_weak_win_rate=[]

    champ_strong=[]
    champ_strong_win_rate=[]

    div_tag_champ= soup.find_all('div', attrs={'class': 'm-18t0flh e1n6zbyc6'})
    for champ in div_tag_champ[0].contents[1].contents:
      champ_weak.append(champ.contents[1].contents[0])
      champ_weak_win_rate.append(champ.contents[2].contents[0])

    for champ in div_tag_champ[1].contents[1].contents:
      champ_strong.append(champ.contents[1].contents[0])
      champ_strong_win_rate.append(champ.contents[2].contents[0])
    
    champ_data={
      "champion_name":name,
      "main_keystone":main_rune,
      "subkeystone_1":first_keystone,
      "subkeystone_2":second_keystone,
      "subkeystone_3":third_keystone,
      "subkeystone_4":fourth_keystone,
      "subkeystone_5":fifth_keystone,
      "stat_1":stats_1,
      "stat_2":stats_2,
      "stat_3":stats_3,
      "summoner_1":summoner_1,
      "summoner_2":summoner_2,
      "begg_item_1":begg_item_1,
      "begg_item_2":begg_item_2,
      "begg_item_3":begg_item_3,
      "core_item_1":core_item_1,
      "core_item_2":core_item_2,
      "core_item_3":core_item_3,
      "full_item_1":full_item_1,
      "full_item_2":full_item_2,
      "full_item_3":full_item_3,
      "full_item_4":full_item_4,
      "full_item_5":full_item_5,
      "full_item_6":full_item_6,
      "skillOrder":skillOrder,
      "champ_weak":champ_weak,
      "champ_strong": champ_strong,
      "champ_weak_win_rate":champ_weak_win_rate,
      "champ_strong_win_rate":champ_strong_win_rate
      }
    Data.append(champ_data)



groqAPIKey = os.getenv('groqAPIKey')
pineconeAPIKey = os.getenv('pineconeAPIKey')
pineconeIndexName = 'championbuildv1'

llm = Groqllama(model="llama3-70b-8192", api_key=groqAPIKey)
pc = Pinecone(api_key=pineconeAPIKey)

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

documents=[]

for ch_data in Data:
  document_template= """
  Champion Overview:

  Champion Name: {champion_name} - Build guide
  {champion_alternative_name}

  Runes:
  Main Keystone: {main_keystone}
  Subkeystones:{subkeystone_1}, {subkeystone_2}, {subkeystone_3}, {subkeystone_4}, {subkeystone_5}
  Stats Bonus:{stat_1}, {stat_2}, {stat_3}
  Summoner Spells: {summoner_1} and {summoner_2}

  Items:
  Starting Items:{begg_item_1}, {begg_item_2}, {begg_item_3}
  Core Items:{core_item_1}, {core_item_2}, {core_item_3}
  Full Build:{full_item_1}, {full_item_2}, {full_item_3}, {full_item_4}, {full_item_5}, {full_item_6}
  Skill Order from lv1 to lv{level}:{skillOrder}

  Matchups:
  Weak Against:
      - {champ_weak_1} (Win Rate: {champ_weak_win_rate_1})
      - {champ_weak_2} (Win Rate: {champ_weak_win_rate_2})
      - {champ_weak_3} (Win Rate: {champ_weak_win_rate_3})
      - {champ_weak_4} (Win Rate: {champ_weak_win_rate_4})
      - {champ_weak_5} (Win Rate: {champ_weak_win_rate_5})
  Strong Against:
      - {champ_strong_1} (Win Rate: {champ_strong_win_rate_1})
      - {champ_strong_2} (Win Rate: {champ_strong_win_rate_2})
      - {champ_strong_3} (Win Rate: {champ_strong_win_rate_3})
      - {champ_strong_4} (Win Rate: {champ_strong_win_rate_4})
      - {champ_strong_5} (Win Rate: {champ_strong_win_rate_5})
  """
  championAltName=""
  if ch_data["champion_name"]=='DrMundo':
    championAltName="Alternative name for the champion: Mundo"
  elif ch_data["champion_name"]=='Monkeyking':
    championAltName="Alternative name for the champion: WuKong"
  elif ch_data["champion_name"]=='TahmKench':
    championAltName="Alternative name for the champion: Kench"

  formatted_string = document_template.format(
      champion_name=ch_data["champion_name"],
      main_keystone=ch_data["main_keystone"],
      subkeystone_1=ch_data["subkeystone_1"],
      subkeystone_2=ch_data["subkeystone_2"],
      subkeystone_3=ch_data["subkeystone_3"],
      subkeystone_4=ch_data["subkeystone_4"],
      subkeystone_5=ch_data["subkeystone_5"],
      stat_1=ch_data["stat_1"],
      stat_2=ch_data["stat_2"],
      stat_3=ch_data["stat_3"],
      summoner_1=ch_data["summoner_1"],
      summoner_2=ch_data["summoner_2"],
      begg_item_1=ch_data["begg_item_1"],
      begg_item_2=ch_data["begg_item_2"],
      begg_item_3=ch_data["begg_item_3"],
      core_item_1=ch_data["core_item_1"],
      core_item_2=ch_data["core_item_2"],
      core_item_3=ch_data["core_item_3"],
      full_item_1=ch_data["full_item_1"],
      full_item_2=ch_data["full_item_2"],
      full_item_3=ch_data["full_item_3"],
      full_item_4=ch_data["full_item_4"],
      full_item_5=ch_data["full_item_5"],
      full_item_6=ch_data["full_item_6"],
      skillOrder=ch_data["skillOrder"],
      champ_weak_1=ch_data["champ_weak"][0],
      champ_strong_1=ch_data["champ_strong"][0],
      champ_weak_win_rate_1=ch_data["champ_weak_win_rate"][0],
      champ_strong_win_rate_1=ch_data["champ_strong_win_rate"][0],
      champ_weak_2=ch_data["champ_weak"][1],
      champ_strong_2=ch_data["champ_strong"][1],
      champ_weak_win_rate_2=ch_data["champ_weak_win_rate"][1],
      champ_strong_win_rate_2=ch_data["champ_strong_win_rate"][1],
      champ_weak_3=ch_data["champ_weak"][2],
      champ_strong_3=ch_data["champ_strong"][2],
      champ_weak_win_rate_3=ch_data["champ_weak_win_rate"][2],
      champ_strong_win_rate_3=ch_data["champ_strong_win_rate"][2],
      champ_weak_4=ch_data["champ_weak"][3],
      champ_strong_4=ch_data["champ_strong"][3],
      champ_weak_win_rate_4=ch_data["champ_weak_win_rate"][3],
      champ_strong_win_rate_4=ch_data["champ_strong_win_rate"][3],
      champ_weak_5=ch_data["champ_weak"][4],
      champ_strong_5=ch_data["champ_strong"][4],
      champ_weak_win_rate_5=ch_data["champ_weak_win_rate"][4],
      champ_strong_win_rate_5=ch_data["champ_strong_win_rate"][4],
      level=len(champ_data["skillOrder"]),
      champion_alternative_name=championAltName
    )
  champ_name=ch_data['champion_name']
  
  print(ch_data['champion_name'])
  document = Document(text=formatted_string, metadata={'filename':f'{champ_name}.html', 'category':'champion build','champion':champ_name})
  documents.append(document)

print(documents[0:3])
index=VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
