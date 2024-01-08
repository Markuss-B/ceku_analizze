# Grocery Receipt Analysis Project

## Overview
This project analyzes rimi grocery receipts to track product prices. It uses Python and Tesseract OCR for scanning receipts. Data from Rimi e-store's sitemap is used to correct OCR results and standardize product names. Main features include:
- Price History for a Specific Product
    - Graph product price history
- Most Bought Products
- Most Expensive Products
- Most Expensive Receipt

## Repository Structure
- `receipts/`: Receipt images for OCR.
- `texts/`: OCR-scanned receipt texts.
- `receipts.txt`: Scanned receipts in dictionary format.
- `rimi_products.txt`: Product names from the Rimi sitemap.
- `receipts_spellchecked.txt`: Enhanced receipt data.

## Getting Started

### Prerequisites
- Python 3.12+
- Pip
- Tesseract OCR

### Setup and Installation
1. **Clone and Navigate:**
   ```shell
   git clone https://github.com/Hus47/ceku_analizze.git
   cd ceku_analizze
   ```

2. **Virtual Environment:**
   - **Windows**: `.\venv\Scripts\activate`

3. **Install Dependencies:**
   ```shell
   pip install -r requirements.txt
   ```

4. **Tesseract OCR (Windows):**
   - Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki).
   - Add to system PATH.

   Verify:
   ```shell
   tesseract --version
   ```

## Usage
Run the application and choose from the analysis options:
```shell
python main.py
```

## Technologies Used
- [Python](https://www.python.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Rich](https://github.com/willmcgugan/rich)
- [Matplotlib](https://matplotlib.org/)

## Contributors
- **Markuss Birznieks** ([Hus47](https://github.com/Hus47))
