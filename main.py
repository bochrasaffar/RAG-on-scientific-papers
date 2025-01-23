from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from index import load_index,add_paper_to_index,remove_document_from_index,get_embedder,search_index
import glob
from generate import generate_answer
from helpers import get_cited_works
app = FastAPI()


class QueryResult(BaseModel):
    answer: str
    source_passage: List[str]
    cited_works: List[str]

embedder = get_embedder()
global faiss_index
faiss_index = load_index(embedder)

@app.post("/index")
def create_index(papers_path: str):
    faiss_index = load_index(embedder)
    if os.path.exists(papers_path):
        list_pdf = glob.glob(os.path.join(papers_path,'*.pdf'))
        if len(list_pdf)==0:
            message = f"path empty and does not contain any pdf file"
        else:
            for pdf_path in list_pdf:
                add_paper_to_index(faiss_index,pdf_path)
                
            message = f" {len(list_pdf)} Documents added successfully"
    else:
        message = "path does not exist"
        

    return {"message": message}

@app.delete("/index/{paper_name}")
def remove_document(paper_name: str):
    if remove_document_from_index(faiss_index,paper_name):
        return {"message": "Document removed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Paper not found")

@app.post("/query", response_model=QueryResult)
def query_index(query: str):
    results = search_index(faiss_index, query)
    results = [x.page_content for x in results]
    answer = generate_answer(results,query)
    cited_works = get_cited_works(' '.join(results))
    
    return QueryResult(
        answer=answer,
        source_passage=results,
        cited_works=cited_works
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
