# Wayang Stories NER Evaluation

Named Entity Recognition (NER) model evaluation for Indonesian Wayang stories, comparing spaCy's multilingual model against a custom-trained domain-specific model.

## 🏆 Results

The **Custom Trained Model** significantly outperforms the baseline:

| Metric | spaCy Multilingual | Custom Trained | Improvement |
|--------|-------------------|----------------|-------------|
| **Exact Match F1** | 0.00% | **23.08%** | +23.08% |
| **Partial Match F1** | 3.92% | **94.34%** | +90.42% |
| **Micro F1** | 0.00% | **18.60%** | +18.60% |

📄 View full results: `docs/NER_EVALUATION_SUMMARY.md`

## 📁 Project Structure

```
.
├── scripts/                        # Data preparation
│   ├── manual_annotations.py       # 45 annotated examples
│   └── create_manual_training_data.py
│
├── evaluation/                     # NER evaluation system
│   ├── ner_trainer.py              # Train custom model
│   ├── ner_evaluator.py            # Calculate metrics
│   └── compare_ner_models.py       # Compare models
│
├── tools/                          # Helper utilities
│   └── annotate_helper.py          # Annotation assistant
│
├── models/                         # Trained models & data
│   ├── train_data.json             # 36 training examples
│   ├── test_data.json              # 9 test examples
│   └── custom_ner_model/           # Trained model
│
├── output/                         # Evaluation reports
│   ├── ner_evaluation_comparison.json
│   └── ner_evaluation_comparison.html
│
├── docs/                           # Documentation
│   ├── NER_EVALUATION_SUMMARY.md
│   ├── NER_EVALUATION_FINAL_RESULTS.md
│   ├── HOW_TO_EXPAND_ANNOTATIONS.md
│   └── NER_EVALUATION.md
│
├── archived/                       # Old/unused files
├── data/                           # Source datasets
├── run_ner_evaluation.py           # Complete workflow
└── requirements.txt
```

## ✨ Features

### 1. Knowledge Graph Visualization
- **Interactive Network**: Explore entity relationships through physics-based graph layout
- **Entity Types**: Color-coded PERSON (blue), LOC (teal), ORG (orange), EVENT (red)
- **Relation Categories**: Family (pink), Conflict (red), Location (cyan), Participation (green)
- **Smart Sizing**: Node size reflects connectivity; edge width shows relation frequency
- **Rich Interactions**: Hover tooltips, zoom, pan, navigation controls
- **Full Dataset**: Visualizes all 45 manually annotated examples

### 2. Dual Model Evaluation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy multilingual model
python -m spacy download xx_ent_wiki_sm
```

### 2. Build Knowledge Graph

```bash
# Build interactive knowledge graph from annotations
python3 build_knowledge_graph.py

# View the graph
xdg-open output/knowledge_graph.html
```

This creates an interactive visualization showing:
- 96 entities from all annotated data
- Relationships between entities (family, conflict, location)
- Color-coded by entity type
- Node size based on connectivity

### 3. Run Complete Evaluation

```bash
# Run the entire workflow
python3 run_ner_evaluation.py
```

This will:
1. Generate training data (36 train / 9 test examples)
2. Train custom NER model (~10 seconds)
3. Compare models and generate reports

### 4. View Results

```bash
# Open interactive HTML report
xdg-open output/ner_evaluation_comparison.html

# Or read the summary
cat docs/NER_EVALUATION_SUMMARY.md
```

## 📊 Knowledge Graph Statistics

From the 45 manually annotated Wayang stories:
- **96 Total Entities**: 68 PERSON, 21 LOC, 5 ORG, 2 EVENT
- **12 Relations Extracted**: Family (8), Conflict (3), Location (1)
- **Top Relations**: sibling_of (4), fought_with (2), child_of (2)
- **Most Connected**: Nakula, Sadewa, Paksi Wilmuna, Kurawa

The knowledge graph provides insights into character relationships, locations, and events across the annotated corpus.

## 📊 Entity Types

The model recognizes four entity types:

- **PERSON** - Character names (Raden Arjuna, Prabu Kresna)
- **LOC** - Locations (Kerajaan Dwarawati, Kahyangan Suralaya)
- **ORG** - Organizations (Pandawa, Kurawa)
- **EVENT** - Named events (Perang Bharatayudha)

## 🛠️ Manual Steps

### Build Knowledge Graph Only

```bash
python3 build_knowledge_graph.py
```

Outputs:
- `output/knowledge_graph.html` - Interactive visualization
- `output/knowledge_graph.json` - Graph data export

### Train Model Only

```bash
python3 evaluation/ner_trainer.py
```

### Compare Models Only

```bash
python3 evaluation/compare_ner_models.py
```

### Add More Annotations

```bash
# Use helper tool
python3 tools/annotate_helper.py

# Or use batch mode
python3 tools/annotate_helper.py --batch

# Edit annotations
nano scripts/manual_annotations.py

# Re-run workflow
python3 run_ner_evaluation.py
```

📖 See: `docs/HOW_TO_EXPAND_ANNOTATIONS.md`

## 📈 Training Data

- **Current:** 45 manually annotated sentences
- **Training:** 36 examples (80%)
- **Testing:** 9 examples (20%)
- **Entities:** 122 total (PERSON: 81, LOC: 24, ORG: 14, EVENT: 3)

### Sample Annotation

```python
(
    "Prabu Kresna memerintah di Kerajaan Dwarawati.",
    [(0, 12, 'PERSON'), (27, 45, 'LOC')]
),
```

## 🎯 Key Findings

1. ✅ **Domain-specific training works** - Custom model achieves 23.08% F1 vs 0.00% baseline
2. ✅ **Excellent boundary detection** - 94.34% Partial Match F1
3. ✅ **Manual annotations effective** - High-quality labels produce good results
4. ⚠️ **Need more data** - Current 45 examples prove concept; target 200+ for production

## 📚 Documentation

- **NER_EVALUATION_SUMMARY.md** - Complete overview and quick reference
- **NER_EVALUATION_FINAL_RESULTS.md** - Detailed analysis with examples
- **HOW_TO_EXPAND_ANNOTATIONS.md** - Guide to add more training data
- **NER_EVALUATION.md** - Technical documentation

## 🔧 Technical Details

**Custom Model:**
- Base: `xx_ent_wiki_sm` (spaCy multilingual)
- Method: Transfer learning
- Training: 30 iterations, batch size 8, dropout 0.2
- Final loss: 0.0105

**Metrics:**
- Exact Match (entity-level)
- Partial Match (token-level)
- Per-label F1 scores
- Macro/Micro F1
- Confusion matrices

## 📝 Next Steps

- [ ] Expand to 100+ annotated examples
- [ ] Add more LOC/ORG entity examples
- [ ] Re-train with larger dataset
- [ ] Target 0.70+ F1 for production

## 👤 Author

Kelompok 1  
NLP Final Assignment - November 2025

**Members:**
1. Achmad Mirzaram Dhani
2. Afito Indra Permana
3. Ahmad Reza Adrian
4. Ahmad Wildan Putro Santoso

## 📄 License

See LICENSE file
