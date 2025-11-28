from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ParsedItem(BaseModel):
    name: str
    price: float

class OCRResponse(BaseModel):
    text: str = Field(..., description="Raw extracted OCR text")
    filename: Optional[str] = Field(None, description="Original filename")
    name: Optional[str] = Field(None, description="Parsed merchant/name")
    price: Optional[float] = Field(None, description="Parsed price (first match)")
    date: Optional[str] = Field(None, description="Parsed date in YYYY-MM-DD")
    items: Optional[List[ParsedItem]] = Field(default=None, description="Line-level parsed items")
