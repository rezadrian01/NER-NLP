# 🚀 Quick Start Guide

## One Command to Rule Them All

```bash
./run_all.sh
```

That's it! This single command will:

1. ✅ **Setup Environment**
   - Check if virtual environment exists (create if not)
   - Install all Python dependencies
   - Download spaCy multilingual model

2. ✅ **Train NER Model**
   - Load training data (36 examples)
   - Train custom spaCy model (30 iterations)
   - Save model to `models/custom_ner_model/`

3. ✅ **Evaluate Models**
   - Compare custom vs multilingual baseline
   - Calculate F1 scores (exact & partial match)
   - Generate comparison reports

4. ✅ **Build Knowledge Graph**
   - Extract entities from 45 annotated stories
   - Apply 3 relation extraction methods:
     * Regex (42 Indonesian patterns)
     * Dependency parsing
     * Co-occurrence statistics
   - Generate interactive visualization

5. ✅ **Show Results**
   - Display execution summary
   - List all output files
   - Show viewing instructions

## 📊 Where to Find Results

After running `./run_all.sh`, open these files in your browser:

### Interactive Visualizations
```bash
# Knowledge Graph (96 entities, 94 relations)
xdg-open output/knowledge_graph.html

# NER Model Comparison
xdg-open output/ner_evaluation_comparison.html
```

Or navigate to:
- `file:///path/to/project/output/knowledge_graph.html`
- `file:///path/to/project/output/ner_evaluation_comparison.html`

### Data Files
- **Graph Data**: `output/knowledge_graph.json`
- **Evaluation Data**: `output/ner_evaluation_comparison.json`
- **Execution Log**: `output/pipeline_execution.log`
- **Trained Model**: `models/custom_ner_model/`

### Entity-Specific Visualizations
- Individual entity graphs: `output/entity_visualizations/`

## 🎯 What You'll See

### Knowledge Graph Visualization
- **Interactive network** with physics simulation
- **Color-coded entities**:
  - 🔵 Blue = PERSON (68 nodes)
  - 🟢 Teal = LOC (21 nodes)
  - 🟠 Orange = ORG (5 nodes)
  - 🔴 Red = EVENT (2 nodes)
- **Relation types**:
  - berinteraksi_dengan (54 relations)
  - terkait_dengan_lokasi (17 relations)
  - anak_dari, melawan, memerintah_di, etc.

### NER Evaluation Report
- **Model comparison table**
- **Per-entity metrics**
- **Confusion matrix**
- **Example predictions**

## ⚙️ Requirements

- **Python**: 3.8+
- **OS**: Linux, macOS, or Windows (with bash)
- **Disk**: ~500MB for models and dependencies
- **Time**: ~5-10 minutes for first run

## 🐛 Troubleshooting

### Script won't run
```bash
chmod +x run_all.sh
./run_all.sh
```

### Permission denied
```bash
bash run_all.sh
```

### Virtual environment issues
```bash
# Remove old venv and run again
rm -rf venv
./run_all.sh
```

### Dependency errors
```bash
# Activate venv and install manually
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download xx_ent_wiki_sm
```

## 📖 Advanced Usage

For manual control or individual steps, see:
- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [NER_EVALUATION_SUMMARY.md](docs/NER_EVALUATION_SUMMARY.md) - Detailed results

## 🔧 Configuration

Edit these files if needed:
- **Training iterations**: `ner_trainer.py` (line ~100, `n_iter=30`)
- **Relation patterns**: `build_knowledge_graph.py` (`_init_relation_patterns()`)
- **Output paths**: `run_all.sh` (variables at top)

## 📝 Execution Log

Check the detailed execution log:
```bash
cat output/pipeline_execution.log
```

Or watch in real-time:
```bash
tail -f output/pipeline_execution.log
```

## 🎉 Success Indicators

The script completed successfully if you see:
```
✨ All pipeline steps completed successfully!
```

And these files exist:
- `output/knowledge_graph.html` ✓
- `output/ner_evaluation_comparison.html` ✓
- `models/custom_ner_model/` ✓
- `output/pipeline_execution.log` ✓
