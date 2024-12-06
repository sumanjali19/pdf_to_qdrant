# -*- coding: utf-8 -*-
"""pdf_to_qdrant.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BIMFGyBNJ7kscDSER52jpRz8jGLOSl4Z
"""

!pip install --upgrade qdrant-client

!pip install pdfplumber
!pip install sentence-transformers
!pip install qdrant-client

!pip install pymupdf

import fitz  # PyMuPDF for text and image extraction
import pdfplumber  # For table extraction
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams
import uuid
import os

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url="https://0dd7af9f-4dfa-4aa2-bf13-155369ab6f6e.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="KhrHS7tuwnszeJcpprSOGhs00kBuogjJePAkua70FOy9fQ5Eons7SA"
)

# Load embedding model for vector representation
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to upload data to Qdrant
def store_in_qdrant(content, metadata, collection_name="suma"):
    # Create embedding
    embedding = model.encode(content).tolist()

    # Generate a UUID for the point ID
    point_id = str(uuid.uuid4())  # UUID4 generates a valid unique ID

    # Construct Qdrant point
    point = PointStruct(
        id=point_id,  # Use the generated UUID as the ID
        vector={"default": embedding},  # Specify the vector name
        payload=metadata  # Store content and metadata in payload
    )

    # Upsert into Qdrant
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[point]
    )

# Process text from PDF
def process_text(pdf_path):
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text()
            if text.strip():
                paragraphs = text.split('\n')
                for para_num, para in enumerate(paragraphs, start=1):
                    metadata = {
                        "text": para.strip(),
                        "page": page_num,
                        "paragraph": para_num
                    }
                    store_in_qdrant(para.strip(), metadata)
                    print(f"Text stored with metadata: {metadata}")

# Process images from PDF
def process_images(pdf_path):
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images, start=1):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                description = f"Image-{img_index} on page-{page_num}"
                metadata = {
                    "description": description,
                    "page": page_num
                }
                store_in_qdrant(description, metadata)
                print(f"Image description stored with metadata: {metadata}")

# Process tables from PDF
def process_tables(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for table_index, table in enumerate(tables, start=1):
                table_content = "\n".join(
                    ["\t".join([cell if cell is not None else "" for cell in row]) for row in table]
                )
                metadata = {
                    "table": table_content,
                    "description": f"Table-{table_index} on page-{page_num}",
                    "page": page_num
                }
                store_in_qdrant(table_content, metadata)
                print(f"Table stored with metadata: {metadata}")

# Main function
if __name__ == "__main__":
    pdf_path = "/content/Algorithms_and_Flowcharts.pdf"  # Replace with your file path

    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist.")
        exit(1)

    # Ensure the collection exists in Qdrant
    def ensure_collection_exists(collection_name):
        try:
            qdrant_client.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists.")
        except Exception:
            print(f"Collection '{collection_name}' does not exist. Creating it...")
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "default": VectorParams(size=384, distance="Cosine")
                }
            )

    ensure_collection_exists("suma")

    try:
        print("Processing text...")
        process_text(pdf_path)
    except Exception as e:
        print(f"Error processing text: {e}")

    try:
        print("Processing images...")
        process_images(pdf_path)
    except Exception as e:
        print(f"Error processing images: {e}")

    try:
        print("Processing tables...")
        process_tables(pdf_path)
    except Exception as e:
        print(f"Error processing tables: {e}")

    print("PDF processing completed and data stored in Qdrant.")