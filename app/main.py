# main.py
from PIL import Image
from .ocr_predictor import run_ocr
from .utils import parse_ocr_text, parse_into_items


def run_local_test(image_path: str):
    print("\n=== OCR LOCAL TEST ===")
    print(f"Image: {image_path}")

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"[ERROR] Failed to open image: {e}")
        return

    try:
        print("\nRunning OCR...")
        ocr_result = run_ocr(img)

        # Ensure ocr_result is a dict with "text"
        text = ""
        if isinstance(ocr_result, dict) and "text" in ocr_result:
            text = ocr_result["text"]
        else:
            text = str(ocr_result)

        print("\n=== RAW OCR TEXT ===")
        print(text)

        print("\n=== PARSED METADATA ===")
        parsed = parse_ocr_text(text)
        for k, v in parsed.items():
            print(f"{k}: {v}")

        print("\n=== PARSED ITEMS ===")
        items = parse_into_items(text)
        for item in items:
            print(f"- {item['name']}: ${item['price']}")

        print("\n=== DONE ===\n")

    except Exception as e:
        print(f"[ERROR] OCR or parsing failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.main path/to/image.jpg")
        sys.exit(1)

    run_local_test(sys.argv[1])
