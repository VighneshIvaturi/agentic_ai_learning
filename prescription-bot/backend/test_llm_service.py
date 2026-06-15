from app.llm_service import analyze_prescription_image

result = analyze_prescription_image(
    "test_data/sample_prescription.png"
)

print(result)