import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from tqdm import tqdm

def IndexFromGit(folder_path: str, embeddings, vectorstore, chunk_size: int = 2000):
    """
    ### Load pdf from folder
    this function loads documents from a folder and creates a Fass index (db).\n
    - folder_path: Path to folder containing PDFs\n
    - chunk_size: Chunk size in characters (default 2000)\n
    - embeddings: Embeddings object from langchain.embeddings\n
    - vectorstore: could be FAISS or ChromaDB\n
    """

    # Assuming your PDFs are in a folder named 'test_pdfs'
    code_files = [f for f in os.listdir(folder_path)]

    documents = []
    # Process each PDF file and split into chunks of 24000 characters
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0, length_function=len, is_separator_regex=False) # FIXED

    documents = []
    # Process each PDF file
    for root, dirs, code_files in os.walk(folder_path):
        for code_file in tqdm(code_files, "Parsing codes"):
            if not code_file.endswith(('.png','.svg', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                with open(os.path.join(root, code_file), 'r', encoding='utf-8') as code:
                    lines = code.readlines()
                    total_text = ''
                    for line in lines:
                        total_text += line  # Extract text from each page
            
                texts = text_splitter.split_text(total_text)

                for text in texts:
                    document = Document(page_content=text, metadata={"title": code_file, "type": "code", "tags": ["code"]})
                    documents.append(document)


    # Store Embeddings in FAISS
    for i in tqdm(range(0,1), "Creating db from documents"):
        db = vectorstore.from_documents(documents, embeddings)
    return db
