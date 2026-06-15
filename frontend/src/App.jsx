import { useRef, useState } from "react";
import Webcam from "react-webcam";
import "./App.css";

function AnalysisView({ analysis, title }) {
  if (!analysis) return null;

  return (
    <div className="analysis-block">
      {title && <h3>{title}</h3>}

      {analysis.patient_information && (
        <div className="section-card">
          <h4>Patient Information</h4>
          <p><strong>Name:</strong> {analysis.patient_information.patient_name || "N/A"}</p>
          <p><strong>Age:</strong> {analysis.patient_information.age || "N/A"}</p>
          <p><strong>Gender:</strong> {analysis.patient_information.gender || "N/A"}</p>
          <p><strong>Date:</strong> {analysis.patient_information.date || "N/A"}</p>
        </div>
      )}

      {analysis.doctor_information && (
        <div className="section-card">
          <h4>Doctor Information</h4>
          <p><strong>Doctor:</strong> {analysis.doctor_information.doctor_name || "N/A"}</p>
          <p><strong>Clinic/Hospital:</strong> {analysis.doctor_information.clinic_or_hospital || "N/A"}</p>
          <p><strong>Registration No:</strong> {analysis.doctor_information.registration_number || "N/A"}</p>
        </div>
      )}

      {analysis.medicines?.length > 0 && (
        <div className="section-card">
          <h4>Medicines</h4>

          {analysis.medicines.map((medicine, index) => (
            <div className="medicine-card" key={index}>
              <h5>{medicine.medicine_name || "Unknown Medicine"}</h5>
              <p><strong>Strength:</strong> {medicine.strength || "N/A"}</p>
              <p><strong>Form:</strong> {medicine.form || "N/A"}</p>
              <p><strong>Dosage:</strong> {medicine.dosage || "N/A"}</p>
              <p><strong>Frequency:</strong> {medicine.frequency || "N/A"}</p>
              <p><strong>Timing:</strong> {medicine.timing || "N/A"}</p>
              <p><strong>Duration:</strong> {medicine.duration || "N/A"}</p>
              <p><strong>Route:</strong> {medicine.route || "N/A"}</p>
              <p><strong>Confidence:</strong> {medicine.confidence || "N/A"}</p>
              <p><strong>Explanation:</strong> {medicine.simple_explanation || "N/A"}</p>
            </div>
          ))}
        </div>
      )}

      {analysis.tests_or_investigations?.length > 0 && (
        <div className="section-card">
          <h4>Tests / Investigations</h4>
          <ul>
            {analysis.tests_or_investigations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {analysis.doctor_advice?.length > 0 && (
        <div className="section-card">
          <h4>Doctor Advice</h4>
          <ul>
            {analysis.doctor_advice.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {analysis.unclear_or_risky_items?.length > 0 && (
        <div className="section-card warning-card">
          <h4>Warnings / Unclear Items</h4>
          <ul>
            {analysis.unclear_or_risky_items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {analysis.overall_simple_explanation && (
        <div className="section-card">
          <h4>Overall Explanation</h4>
          <p>{analysis.overall_simple_explanation}</p>
        </div>
      )}

      {analysis.safety_note && (
        <div className="section-card safety-card">
          <h4>Safety Note</h4>
          <p>{analysis.safety_note}</p>
        </div>
      )}
    </div>
  );
}

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);

  const webcamRef = useRef(null);

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze-prescription", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        error: "Failed to analyze prescription",
      });
    } finally {
      setLoading(false);
    }
  };

  const capturePhoto = async () => {
    if (!webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();

    if (!imageSrc) return;

    setCapturedImage(imageSrc);

    const response = await fetch(imageSrc);
    const blob = await response.blob();

    const file = new File([blob], "camera_capture.jpg", {
      type: "image/jpeg",
    });

    setSelectedFile(file);
    setResult(null);
    setShowCamera(false);
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setCapturedImage(null);
    setResult(null);
    setShowCamera(false);
  };

  return (
    <div className="app-container">
      <h1>PrescriptionBot</h1>
      <p>AI Powered Prescription Analyzer</p>

      <div className="upload-card">
        <h2>Upload Prescription</h2>

        <input
          type="file"
          accept=".jpg,.jpeg,.png,.pdf,.docx"
          onChange={(e) => {
            setSelectedFile(e.target.files[0]);
            setCapturedImage(null);
            setResult(null);
          }}
        />

        <div className="camera-actions">
          <button type="button" onClick={() => setShowCamera(!showCamera)}>
            {showCamera ? "Close Camera" : "Open Camera"}
          </button>

          {selectedFile && (
            <button type="button" className="secondary-button" onClick={clearSelection}>
              Clear
            </button>
          )}
        </div>

        {showCamera && (
          <div className="camera-box">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam"
            />

            <button type="button" onClick={capturePhoto}>
              Capture Photo
            </button>
          </div>
        )}

        {capturedImage && (
          <div className="preview-box">
            <h4>Captured Preview</h4>
            <img src={capturedImage} alt="Captured prescription" />
          </div>
        )}

        {selectedFile && (
          <p className="file-name">Selected file: {selectedFile.name}</p>
        )}

        <button disabled={!selectedFile || loading} onClick={handleAnalyze}>
          {loading ? "Analyzing..." : "Analyze Prescription"}
        </button>

        {result?.error && (
          <div className="section-card error-card">
            <h4>Error</h4>
            <p>{result.error}</p>
          </div>
        )}

        {result && !result.error && (
          <div className="result-container">
            <h3>Analysis Result</h3>

            <div className="section-card">
              <p><strong>File:</strong> {result.filename || "N/A"}</p>
              <p><strong>File Type:</strong> {result.file_type || "N/A"}</p>
            </div>

            {result.file_type === "pdf" && (
              <div className="section-card">
                <h4>PDF Summary</h4>
                <p><strong>Total Pages:</strong> {result.total_pages_in_pdf}</p>
                <p><strong>Pages Analyzed:</strong> {result.pages_analyzed}</p>
                <p><strong>Status:</strong> {result.message}</p>
              </div>
            )}

            {result.file_type === "docx" && (
              <div className="section-card">
                <h4>DOCX Summary</h4>
                <p><strong>Text Found:</strong> {result.text_found ? "Yes" : "No"}</p>
                <p><strong>Embedded Images:</strong> {result.embedded_images_found}</p>
              </div>
            )}

            {result.file_type === "image" && (
              <AnalysisView analysis={result.analysis} />
            )}

            {result.file_type === "pdf" &&
              result.analyses?.map((page, index) => (
                <AnalysisView
                  key={index}
                  title={`Page ${page.page_number}`}
                  analysis={page.analysis}
                />
              ))}

            {result.file_type === "docx" && result.text_analysis && (
              <AnalysisView
                title="Typed DOCX Text Analysis"
                analysis={result.text_analysis}
              />
            )}

            {result.file_type === "docx" &&
              result.image_analyses?.map((image, index) => (
                <AnalysisView
                  key={index}
                  title={`Embedded Image ${image.image_number}`}
                  analysis={image.analysis}
                />
              ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;