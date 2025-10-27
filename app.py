from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='frontend')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")

# ============================================
# UTILITY FUNCTIONS
# ============================================

def parse_excel_file(file) -> pd.DataFrame:
    """Parse uploaded Excel file"""
    try:
        df = pd.read_excel(file)
        logger.info(f"Parsed Excel file: {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error parsing Excel: {str(e)}")
        raise

def get_data_context(df: pd.DataFrame) -> Dict[str, Any]:
    """Extract context from DataFrame"""
    return {
        "columns": df.columns.tolist(),
        "row_count": len(df),
        "sample_row": df.iloc[0].to_dict() if len(df) > 0 else {},
        "data_types": df.dtypes.astype(str).to_dict()
    }

# ============================================
# FORMULA GENERATION
# ============================================

@app.route('/api/generate-formula', methods=['POST'])
def generate_formula():
    """Generate Excel formula from natural language"""
    try:
        data = request.get_json()
        user_request = data.get('request')
        context = data.get('context', {})
        
        if not user_request:
            return jsonify({"error": "Request is required"}), 400
        
        system_prompt = """You are an Excel formula expert. Generate accurate Excel formulas.

Rules:
1. Use proper Excel syntax
2. Start formulas with =
3. Use cell references (A1, B2, etc.)
4. Provide clear explanations

Return JSON:
{
  "formula": "=IF(A2>10000, A2*0.05, A2*0.03)",
  "explanation": "Clear explanation",
  "example": "Usage example"
}"""
        
        user_prompt = f"""User Request: {user_request}

Data Context: {json.dumps(context)}

Generate the Excel formula."""
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        # Parse response content as JSON
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback if not JSON
            content = response.choices[0].message.content
            result = {
                "formula": content.split('\n')[0] if content else "=ERROR",
                "explanation": content,
                "example": "See explanation above"
            }
        
        # Ensure formula starts with =
        if 'formula' in result and not result['formula'].startswith('='):
            result['formula'] = '=' + result['formula']
        
        logger.info(f"Generated formula: {result.get('formula')}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error generating formula: {str(e)}")
        return jsonify({"error": str(e)}), 500
# ============================================
# DATA QUERY
# ============================================

@app.route('/api/query-data', methods=['POST'])
def query_data():
    """Answer natural language questions about Excel data"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        question = request.form.get('question')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        # Parse Excel file
        df = parse_excel_file(file)
        
        # Prepare data summary (convert timestamps to strings)
        sample_data = df.head(3).copy()
        for col in sample_data.columns:
            if sample_data[col].dtype == 'datetime64[ns]':
                sample_data[col] = sample_data[col].dt.strftime('%Y-%m-%d')
        
        data_summary = {
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "sample_data": sample_data.to_dict('records'),
            "numeric_columns": df.select_dtypes(include='number').columns.tolist()
        }
        
        system_prompt = """You are a data analyst. Answer questions about data.

Return JSON format:
{
  "answer": "Direct answer",
  "details": "Detailed explanation",
  "visualization": "chart_type or null"
}"""
        
        user_prompt = f"""Question: {question}

Data Summary:
- Columns: {', '.join(data_summary['columns'])}
- Row Count: {data_summary['row_count']}
- Sample: {json.dumps(data_summary['sample_data'][:2])}

Answer the question."""
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        # Parse response
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            content = response.choices[0].message.content
            result = {
                "answer": content,
                "details": "Analysis completed",
                "visualization": None
            }
        
        logger.info(f"Query answered: {question}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error querying data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============================================
# INSIGHTS GENERATION
# ============================================

@app.route('/api/generate-insights', methods=['POST'])
def generate_insights():
    """Generate automatic insights from Excel data"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        df = parse_excel_file(file)
        
        # Calculate statistics (convert timestamps to strings)
        sample_data = df.head(5).copy()
        for col in sample_data.columns:
            if sample_data[col].dtype == 'datetime64[ns]':
                sample_data[col] = sample_data[col].dt.strftime('%Y-%m-%d')
        
        stats = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_columns": df.select_dtypes(include='number').columns.tolist(),
            "sample_data": sample_data.to_dict('records')
        }
        
        system_prompt = """You are a business intelligence analyst. Analyze data and provide actionable insights.

IMPORTANT: Return ONLY valid JSON in this exact format:
{
  "insights": ["Key finding 1", "Key finding 2", "Key finding 3"],
  "trends": ["Trend 1", "Trend 2"],
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}

Focus on:
- Data patterns and distributions
- Notable statistics
- Business implications
- Actionable recommendations"""
        
        user_prompt = f"""Analyze this sales dataset:

Dataset Overview:
- Total Records: {stats['row_count']}
- Columns: {stats['column_count']}
- Numeric Columns: {', '.join(stats['numeric_columns'])}

Sample Data (first 3 rows):
{json.dumps(stats['sample_data'][:3], default=str, indent=2)}

Provide insights about sales performance, patterns, and business recommendations."""
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        # Parse response
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            content = response.choices[0].message.content
            lines = content.split('\n')
            result = {
                "insights": lines[:3] if len(lines) >= 3 else lines,
                "trends": [],
                "recommendations": []
            }
        
        logger.info("Generated insights")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============================================
# FORMULA EXPLANATION
# ============================================

@app.route('/api/explain-formula', methods=['POST'])
def explain_formula():
    """Explain an Excel formula in plain English"""
    try:
        data = request.get_json()
        formula = data.get('formula')
        
        if not formula:
            return jsonify({"error": "Formula is required"}), 400
        
        system_prompt = """You are an Excel teacher. Explain formulas clearly.

Return JSON format:
{
  "summary": "One-line summary",
  "explanation": "Detailed explanation",
  "example": "Usage example"
}"""
        
        user_prompt = f"""Explain this Excel formula: {formula}"""
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        # Parse response
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            content = response.choices[0].message.content
            result = {
                "summary": "Formula explanation",
                "explanation": content,
                "example": "See explanation above"
            }
        
        logger.info(f"Explained formula: {formula}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error explaining formula: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============================================
# SERVE FRONTEND
# ============================================

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/analyze-context', methods=['POST'])
def analyze_context():
    """Analyze uploaded file and suggest relevant questions"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        df = parse_excel_file(file)
        
        # Quick analysis
        context = {
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "numeric_columns": df.select_dtypes(include='number').columns.tolist(),
            "text_columns": df.select_dtypes(include='object').columns.tolist(),
            "has_dates": any('date' in col.lower() for col in df.columns)
        }
        
        system_prompt = """You are an Excel expert. Based on the data structure, suggest 5 relevant questions a financial analyst might ask.

Return JSON:
{
  "suggestions": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]
}"""
        
        user_prompt = f"""Data structure:
- Columns: {', '.join(context['columns'])}
- Numeric columns: {', '.join(context['numeric_columns'])}
- Text columns: {', '.join(context['text_columns'])}
- Has dates: {context['has_dates']}
- Row count: {context['row_count']}

Suggest 5 specific questions for this dataset."""
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            result = {"suggestions": [
                "What's the total revenue?",
                "Which category performs best?",
                "What are the trends over time?",
                "What's the average transaction value?",
                "Which region has highest sales?"
            ]}
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error analyzing context: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "azure_openai": "connected"}), 200

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)