import re
from datetime import datetime
from typing import Dict, Any, List

PRICE_RE = re.compile(r"(?<!\d)(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2}))(?!\d)")
DATE_RES = [
    re.compile(r"(\d{4}-\d{2}-\d{2})"),
    re.compile(r"(\d{2}/\d{2}/\d{4})"),
    re.compile(r"(\d{2}\.\d{2}\.\d{4})"),
]

def normalize_price_str(price_str: str) -> float:
    s = price_str.replace(",", "").replace(" ", "")
    try:
        return float(s)
    except ValueError:
        s = s.replace(".", "")
        try:
            return float(s) / 100.0
        except Exception:
            return 0.0

def extract_first_price(text: str) -> float:
    if not text:
        return 0.0
    m = PRICE_RE.findall(text)
    if not m:
        return 0.0
    prices = [normalize_price_str(p) for p in m]
    total_line = re.search(r"Total[:\s]*([\d.,]+)", text, re.IGNORECASE)
    if total_line:
        return normalize_price_str(total_line.group(1))
    return max(prices)

def extract_first_date(text: str) -> str:
    if not text:
        return datetime.utcnow().strftime("%Y-%m-%d")
    for rex in DATE_RES:
        m = rex.search(text)
        if m:
            raw = m.group(1)
            try:
                if "-" in raw:
                    return raw
                if "/" in raw:
                    dt = datetime.strptime(raw, "%m/%d/%Y")
                    return dt.strftime("%Y-%m-%d")
                if "." in raw:
                    dt = datetime.strptime(raw, "%d.%m.%Y")
                    return dt.strftime("%Y-%m-%d")
            except Exception:
                continue
    return datetime.utcnow().strftime("%Y-%m-%d")

def extract_top_line(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "Unknown"
    return lines[0]

def parse_ocr_text(text: str) -> Dict[str, Any]:
    return {
        "name": extract_top_line(text),
        "price": extract_first_price(text),
        "date": extract_first_date(text),
        "raw_text": text,
    }

def parse_into_items(text: str) -> List[Dict[str, Any]]:
    items = []
    prev_line = ""
    for line in text.splitlines():
        ln = line.strip()
        if not ln:
            continue
        m = PRICE_RE.search(ln)
        if m:
            price = normalize_price_str(m.group(1))
            name = PRICE_RE.sub("", ln).strip(" -:,.")
            # if name is empty, try using previous line as the item name
            if not name and prev_line:
                name = prev_line
            # skip totals
            if re.search(r"total|sub[- ]?total|sales tax|balance", name, re.IGNORECASE):
                prev_line = ""
                continue
            items.append({"name": name if name else "Item", "price": price})
        else:
            prev_line = ln  # store this line as potential item name
    return items

