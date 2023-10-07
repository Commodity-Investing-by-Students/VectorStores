from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings


sentence_transformer_ef = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(collection_name='news_rss', persist_directory='chroma_rss',
                     embedding_function=sentence_transformer_ef)

llm = ChatOpenAI(
    openai_api_key='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',
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

answer_bank = ''

while True:
    query = input("Enter query: ")
    if query == 'quit':
        break
    answer = qa(query)['result']
    answer_bank += answer + ' '
    sources = vectorstore.similarity_search(answer)
    sources = [s.metadata['source'] for s in sources]

    print(answer, '\n')
    print('Sources: ')
    for source in sources:
        print(source, '\n')