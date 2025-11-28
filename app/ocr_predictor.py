from doctr.models import ocr_predictor
from PIL import Image
from typing import Dict
import numpy as np

model = ocr_predictor(pretrained=True)

def run_ocr(image: Image.Image) -> Dict:
    try:
        if image.mode != "RGB":
            image = image.convert("RGB")

        img_array = np.array(image)

        doc = model([img_array])

        text = "\n".join(
            " ".join(word.value for word in line.words)
            for page in doc.pages
            for block in page.blocks
            for line in block.lines
        )

        return {"text": text, "raw_result": doc}

    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {e}")
