# pdf_to_qdrant
PDF to Qdrant

This code pulls data from a PDF: text, tables, and images. Data is stored in the Qdrant collection to efficiently query and retrieve that information.


## Features

Extracts text from PDF with metadata about page number and paragraph number
Extracts Tables with structure along with page and description
Extracts Image descriptions with metadata: page number and description
Store vectors for fast similarity search in a Qdrant collection.
- Demonstrates how to query the stored data with some example search queries.

## Requirements
- Python 3.7+
- Libraries:
  - `pymupdf`
  - `pdfplumber`
  - `sentence-transformers`
  - `qdrant-client`
  - `requests`


## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/sumanjali19/pdf_to_qdrant.git
   cd pdf_to_qdrant
2. Update pdf_to_qdrant.py with your Qdrant API Key and Cluster URL:

qdrant_client = QdrantClient(
    url="YOUR_QDRANT_URL",
    api_key="YOUR_API_KEY"
)
Save your PDF document (like Algorithms_and_Flowcharts.pdf) in the same folder, or mention the path of that PDF.
*How to Run*
Process the PDF and upload data to Qdrant:

python pdf_to_qdrant.py
Run example queries to retrieve data:

python examples/example_query.py
