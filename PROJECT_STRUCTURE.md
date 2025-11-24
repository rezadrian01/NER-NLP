# Project Structure

This document describes the organized structure of the Wayang Stories NER Evaluation project.

## 📁 Directory Layout

```
.
├── README.md                       # Main project documentation
├── LICENSE                         # Project license
├── requirements.txt                # Python dependencies
├── run_ner_evaluation.py           # Main workflow script
│
├── scripts/                        # Data Preparation Scripts
│   ├── manual_annotations.py       # 45 manually curated annotations
│   └── create_manual_training_data.py  # Generate train/test split
│
├── evaluation/                     # NER Evaluation System
│   ├── ner_trainer.py              # Train custom spaCy model
│   ├── ner_evaluator.py            # Calculate comprehensive metrics
│   └── compare_ner_models.py       # Side-by-side model comparison
│
├── tools/                          # Helper Utilities
│   └── annotate_helper.py          # Interactive annotation tool
│
├── models/                         # Training Data & Models
│   ├── train_data.json             # 36 training examples
│   ├── test_data.json              # 9 test examples
│   ├── full_data.json              # All 45 examples
│   └── custom_ner_model/           # Trained spaCy model
│
├── output/                         # Evaluation Reports
│   ├── ner_evaluation_comparison.json  # Detailed results
│   ├── ner_evaluation_comparison.html  # Interactive report
│   └── README.md                   # Output directory info
│
├── docs/                           # Documentation
│   ├── NER_EVALUATION_SUMMARY.md   # Quick overview
│   ├── NER_EVALUATION_FINAL_RESULTS.md  # Detailed analysis
│   ├── HOW_TO_EXPAND_ANNOTATIONS.md     # Annotation guide
│   ├── NER_EVALUATION.md           # Technical documentation
│   └── NER_EVALUATION_QUICKSTART.md     # Quick start guide
│
├── data/                           # Source Datasets
│   ├── wayang_stories.csv          # Main wayang stories
│   └── sitija_takon_bapa_story.csv # Sitija stories
│
├── archived/                       # Old/Unused Files
│   ├── create_training_data.py     # Old regex-based extractor
│   ├── test_*.py                   # Old test files
│   ├── ner_extraction.py           # Old extraction module
│   ├── preprocessing.py            # Old preprocessing
│   ├── visualization.py            # Old visualization
│   ├── app.py                      # Old Flask app
│   ├── pipeline.py                 # Old pipeline
│   └── README_OLD.md               # Previous README versions
│
├── templates/                      # HTML Templates (legacy)
├── lib/                            # JavaScript Libraries (legacy)
└── venv/                           # Virtual environment
```

## 🎯 Core Workflow

### Step 1: Manual Annotations
**File:** `scripts/manual_annotations.py`

Contains 45 manually curated sentence annotations with exact character positions:
```python
MANUAL_ANNOTATIONS = [
    (
        "Prabu Kresna memerintah di Kerajaan Dwarawati.",
        [(0, 12, 'PERSON'), (27, 45, 'LOC')]
    ),
    # ... 44 more examples
]
```

### Step 2: Generate Training Data
**File:** `scripts/create_manual_training_data.py`

Splits annotations into:
- `models/train_data.json` - 36 examples (80%)
- `models/test_data.json` - 9 examples (20%)

Run: `python3 scripts/create_manual_training_data.py`

### Step 3: Train Custom Model
**File:** `evaluation/ner_trainer.py`

Trains spaCy NER model using transfer learning:
- Base model: `xx_ent_wiki_sm`
- 30 iterations, batch size 8, dropout 0.2
- Output: `models/custom_ner_model/`

Run: `python3 evaluation/ner_trainer.py`

### Step 4: Evaluate & Compare
**File:** `evaluation/compare_ner_models.py`

Compares two models:
1. spaCy Multilingual (`xx_ent_wiki_sm`)
2. Custom Trained Model

Generates:
- `output/ner_evaluation_comparison.json`
- `output/ner_evaluation_comparison.html`

Run: `python3 evaluation/compare_ner_models.py`

## 🔧 Helper Tools

### Annotation Helper
**File:** `tools/annotate_helper.py`

Interactive tool to help create new annotations:
```bash
# Interactive mode
python3 tools/annotate_helper.py

# Batch examples
python3 tools/annotate_helper.py --batch
```

## 📊 Entity Types

1. **PERSON** - Character names (Raden Arjuna, Prabu Kresna)
2. **LOC** - Locations (Kerajaan Dwarawati, Kahyangan Suralaya)
3. **ORG** - Organizations (Pandawa, Kurawa)
4. **EVENT** - Named events (Perang Bharatayudha)

## 🚀 Complete Workflow

**Automated:**
```bash
python3 run_ner_evaluation.py
```

**Manual Steps:**
```bash
# 1. Generate training data
python3 scripts/create_manual_training_data.py

# 2. Train model
python3 evaluation/ner_trainer.py

# 3. Compare models
python3 evaluation/compare_ner_models.py

# 4. View results
xdg-open output/ner_evaluation_comparison.html
```

## 📝 Key Files to Edit

### Adding Annotations
Edit: `scripts/manual_annotations.py`

Add tuples to `MANUAL_ANNOTATIONS` list:
```python
(
    "Your sentence here.",
    [(start, end, 'LABEL'), ...]
),
```

### Configuration
Training parameters in: `evaluation/ner_trainer.py`
- `n_iter` - Training iterations (default: 30)
- `batch_size` - Batch size (default: 8)
- `drop` - Dropout rate (default: 0.2)

## 🗑️ Archived Files

The `archived/` directory contains:
- Old extraction methods (regex-based)
- Old test files
- Previous visualization tools
- Legacy pipeline components
- Old documentation versions

These are kept for reference but not used in the current workflow.

## 📖 Documentation

All documentation is in `docs/`:

1. **NER_EVALUATION_SUMMARY.md** - Quick overview, results, usage
2. **NER_EVALUATION_FINAL_RESULTS.md** - Complete analysis with tables
3. **HOW_TO_EXPAND_ANNOTATIONS.md** - Step-by-step annotation guide
4. **NER_EVALUATION.md** - Technical details and API reference
5. **NER_EVALUATION_QUICKSTART.md** - Fast start guide

## 🎓 Purpose

This is a clean, focused NER evaluation system that:
1. Uses manual annotations (not regex)
2. Trains domain-specific models
3. Provides comprehensive metrics
4. Generates beautiful reports
5. Makes it easy to expand training data

**Status:** Production-ready proof-of-concept. Ready for dataset expansion phase.

---

Last updated: November 24, 2025
