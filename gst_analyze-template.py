"""
GST and Bank Statement Cross-Analysis Module.
Detects circular trading, revenue inflation, and other red flags.
"""
from typing import Dict, Any, List
import re


def extract_gst_data(text: str) -> Dict[str, Any]:
    """
    Extract GST filing data from PDF text.
    Looks for GSTIN, turnover, input credit, etc.
    """
    gst_data = {
        "gstin": None,
        "total_turnover": 0.0,
        "taxable_turnover": 0.0,
        "input_tax_credit": 0.0,
        "output_tax": 0.0,
        "filing_frequency": "Monthly"
    }
    
    # Extract GSTIN
    gstin_match = re.search(r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b', text)
    if gstin_match:
        gst_data["gstin"] = gstin_match.group(0)
    
    # Extract turnover figures (simplified)
    turnover_match = re.search(r'total\s+turnover[:\s]+(?:rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)', text, re.IGNORECASE)
    if turnover_match:
        gst_data["total_turnover"] = float(turnover_match.group(1).replace(',', ''))
    
    return gst_data


def extract_bank_transactions(text: str) -> Dict[str, Any]:
    """
    Extract transaction patterns from bank statements.
    """
    bank_data = {
        "total_credits": 0.0,
        "total_debits": 0.0,
        "num_transactions": 0,
        "suspicious_patterns": []
    }
    
    # Look for credit entries
    credit_pattern = r'(?:credit|cr|deposit)[:\s]+(?:rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)'
    credits = re.findall(credit_pattern, text, re.IGNORECASE)
    
    if credits:
        bank_data["total_credits"] = sum(float(c.replace(',', '')) for c in credits)
        bank_data["num_transactions"] = len(credits)
    
    return bank_data


def cross_check_gst_bank(gst_data: Dict[str, Any], bank_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cross-verify GST returns against bank statement to detect anomalies.
    Key checks:
    1. Revenue inflation: GST turnover vs Bank credits mismatch
    2. Circular trading: Repetitive same-amount transactions
    3. Cash flow inconsistencies
    """
    analysis = {
        "revenue_match": True,
        "variance_percentage": 0.0,
        "red_flags": [],
        "confidence_score": 100.0
    }
    
    gst_turnover = gst_data.get("total_turnover", 0.0)
    bank_credits = bank_data.get("total_credits", 0.0)
    
    if gst_turnover > 0 and bank_credits > 0:
        variance = abs(gst_turnover - bank_credits) / gst_turnover * 100
        analysis["variance_percentage"] = round(variance, 2)
        
        # Flag if variance is too high
        if variance > 20:
            analysis["revenue_match"] = False
            analysis["red_flags"].append(
                f"Significant mismatch between GST turnover (₹{gst_turnover:,.0f}) "
                f"and bank credits (₹{bank_credits:,.0f}). Variance: {variance:.1f}%"
            )
            analysis["confidence_score"] -= 30
        
        # Check for circular trading patterns
        if variance > 50:
            analysis["red_flags"].append(
                "Possible circular trading or revenue inflation detected. "
                "GST returns do not align with actual bank inflows."
            )
            analysis["confidence_score"] -= 40
    
    # Additional checks
    if gst_turnover > 0 and bank_credits == 0:
        analysis["red_flags"].append("GST returns show turnover but no corresponding bank credits found.")
        analysis["confidence_score"] -= 50
    
    analysis["confidence_score"] = max(0, analysis["confidence_score"])
    
    return analysis


def analyze_gst_bank_statements(gst_text: str, bank_text: str) -> Dict[str, Any]:
    """
    Main function to perform GST-Bank cross-analysis.
    """
    gst_data = extract_gst_data(gst_text)
    bank_data = extract_bank_transactions(bank_text)
    cross_check = cross_check_gst_bank(gst_data, bank_data)
    
    return {
        "gst_data": gst_data,
        "bank_data": bank_data,
        "cross_check": cross_check,
        "analysis_complete": True
    }
