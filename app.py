import streamlit as st
import cv2
import numpy as np
import imghdr
import pytesseract
from PIL import Image, ImageChops
import json


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def load_image(file_bytes):
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    return img

def analyze_image(img):
    h, w = img.shape[:2]
    results = {
        "resolution": f"{w}x{h}",
        "low_resolution_flag": bool(w < 500 or h < 500)
    }
    edges = cv2.Canny(img, 100, 200)
    edge_density = float(np.sum(edges) / (w * h))
    results["edge_density"] = edge_density
    results["suspicious_edges_flag"] = bool(edge_density > 0.05)
    mean, stddev = cv2.meanStdDev(img)
    results["color_stddev"] = [float(x) for x in stddev.flatten()]
    results["color_inconsistency_flag"] = bool(any(s > 60 for s in stddev.flatten()))
    return results

def extract_text(img):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return pytesseract.image_to_string(pil_img)

def analyze_text(text):
    return {
        "text_length": int(len(text.strip())),
        "contains_id_number": bool(any(char.isdigit() for char in text)),
        "suspicious_text_flag": bool(len(text.strip()) < 20)
    }

def perform_ela(uploaded_file, quality=90):
    original = Image.open(uploaded_file).convert("RGB")
    temp_path = "temp_ela.jpg"
    original.save(temp_path, "JPEG", quality=quality)
    recompressed = Image.open(temp_path)
    diff = ImageChops.difference(original, recompressed)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1
    ela_image = diff.point(lambda x: x * scale)
    return ela_image

def generate_report(image_results, text_results, ela_flag=False):
    risk_score = sum([
        image_results["low_resolution_flag"],
        image_results["suspicious_edges_flag"],
        image_results["color_inconsistency_flag"],
        text_results["suspicious_text_flag"],
        ela_flag
    ])
    return {
        "Forgery Risk Report": {
            "Image Analysis": image_results,
            "Text Analysis": text_results,
            "ELA Flag": ela_flag,
            "Overall Risk": "Suspicious" if risk_score >= 2 else "Likely Genuine"
        }
    }


st.title("ID Document Fraud Detection Prototype")

uploaded_file = st.file_uploader("Upload an ID image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    img = load_image(file_bytes)

    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Uploaded ID", use_column_width=True)

    
    image_results = analyze_image(img)
    text_output = extract_text(img)
    text_results = analyze_text(text_output)

    
    st.subheader("Extracted Text")
    st.text(text_output)

    
    ela_result = perform_ela(uploaded_file)
    st.subheader("ELA Visualization")
    st.image(ela_result, caption="Error Level Analysis", use_column_width=True)

    ela_flag = True

    
    report = generate_report(image_results, text_results, ela_flag)

    st.subheader("Forgery Risk Report")
    st.json(report)

    
    st.download_button(
        label="Download Report as JSON",
        data=json.dumps(report, indent=4),
        file_name="fraud_report.json",
        mime="application/json"

    )
