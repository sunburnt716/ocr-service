# OCR Service for Financial-Tracker App

This repository contains the standalone OCR microservice built to support the Financial-Tracker web application. It processes scanned or uploaded receipts, extracts structured transaction data, and returns a clean JSON response consumable by the JavaScript frontend.

The service enables users to take a photo of a receipt or upload one, automatically convert it into editable transactions, and send them directly to the financial tracking system.

---

## Overview

The OCR system performs the following tasks:

- Accepts uploaded receipt images through a REST API.
- Processes images using Python DocTR, Pytesseract, and custom parsing logic.
- Extracts:
  - Item names  
  - Prices  
  - Purchase date  
  - Store name  
- Cleans and normalizes text for frontend consumption.
- Returns results as a structured list of transactions.

This allows the frontend to populate transactions automatically based on scanned receipts.

---

## Technology and Tools Used

- Python 3  
- FastAPI for the REST API backend  
- Pydantic for schema validation  
- python-doctr for OCR  
- Pytesseract for fallback OCR and detail extraction  
- Pillow for preprocessing  
- Docker for containerization  

---

## Project Structure

ocr-service/
│── app.py # FastAPI server
│── pipeline.py # OCR and parsing pipeline
│── models.py # Response and schema models
│── utils.py # Helper functions for OCR and preprocessing
│── requirements.txt # Python dependencies
│── Dockerfile # Container configuration
│── sample_receipts/ # Optional test images
│── README.md # Project documentation

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/<your-username>/ocr-service.git
cd ocr-service
2. Create and Activate a Virtual Environment
Windows:

python -m venv venv
venv\Scripts\activate
Mac/Linux:

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies


pip install -r requirements.txt
Running the OCR Service
Start the API server:

uvicorn app:app --reload
Server will run at:

http://localhost:8000
Swagger documentation:

http://localhost:8000/docs
API Usage
POST /scan
Uploads an image and receives OCR-parsed receipt data.

Request (multipart/form-data):

file: <image>
Example Response:

json
Copy code
{
  "items": [
    {
      "name": "Bananas",
      "price": 1.99,
      "date": "2024-11-20",
      "store": "Costco"
    },
    {
      "name": "Milk",
      "price": 3.49,
      "date": "2024-11-20",
      "store": "Costco"
    }
  ]
}
How the OCR Pipeline Works
1. Image Preprocessing
Resize and sharpen

Convert to grayscale

Normalize lighting and contrast

2. Text Detection and Recognition (DocTR)
Detects text regions

Extracts words and lines

3. Keyword and Pattern Matching
Finds store name

Identifies purchase date

Extracts prices using regex-based number detection

4. Item–Price Pairing Algorithm
Associates each item name with a nearby price

Filters noise (tax, total, coupons)

5. JSON Formatting
Sends structured, clean transaction data to the frontend

Frontend Integration
The React frontend performs the following:

User selects Take Photo or Upload Document

Image is stored in state

The frontend sends the file to the OCR service:

await axios.post("http://localhost:8000/scan", formData);
The OCR service returns parsed transaction objects

The user can edit or delete items before saving

This creates a seamless receipt-to-transaction workflow.

Running with Docker
Build the container:
docker build -t ocr-service .
Run the container:
docker run -p 8000:8000 ocr-service
This allows the OCR service to run with no Python environment setup required.

Learnings Gained From This Project

-> Learned Python in the context of building production-ready tools
-> Learned how OCR models detect text, bounding boxes, and sequences
-> Understood python-doctr and pytesseract pipelines
-> Built modular parsing algorithms for receipts
-> Connected a JavaScript/React frontend to a Python backend
-> Designed a real microservice with Docker for deployment
-> Learned to classify and extract item, price, and date from noisy receipts
-> Built a scalable parsing pipeline for generalizing across receipt formats

Future Improvements

-> Support for multi-page receipts
-> Confidence scoring per item
-> Custom store-specific OCR models
-> Automatic rotation correction
-> Bulk receipt scanning endpoint
