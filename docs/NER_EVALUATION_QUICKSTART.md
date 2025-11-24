# NER Model Evaluation - Quick Reference

## 🎯 What You Get

This evaluation system allows you to:

1. **Train a custom NER model** on your wayang stories dataset
2. **Compare it with spaCy's multilingual model** using comprehensive metrics
3. **Get detailed reports** in both JSON and HTML formats

## 📊 Metrics Provided

### Exact Match Metrics
- **Precision**: What % of predicted entities are correct
- **Recall**: What % of true entities were found
- **F1 Score**: Balance between precision and recall

### Partial Match Metrics
- Same as exact match but more lenient (allows boundary overlap)

### Aggregate Metrics
- **Macro F1**: Average F1 across all entity types
- **Micro F1**: Overall F1 (recommended for overall performance)

### Per-Label Analysis
- F1, Precision, Recall for each entity type:
  - PERSON (characters)
  - LOC (locations/kingdoms)
  - ORG (organizations like Pandawa, Kurawa)
  - EVENT (battles, ceremonies)

## 🚀 Three Ways to Run

### 1. Complete Workflow (Easiest)
```bash
python run_ner_evaluation.py
```
- Creates training data
- Trains custom model (5-10 minutes)
- Evaluates both models
- Generates reports

### 2. Step by Step
```bash
# Step 1: Extract training data (30 seconds)
python create_training_data.py

# Step 2: Train model (5-10 minutes)
python ner_trainer.py

# Step 3: Compare models (1-2 minutes)
python compare_ner_models.py
```

### 3. Re-run Comparison Only
```bash
# If you already have trained model
python compare_ner_models.py
```

## 📁 Output Files

After running, you'll get:

```
models/
├── train_data.json              # Training examples with annotations
├── test_data.json               # Test examples for evaluation
├── full_data.json               # All examples combined
└── custom_ner_model/            # Your trained spaCy model

output/
├── ner_evaluation_comparison.json      # Detailed metrics (machine-readable)
└── ner_evaluation_comparison.html      # Beautiful visual report (open in browser)
```

## 📊 Reading the HTML Report

Open `output/ner_evaluation_comparison.html` and you'll see:

1. **🏆 Winner Banner**: Which model performed better
2. **Overall Metrics Table**: Direct comparison of key metrics
3. **Per-Label Bar Charts**: Visual comparison for each entity type
4. **Detailed Metrics**: TP/FP/FN counts
5. **Interpretation Guide**: Explains what everything means

## 🎓 Understanding the Results

| Micro F1 Score | What It Means |
|----------------|---------------|
| 0.90+          | Excellent! 🎉 |
| 0.80-0.89      | Good 👍 |
| 0.70-0.79      | Fair 😐 |
| < 0.70         | Needs improvement 😕 |

### Expected Outcome

**Custom Model Usually Wins** because:
- Trained specifically on your domain (wayang stories)
- Learns your specific naming patterns
- Optimized for your entity types

**If spaCy Wins**, it might mean:
- Need more training data (try getting 50+ examples)
- Annotations need improvement
- Consider training for more iterations

## ⚙️ Customization

### Train Longer
Edit `ner_trainer.py`, line ~90:
```python
# Change n_iter from 30 to 50
losses = trainer.train(training_data, n_iter=50, dropout=0.2, batch_size=8)
```

### Add More Entity Patterns
Edit `create_training_data.py`, add patterns:
```python
'PERSON': [
    r'\bYourNewPattern\b',
    # Add your patterns here
],
```

### Adjust Train/Test Split
Edit `create_training_data.py`, line ~150:
```python
# Use 30% for testing instead of 20%
train_data, test_data = extractor.split_train_test(training_data, test_size=0.3)
```

## 🐛 Common Issues

### "Test data not found"
→ Run `python create_training_data.py` first

### "Custom model not found"
→ Run `python ner_trainer.py` first

### Low F1 scores
→ Need more training data or better patterns

### Out of memory
→ Edit `ner_trainer.py`, reduce `batch_size` to 4

## 📞 Quick Help

1. Check console for error messages
2. Verify spaCy model installed: `python -m spacy download xx_ent_wiki_sm`
3. Read full guide: `docs/NER_EVALUATION.md`

## 🎯 Next Steps After Evaluation

1. **Open the HTML report** - Review visual comparisons
2. **Check which model won** - Usually the custom model
3. **Review per-label performance** - See which entity types need work
4. **Use the better model** - Integrate into your pipeline
5. **Iterate and improve** - Add more data, refine patterns

---

**Ready to start?**
```bash
python run_ner_evaluation.py
```

Then open `output/ner_evaluation_comparison.html` in your browser! 🚀
