# System Architecture

This document describes the architecture of the Wayang Stories NER & Knowledge Graph system.

## 📐 System Overview

The system consists of three main components:
1. **NER Evaluation Pipeline** - Training and evaluating Named Entity Recognition models
2. **Knowledge Graph Builder** - Extracting and visualizing entity relationships
3. **Annotation Tools** - Helper utilities for creating training data

```
┌─────────────────────────────────────────────────────────────────┐
│                     Wayang Stories NER System                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐   ┌────────────────┐   ┌──────────────────┐ │
│  │  Annotation   │   │      NER       │   │   Knowledge      │ │
│  │     Tools     │──▶│   Evaluation   │──▶│  Graph Builder   │ │
│  │               │   │    Pipeline    │   │                  │ │
│  └───────────────┘   └────────────────┘   └──────────────────┘ │
│         │                    │                      │           │
│         ▼                    ▼                      ▼           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                       Data Layer                          │ │
│  │  • CSV Stories  • JSON Annotations  • Trained Models     │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture Diagram

### High-Level Architecture

```
                    ┌──────────────────────┐
                    │   User Interface     │
                    │   (CLI Commands)     │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
    │  Annotation     │ │     NER     │ │  Knowledge      │
    │  Helpers        │ │  Evaluator  │ │  Graph Builder  │
    └────────┬────────┘ └──────┬──────┘ └────────┬────────┘
             │                 │                  │
             │                 │                  │
             ▼                 ▼                  ▼
    ┌──────────────────────────────────────────────────────┐
    │              Data Storage & Models                    │
    ├──────────────────────────────────────────────────────┤
    │  • Raw Stories (CSV)                                 │
    │  • Annotated Data (JSON)                             │
    │  • Trained NER Models                                │
    │  • Knowledge Graph (JSON/HTML)                       │
    └──────────────────────────────────────────────────────┘
```

## 📦 Component Architecture

### 1. Annotation Tools Layer

**Purpose**: Create and manage manual annotations for training data

```
┌─────────────────────────────────────────────────────────┐
│              Annotation Tools Component                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  tools/annotate_helper.py                               │
│  ├─ Interactive Mode: One-by-one annotation             │
│  └─ Batch Mode: Multiple annotations                    │
│                                                           │
│  scripts/manual_annotations.py                           │
│  ├─ 45 Pre-annotated Examples                           │
│  ├─ Character positions (start, end, label)             │
│  └─ Entity types: PERSON, LOC, ORG, EVENT               │
│                                                           │
│  scripts/create_manual_training_data.py                  │
│  ├─ Generate train/test split (80/20)                   │
│  └─ Export: train_data.json, test_data.json             │
│                                                           │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
                    models/full_data.json
                    models/train_data.json
                    models/test_data.json
```

**Data Format**:
```python
[
    ("Raden Arjuna adalah putra Prabu Pandudewanata",
     {"entities": [(0, 13, "PERSON"), (27, 49, "PERSON")]})
]
```

### 2. NER Evaluation Pipeline

**Purpose**: Train and compare NER models

```
┌──────────────────────────────────────────────────────────────┐
│                NER Evaluation Pipeline                        │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  evaluation/ner_trainer.py                                    │
│  ├─ Load training data (36 examples)                         │
│  ├─ Initialize blank spaCy model                             │
│  ├─ Configure NER pipeline                                   │
│  ├─ Train for 30 iterations                                  │
│  └─ Save to: models/custom_ner_model/                        │
│                                                                │
│  evaluation/ner_evaluator.py                                  │
│  ├─ Load test data (9 examples)                              │
│  ├─ Extract entities with model                              │
│  ├─ Calculate metrics:                                        │
│  │   • Exact Match F1                                        │
│  │   • Partial Match F1                                      │
│  │   • Token-level accuracy                                  │
│  │   • Per-entity-type scores                                │
│  └─ Generate evaluation report                               │
│                                                                │
│  evaluation/compare_ner_models.py                             │
│  ├─ Model 1: spaCy Multilingual (xx_ent_wiki_sm)            │
│  ├─ Model 2: Custom Trained Model                            │
│  ├─ Side-by-side comparison                                  │
│  └─ Export HTML/JSON reports                                 │
│                                                                │
│  run_ner_evaluation.py (Orchestrator)                         │
│  ├─ Step 1: Create training data split                       │
│  ├─ Step 2: Train custom model                               │
│  ├─ Step 3: Compare models                                   │
│  └─ Step 4: Generate reports                                 │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

**Workflow**:
```
Raw Annotations → Train/Test Split → Train Model → Evaluate → Compare
     (45)            (36/9)         (30 iters)     (Metrics)  (Report)
```

### 3. Knowledge Graph Builder

**Purpose**: Extract relationships and visualize entity network

```
┌────────────────────────────────────────────────────────────────┐
│               Knowledge Graph Builder                           │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  build_knowledge_graph.py                                       │
│  │                                                               │
│  ├─ 1. Data Loading                                            │
│  │    ├─ Load full_data.json (45 annotations)                 │
│  │    ├─ Load custom NER model                                │
│  │    └─ Initialize NetworkX DiGraph                          │
│  │                                                               │
│  ├─ 2. Entity Extraction                                       │
│  │    ├─ Extract entities from annotations                    │
│  │    ├─ Count entity mentions                                │
│  │    └─ Add nodes to graph                                   │
│  │                                                               │
│  ├─ 3. Relation Extraction (Triple Method)                    │
│  │    │                                                         │
│  │    ├─ A. Regex Pattern Matching (42 patterns)              │
│  │    │    ├─ Keluarga (11): anak_dari, saudara_dari, etc    │
│  │    │    ├─ Konflik (7): melawan, dibunuh_oleh, etc        │
│  │    │    ├─ Lokasi (6): memerintah_di, berada_di, etc      │
│  │    │    ├─ Partisipasi (4): ikut_dalam, memimpin, etc     │
│  │    │    └─ Sosial (5): bertemu_dengan, membantu, etc      │
│  │    │                                                         │
│  │    ├─ B. Dependency Parsing                                │
│  │    │    ├─ Parse sentence with spaCy                       │
│  │    │    ├─ Analyze subject-verb-object                     │
│  │    │    ├─ Infer relations from verbs                      │
│  │    │    └─ Handle prepositions (di, dari, ke)             │
│  │    │                                                         │
│  │    └─ C. Co-occurrence Statistics                          │
│  │         ├─ Detect entities in same sentence               │
│  │         ├─ PERSON+PERSON → berinteraksi_dengan            │
│  │         ├─ PERSON+LOC → terkait_dengan_lokasi             │
│  │         └─ PERSON+ORG/EVENT → terlibat_dalam              │
│  │                                                               │
│  ├─ 4. Graph Analysis                                          │
│  │    ├─ Calculate degree centrality                          │
│  │    ├─ Compute graph density                                │
│  │    ├─ Entity type distribution                             │
│  │    └─ Relation type distribution                           │
│  │                                                               │
│  ├─ 5. Visualization (PyVis)                                   │
│  │    ├─ Create interactive HTML network                      │
│  │    ├─ Color by entity type                                 │
│  │    ├─ Size by connectivity                                 │
│  │    ├─ Edge color by relation category                      │
│  │    ├─ Physics-based layout (Barnes-Hut)                    │
│  │    └─ Add Indonesian legend                                │
│  │                                                               │
│  └─ 6. Export                                                   │
│       ├─ knowledge_graph.html (interactive viz)               │
│       └─ knowledge_graph.json (graph data)                    │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

**Relation Extraction Pipeline**:
```
Text: "Nakula dan Sadewa adalah saudara"
       ↓
   ┌───────────────────────────────────────────┐
   │  Entities: [Nakula, Sadewa]              │
   └───────────────────────────────────────────┘
       ↓
   ┌───────────────────────────────────────────┐
   │  1. Regex: "(.+?) dan (.+?) adalah saudara"│
   │     → Match! saudara_dari (bidirectional) │
   └───────────────────────────────────────────┘
       ↓
   ┌───────────────────────────────────────────┐
   │  2. Dependency: conj(Nakula, Sadewa)     │
   │     → Additional context                  │
   └───────────────────────────────────────────┘
       ↓
   ┌───────────────────────────────────────────┐
   │  3. Co-occurrence: PERSON + PERSON        │
   │     → berinteraksi_dengan (if no stronger)│
   └───────────────────────────────────────────┘
       ↓
   Graph: Nakula ←→ saudara_dari ←→ Sadewa
```

## 🔄 Data Flow Architecture

### Complete System Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                               │
├──────────────────────────────────────────────────────────────────┤
│  data/wayang_stories.csv                                          │
│  data/sitija_takon_bapa_story.csv                               │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                      ANNOTATION LAYER                             │
├──────────────────────────────────────────────────────────────────┤
│  tools/annotate_helper.py                                        │
│  ├─ Manual annotation interface                                  │
│  └─ Output: scripts/manual_annotations.py                        │
│                                                                   │
│  scripts/create_manual_training_data.py                           │
│  └─ Generate train/test split                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                                 │
├──────────────────────────────────────────────────────────────────┤
│  models/                                                          │
│  ├─ full_data.json      (45 examples)                           │
│  ├─ train_data.json     (36 examples)                           │
│  └─ test_data.json      (9 examples)                            │
└─────────┬──────────────────────────────┬─────────────────────────┘
          │                              │
          │                              │
          ▼                              ▼
┌───────────────────────┐      ┌─────────────────────────────────┐
│   NER TRAINING        │      │  KNOWLEDGE GRAPH BUILDING       │
├───────────────────────┤      ├─────────────────────────────────┤
│ evaluation/           │      │ build_knowledge_graph.py        │
│ ner_trainer.py        │      │ ├─ Load full_data.json         │
│ ├─ Load train_data    │      │ ├─ Load custom NER model       │
│ ├─ Train spaCy model  │      │ ├─ Extract entities            │
│ └─ Save model         │      │ ├─ Extract relations (3 ways)  │
│                       │      │ ├─ Build NetworkX graph        │
│         │             │      │ ├─ Analyze graph               │
│         ▼             │      │ └─ Visualize with PyVis        │
│  models/              │      │           │                     │
│  custom_ner_model/    │──────┘           │                     │
│  ├─ config.cfg        │                  │                     │
│  ├─ ner/              │                  │                     │
│  └─ vocab/            │                  │                     │
│         │             │                  │                     │
│         ▼             │                  ▼                     │
│ ┌─────────────────┐   │      ┌─────────────────────────────┐  │
│ │ NER EVALUATION  │   │      │  output/                    │  │
│ ├─────────────────┤   │      │  ├─ knowledge_graph.html    │  │
│ │ compare_ner_    │   │      │  └─ knowledge_graph.json    │  │
│ │ models.py       │   │      └─────────────────────────────┘  │
│ ├─ Load test_data │   │                                        │
│ ├─ Evaluate both  │   │                                        │
│ └─ Compare metrics│   │                                        │
│         │         │   │                                        │
│         ▼         │   │                                        │
│  output/          │   │                                        │
│  ├─ ner_evaluation│   │                                        │
│  │   _comparison  │   │                                        │
│  │   .html        │   │                                        │
│  └─ ner_evaluation│   │                                        │
│      _comparison  │   │                                        │
│      .json        │   │                                        │
└───────────────────┘   │                                        │
                        │                                        │
                        ▼                                        │
              ┌──────────────────┐                              │
              │  OUTPUT LAYER    │                              │
              ├──────────────────┤                              │
              │ • HTML Reports   │◀─────────────────────────────┘
              │ • JSON Data      │
              │ • Visualizations │
              └──────────────────┘
```

## 🧩 Module Dependencies

### Dependency Graph

```
┌─────────────────────────────────────────────────────────────┐
│                    External Dependencies                     │
├─────────────────────────────────────────────────────────────┤
│  • spacy (3.x)         - NER models & NLP processing        │
│  • networkx            - Graph data structure               │
│  • pyvis               - Interactive visualization          │
│  • pandas              - Data manipulation                  │
│  • json                - Data serialization                 │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Annotation   │  │     NER      │  │  Knowledge   │
    │   Tools      │  │  Evaluation  │  │    Graph     │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                  │
           └─────────────────┼──────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Data Models   │
                    │  (JSON format) │
                    └────────────────┘
```

### Module Import Structure

```python
# Annotation Tools
tools/annotate_helper.py
    └─ imports: None (standalone)

scripts/manual_annotations.py
    └─ imports: None (data only)

scripts/create_manual_training_data.py
    ├─ from scripts.manual_annotations import ANNOTATIONS
    └─ imports: json, random

# NER Evaluation
evaluation/ner_trainer.py
    ├─ imports: spacy, json, random, Path
    └─ uses: models/train_data.json

evaluation/ner_evaluator.py
    ├─ imports: spacy, json, Counter, defaultdict
    └─ uses: models/test_data.json, custom_ner_model

evaluation/compare_ner_models.py
    ├─ imports: spacy, json, Path, datetime
    ├─ from evaluation.ner_evaluator import NEREvaluator
    └─ uses: both models

run_ner_evaluation.py
    ├─ imports: subprocess, sys, Path
    ├─ calls: create_manual_training_data.py
    ├─ calls: ner_trainer.py
    └─ calls: compare_ner_models.py

# Knowledge Graph
build_knowledge_graph.py
    ├─ imports: spacy, networkx, pyvis, json, re
    ├─ uses: models/custom_ner_model
    └─ uses: models/full_data.json
```

## 🔐 Design Patterns

### 1. Pipeline Pattern
**Used in**: `run_ner_evaluation.py`

```
Step 1 → Step 2 → Step 3 → Step 4
 Data     Train   Evaluate  Report
```

### 2. Builder Pattern
**Used in**: `KnowledgeGraphBuilder`

```python
builder = KnowledgeGraphBuilder(model_path)
builder.load_from_json(data)
builder.create_visualization(output)
builder.save_json(output)
```

### 3. Strategy Pattern
**Used in**: Relation extraction

```python
# Three strategies for relation extraction
1. regex_strategy()        # Pattern matching
2. dependency_strategy()   # Syntactic analysis
3. cooccurrence_strategy() # Statistical
```

### 4. Factory Pattern
**Used in**: Model creation

```python
def create_ner_model(model_type):
    if model_type == "multilingual":
        return spacy.load("xx_ent_wiki_sm")
    elif model_type == "custom":
        return spacy.load("models/custom_ner_model")
```

## 🎯 Key Algorithms

### 1. NER Training Algorithm

```
INPUT: Annotated examples [(text, entities)]
OUTPUT: Trained spaCy model

ALGORITHM:
1. Initialize blank spaCy model
2. Add NER pipeline component
3. Add entity labels to NER
4. FOR iteration in range(30):
     a. Shuffle training data
     b. Batch examples
     c. FOR batch in batches:
          i. Update model with batch
          ii. Calculate loss
     d. Dropout rate decay
5. Save trained model
```

### 2. Relation Extraction Algorithm

```
INPUT: Text with entities [(entity, type)]
OUTPUT: Relations [(source, relation, target)]

ALGORITHM:
1. REGEX MATCHING:
   FOR each pattern in patterns:
     IF pattern matches text:
       Extract subject and object
       Map to entities
       Add relation to graph

2. DEPENDENCY PARSING:
   Parse text with spaCy
   FOR each token:
     IF token is entity:
       FOR each child:
         IF child is entity:
           Infer relation from dependency
           Add to graph

3. CO-OCCURRENCE:
   FOR each entity pair in sentence:
     IF no existing relation:
       Determine relation by entity types
       Add weak association to graph

4. RETURN all extracted relations
```

### 3. Graph Centrality Calculation

```
INPUT: NetworkX graph G
OUTPUT: Top K most connected entities

ALGORITHM:
1. Calculate degree for each node
2. Sort nodes by degree (descending)
3. Return top K nodes
4. Use for visualization sizing
```

## 📊 Performance Characteristics

### Time Complexity

| Component | Operation | Complexity | Notes |
|-----------|-----------|------------|-------|
| NER Training | Train model | O(n × m × i) | n=examples, m=tokens, i=iterations |
| NER Evaluation | Evaluate | O(n × m) | n=test examples, m=tokens |
| Regex Extraction | Match patterns | O(n × p × t) | n=sentences, p=patterns, t=text length |
| Dependency Parsing | Parse sentence | O(n²) | n=tokens per sentence |
| Co-occurrence | Entity pairs | O(e²) | e=entities per sentence |
| Graph Visualization | Render | O(n + e) | n=nodes, e=edges |

### Space Complexity

| Component | Memory Usage | Notes |
|-----------|--------------|-------|
| Custom NER Model | ~50-100 MB | Trained weights |
| Knowledge Graph | ~1-5 MB | NetworkX structure |
| Visualization | ~500 KB | HTML + JavaScript |
| Training Data | ~100 KB | 45 annotated examples |

### Scalability

```
Current: 45 annotations → 96 entities → 94 relations
Scale to: 500 annotations → ~1000 entities → ~1000 relations
Bottleneck: Co-occurrence (O(e²) per sentence)
Solution: Limit entity pairs, use sampling, parallel processing
```

## 🔧 Configuration

### System Configuration Files

```
models/custom_ner_model/config.cfg
├─ [nlp]
│  └─ pipeline = ["ner"]
├─ [components.ner]
│  └─ labels = ["PERSON", "LOC", "ORG", "EVENT"]
└─ [training]
    ├─ iterations = 30
    └─ dropout = 0.2
```

### Hyperparameters

```python
# NER Training
TRAIN_ITERATIONS = 30
DROPOUT_START = 0.5
DROPOUT_END = 0.2
BATCH_SIZE = 8
TRAIN_TEST_SPLIT = 0.8

# Knowledge Graph
MAX_NODES_DISPLAY = 100
COOCCURRENCE_MIN_ENTITIES = 2
COOCCURRENCE_MAX_ENTITIES = 4
PHYSICS_ITERATIONS = 200
```

## 🚀 Deployment Architecture

```
Development Environment
├─ Python 3.10+
├─ Virtual Environment (venv/)
├─ Dependencies (requirements.txt)
└─ Git Repository

Production Considerations
├─ Docker Container (optional)
├─ Model serving (FastAPI/Flask)
├─ Batch processing scripts
└─ Monitoring & Logging
```

## 📈 Future Enhancements

### Planned Improvements

1. **Relation Extraction**
   - Add attention-based neural relation extraction
   - Implement relation classification model
   - Add coreference resolution

2. **Knowledge Graph**
   - Add graph database (Neo4j)
   - Implement SPARQL queries
   - Add graph reasoning

3. **Visualization**
   - Add filtering by entity type
   - Implement subgraph extraction
   - Add temporal analysis

4. **Performance**
   - Parallelize relation extraction
   - Add caching layer
   - Optimize graph algorithms

## 📚 Technical Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **NLP Core** | spaCy 3.x | NER model training & inference |
| **Graph** | NetworkX | Graph data structure & algorithms |
| **Visualization** | PyVis | Interactive HTML visualization |
| **Data** | JSON | Serialization format |
| **Analysis** | Python Collections | Statistics & counting |
| **CLI** | subprocess | Orchestration |

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Authors**: Kelompok 1  
**System Version**: 1.0.0
