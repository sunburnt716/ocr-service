# 📄 OCR Microservice – Receipt Processing Engine

This repository contains the standalone **OCR Microservice** used by the Financial-Tracker application.
Its purpose is to process scanned or uploaded **receipt images**, extract relevant **transaction data**, and return it in structured JSON format for downstream use.

---

## 🚀 Overview

This microservice exposes a REST API for uploading receipt images through a multipart form-data request.
Once an image is uploaded, it:

1. Runs the image through an OCR engine
2. Cleans and normalizes the extracted text
3. Parses out:

   * Vendor / Transaction Name
   * Date
   * Total Amount
   * Line items (if applicable)
4. Returns the extracted data as a JSON response

Built as a lightweight, independent service, it integrates easily with other applications.

---

## 🧩 Features

* Accepts image formats: `.jpg`, `.jpeg`, `.png`, `.pdf`
* Uses OCR to extract structured receipt data
* Simple REST interface with JSON output
* Can be used standalone or plugged into any larger system
* Asynchronous and efficient
* **Docker support planned** (see Roadmap)

---

## 📦 Tech Stack

* **Node.js** (Express)
* **Tesseract OCR / External OCR Provider**
* **Multer** for file uploads
* **Custom parsing utilities** for receipts

---

## 📁 Project Structure

```
/ocr-service
│── /controllers
│     └── ocrController.js       # Main logic for OCR extraction
│── /routes
│     └── ocrRoutes.js           # OCR API routes
│── /utils
│     └── parser.js              # Logic to interpret raw OCR text
│── server.js                    # Express server setup
└── package.json
```

---

## 🛠 Installation

Clone the repository:

```
git clone <your-repo-url>
cd ocr-service
```

Install dependencies:

```
npm install
```

Start the server:

```
npm run dev
```

Default URL:

```
http://localhost:5001
```

---

## 📡 API Endpoints

### **POST /api/ocr/receipt**

Uploads a receipt image and returns structured transaction data.

#### **Request (multipart/form-data)**

| Field | Type | Description   |
| ----- | ---- | ------------- |
| file  | File | Receipt image |

#### Example (cURL)

```
curl -X POST -F "file=@receipt.jpg" http://localhost:5001/api/ocr/receipt
```

---

## 🧾 Example Response

```json
{
  "vendor": "Trader Joe's",
  "date": "2024-11-21",
  "amount": 32.50,
  "rawText": "Original OCR output...",
  "confidence": 0.92
}
```

---

## 🌐 Integration Guide

This microservice is designed to integrate seamlessly with:

* Finance tracking applications
* Expense management tools
* Gmail API receipt importers
* Backend data pipelines

The main application simply sends the uploaded image → the microservice processes it → returns parsed JSON → the main backend stores or analyzes it.

---

## 🧪 Running Tests

```
npm test
```

---

## 🗺 Roadmap

The following enhancements are planned for future releases:

### 🔜 **Docker Compatibility**

* Add a `Dockerfile` for containerized deployment
* Add a lightweight OCR image with Tesseract installed
* Create optional `docker-compose.yml` for multi-service integration
* Allow running the service using:

  ```
  docker build -t ocr-service .
  docker run -p 5001:5001 ocr-service
  ```

### 🔜 Improved Parsing

* Better vendor detection
* Improved date formatting / locale handling
* Multi-currency support

### 🔜 Cloud Integration

* AWS S3 image upload
* Pipeline with Gmail API receipt ingestion
* Google Cloud Vision / AWS Textract option

---
