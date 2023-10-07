import pandas as pd
import chromadb
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from get_news_data import get_news


chroma_client = chromadb.PersistentClient(path='chroma_rss')
sentence_transformer_ef = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
merged_country_news = get_news()

texts = []
metadatas = []
for i in range(merged_country_news.shape[0]):
    news_slice = merged_country_news.iloc[i]
    title = news_slice['Title']
    summary = news_slice['Summary']
    date = news_slice['Published']
    source = news_slice['Link']
    text = f'{date} {title} {summary}'
    texts.append(text)
    metadatas.append({'source': source})

vectordb = Chroma.from_texts(texts, collection_name='news_rss', persist_directory='chroma_rss', embedding=sentence_transformer_ef, metadatas=metadatas)