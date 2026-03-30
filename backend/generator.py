import requests

def generate_answer(context: str, query: str, temperature: float = 0.2) -> str:
    prompt = f"""
You are a strict medical assistant.
only response what user ask to get accurate response only want
Answer ONLY using the given context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {query}

Answer:
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral:latest",
            "prompt": prompt,
            "stream": False,
            "options": {   # ✅ fixed
                "temperature": temperature
            }
        }
    )

    data = res.json()

    # Debug
    print("OLLAMA RESPONSE:", data)

    if "response" in data:
        return data["response"].strip()
    elif "message" in data:
        return data["message"].get("content", "").strip()
    else:
        return str(data)