import pickle
import os
from typing import Any
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from query_data import get_chain
from stores import create_vectors_from_url

app = FastAPI()

d = {}
# loads all files in a certain path and adds them to dict
import os
import pickle

for filename in os.listdir("vecstores"):
    with open("vecstores/" + filename, "rb") as f:
        d["{0}".format(filename)] = pickle.load(f)
print(d)


def dict_of_vecs(filename):
    with open("vecstores/" + filename + ".pkl", "rb") as f:
        d["{0}".format(filename)] = pickle.load(f)
    print(d)


class Query(BaseModel):
    question: str
    history: Any
    file_name: str
    url: str
    dname: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat")
async def query(query: Query, background_tasks: BackgroundTasks):
    file_name_ext = query.file_name + ".pkl"
    if file_name_ext in d:
        print("I ALREADY EXIST")
        # look up the right vector store for str url.
        qa_chain = get_chain(d[file_name_ext])
        # Need to modify prompt to take further params for the specific document being use
        # currently hard coded for one report.
        result = qa_chain(
            {
                "question": query.question,
                "chat_history": query.history,
                "doc_name": query.dname,
            }
        )
        results = {"answer": result["answer"]}
        return results
    else:
        vectorstore = create_vectors_from_url(query.url, query.file_name)
        print("MAKING A NEW STORE. DON'T EXIST")
        qa_chain = get_chain(vectorstore)
        result = qa_chain(
            {
                "question": query.question,
                "chat_history": query.history,
                "doc_name": query.dname,
            }
        )
        results = {"answer": result["answer"]}
        background_tasks.add_task(dict_of_vecs, query.file_name)
        return results
