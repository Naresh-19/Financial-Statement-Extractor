# 🏦 Financial Statement Extractor

VLM based transaction extraction from Credit Card Statements and Bank Statements using advanced OCR and Vision models.

## 🌟 Features

- **Dual Processing Modes**: Choose between Credit Card or Bank Statement extraction
- **Smart AI Processing**: Uses Groq + Gemini AI for accurate data extraction
- **Privacy Protected**: Automatic data redaction and secure processing
- **Multiple Export Formats**: Download results as CSV or JSON
- **Password Protection**: Supports encrypted PDF documents

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Open in Browser
Visit `http://localhost:8501` to access the application.

## 📄 Supported Document Types

### 💳 Credit Card Statements
- PDF credit card statements from major banks
- Password-protected documents
- Multi-page statements
- Transaction categorization and analysis

### 🏦 Bank Statements
- PDF bank statements (checking/savings)
- Smart table detection and processing
- Dynamic schema recognition
- Comprehensive transaction summaries

## 🛠️ How It Works

1. **Upload**: Choose your document type and upload a PDF file
2. **Process**: AI models analyze and extract transaction data
3. **Review**: View extracted transactions with summaries and metrics
4. **Download**: Export results as CSV or JSON files

## 📁 Project Structure

```
financial-statement-extractor/
├── app.py                      # Main unified application
├── main.py                     # Credit card extractor
├── vlm_extractor.py           # Bank statement extractor
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env                       # API keys (create this)
├── credit_card_modules/       # Credit card processing modules
│   ├── pdf_processor.py
│   ├── image_converter.py
│   ├── markdown_processor.py
│   ├── gemini_extractor.py
│   └── ui_components.py
└── bank_statement_modules/    # Bank statement processing modules
    ├── ai_functions.py
    ├── camelot_cropper.py
    ├── css.py
    ├── utils.py
    └── prompts.py
```

## 🔧 Requirements

### Python Version
- Python 3.8 or higher

### Key Dependencies
- `streamlit` - Web interface
- `groq` - Groq API client
- `google-generativeai` - Gemini AI
- `PyPDF2` - PDF processing
- `pandas` - Data manipulation
- `Pillow` - Image processing
- `camelot-py` - Table extraction

## 🔑 API Keys Required

1. **Groq API Key**: Get from [Groq Console](https://console.groq.com/)
2. **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/)

## 🎯 Usage Tips

### For Credit Card Statements:
- Ensure statements are clear and readable
- Works best with standard credit card statement formats
- Supports password-protected PDFs

### For Bank Statements:
- Upload complete statement pages
- Works with various bank statement formats
- Automatically detects transaction tables

## 📊 Output Formats

### CSV Export
- Standard comma-separated values
- Compatible with Excel and data analysis tools
- Includes all extracted transaction fields

### JSON Export
- Structured data format
- Ideal for programmatic processing
- Maintains data types and relationships

## 🔒 Privacy & Security

- **No Data Storage**: Files are processed temporarily and deleted
- **Local Processing**: Most operations happen on your machine
- **Secure APIs**: Privacy protected communication with AI services
- **Data Redaction**: Sensitive information automatically masked

