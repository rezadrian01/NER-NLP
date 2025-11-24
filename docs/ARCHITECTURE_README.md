# Architecture Documentation Summary

This document provides an overview of the architecture documentation for the Wayang Stories NER & Knowledge Graph System.

## 📚 Documentation Files

### 1. ARCHITECTURE.md
**Purpose**: Complete system architecture documentation

**Contents**:
- System overview with component diagrams
- Three-layer architecture (Annotation → NER → Knowledge Graph)
- Data flow architecture
- Module dependencies and import structure
- Design patterns (Pipeline, Builder, Strategy, Factory)
- Key algorithms (NER training, relation extraction, graph centrality)
- Performance characteristics and complexity analysis
- Configuration and hyperparameters
- Technology stack summary

**When to use**: Understanding the overall system design, component interactions, and technical implementation details.

### 2. architecture.drawio
**Purpose**: Visual architecture diagrams (editable)

**Contents**:
- **Diagram 1: System Architecture**
  - Complete system overview
  - Input/Annotation/NER/Knowledge Graph layers
  - Data flow between components
  - Output layer visualization
  - Color-coded legend

- **Diagram 2: Data Flow**
  - Annotation flow (CSV → 45 examples → train/test)
  - NER training flow (36 examples → model → evaluation)
  - Knowledge graph flow (full data → 3 extraction methods → viz)
  - Performance metrics
  - Technology stack

**How to use**: 
1. Open with [draw.io](https://app.diagrams.net) (online) or desktop app
2. Edit shapes, arrows, colors
3. Export to PNG/SVG/PDF for presentations
4. Two tabs: "System Architecture" and "Data Flow"

**When to use**: Creating presentations, explaining system to stakeholders, documenting changes.

## 🎯 Quick Reference

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   INPUT LAYER                            │
│  • CSV Stories (wayang_stories.csv)                     │
│  • Raw Indonesian text                                  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              ANNOTATION LAYER                            │
│  • tools/annotate_helper.py                             │
│  • scripts/manual_annotations.py (45 examples)          │
│  • scripts/create_manual_training_data.py               │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│               DATA STORAGE                               │
│  • models/full_data.json (45)                           │
│  • models/train_data.json (36)                          │
│  • models/test_data.json (9)                            │
└───────┬─────────────────────────┬───────────────────────┘
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌────────────────────────────┐
│  NER TRAINING    │    │  KNOWLEDGE GRAPH BUILDING  │
│  ├─ Trainer      │    │  ├─ Load data & model      │
│  ├─ Evaluator    │    │  ├─ Extract entities       │
│  └─ Comparator   │    │  ├─ Extract relations      │
│                  │    │  │   • Regex (42)          │
│                  │    │  │   • Dependency parsing  │
│                  │    │  │   • Co-occurrence       │
│                  │    │  ├─ Build NetworkX graph   │
│                  │    │  └─ Visualize with PyVis   │
└──────┬───────────┘    └────────┬───────────────────┘
       │                         │
       ▼                         ▼
┌────────────────────────────────────────────────────┐
│                OUTPUT LAYER                         │
│  • ner_evaluation_comparison.html                  │
│  • ner_evaluation_comparison.json                  │
│  • knowledge_graph.html                            │
│  • knowledge_graph.json                            │
└────────────────────────────────────────────────────┘
```

### Key Metrics

| Component | Input | Output | Performance |
|-----------|-------|--------|-------------|
| **Annotation** | CSV stories | 45 annotations | Manual labor |
| **NER Training** | 36 examples | Custom model | 23.08% F1 exact |
| **NER Evaluation** | 9 test examples | Metrics report | 94.34% F1 partial |
| **KG Extraction** | 45 annotations | 96 entities | 94 relations |
| **Visualization** | Graph data | Interactive HTML | <1s render |

### Technology Stack

```
Layer              Technology       Purpose
─────────────────────────────────────────────────────────
NLP Core           spaCy 3.x        NER training & parsing
Graph Structure    NetworkX         Graph algorithms
Visualization      PyVis            Interactive HTML
Data Storage       JSON             Serialization
Analysis           Python           Statistics & counting
Orchestration      subprocess       Pipeline coordination
```

### Design Patterns

1. **Pipeline Pattern** (`run_ner_evaluation.py`)
   ```
   Data Prep → Train → Evaluate → Compare → Report
   ```

2. **Builder Pattern** (`KnowledgeGraphBuilder`)
   ```python
   builder.load_from_json()
   builder.extract_relations()
   builder.create_visualization()
   ```

3. **Strategy Pattern** (Relation extraction)
   ```
   Strategy 1: Regex matching
   Strategy 2: Dependency parsing
   Strategy 3: Co-occurrence statistics
   ```

### File Paths Reference

```
docs/
├── ARCHITECTURE.md                 # Main architecture doc
├── architecture.drawio             # Visual diagrams (editable)
├── KNOWLEDGE_GRAPH_RELATIONS.md   # Relation extraction details
├── NER_EVALUATION_SUMMARY.md      # NER results summary
├── NER_EVALUATION_FINAL_RESULTS.md # Detailed NER results
├── NER_EVALUATION.md              # NER methodology
├── NER_EVALUATION_QUICKSTART.md   # Quick start guide
└── HOW_TO_EXPAND_ANNOTATIONS.md   # Adding more data

evaluation/
├── ner_trainer.py                 # Train NER model
├── ner_evaluator.py               # Evaluate model
└── compare_ner_models.py          # Compare two models

scripts/
├── manual_annotations.py          # 45 annotated examples
└── create_manual_training_data.py # Generate train/test split

tools/
└── annotate_helper.py             # Annotation UI

models/
├── full_data.json                 # All annotations
├── train_data.json                # Training set
├── test_data.json                 # Test set
└── custom_ner_model/              # Trained model

output/
├── ner_evaluation_comparison.html # NER comparison report
├── ner_evaluation_comparison.json # NER comparison data
├── knowledge_graph.html           # Interactive graph
└── knowledge_graph.json           # Graph data

Root level:
├── build_knowledge_graph.py       # KG builder (757 lines)
├── run_ner_evaluation.py          # NER pipeline orchestrator
├── requirements.txt               # Dependencies
└── README.md                      # Main documentation
```

## 🔍 How to Navigate

### For Developers
1. Start with **README.md** for overview
2. Read **ARCHITECTURE.md** for system design
3. Open **architecture.drawio** for visual understanding
4. Check specific docs for implementation details

### For Researchers
1. Read **NER_EVALUATION_SUMMARY.md** for results
2. Review **KNOWLEDGE_GRAPH_RELATIONS.md** for extraction methods
3. Check **ARCHITECTURE.md** for methodology
4. View outputs in `output/` directory

### For Stakeholders
1. Review **README.md** for project overview
2. Open **architecture.drawio** diagrams
3. View interactive visualizations in `output/`
4. Check performance metrics in results docs

## 🎨 Diagram Color Coding

### In draw.io diagrams:

| Color | Component Type | Examples |
|-------|---------------|----------|
| 🟢 Green | Input data | CSV files, raw text |
| 🟡 Yellow | Processing | Annotation tools, training |
| 🔵 Blue | Storage | JSON files, databases |
| 🟠 Orange | ML Models | Custom NER model |
| 🔷 Light Blue | Graph | NetworkX structure |
| 🟣 Purple | Output | HTML reports, visualizations |
| ⚪ Gray | Utilities | Helper functions |

## 📊 Complexity Analysis

### Time Complexity

| Operation | Complexity | Factors |
|-----------|-----------|---------|
| NER Training | O(n×m×i) | n=examples, m=tokens, i=iterations |
| Regex Extraction | O(n×p×t) | n=sentences, p=patterns, t=length |
| Dependency Parse | O(n²) | n=tokens per sentence |
| Co-occurrence | O(e²) | e=entities per sentence |
| Graph Render | O(n+e) | n=nodes, e=edges |

### Space Complexity

| Component | Size | Notes |
|-----------|------|-------|
| Custom Model | 50-100 MB | spaCy weights |
| Graph Data | 1-5 MB | NetworkX structure |
| Visualization | ~500 KB | HTML + JS |
| Annotations | ~100 KB | 45 examples |

## 🚀 Scalability Considerations

### Current Scale
- 45 annotations → 96 entities → 94 relations
- Processing time: ~10 seconds total
- Memory usage: ~200 MB

### Projected Scale (500 annotations)
- ~1000 entities → ~1000 relations
- Processing time: ~2-3 minutes
- Memory usage: ~500 MB
- Bottleneck: Co-occurrence (O(e²))

### Solutions
1. Limit entity pairs in co-occurrence
2. Use sampling for large documents
3. Parallelize relation extraction
4. Add caching layer

## 🔧 Customization Guide

### Adding New Components
1. Create module in appropriate directory
2. Update ARCHITECTURE.md with new component
3. Add to architecture.drawio diagram
4. Update README.md if user-facing

### Modifying Diagrams
1. Open architecture.drawio in draw.io
2. Select appropriate tab (System/Data Flow)
3. Edit shapes, connections, labels
4. Export to PNG for README if needed
5. Commit both .drawio and exports

### Documentation Standards
- Use Markdown for text docs
- Use draw.io XML for diagrams
- Include code examples where helpful
- Add tables for structured data
- Use emojis for visual navigation

## 📝 Maintenance

### Regular Updates
- [ ] Update ARCHITECTURE.md when adding features
- [ ] Regenerate diagrams when flow changes
- [ ] Keep README.md metrics current
- [ ] Update complexity analysis with benchmarks
- [ ] Maintain links between documents

### Version Control
- Commit .drawio source files
- Export PNG versions for easy viewing
- Tag architectural changes in commits
- Update "Last Modified" dates

## 📚 Additional Resources

### Internal Documentation
- `docs/NER_EVALUATION.md` - NER methodology
- `docs/KNOWLEDGE_GRAPH_RELATIONS.md` - Extraction methods
- `docs/HOW_TO_EXPAND_ANNOTATIONS.md` - Adding data

### External Resources
- [spaCy Documentation](https://spacy.io/usage/training)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [PyVis Documentation](https://pyvis.readthedocs.io/)
- [draw.io User Guide](https://www.diagrams.net/doc/)

---

**Last Updated**: November 2025  
**Maintained by**: Kelompok 1  
**Version**: 1.0.0
