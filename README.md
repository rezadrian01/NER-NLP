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

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy multilingual model
python -m spacy download xx_ent_wiki_sm
```

### 2. Run Complete Evaluation

```bash
# Run the entire workflow (auto)
python3 run_ner_evaluation.py
```

This will:
1. Generate training data (36 train / 9 test examples)
2. Train custom NER model (~10 seconds)
3. Compare models and generate reports

### 3. View Results

```bash
# Open interactive HTML report
xdg-open output/ner_evaluation_comparison.html

# Or read the summary
cat docs/NER_EVALUATION_SUMMARY.md
```

## 📊 Entity Types

The model recognizes four entity types:

- **PERSON** - Character names (Raden Arjuna, Prabu Kresna)
- **LOC** - Locations (Kerajaan Dwarawati, Kahyangan Suralaya)
- **ORG** - Organizations (Pandawa, Kurawa)
- **EVENT** - Named events (Perang Bharatayudha)

## 🛠️ Manual Steps

### Train Only

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

Ahmad Reza Adrian  
NLP Final Assignment - November 2025

## 📄 License

See LICENSE file
