from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain.schema.document import Document

import os

os.environ["TOKENIZERS_PARALLELISM"] = "true"


def analyze(text_to_analyze: str) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1024,
                                              chunk_overlap=50)
    doc = Document(page_content=text_to_analyze, metadata={"source": "local"})
    texts = splitter.split_documents([doc])
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'})
    return FAISS.from_documents(texts, embeddings)


def build_llm(db: FAISS) -> RetrievalQA:
    """
    Create an AI Chat large language model prepared
    to answer questions about content of the database
    """

    template = """
    Use information from the following text to answer questions about its content.
    If you do not know the answer, say that you do not know, and do not try to make up an answer.
    Context: {context}
    Question: {question}
    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

    llm = CTransformers(model=os.getenv("MODEL_PATH"),
                        model_type=os.getenv("MODEL_TYPE"),
                        config={'max_new_tokens': 256, 'temperature': 0.3})
    retriever = db.as_retriever(search_kwargs={'k': 1})
    prompt = PromptTemplate(
        template=template,
        input_variables=['context', 'question'])

    return RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever, return_source_documents=False,
                                       chain_type_kwargs={'prompt': prompt})


def summarize_article(query: str, text_to_analyze: str) -> dict:
    db = analyze(text_to_analyze)
    qa_llm = build_llm(db)
    output = qa_llm({"query": query})
    print("===== output ====")
    print(output)

    return output
