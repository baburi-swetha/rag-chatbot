from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

from embeddings import get_embedding_model
from vector_db import load_vector_db
from query_classifier import classify_query

load_dotenv()

# ----------------------------
# Load Groq API Key
# ----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI(title=" RAG System")

# ----------------------------
# Load Embedding Model
# ----------------------------

embeddings = get_embedding_model()

# ----------------------------
# Load Vector Database
# ----------------------------

vectorstore = load_vector_db(embeddings)

print("Vector Store Loaded Successfully")

# ----------------------------
# Request Model
# ----------------------------

class QueryRequest(BaseModel):
    question: str

# ----------------------------
# Home API
# ----------------------------

@app.get("/")
def home():
    return {
        "message": "Enterprise RAG API Running Successfully"
    }

# ----------------------------
# Ask API
# ----------------------------

@app.post("/ask", summary="Ask Enterprise Assistant")
def ask(request: QueryRequest):

    # Predict metadata
    prediction = classify_query(request.question)

    department = prediction["department"]
    category = prediction["category"]

    # Retrieve similar chunks
    docs = vectorstore.similarity_search(
        request.question,
        k=5
    )

    filtered_docs = []

    # Metadata Filtering
    for doc in docs:

        doc_department = doc.metadata.get("department", "")
        doc_category = doc.metadata.get("category", "")

        if (
            doc_department.lower() == department.lower()
            or
            doc_category.lower() == category.lower()
        ):
            filtered_docs.append(doc)

    # No Results
    if len(filtered_docs) == 0:
        return {
            "question": request.question,
            "predicted_department": department,
            "predicted_category": category,
            "answer": "No relevant documents found.",
            "sources": []
        }

    # Build Context
    context = ""

    source_set = set()

    for doc in filtered_docs:

        context += doc.page_content + "\n\n"

        source_set.add(
            doc.metadata.get(
                "filename",
                "Unknown"
            )
        )

    sources = list(source_set)

    # Prompt
    prompt = f"""
You are an intelligent enterprise assistant.

Answer ONLY from the given context.

If the answer is not available, reply:

"I don't have enough information."

Explain in simple English.

Context:
{context}

Question:
{request.question}
"""

  
    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You answer only from the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        answer = response.choices[0].message.content

    except Exception as e:

        answer = f"Groq API Error: {str(e)}"

    

    return {

        "question": request.question,

        "predicted_department": department,

        "predicted_category": category,

        "answer": answer,

        "sources": sources

    }