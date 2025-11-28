import io
import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from PIL import Image
from dotenv import load_dotenv

from .ocr_predictor import run_ocr
from .utils import parse_ocr_text, parse_into_items

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "ocrDatabase")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "ocrTexts")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

app = FastAPI(title="OCR Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract/")
async def extract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG/PNG allowed.")

    try:
        content = await file.read()
        pil_img = Image.open(io.BytesIO(content)).convert("RGB")
        result = run_ocr(pil_img)
        text = result.get("text", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {e}")

    parsed = parse_ocr_text(text)
    items = parse_into_items(text)

    doc = {
        "filename": file.filename,
        "text": text,
        "parsed": parsed,
        "items": items,
        "timestamp": datetime.utcnow(),
    }

    try:
        collection.insert_one(doc)
    except Exception as e:
        print("Warning: failed to save to DB:", e)

    return {
        "text": text,
        "filename": file.filename,
        "name": parsed.get("name"),
        "price": parsed.get("price"),
        "date": parsed.get("date"),
        "items": items,
    }
