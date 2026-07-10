import os

from loaders import load_document
from metadata import detect_metadata
from embeddings import get_embedding_model
from vector_db import create_vector_db

from langchain_text_splitters import RecursiveCharacterTextSplitter


UPLOAD_FOLDER = "uploads"

documents = []

print("\n========================================")
print("Starting Document Ingestion...")
print("========================================\n")


for file in os.listdir(UPLOAD_FOLDER):

    file_path = os.path.join(UPLOAD_FOLDER, file)

    if os.path.isdir(file_path):
        continue

    print(f"Reading File : {file}")

    try:

        docs = load_document(file_path)

        # Attach Metadata Automatically

        for doc in docs:

            metadata = detect_metadata(
                file,
                doc.page_content
            )

            doc.metadata.update(metadata)

        documents.extend(docs)

        print(f"Successfully Loaded : {file}\n")

    except Exception as e:

        print(f"Error Loading {file}")

        print(e)

print("----------------------------------------")
print(f"Total Documents Loaded : {len(documents)}")
print("----------------------------------------\n")


print("Splitting Documents...")

splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50

)

chunks = splitter.split_documents(documents)

print(f"Chunks Created : {len(chunks)}")


print("\nLoading Embedding Model...")

embedding_model = get_embedding_model()

print("Embedding Model Loaded Successfully.")


print("\nCreating FAISS Vector Store...")

vectorstore = create_vector_db(

    chunks,

    embedding_model

)

print("Vector Store Created Successfully.")

print("\nSample Metadata\n")

for i, chunk in enumerate(chunks[:5]):

    print(f"Chunk {i+1}")

    print(chunk.metadata)

    print("----------------------------------")

print("\n========================================")
print("Ingestion Completed Successfully")
print("========================================")