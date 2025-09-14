# bank_statement_modules/file_utils.py
import re
import os
import json
import shutil
import logging
import pandas as pd
from pathlib import Path
from bank_statement_modules.ai_core import clean_and_fix_json

TEMP_ROOT = "temp"

# --------------------------------------------------------
# File Handling Utilities
# --------------------------------------------------------

def cleanup_temp_dir(pdf_name: str):
    """
    Delete the entire temp folder for a given PDF.
    """
    try:
        base_stem = os.path.splitext(os.path.basename(pdf_name))[0]
        folder_path = os.path.join(TEMP_ROOT, base_stem)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            logging.info(f"🧹 Deleted temp folder: {folder_path}")
    except Exception as e:
        logging.warning(f"Cleanup failed: {e}")
        
def ensure_temp_dir(pdf_name: str) -> str:
    """
    Create a dedicated temp folder for each PDF.
    Example: temp/<pdf_stem>/
    Returns the folder path.
    """
    base_stem = os.path.splitext(os.path.basename(pdf_name))[0]
    folder_path = os.path.join(TEMP_ROOT, base_stem)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


# --------------------------------------------------------
# DataFrame Helpers
# --------------------------------------------------------
def expand_compact_json(compact_transactions):
    """Convert compact JSON format to full schema"""
    expanded_transactions = []
    
    for transaction in compact_transactions:
        expanded = {
            "date": transaction.get("dt"),
            "narration": transaction.get("desc"),
            "reference_number": transaction.get("ref"),
            "withdrawal_dr": float(transaction.get("dr", 0.0) or 0.0),
            "deposit_cr": float(transaction.get("cr", 0.0) or 0.0),
            "balance": float(transaction.get("bal", 0.0) or 0.0),
            "transaction_type": "Withdrawal"
            if str(transaction.get("type", "")).strip().upper() == "W"
            else "Deposit",
        }
        expanded_transactions.append(expanded)
    
    return expanded_transactions


def combine_json_texts_to_dataframe(json_texts, cropped_image_paths, source_pdf):
    all_records = []
    for idx, json_text in enumerate(json_texts):
        try:
            if not json_text or json_text.strip().startswith("Error extracting table:"):
                logging.warning(f"Skipping table {idx+1} due to error or empty response")
                continue

            clean_json = clean_and_fix_json(json_text)

            try:
                transactions = json.loads(clean_json)
            except json.JSONDecodeError as e:
                logging.warning(f"Table {idx+1}: JSON parse failed, attempting recovery: {e}")
                # Attempt to extract individual objects as fallback
                pattern = r'\{[^{}]*"dt"[^{}]*?\}'
                matches = re.finditer(pattern, clean_json, re.DOTALL)
                transactions = []
                for match in matches:
                    try:
                        obj_text = match.group(0)
                        obj_text = re.sub(r",\s*}", "}", obj_text)
                        obj_text = obj_text.replace('\\\\', '\\')
                        transaction = json.loads(obj_text)
                        transactions.append(transaction)
                    except Exception as inner_e:
                        logging.warning(f"Failed to parse individual transaction: {inner_e}")
                        continue

                if not transactions:
                    logging.error(f"Table {idx+1}: Could not parse JSON. Raw start: {clean_json[:200]}")
                    continue

            if not isinstance(transactions, list):
                logging.warning(f"Table {idx+1}: Expected array, got {type(transactions)}")
                continue

            # Expand compact schema → full schema
            expanded = expand_compact_json(transactions)

            # Attach metadata
            for r in expanded:
                r["_source_table"] = Path(cropped_image_paths[idx]).name if idx < len(cropped_image_paths) else ""
                r["_source_pdf"] = Path(source_pdf).name if source_pdf else ""

            all_records.extend(expanded)

        except Exception as e:
            logging.warning(f"Failed to process table {idx+1}: {e}")
            continue

    if not all_records:
        logging.info("No valid JSON records extracted.")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)

    # Drop metadata if not needed
    if "_source_table" in df.columns:
        df.drop(columns=["_source_table"], inplace=True)
    if "_source_pdf" in df.columns:
        df.drop(columns=["_source_pdf"], inplace=True)

    return df
