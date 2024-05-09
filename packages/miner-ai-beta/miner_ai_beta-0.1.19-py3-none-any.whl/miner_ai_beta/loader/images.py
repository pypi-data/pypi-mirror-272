import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from openai import OpenAI
from tqdm import tqdm
import base64

api_key = os.environ.get('OPENAI_API_KEY')

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def IndexFromImages(folder_path: str, embeddings, vectorstore, chunk_size: int = 2000):
    """
    ### Load pdf from folder
    this function loads documents from a folder and creates a Fass index (db).\n
    - folder_path: Path to folder containing PDFs\n
    - chunk_size: Chunk size in characters (default 2000)\n
    - embeddings: Embeddings object from langchain.embeddings\n
    - vectorstore: could be FAISS or ChromaDB\n
    """

    documents = []
    # Process each PDF file and split into chunks of 24000 characters
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0, length_function=len, is_separator_regex=False) # FIXED

    documents = []
    # Process each PDF file
    for root, dirs, image_files in os.walk(folder_path):
        for image_file in tqdm(image_files, "Parsing codes"):
            file_name, file_extension = os.path.splitext(image_file)
            if  image_file.endswith(('.png','.svg', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                base64_image = encode_image(os.path.join(root, image_file))
                client = OpenAI(
                    api_key=api_key,
                )

                messages = [
                        {"role": "user", 
                            "content": [
                                    {
                                    "type": "text",
                                    "text": "Descrivi il contenuto di questa immagine"
                                    },
                                    {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ]
                
                response = client.chat.completions.create(
                        model="gpt-4-vision-preview", # model = "deployment_name".
                        messages=messages
                    )
                
                image_content = response.choices[0].message.content

                # Extract text from each page            
                texts = text_splitter.split_text(image_content)

                for text in texts:
                    document = Document(page_content=text, metadata={"image_name": file_name, "image_extension": file_extension, "tags": ["image"]})
                    documents.append(document)

    # Store Embeddings in FAISS
    for i in tqdm(range(0,1), "Creating db from documents"):
        db = vectorstore.from_documents(documents, embeddings)
    return db
