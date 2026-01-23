from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

CLEAN_DIR = Path("regshield/data/cleaned_rules_us")
DB_DIR = Path("regshield/data/chroma_us")
DB_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("DEBUG 1: main start")
    print("DEBUG 2: CLEAN_DIR =", CLEAN_DIR)
    print("DEBUG 3: DB_DIR =", DB_DIR)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    print("DEBUG 4: DB_DIR created, exists =", DB_DIR.exists())
    import sys
    print("DEBUG 5: exiting early before embeddings")
    sys.exit(0)


    files = list(CLEAN_DIR.glob("*.txt"))[:1]
    if not files:
        raise SystemExit(f"No cleaned rule files found in: {CLEAN_DIR}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = []
    for f in files:
        text = f.read_text(errors="ignore")
        chunks = splitter.split_text(text)
        for i, ch in enumerate(chunks):
            docs.append(Document(page_content=ch, metadata={
                "rule_file": f.name,
                "chunk": i,
                "jurisdiction": "US"
            }))

    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # recreate index each run (simple + reliable for MVP)
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embed,
        persist_directory=str(DB_DIR),
        collection_name="regshield_us_rules"
    )
    vectordb.persist()

    print("INDEXED_FILES:", len(files))
    print("INDEXED_CHUNKS:", len(docs))
    print("DB_DIR:", DB_DIR)

if __name__ == "__main__":
    main()
