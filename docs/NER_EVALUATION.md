# NER Model Evaluation Guide

## 📋 Overview

This guide explains how to evaluate and compare two NER models:
1. **spaCy Multilingual Model** (`xx_ent_wiki_sm`) - Pre-trained on multiple languages
2. **Custom Trained Model** - Trained specifically on your wayang stories dataset

## 🎯 Evaluation Metrics

### Exact Match Metrics
- **Precision**: Percentage of predicted entities that are correct
- **Recall**: Percentage of true entities that were found
- **F1 Score**: Harmonic mean of precision and recall
- Requires entity boundaries AND type to match exactly

### Partial Match Metrics
- Same as exact match but allows overlapping boundaries
- More lenient evaluation - useful for boundary detection analysis

### Per-Label Metrics
- **Macro F1**: Average F1 across all entity types (treats all types equally)
- **Micro F1**: F1 calculated from total TP/FP/FN (weighted by frequency)
- Individual precision, recall, F1 for each entity type (PERSON, LOC, ORG, EVENT)

### Confusion Matrix
- Shows which entity types are confused with each other
- Helps identify systematic errors

## 🚀 Quick Start

### Option 1: Run Complete Workflow (Recommended)

```bash
# This runs everything: data creation, training, evaluation
python run_ner_evaluation.py
```

This single command will:
1. Extract training data from your datasets
2. Train the custom NER model (takes 5-10 minutes)
3. Evaluate both models on test data
4. Generate comparison reports

### Option 2: Step-by-Step

```bash
# Step 1: Create training/test data
python create_training_data.py

# Step 2: Train custom model
python ner_trainer.py

# Step 3: Compare both models
python compare_ner_models.py
```

## 📊 Understanding the Results

### Output Files

1. **`models/train_data.json`** - Training examples with entity annotations
2. **`models/test_data.json`** - Test examples for evaluation
3. **`models/custom_ner_model/`** - Trained spaCy model directory
4. **`output/ner_evaluation_comparison.json`** - Detailed metrics in JSON format
5. **`output/ner_evaluation_comparison.html`** - Interactive visual report

### Reading the HTML Report

Open `output/ner_evaluation_comparison.html` in your browser. The report includes:

- **Winner Banner**: Shows which model performed better overall
- **Overall Metrics Table**: Direct comparison of key metrics
- **Per-Label Bar Charts**: Visual comparison for each entity type
- **Detailed Metrics**: TP/FP/FN counts for both models
- **Interpretation Guide**: Explains what each metric means

### Interpreting Scores

| F1 Score | Interpretation |
|----------|----------------|
| 0.90+    | Excellent      |
| 0.80-0.89| Good           |
| 0.70-0.79| Fair           |
| < 0.70   | Needs improvement |

## 🔍 Common Scenarios

### Scenario 1: Custom Model Performs Better

This is expected because:
- Custom model is trained on your specific domain (wayang stories)
- Learns your specific entity patterns and naming conventions
- Optimized for Indonesian language constructs in your data

**Action**: Use the custom model in production pipeline.

### Scenario 2: spaCy Model Performs Better

This might happen if:
- Training data is too small (< 50 examples)
- Training data has inconsistent annotations
- Base model already has good Indonesian coverage

**Action**: 
- Collect more training data
- Improve annotation consistency
- Try training for more iterations

### Scenario 3: Similar Performance

Both models are comparable. Consider:
- Use custom model for better domain adaptation
- Use spaCy model for faster inference (if speed matters)
- Ensemble both models for better coverage

## 🛠️ Advanced Usage

### Adjust Training Parameters

Edit `ner_trainer.py`:

```python
# Train for more iterations (better accuracy, takes longer)
losses = trainer.train(training_data, n_iter=50, dropout=0.2, batch_size=8)

# Increase dropout for better generalization
losses = trainer.train(training_data, n_iter=30, dropout=0.3, batch_size=8)

# Smaller batch size for smaller datasets
losses = trainer.train(training_data, n_iter=30, dropout=0.2, batch_size=4)
```

### Modify Entity Patterns

Edit `create_training_data.py` to add more entity patterns:

```python
'PERSON': [
    r'\bYourNewPattern\b',
    # Add more patterns
],
```

### Change Train/Test Split

In `create_training_data.py`:

```python
# Use 30% for testing instead of 20%
train_data, test_data = extractor.split_train_test(training_data, test_size=0.3)
```

## 📈 Improving Model Performance

### 1. Add More Training Data
- Manually annotate more examples
- Use active learning to find difficult cases
- Balance entity type distribution

### 2. Refine Entity Patterns
- Add more specific patterns for your domain
- Handle variations in spelling and naming
- Include context-dependent patterns

### 3. Tune Hyperparameters
- Increase training iterations (30 → 50)
- Adjust learning rate
- Modify dropout rate

### 4. Post-Processing
- Add business rules for common errors
- Use entity linking for disambiguation
- Apply confidence thresholding

## 🐛 Troubleshooting

### Issue: "Test data not found"
**Solution**: Run `python create_training_data.py` first

### Issue: "Custom model not found"
**Solution**: Run `python ner_trainer.py` first

### Issue: Low F1 scores (< 0.5)
**Possible causes**:
- Insufficient training data
- Poor quality annotations
- Entity patterns too specific/general

**Solutions**:
- Collect more training examples (aim for 100+)
- Review and fix annotation quality
- Adjust entity patterns in `create_training_data.py`

### Issue: Out of memory during training
**Solution**: Reduce batch size in `ner_trainer.py`:
```python
losses = trainer.train(training_data, n_iter=30, dropout=0.2, batch_size=4)
```

### Issue: Training takes too long
**Solution**: Reduce iterations or use fewer examples:
```python
losses = trainer.train(training_data[:100], n_iter=20, dropout=0.2, batch_size=8)
```

## 📚 File Structure

```
├── create_training_data.py      # Extract annotations from dataset
├── ner_trainer.py                # Train custom spaCy model
├── ner_evaluator.py              # Evaluation metrics module
├── compare_ner_models.py         # Compare two models
├── run_ner_evaluation.py         # Complete workflow script
├── models/
│   ├── train_data.json          # Training examples
│   ├── test_data.json           # Test examples
│   └── custom_ner_model/        # Trained model
└── output/
    ├── ner_evaluation_comparison.json
    └── ner_evaluation_comparison.html
```

## 🎓 Best Practices

1. **Always use a held-out test set** - Don't train and test on the same data
2. **Balance your entity types** - Ensure all types are represented in training
3. **Review predictions manually** - Look at actual predictions, not just metrics
4. **Iterate and improve** - Use evaluation results to refine patterns and training
5. **Document your decisions** - Keep notes on why certain patterns/parameters work

## 📞 Need Help?

If you encounter issues:
1. Check the console output for specific error messages
2. Review this guide's troubleshooting section
3. Verify all prerequisite files exist
4. Check that spaCy model is downloaded: `python -m spacy download xx_ent_wiki_sm`

---

**Generated by**: NER Evaluation System for Wayang Stories  
**Author**: Ahmad Reza Adrian  
**Date**: November 24, 2025
