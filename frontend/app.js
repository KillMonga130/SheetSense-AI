// Global variables
let currentFile = null;

// Tab functionality
function showTab(tabName, buttonElement) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    if (buttonElement) {
        buttonElement.classList.add('active');
    }
}

// Utility functions
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    document.getElementById('error-text').textContent = message;
    document.getElementById('error-message').style.display = 'flex';
    setTimeout(hideError, 5000); // Auto hide after 5 seconds
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

// File upload handling
function handleFileUpload(type) {
    const fileInput = document.getElementById(`${type}-file`);
    const file = fileInput.files[0];
    
    if (file) {
        currentFile = file;
        console.log(`File uploaded for ${type}:`, file.name);
        
        // Update the label to show file name
        const label = document.querySelector(`label[for="${type}-file"]`);
        if (label) {
            label.textContent = `✅ ${file.name}`;
            label.style.background = '#4CAF50';
            label.style.color = 'white';
        }
        
        // Show smart suggestions button for query tab
        if (type === 'query') {
            document.getElementById('smart-suggestions-btn').style.display = 'block';
        }
    }
}

// Smart suggestions
async function getSmartSuggestions() {
    const fileInput = document.getElementById('query-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please upload a file first');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/analyze-context', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display smart suggestions
        const container = document.getElementById('smart-suggestion-chips');
        container.innerHTML = '';
        
        data.suggestions.forEach(suggestion => {
            const chip = document.createElement('button');
            chip.className = 'suggestion-chip';
            chip.textContent = suggestion;
            chip.onclick = () => fillDataQuestion(suggestion);
            container.appendChild(chip);
        });
        
        document.getElementById('smart-suggestions').style.display = 'block';
        
    } catch (error) {
        showError('Error getting suggestions: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Formula Generator
async function generateFormula() {
    const request = document.getElementById('formula-request').value.trim();
    
    if (!request) {
        showError('Please enter a formula request');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/generate-formula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                request: request,
                context: {}
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display results
        document.getElementById('formula-code').textContent = data.formula || 'No formula generated';
        document.getElementById('formula-explanation').textContent = data.explanation || 'No explanation available';
        document.getElementById('formula-example').textContent = data.example || 'No example available';
        document.getElementById('formula-result').style.display = 'block';
        
    } catch (error) {
        showError('Error generating formula: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Copy formula to clipboard
function copyFormula() {
    const formula = document.getElementById('formula-code').textContent;
    navigator.clipboard.writeText(formula).then(() => {
        const btn = document.querySelector('.copy-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    });
}

// Data Query
async function queryData() {
    const question = document.getElementById('data-question').value.trim();
    
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    // Get the file from the query tab specifically
    const fileInput = document.getElementById('query-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please upload an Excel file first');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('question', question);
        
        const response = await fetch('/api/query-data', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display results
        document.getElementById('query-answer').textContent = data.answer || 'No answer available';
        document.getElementById('query-details').textContent = data.details || 'No details available';
        document.getElementById('query-result').style.display = 'block';
        
    } catch (error) {
        showError('Error querying data: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Generate Insights
async function generateInsights() {
    // Get the file from the insights tab specifically
    const fileInput = document.getElementById('insights-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please upload an Excel file first');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/generate-insights', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display insights
        displayList('insights-list', data.insights || []);
        displayList('trends-list', data.trends || []);
        displayList('recommendations-list', data.recommendations || []);
        
        document.getElementById('insights-result').style.display = 'block';
        
    } catch (error) {
        showError('Error generating insights: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Helper function to display lists
function displayList(elementId, items) {
    const list = document.getElementById(elementId);
    list.innerHTML = '';
    
    if (items.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No items found';
        li.style.fontStyle = 'italic';
        li.style.color = '#666';
        list.appendChild(li);
        return;
    }
    
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        list.appendChild(li);
    });
}

// Formula Explainer
async function explainFormula() {
    const formula = document.getElementById('formula-input').value.trim();
    
    if (!formula) {
        showError('Please enter a formula to explain');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/explain-formula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                formula: formula
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display results
        document.getElementById('explain-summary').textContent = data.summary || 'No summary available';
        document.getElementById('explain-details').textContent = data.explanation || 'No explanation available';
        document.getElementById('explain-example').textContent = data.example || 'No example available';
        document.getElementById('explain-result').style.display = 'block';
        
    } catch (error) {
        showError('Error explaining formula: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Drag and drop functionality
function setupDragAndDrop() {
    const fileLabels = document.querySelectorAll('.file-label');
    
    fileLabels.forEach(label => {
        const fileInput = document.getElementById(label.getAttribute('for'));
        
        label.addEventListener('dragover', (e) => {
            e.preventDefault();
            label.style.background = '#667eea';
            label.style.color = 'white';
        });
        
        label.addEventListener('dragleave', (e) => {
            e.preventDefault();
            if (!fileInput.files[0]) {
                label.style.background = '#f8f9fa';
                label.style.color = '#667eea';
            }
        });
        
        label.addEventListener('drop', (e) => {
            e.preventDefault();
            const files = e.dataTransfer.files;
            
            if (files.length > 0 && files[0].name.match(/\.(xlsx|xls)$/i)) {
                fileInput.files = files;
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            } else {
                showError('Please drop an Excel file (.xlsx or .xls)');
            }
        });
    });
}

// Suggestion functions
function fillSuggestion(text) {
    document.getElementById('formula-request').value = text;
    document.getElementById('formula-request').focus();
}

function fillDataQuestion(text) {
    document.getElementById('data-question').value = text;
    document.getElementById('data-question').focus();
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('SheetSense AI initialized');
    
    // Setup drag and drop
    setupDragAndDrop();
    
    // Test API connection
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('API Health Check:', data);
        })
        .catch(error => {
            console.error('API connection failed:', error);
            showError('Failed to connect to API. Please check your setup.');
        });
});