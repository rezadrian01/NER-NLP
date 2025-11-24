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

- **Multi-Method NER**: Combines rule-based, spaCy, and transformer models
- **Custom NER Training**: Train domain-specific models on your data
- **Model Evaluation**: Comprehensive metrics (Precision, Recall, F1, Exact/Partial Match)
- **Model Comparison**: Side-by-side evaluation of multiple NER models
- **Dynamic Relation Labeling**: Automatic relation type inference
- **Multi-Dataset Support**: Process multiple CSV datasets simultaneously
- **Knowledge Graph Construction**: Build entity-relationship graphs
- **Interactive Visualizations**: PyVis-powered network visualizations
- **Web Interface**: Flask app for entity exploration
- **Comprehensive Metrics**: Detailed pipeline performance tracking
- **Indonesian Language**: Optimized for Indonesian text processing

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

### Datasets

The project uses two wayang story datasets:
- `data/wayang_stories_dataset.csv` - Main wayang stories collection
- `data/sitija_takon_bapa_dataset.csv` - Sitija Takon Bapa stories

Both datasets are automatically loaded and merged during processing.

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

This will:
1. Load and merge both datasets from `data/` folder
2. Preprocess all texts
3. Extract entities using NER
4. Extract relations between entities
5. Build knowledge graph
6. Generate interactive visualization

Output files will be saved to `output/` directory:
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
- `pipeline_metrics.json` - Complete metrics report in JSON
- `pipeline_metrics.html` - Visual metrics dashboard

### Launch Web Interface

```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

---

## 📖 Usage

### Command-Line Options

```bash
# Use default multiple datasets (both wayang_stories and sitija_takon_bapa)
python pipeline.py

# Use single dataset only
python pipeline.py --single-dataset --dataset /path/to/dataset.csv

# Use custom multiple datasets
python pipeline.py --datasets /path/to/dataset1.csv /path/to/dataset2.csv

# Specify output directory
python pipeline.py --output /path/to/output

# Use transformer-based NER
### Programmatic Usage

```python
from pipeline import WayangPipeline

# Initialize pipeline with multiple datasets (default)
pipeline = WayangPipeline(
## 📖 Usage

### Evaluate NER Models

Compare spaCy multilingual model with a custom trained model:

```bash
# Run complete evaluation workflow
python run_ner_evaluation.py

# Or step by step:
python create_training_data.py     # Extract training data
python ner_trainer.py               # Train custom model
python compare_ner_models.py        # Compare and generate reports
```

See [docs/NER_EVALUATION.md](docs/NER_EVALUATION.md) for detailed guide.

### Command-Line Optionsy'
)

# Or use single dataset
pipeline = WayangPipeline(
    dataset_path='data/wayang_stories_dataset.csv',
    use_multiple_datasets=False,
    output_dir='output',
    ner_model_type='spacy'
)

# Run full pipeline
pipeline.run_full_pipeline(max_vis_nodes=100)
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
### `visualization.py`

**GraphVisualizer** - Creates interactive visualizations

```python
visualizer = GraphVisualizer()
visualizer.visualize_from_knowledge_graph(kg, 'output.html')
```

### `metrics.py`

**MetricsCollector** - Collects and reports pipeline metrics

```python
from metrics import MetricsCollector, generate_metrics_report

metrics = MetricsCollector()
metrics.start_pipeline(config)
# ... run pipeline stages ...
metrics.finalize_metrics()
metrics.save_metrics('output/metrics.json')
metrics.print_summary()

# Generate HTML report
generate_metrics_report('output/metrics.json', 'output/report.html')
```

**Metrics Include:**
- Data loading statistics
- Preprocessing metrics (sentences, text lengths)
- NER extraction (entity counts, types, methods)
- Relation extraction (relation types, confidence)
- Knowledge graph analytics (density, centrality, clustering)
- Execution time breakdown by stage
- Memory usage

---
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
## 🎯 Project Structure

```
.
├── data/                    # Datasets directory
│   ├── wayang_stories_dataset.csv      # Main wayang stories
│   └── sitija_takon_bapa_dataset.csv   # Sitija stories
├── requirements.txt         # Python dependencies
├── config.py                # Configuration file

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
