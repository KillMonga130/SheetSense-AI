# 🧠 SheetSense AI - Excel Assistant

An intelligent Excel assistant powered by Azure OpenAI that transforms spreadsheet complexity into simple natural language interactions.

## 🚀 Features

- **Formula Generator**: Describe what you want in plain English, get working Excel formulas
- **Data Query Engine**: Ask questions about your Excel data in natural language
- **Auto Insights**: Get automatic analysis and insights from your spreadsheets
- **Formula Explainer**: Understand complex formulas with plain English explanations

## 🏗️ Architecture

Built with:
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Azure OpenAI Service (GPT-3.5-Turbo/GPT-4)
- **Data Processing**: pandas, openpyxl

## 📋 Prerequisites

1. **Python 3.8+**
2. **Azure OpenAI Service** with deployed model
3. **API Key and Endpoint** from Azure

## 🛠️ Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

1. Update `.env` file with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📊 Usage Examples

### Formula Generator
**Input**: "Calculate 15% commission on sales over 5000, otherwise 10%"
**Output**: `=IF(A2>5000, A2*0.15, A2*0.1)`

### Data Query
**Input**: "What's the total revenue by region?"
**Output**: Analyzes your Excel data and provides the answer

### Auto Insights
**Input**: Upload Excel file
**Output**: Automatic insights like trends, patterns, and recommendations

### Formula Explainer
**Input**: `=VLOOKUP(A2,Sheet2!A:C,3,FALSE)`
**Output**: Plain English explanation of what the formula does

## 🧪 Testing

Use the included `sample_sales_data.xlsx` file to test all features:

```bash
python sample_data.py  # Generates test data
```

## 🔧 API Endpoints

- `POST /api/generate-formula` - Generate Excel formulas
- `POST /api/query-data` - Query Excel data
- `POST /api/generate-insights` - Generate data insights
- `POST /api/explain-formula` - Explain formulas
- `GET /api/health` - Health check

## 🎯 Project Goals

This project was built for the Azure Codeathon 2025, focusing on:
- **Innovation**: Novel AI-powered Excel assistance
- **Technical Excellence**: Robust Azure OpenAI integration
- **Real Impact**: Solving actual Excel user pain points

## 🚀 Future Enhancements

- Chart generation from natural language
- Multi-sheet analysis
- Advanced statistical functions
- Real-time collaboration features
- Mobile app version

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

---

**Built with ❤️ using Azure OpenAI Services**