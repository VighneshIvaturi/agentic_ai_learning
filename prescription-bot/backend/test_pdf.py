from app.document_service import convert_pdf_to_images

pdf_path = "test_data/sample_prescription.pdf"
output_dir = "test_data/pdf_pages"

image_paths = convert_pdf_to_images(
    pdf_path,
    output_dir
)

print("Images created:")

for image_path in image_paths:
    print(image_path)