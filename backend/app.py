from fastapi import FastAPI
from backend.retrieve import search, get_subgraph
from backend.generator import generate_answer

app = FastAPI()

@app.get("/query")
def query(q: str):
    if not q:
        return {"error": "Query cannot be empty"}

    try:
        nodes = search(q)

        context = []
        for n in nodes:
            context.extend(get_subgraph(n))

        # remove duplicates
        context = list(set(context))

        answer = generate_answer("\n".join(context), q)

        return {
            "query": q,
            "answer": answer,
            "context": context[:5]  # limit output
        }

    except Exception as e:
        return {"error": str(e)}