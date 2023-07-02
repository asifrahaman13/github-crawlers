import os
import time
import pinecone
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma, Pinecone
from langchain.chains.question_answering import load_qa_chain

# Load environment variables from .env file
load_dotenv()
api_key = os.environ['OPEN_AI_KEY']
pinecone_key = os.environ['PINECONE_API_KEY']
pinecone_env = os.environ['PINECONE_API_ENV']


def embeddings(username, service):
    responses = []
    if(service == "chroma_service"):
        responses = chroma_embedding(username)
    elif(service == "pinecone_service"):
        responses = pinecone_embedding(username)
    else:
        pass
    return responses


def chroma_embedding(username):
    start_time = time.time()
    OPENAI_API_KEY = os.environ.get(
        'OPENAI_API_KEY', api_key)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    loader = PyPDFLoader(f"pdf_data/api_endpoints_{username}.pdf")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    print(f'Now you have {len(texts)} documents')
    # print(texts[:100])
    print("Upserting the documents.............................................")
    docsearch = Chroma.from_documents(texts, embeddings)
    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY,
                   max_tokens=300),
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )
    responses = []
    print("Trying to load the query.......................................")
    # query = "The document contains the repository along with the codes. Now you need to decide which Repository contains the most complex code. Tell the name of the repository. Also explain in 100 words why you think the repository is the most complex"
    query1 = '''Your task is to identify the repository that contains the most complex code. Provide your response in the following format:

    'Name: [Name of the repository]'

    For instance:

    'Name: Blockdemon'

    Please analyze the document and determine the repository with the most complex code.'''

    # Run the first query.
    response1 = chain.run(query1)
    # Pass the previous response to the second prompt through string formatting for better response and avoiding any conflicts between the answers.
    query2 = f'''Desribe the repository {response1[7:]} in about 150 words.'''

    # Run the second query
    response2 = chain.run(query2)
    end_time = time.time()
    print(response2)
    print(response1)
    responses.append(response1)
    responses.append(response2)
    responses.append(end_time-start_time)
    return responses


def pinecone_embedding(username):
    # Start the timer
    start_time = time.time()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', api_key)
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', pinecone_key)
    PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', pinecone_env)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
    index_name = "testing"
    print("Deleting the previous vectors.........................")
    index = pinecone.Index(index_name)
    index.delete(deleteAll=True)
    # put in the name of your pinecone index here

    loader = PyPDFLoader(f"pdf_data/api_endpoints_{username}.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    print(f'Now you have {len(texts)} documents')
    # print(texts[:100])

    print("Upserting the documents.............................................")
    docsearch = Pinecone.from_texts(
        [t.page_content for t in texts], embeddings, index_name=index_name)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, max_tokens=300)
    chain = load_qa_chain(llm, chain_type="stuff")
    responses = []
    print("Trying to load the query.......................................")
    # query = "The document contains the repository along with the codes. Now you need to decide which Repository contains the most complex code. Tell the name of the repository. Also explain in 100 words why you think the repository is the most complex"
    query1 = '''Your task is to identify the repository that contains the most complex code. Provide your response in the following format:

    'Name: [Name of the repository]'

    For instance:

    'Name: Blockdemon'

    Please analyze the document and determine the repository with the most complex code.'''

    # Run the first query.
    # response1 = chain.run(query1)
    docs = docsearch.similarity_search(query1)
    response1 = chain.run(input_documents=docs, question=query1)
    print(response1)
    # Pass the previous response to the second prompt through string formatting for better response and avoiding any conflicts between the answers.
    query2 = f'''Desribe the repository {response1[7:]} in about 150 words'''

    # Run the second query
    # response2 = chain.run(query2)
    docs = docsearch.similarity_search(query2)
    response2 = chain.run(input_documents=docs, question=query2)
    print(response2)
    print(response1)
    responses.append(response1)
    responses.append(response2)
    index.delete(deleteAll=True)
    end_time = time.time()
    responses.append(end_time-start_time)
    return responses
