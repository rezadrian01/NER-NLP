# Google Colab Setup Guide for NLP Knowledge Graph Pipeline

## Method 1: Using the Python Script (Recommended)

### Step 1: Clone the repository
```bash
!git clone https://github.com/rezadrian01/NER-NLP.git
%cd NER-NLP
```

### Step 2: Run the Colab-optimized pipeline
```python
!python run_colab.py
```

## Method 2: Using Modified Bash Script

### Step 1: Clone the repository
```bash
!git clone https://github.com/rezadrian01/NER-NLP.git
%cd NER-NLP
```

### Step 2: Make script executable and run
```bash
!chmod +x run_all.sh
!./run_all.sh
```

## Method 3: Manual Step-by-Step (If above methods fail)

### Step 1: Clone and setup
```bash
!git clone https://github.com/rezadrian01/NER-NLP.git
%cd NER-NLP
```

### Step 2: Install dependencies
```bash
!pip install -r requirements.txt
!python -m spacy download xx_ent_wiki_sm
```

### Step 3: Run pipeline components
```bash
# Train the NER model
!python ner_trainer.py

# Evaluate and compare models
!python compare_ner_models.py

# Build knowledge graph
!python build_knowledge_graph.py
```

### Step 4: View results
```python
# List generated files
!ls -la output/

# Download HTML reports for viewing
from google.colab import files
files.download('output/ner_evaluation_comparison.html')
files.download('output/knowledge_graph.html')
```

## Troubleshooting Tips

1. **Virtual Environment Issues**: The modified script automatically detects Google Colab and skips virtual environment creation.

2. **Memory Issues**: If you encounter memory issues, restart the runtime and try again.

3. **Dependency Conflicts**: Use `!pip install --force-reinstall <package>` for specific packages if needed.

4. **File Access**: Use Google Colab's file browser (left sidebar) to navigate and download output files.

5. **GPU Usage**: The pipeline will automatically use GPU if available in your Colab session.

## Expected Output Files

After successful execution, you should find these files in the `output/` directory:
- `ner_evaluation_comparison.html` - Model comparison report
- `ner_evaluation_comparison.json` - Raw comparison data
- `knowledge_graph.html` - Interactive knowledge graph
- `knowledge_graph.json` - Graph data
- `entity_visualizations/` - Individual entity visualizations

## Viewing Results

Since Google Colab doesn't directly open HTML files, you have two options:
1. Download the files using `files.download()` and open locally
2. Use Colab's built-in HTML display for simple viewing:

```python
from IPython.display import HTML
with open('output/knowledge_graph.html', 'r', encoding='utf-8') as f:
    HTML(f.read())
```