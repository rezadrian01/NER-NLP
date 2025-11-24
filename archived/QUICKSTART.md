# Wayang NER - Quick Start Guide

## � Data Structure

The project uses two datasets located in the `data/` folder:

1. **wayang_stories_dataset.csv** - Main wayang stories collection (502 records)
2. **sitija_takon_bapa_dataset.csv** - Sitija Takon Bapa stories

Both datasets are automatically loaded and merged when you run the pipeline.

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run setup script
./setup.sh
```

The script will guide you through:
- Virtual environment creation
- Dependency installation
- spaCy model download
- Directory setup
- Test suite execution

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional but recommended)
python -m spacy download xx_ent_wiki_sm

# Create output directories
mkdir -p output templates data
```

---

## 📊 Running the System

### 1. Process the Full Dataset

```bash
python pipeline.py
```

**What it does:**
- Loads `wayang.csv` (501 Indonesian wayang stories)
- Preprocesses all texts
- Extracts entities (PERSON, LOC, ORG, EVENT)
- Extracts relations (child_of, married_to, fought_with, etc.)
- Builds knowledge graph
- Generates interactive visualization

**Output files** (in `output/` directory):
- `preprocessed_data.csv` - Cleaned texts
- `knowledge_graph.json` - Graph data
- `knowledge_graph.html` - Interactive visualization

**Expected runtime:** 2-10 minutes depending on NER method

---

### 2. Launch Web Interface

```bash
python app.py
```

Then open in browser: **http://localhost:5000**

**Features:**
- 📊 Dashboard with graph statistics
- 🔍 Search for entities
- 🎨 Interactive graph visualization
- 📖 Entity detail pages

---

### 3. Run Tests & Examples

```bash
python test_examples.py
```

**Tests include:**
- Text preprocessing
- Entity extraction
- Relation extraction
- Graph construction
- Visualization generation
- Mini pipeline demo

**Output:** Sample visualizations in `output/` directory

---

## 🎯 Common Use Cases

### Example 1: Basic Pipeline

```python
from pipeline import WayangPipeline

# Initialize
pipeline = WayangPipeline()

# Run full pipeline
pipeline.run_full_pipeline(max_vis_nodes=100)
```

### Example 2: Query Specific Entity

```python
from pipeline import WayangPipeline

pipeline = WayangPipeline()
pipeline.load_data()
pipeline.preprocess()
pipeline.extract_entities()
pipeline.extract_relations()
pipeline.build_knowledge_graph()

# Get entity information
info = pipeline.get_entity_info('Abimanyu')
print(f"Type: {info['type']}")
print(f"Connections: {info['degree']}")
print(f"Relations: {info['outgoing_relations']}")
```

### Example 3: Create Subgraph

```python
from pipeline import WayangPipeline

pipeline = WayangPipeline()
# ... run pipeline ...

# Create subgraph around specific entity
pipeline.create_subgraph_visualization('Arjuna', depth=2)
# Output: output/subgraph_arjuna.html
```

### Example 4: Custom NER Model

```bash
# Use transformer-based model (IndoBERT)
python pipeline.py --ner-model transformers

# Use only spaCy
python pipeline.py --ner-model spacy
```

---

## 📁 Expected Output

### After running pipeline.py:

```
output/
├── preprocessed_data.csv      # 501 rows with cleaned text
├── knowledge_graph.json       # ~200-300 nodes, ~300-500 edges
└── knowledge_graph.html       # Interactive visualization
```

### Sample Statistics:

```
Entities: 245
Relations: 387
Density: 0.0065
Top Entity Types:
  - PERSON: 189 (77%)
  - LOC: 32 (13%)
  - EVENT: 15 (6%)
  - ORG: 9 (4%)
```

---

## ⚡ Performance Tips

### Fast Processing (Rule-based only)
```bash
# Fastest - uses only pattern matching
python pipeline.py --max-nodes 50
# Runtime: ~1-2 minutes
```

### Balanced (spaCy + Rules)
```bash
# Good balance of speed and accuracy
python pipeline.py --ner-model spacy
# Runtime: ~3-5 minutes
```

### Maximum Accuracy (Transformers)
```bash
# Most accurate but slower
python pipeline.py --ner-model transformers
# Runtime: ~10-15 minutes
# Requires: GPU recommended, ~4GB RAM
```

---

## 🔍 Understanding the Output

### knowledge_graph.json Structure

```json
{
  "nodes": [
    {
      "id": "Abimanyu",
      "label": "Abimanyu",
      "type": "PERSON",
      "count": 15
    }
  ],
  "edges": [
    {
      "source": "Abimanyu",
      "target": "Arjuna",
      "relations": ["child_of"],
      "confidence": 0.9
    }
  ],
  "statistics": { ... }
}
```

### knowledge_graph.html

Interactive features:
- **Click & drag** nodes to reposition
- **Hover** over nodes/edges for details
- **Scroll** to zoom in/out
- **Navigation buttons** in bottom right
- **Color coding** by entity type

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: spaCy model not found

**Solution:**
```bash
python -m spacy download xx_ent_wiki_sm
```

### Issue: Dataset not found

**Solution:** Ensure `wayang.csv` is in the project root directory
```bash
ls wayang.csv  # Should show the file
```

### Issue: Out of memory

**Solution:** Reduce visualization nodes
```bash
python pipeline.py --max-nodes 30
```

### Issue: Port 5000 already in use

**Solution:** Change port in `config.py`
```python
FLASK_PORT = 5001  # Use different port
```

---

## 📚 Next Steps

1. ✅ Run the full pipeline
2. ✅ Explore the web interface
3. ✅ View the interactive visualization
4. 📖 Read the full [README.md](README.md)
5. 🔧 Customize relation patterns in `config.py`
6. 🎨 Adjust visualization colors in `visualization.py`
7. 📊 Analyze graph statistics
8. 🔍 Query specific entities

---

## 💡 Tips

- **First run:** Use rule-based NER for quick testing
- **Production:** Use spaCy or transformers for better accuracy
- **Large graphs:** Limit visualization nodes (--max-nodes)
- **Custom patterns:** Edit RELATION_PATTERNS in config.py
- **Entity colors:** Modify entity_colors in visualization.py

---

## 📞 Getting Help

1. Check [README.md](README.md) for detailed documentation
2. Run `python test_examples.py` to verify setup
3. Check module docstrings for API reference
4. View inline code comments for implementation details

---

**Happy exploring! 🎭**
