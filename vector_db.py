from langchain_community.vectorstores import FAISS


VECTOR_DB_PATH = "vectorstore"


def create_vector_db(chunks, embedding_model):

    vectorstore = FAISS.from_documents(

        documents=chunks,

        embedding=embedding_model

    )

    vectorstore.save_local(VECTOR_DB_PATH)

    print("\nVector Store Saved Successfully.")

    return vectorstore


def load_vector_db(embedding_model):

    vectorstore = FAISS.load_local(

        VECTOR_DB_PATH,

        embedding_model,

        allow_dangerous_deserialization=True

    )

    return vectorstore