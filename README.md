# ID Card Fraud Detection

This project is a simple prototype for detecting possible tampering in ID card images using image processing techniques.

The system analyzes uploaded ID images and generates a fraud detection report using Error Level Analysis (ELA), image processing and OCR.

---

## Features

- Upload ID card image
- Detect possible image tampering using Error Level Analysis (ELA)
- Extract text using OCR
- Generate fraud detection report
- Simple web interface using Streamlit

---

## Technologies Used

- Python
- OpenCV
- Streamlit
- Tesseract OCR
- PIL (Python Imaging Library)

---

## Project Structure

id-fraud-detection
│
├── app.py
├── requirements.txt
├── fraud_report.json
└── README.md

---

## Installation

Clone the repository:

git clone https://github.com/aiswaryasrikesh/id-fraud-detection.git

Install dependencies:

pip install -r requirements.txt

---

## Run the Application

streamlit run app.py

Then open in browser:

http://localhost:8501

---

## Output

The application analyzes the uploaded ID card image and generates a fraud detection report based on possible image tampering.

---

## Author

Aiswarya s pai 

