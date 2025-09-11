import streamlit as st
import sys
import os
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

class FinancialStatementRouter:
    """
    Unified router app that directs users to either Credit Card or Bank Statement extractors
    based on their selection. This keeps your existing scripts separate and modular.
    """
    
    def __init__(self):
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Financial Statement Extractor",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'statement_type' not in st.session_state:
            st.session_state.statement_type = None
        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = False
    
    def load_css(self):
        """Load custom CSS styles for dark theme"""
        return """
        <style>
        body, .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        .main-header {
            background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            color: #ffffff;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.85;
        }
        
        .statement-card {
            background: #1e1e2f;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.6);
            border: 2px solid transparent;
            transition: all 0.3s ease;
            margin: 1rem;
            cursor: pointer;
            text-align: center;
        }
        
        .statement-card:hover {
            border-color: #8b5cf6;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
        }
        
        .statement-card.selected {
            border-color: #8b5cf6;
            background: linear-gradient(135deg, #1a1a28 0%, #2a2a40 100%);
        }
        
        .card-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #8b5cf6;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #f5f5f5;
            margin-bottom: 1rem;
        }
        
        .card-description {
            color: #cfcfcf;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .feature-list {
            text-align: left;
            margin: 1rem 0;
        }
        
        .feature-item {
            background: #2a2a40;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 3px solid #8b5cf6;
            font-size: 0.9rem;
            color: #e0e0e0;
        }
        
        .proceed-button {
            background: linear-gradient(135deg, #667eea 0%, #8b5cf6 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        }
        
        .proceed-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6);
        }
        
        .info-section {
            background: #1e1e2f;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #8b5cf6;
            color: #e0e0e0;
        }
        
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: #1e1e2f;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.6);
            color: #f5f5f5;
        }
        
        .comparison-table th {
            background: linear-gradient(135deg, #667eea 0%, #8b5cf6 100%);
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: bold;
        }
        
        .comparison-table td {
            padding: 1rem;
            border-bottom: 1px solid #333;
        }
        
        .comparison-table tr:hover {
            background: #2a2a40;
        }
        
        .back-button {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(139, 92, 246, 0.1);
            border: 2px solid #8b5cf6;
            color: #8b5cf6;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .back-button:hover {
            background: #8b5cf6;
            color: white;
        }
        </style>
        """

        
    def render_welcome_screen(self):
        """Render the main welcome/selection screen"""
        st.markdown(self.load_css(), unsafe_allow_html=True)
        
        # Main Header
        st.markdown("""
        <div class="main-header">
            <h1>🏦 Financial Statement Extractor</h1>
            <p>Choose your document type to get started with AI-powered transaction extraction</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Selection Cards
        st.markdown("## 📋 Select Your Document Type")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="statement-card" onclick="selectCreditCard()">
                <div class="card-icon">💳</div>
                <div class="card-title">Credit Card Statement</div>
                <div class="card-description">
                    Extract transactions from credit card statements using advanced OCR and AI processing.
                </div>
                <div class="feature-list">
                    <div class="feature-item">📄 PDF password protection support</div>
                    <div class="feature-item">🔍 Smart data redaction for privacy</div>
                    <div class="feature-item">🤖 Groq + Gemini AI processing</div>
                    <div class="feature-item">📊 Transaction categorization</div>
                    <div class="feature-item">💾 CSV/JSON export options</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Process Credit Card Statement", key="cc_btn", use_container_width=True):
                st.session_state.statement_type = "credit_card"
                st.session_state.app_initialized = True
                st.rerun()
        
        with col2:
            st.markdown("""
            <div class="statement-card" onclick="selectBankStatement()">
                <div class="card-icon">🏦</div>
                <div class="card-title">Bank Statement</div>
                <div class="card-description">
                    Extract transactions from bank statements with smart schema detection and table processing.
                </div>
                <div class="feature-list">
                    <div class="feature-item">🔍 Automatic table detection</div>
                    <div class="feature-item">🧠 Smart schema detection</div>
                    <div class="feature-item">🎯 Llama + Gemini hybrid approach</div>
                    <div class="feature-item">📈 Transaction analysis & summaries</div>
                    <div class="feature-item">🔒 Privacy-focused processing</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Process Bank Statement", key="bank_btn", use_container_width=True):
                st.session_state.statement_type = "bank_statement"
                st.session_state.app_initialized = True
                st.rerun()
        
        # Comparison Section
        st.markdown("## 📊 Feature Comparison")
        
        comparison_data = """
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Feature</th>
                    <th>Credit Card Extractor</th>
                    <th>Bank Statement Extractor</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>AI Models</strong></td>
                    <td>Groq + Gemini </td>
                    <td>Llama + Gemini </td>
                </tr>
                <tr>
                    <td><strong>Processing Approach</strong></td>
                    <td>Image → Markdown → Extraction</td>
                    <td>PDF → Table Detection → Schema → Extraction</td>
                </tr>
                <tr>
                    <td><strong>Privacy Protection</strong></td>
                    <td>Automatic data redaction</td>
                    <td>Table-only processing</td>
                </tr>
                <tr>
                    <td><strong>Schema Detection</strong></td>
                    <td>Fixed transaction schema</td>
                    <td>Dynamic schema detection</td>
                </tr>
                <tr>
                    <td><strong>Export Formats</strong></td>
                    <td>CSV</td>
                    <td>CSV, JSON</td>
                </tr>
                <tr>
                    <td><strong>Best For</strong></td>
                    <td>Credit card statements, charge summaries</td>
                    <td>Bank statements, detailed transaction logs</td>
                </tr>
            </tbody>
        </table>
        """
        
        st.markdown(comparison_data, unsafe_allow_html=True)
        
        # Info Section
        st.markdown("""
        <div class="info-section">
            <h3>🛡️ Privacy & Security</h3>
            <p>Both extractors are designed with privacy in mind:</p>
            <ul>
                <li><strong>No Data Storage:</strong> Your documents are processed temporarily and immediately deleted</li>
                <li><strong>Local Processing:</strong> Most processing happens on your machine</li>
                <li><strong>Smart Redaction:</strong> Sensitive information is automatically masked before AI processing</li>
                <li><strong>Secure APIs:</strong> Only necessary data is sent to AI services via encrypted connections</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def run_credit_card_extractor(self):
        """Import and run the credit card extractor"""
        try:
            # Add back button
            if st.button("← Back to Main Menu", key="back_cc"):
                st.session_state.statement_type = None
                st.session_state.app_initialized = False
                st.rerun()
            
            st.markdown("---")
            
            # Import and run the credit card main function
            # Assuming your credit card extractor main.py has a main() function
            try:
                from main import main as credit_card_main
                st.markdown("## 💳 Credit Card Statement Extractor")
                st.info("🔄 Loading Credit Card Extractor...")
                credit_card_main()
            except ImportError as e:
                st.error(f"""
                ❌ **Credit Card Extractor Not Found**
                
                Please ensure you have the following files in your project directory:
                - `main.py` (from HarxSan/Transaction-Extractor)
                - All required dependencies and modules
                
                Error details: {str(e)}
                
                **Setup Instructions:**
                1. Copy `main.py` from your credit card extractor repository
                2. Copy all supporting modules (pdf_processor.py, image_converter.py, etc.)
                3. Install required dependencies: `pip install -r requirements.txt`
                """)
            except Exception as e:
                st.error(f"Error running credit card extractor: {str(e)}")
                
        except Exception as e:
            st.error(f"Failed to load credit card extractor: {str(e)}")
    
    def run_bank_statement_extractor(self):
        """Import and run the bank statement extractor"""
        try:
            # Add back button
            if st.button("← Back to Main Menu", key="back_bank"):
                st.session_state.statement_type = None
                st.session_state.app_initialized = False
                st.rerun()
            
            st.markdown("---")
            
            # Import and run the bank statement main function
            try:
                from vlm_extractor import main as bank_statement_main
                bank_statement_main()
            except ImportError as e:
                st.error(f"""
                ❌ **Bank Statement Extractor Not Found**
                
                Please ensure you have the following files in your project directory:
                - `vlm_extractor.py` (from Naresh-19/Bank-Statement-Extraction-Using-VLM)
                - All required dependencies and modules
                
                Error details: {str(e)}
                
                **Setup Instructions:**
                1. Copy `vlm_extractor.py` from your bank statement extractor repository
                2. Copy all supporting modules (camelot_cropper.py, ai_functions.py, utils.py, css.py, etc.)
                3. Install required dependencies: `pip install -r requirements.txt`
                """)
            except Exception as e:
                st.error(f"Error running bank statement extractor: {str(e)}")
                
        except Exception as e:
            st.error(f"Failed to load bank statement extractor: {str(e)}")
    
    def run(self):
        """Main application runner"""
        
        # Route to appropriate extractor if one is selected
        if st.session_state.app_initialized and st.session_state.statement_type:
            if st.session_state.statement_type == "credit_card":
                self.run_credit_card_extractor()
            elif st.session_state.statement_type == "bank_statement":
                self.run_bank_statement_extractor()
        else:
            # Show welcome screen for selection
            self.render_welcome_screen()


def main():
    """Main entry point"""
    app = FinancialStatementRouter()
    app.run()


if __name__ == "__main__":
    main()