from app.document_service import convert_pdf_to_images
from app.llm_service import analyze_prescription_image

pdf_path = "test_data/sample_prescription.pdf"
output_dir = "test_data/pdf_pages_for_analysis"

image_paths = convert_pdf_to_images(pdf_path, output_dir)

all_results = []

for index, image_path in enumerate(image_paths, start=1):
    print(f"Analyzing page {index}...")

    result = analyze_prescription_image(image_path)

    all_results.append({
        "page_number": index,
        "image_path": image_path,
        "analysis": result
    })

print("\nFINAL PDF ANALYSIS:")

for page_result in all_results:
    print("=" * 50)
    print(f"PAGE {page_result['page_number']}")
    print(page_result["analysis"])