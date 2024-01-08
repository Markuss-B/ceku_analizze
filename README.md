# Grocery Receipt Analysis Project

This project analyzes grocery receipts to track product prices and shopping habits. It uses Python for OCR (Optical Character Recognition), data parsing, and analysis.
Project uses rimi estore sitemap data for fixing ocr data (standardizes product names).
Scanning receipts and fixing names takes a while.

The folder 'receipts' holds the receipt images to be scanned by ocr
The folder 'texts' holds the OCR scanned receipt texts in individidual files
The file 'receipts.txt' holds the receipts as a dictionary
The file 'rimi_products.txt' hold the product names extracted from the sitemap.
The file 'receipts_spellchecked.txt' hold that same dictionary spellechecked with the rimi sitemap data and with the help of fuzzywuzzy.



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.12 or higher
- Pip (Python package manager)
- Tesseract OCR

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. **Clone the Repository**
   
   ```
   git clone https://github.com/your-username/grocery-receipt-analysis.git
   cd grocery-receipt-analysis
   ```

2. **Set Up a Virtual Environment**

   - Create a virtual environment:
     
     ```bash
     python -m venv venv
     ```
   
   - Activate the virtual environment:
     
     - **Windows**:
       
       ```
       .\venv\Scripts\activate
       ```

3. **Install Python Dependencies**

   ```
   pip install -r requirements.txt
   ```

### Installing Tesseract OCR

Tesseract OCR is used for image processing and text extraction.

- **Windows**:
  
  Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki). During installation, make sure to add Tesseract to the system PATH.


After installation, verify the installation by running:

```
tesseract --version
```

## Running the Application

```
python main.py
```

## Built With

* [Python](https://www.python.org/) - The programming language used
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
* [Rich](https://github.com/willmcgugan/rich) - Used for beautiful CLI interfaces


## Authors

* **Markuss Birznieks** - *Initial work* - [Hus47](https://github.com/Hus47)