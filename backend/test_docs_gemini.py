from app.document_service import extract_text_from_docx, extract_images_from_docx
#from app.llm_service import analyze_prescription_image
from app.llm_service import analyze_prescription_image, analyze_prescription_text

docx_path = "test_data/sample_text_prescription.docx"
output_dir = "test_data/docx_images_for_analysis"

text = extract_text_from_docx(docx_path)
image_paths = extract_images_from_docx(docx_path, output_dir)

print("DOCX TEXT:")
print(text if text else "No typed text found")
if text:
    print("\nAnalyzing typed DOCX text...")
    text_result = analyze_prescription_text(text)
    print(text_result)

print("\nAnalyzing embedded images...")

all_results = []

for index, image_path in enumerate(image_paths, start=1):
    print(f"Analyzing DOCX image {index}...")

    result = analyze_prescription_image(image_path)

    all_results.append({
        "image_number": index,
        "image_path": image_path,
        "analysis": result
    })

print("\nFINAL DOCX IMAGE ANALYSIS:")

for item in all_results:
    print("=" * 50)
    print(f"DOCX IMAGE {item['image_number']}")
    print(item["analysis"])