# Output Directory Structure

This directory contains all generated outputs from the Wayang NER pipeline.

## 📁 Directory Organization

### Main Output Files
- **`knowledge_graph.html`** - Interactive visualization of the complete knowledge graph
- **`knowledge_graph.json`** - Complete graph data in JSON format (nodes and edges)
- **`preprocessed_data.csv`** - Cleaned and processed text data
- **`pipeline_metrics.json`** - Detailed pipeline performance metrics
- **`pipeline_metrics.html`** - Visual metrics dashboard

### Subdirectories

#### `entity_visualizations/`
Individual entity-focused visualizations showing 1-level connections:
- `entity_<name>.html` - One HTML file per entity

Generated when searching for entities in the web interface.

#### `test_visualizations/`
Test and experimental visualizations:
- `test_*.html` - Various test visualization files
- `test_*.json` - Test graph data

These are generated during development and testing.

#### `archives/`
Old or archived output files from previous runs.

## 🗂️ File Types

### HTML Files
Interactive visualizations that can be opened in any web browser.
- Physics-based network layout
- Hover for entity details
- Click and drag nodes
- Zoom and pan controls

### JSON Files
Structured data files for programmatic access:
- `knowledge_graph.json` - Full graph structure
- `pipeline_metrics.json` - Performance metrics
- `test_graph.json` - Test data

### CSV Files
Tabular data:
- `preprocessed_data.csv` - Processed text with metadata

## 🔄 Regenerating Files

To regenerate all main output files:
```bash
python pipeline.py
```

This will create/overwrite:
- `knowledge_graph.html`
- `knowledge_graph.json`
- `preprocessed_data.csv`
- `pipeline_metrics.json`
- `pipeline_metrics.html`

## 🧹 Cleaning Up

To clean all output files:
```bash
rm -rf output/*
```

To clean only test files:
```bash
rm -rf output/test_visualizations/*
```

To clean only entity visualizations:
```bash
rm -rf output/entity_visualizations/*
```

## 💾 Storage

Typical file sizes:
- `knowledge_graph.html`: 1-2 MB (full graph)
- `knowledge_graph.json`: 500 KB - 1 MB
- `preprocessed_data.csv`: 100-300 KB
- `pipeline_metrics.json`: ~10 KB
- `pipeline_metrics.html`: ~7 KB
- Entity visualizations: 5-50 KB each

Total storage for a full run: **~2-4 MB**

## ⚠️ .gitignore

Most output files should be in `.gitignore` as they are:
- Generated files (can be recreated)
- Large binary/data files
- User-specific results

Keep in git:
- This README
- Sample/example outputs (if needed)
- Directory structure
