from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
import os
from dotenv.main import load_dotenv
load_dotenv()

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
You can assume the question about the {doc_name}.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate(template=_template, input_variables=["question", "chat_history","doc_name"])

template = """You are an AI assistant for answering questions about the {doc_name}.
You are given the following extracted parts of a long document and a question. Provide a conversational answer.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not about the {doc_name}, politely inform them that you are tuned to only answer questions about the {doc_name}.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context","doc_name"])

def get_chain(vectorstore):
    os.environ['OPENAI_API_KEY'] = os.environ['KEY'] 
    llm = OpenAI(temperature=0)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )
    return qa_chain
