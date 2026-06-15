from app.ocr_service import extract_text_from_image

image_path = "test_data/sample_prescription.png"

text = extract_text_from_image(image_path)

print("OCR OUTPUT:")
print(text)