# Wayang NER and Knowledge Graph Builder

**Author:** Ahmad Reza Adrian  
**Domain:** Natural Language Processing (NLP)  
**Language:** Python 3.10+

An NLP system that performs Named Entity Recognition (NER) and builds a Knowledge Graph from Indonesian wayang stories. The system extracts entities (PERSON, LOCATION, ORGANIZATION, EVENT, OBJECT) and their semantic relationships, then visualizes them as an interactive graph.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Module Documentation](#module-documentation)
- [Output Examples](#output-examples)
- [API Reference](#api-reference)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Named Entity Recognition (NER)**
  - Multi-method approach: Rule-based + spaCy + Transformers (IndoBERT)
  - Specialized patterns for Indonesian wayang texts
  - Entity types: PERSON, LOC, ORG, EVENT, OBJECT

- **Relation Extraction**
  - Rule-based pattern matching for Indonesian language
  - Relation types: child_of, married_to, fought_with, killed_by, sibling_of, ruled_in, died_in, etc.
  - Confidence scoring

- **Knowledge Graph**
  - Built with NetworkX
  - Graph analytics and statistics
  - Entity information retrieval
  - Path finding between entities
  - Subgraph extraction

- **Interactive Visualization**
  - Web-based visualization with PyVis
  - Color-coded entity types and relations
  - Interactive node exploration
  - Responsive design

- **Web Interface**
  - Flask-based dashboard
  - Search functionality
  - Entity detail pages
  - Graph statistics

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     WAYANG NER PIPELINE                       │
└──────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   CSV Data  │───▶│ Preprocessing│───▶│   NER Extract   │
│ wayang.csv  │    │   (Clean &   │    │  (spaCy/BERT +  │
└─────────────┘    │  Normalize)  │    │   Rule-based)   │
                   └──────────────┘    └─────────────────┘
                                              │
                                              ▼
                   ┌──────────────┐    ┌─────────────────┐
                   │ Visualization│◀───│    Knowledge    │
                   │   (PyVis)    │    │  Graph Builder  │
                   └──────────────┘    │   (NetworkX)    │
                          │            └─────────────────┘
                          ▼                   ▲
                   ┌──────────────┐           │
                   │  Web UI      │    ┌──────────────────┐
                   │  (Flask)     │    │Relation Extractor│
                   └──────────────┘    │  (Rule-based)    │
                                       └──────────────────┘

MODULE STRUCTURE:
├── config.py              # Configuration and settings
├── preprocessing.py       # Text cleaning and normalization
├── ner_extraction.py      # Named entity recognition
├── relation_extraction.py # Relation pattern matching
├── graph_builder.py       # Knowledge graph construction
├── visualization.py       # Interactive graph visualization
├── pipeline.py            # End-to-end orchestration
└── app.py                 # Flask web application
```

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Step 1: Clone or download the project

```bash
cd "/home/asus/Lectures/5. Semester 5/NLP/Tugas Akhir NLP"
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy model (optional but recommended)

```bash
python -m spacy download xx_ent_wiki_sm
```

For better Indonesian support, you can use multilingual models or IndoBERT through transformers.

---

## 🚀 Quick Start

### Run Complete Pipeline

```bash
python pipeline.py
```

This will:
1. Load `wayang.csv` dataset
2. Preprocess all texts
3. Extract entities using NER
4. Extract relations between entities
5. Build knowledge graph
6. Generate interactive visualization

Output files will be saved to `output/` directory:
- `preprocessed_data.csv` - Cleaned and processed texts
- `knowledge_graph.json` - Graph data in JSON format
- `knowledge_graph.html` - Interactive visualization

### Launch Web Interface

```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

---

## 📖 Usage

### Command-Line Options

```bash
# Use custom dataset
python pipeline.py --dataset /path/to/your/wayang.csv

# Specify output directory
python pipeline.py --output /path/to/output

# Use transformer-based NER
python pipeline.py --ner-model transformers

# Limit visualization nodes
python pipeline.py --max-nodes 50
```

### Programmatic Usage

```python
from pipeline import WayangPipeline

# Initialize pipeline
pipeline = WayangPipeline(
    dataset_path='wayang.csv',
    output_dir='output',
    ner_model_type='spacy'
)

# Run full pipeline
pipeline.run_full_pipeline(max_vis_nodes=100)

# Or run step by step
pipeline.load_data()
pipeline.preprocess()
pipeline.extract_entities()
pipeline.extract_relations()
pipeline.build_knowledge_graph()
pipeline.visualize_graph()

# Query specific entity
info = pipeline.get_entity_info('Abimanyu')
print(info)

# Create subgraph visualization
pipeline.create_subgraph_visualization('Arjuna', depth=2)
```

---

## 📚 Module Documentation

### `preprocessing.py`

**TextPreprocessor** - Cleans and normalizes Indonesian text

```python
preprocessor = TextPreprocessor()
result = preprocessor.preprocess(text)
# Returns: {'cleaned', 'normalized', 'sentences', 'sentence_count'}
```

### `ner_extraction.py`

**WayangNER** - Extracts named entities

```python
ner = WayangNER(model_type='spacy')
entities = ner.extract_entities(text)
# Returns: List of {'text', 'type', 'start', 'end', 'method'}
```

Supported entity types:
- `PERSON` - Characters (Abimanyu, Arjuna, etc.)
- `LOC` - Locations (Kerajaan Dwarawati, etc.)
- `ORG` - Organizations (Pandawa, Kurawa)
- `EVENT` - Events (Perang Bharatayudha)
- `OBJECT` - Objects

### `relation_extraction.py`

**RelationExtractor** - Extracts semantic relations

```python
extractor = RelationExtractor()
relations = extractor.extract_relations_from_entities(text, entities)
# Returns: List of {'subject', 'relation', 'object', 'confidence', 'context'}
```

Supported relation types:
- `child_of` / `parent_of`
- `married_to`
- `sibling_of`
- `fought_with`
- `killed_by`
- `ruled_in`
- `died_in`
- `associated_with`

### `graph_builder.py`

**KnowledgeGraph** - Constructs and manages the graph

```python
kg = KnowledgeGraph()
kg.add_entity('Abimanyu', 'PERSON')
kg.add_relation('Abimanyu', 'child_of', 'Arjuna')

# Get statistics
stats = kg.get_statistics()

# Query entity
info = kg.get_entity_info('Abimanyu')

# Export to JSON
kg.to_json('graph.json')
```

### `visualization.py`

**GraphVisualizer** - Creates interactive visualizations

```python
visualizer = GraphVisualizer()
visualizer.visualize_from_knowledge_graph(kg, 'output.html')
```

---

## 📊 Output Examples

### Sample Entity Extraction

**Input Text:**
```
Abimanyu adalah putra Arjuna dan Subadra. 
Ia gugur dalam perang Bharatayudha.
```

**Output Entities:**
```json
[
  {"text": "Abimanyu", "type": "PERSON", "method": "rule-based"},
  {"text": "Arjuna", "type": "PERSON", "method": "rule-based"},
  {"text": "Subadra", "type": "PERSON", "method": "rule-based"},
  {"text": "perang Bharatayudha", "type": "EVENT", "method": "rule-based"}
]
```

### Sample Relation Extraction

**Output Relations:**
```json
[
  {
    "subject": "Abimanyu",
    "relation": "child_of",
    "object": "Arjuna",
    "confidence": 0.8
  },
  {
    "subject": "Abimanyu",
    "relation": "child_of",
    "object": "Subadra",
    "confidence": 0.8
  },
  {
    "subject": "Abimanyu",
    "relation": "died_in",
    "object": "Bharatayudha",
    "confidence": 0.85
  }
]
```

### Sample Graph Statistics

```json
{
  "total_nodes": 245,
  "total_edges": 387,
  "density": 0.0065,
  "entity_type_distribution": {
    "PERSON": 189,
    "LOC": 32,
    "EVENT": 15,
    "ORG": 9
  },
  "relation_type_distribution": {
    "child_of": 87,
    "married_to": 45,
    "ruled_in": 34,
    "fought_with": 28
  }
}
```

---

## 🔌 API Reference

### Flask Web API Endpoints

#### `GET /`
Home page with dashboard

#### `GET /api/graph`
Get complete graph data (JSON)

#### `GET /api/statistics`
Get graph statistics

#### `GET /api/entity/<entity_name>`
Get detailed entity information

#### `GET /api/search?q=<query>`
Search for entities

#### `GET /visualization`
View interactive graph visualization

#### `GET /entity/<entity_name>`
Entity detail page

---

## ⚡ Performance

### Expected Performance

- **NER Extraction:** ~10-50 docs/second (depending on method)
- **Relation Extraction:** ~20-100 docs/second
- **Graph Construction:** <1 second for 500 documents
- **Visualization Generation:** 1-5 seconds

### Optimization Tips

1. Use rule-based NER only for faster processing
2. Limit visualization nodes for large graphs
3. Process dataset in batches for memory efficiency
4. Cache processed results

---

## 🔧 Troubleshooting

### Issue: spaCy model not found

**Solution:**
```bash
python -m spacy download xx_ent_wiki_sm
```

### Issue: Out of memory with transformers

**Solution:** Use spaCy or rule-based NER:
```bash
python pipeline.py --ner-model spacy
```

### Issue: Visualization not loading

**Solution:** Check if output directory exists and has proper permissions:
```bash
mkdir -p output
chmod 755 output
```

### Issue: No entities detected

**Solution:** Check text encoding in CSV. Ensure UTF-8:
```python
df = pd.read_csv('wayang.csv', encoding='utf-8')
```

---

## 📝 Testing

Run individual module tests:

```bash
# Test preprocessing
python preprocessing.py

# Test NER
python ner_extraction.py

# Test relation extraction
python relation_extraction.py

# Test graph builder
python graph_builder.py

# Test visualization
python visualization.py
```

---

## 🎯 Project Structure

```
.
├── wayang.csv               # Dataset (Indonesian wayang stories)
├── requirements.txt         # Python dependencies
├── config.py                # Configuration file
├── preprocessing.py         # Text preprocessing module
├── ner_extraction.py        # NER module
├── relation_extraction.py   # Relation extraction module
├── graph_builder.py         # Knowledge graph builder
├── visualization.py         # Graph visualization
├── pipeline.py              # Main pipeline orchestration
├── app.py                   # Flask web application
├── README.md                # This file
├── output/                  # Output directory
│   ├── preprocessed_data.csv
│   ├── knowledge_graph.json
│   └── knowledge_graph.html
└── templates/               # Flask HTML templates
    ├── index.html
    └── entity.html
```

---

## 🎓 Academic Context

This project is part of a Natural Language Processing course assignment focused on:
- Information extraction from unstructured Indonesian text
- Knowledge representation and graph construction
- Practical application of NER and relation extraction
- Visualization of semantic relationships

---

## 📄 License

This is an academic project for educational purposes.

---

## 👤 Author

**Ahmad Reza Adrian**  
Natural Language Processing  
Semester 5

---

## 🙏 Acknowledgments

- Dataset: Indonesian wayang story collection
- Libraries: spaCy, transformers, NetworkX, PyVis, Flask
- Indonesian NLP community

---

**For questions or issues, please refer to the module documentation or test the individual components.**
