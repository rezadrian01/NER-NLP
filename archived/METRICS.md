# Pipeline Metrics Documentation

## Overview

The Wayang NER pipeline now includes comprehensive metrics collection and reporting. Every pipeline run automatically generates detailed performance metrics in both JSON and HTML formats.

## Generated Files

After running the pipeline, you'll find these metrics files in the `output/` directory:

1. **`pipeline_metrics.json`** - Complete metrics data in JSON format
2. **`pipeline_metrics.html`** - Interactive HTML dashboard with visualizations

## Metrics Sections

### 1. Pipeline Info
- Start and end timestamps
- Total execution duration
- Configuration settings (NER model, dataset mode, visualization settings)

### 2. Data Loading
- Total documents loaded
- Column structure
- Source distribution (per dataset)
- Memory usage (MB)

### 3. Preprocessing
- Total sentences extracted
- Average sentences per document
- Text length statistics (min, max, avg, total)
- Source-specific statistics

### 4. NER Extraction
- **Total entities extracted**
- **Unique entities**
- **Average entities per document**
- Entity type distribution (PERSON, LOC, ORG, EVENT, etc.)
- Entity extraction method distribution (rule-based, spacy, transformer)
- Top 20 most frequent entities
- Documents with/without entities
- Source-specific statistics

### 5. Relation Extraction
- **Total relations extracted**
- **Average relations per document**
- **Average confidence score**
- Relation type distribution (child_of, married_to, fought_with, etc.)
- Relations with dynamic labels (count and percentage)
- Top 10 relation patterns
- Top entity type pairs
- Source-specific statistics

### 6. Knowledge Graph
- **Total nodes**
- **Total edges**
- **Graph density**
- **Average degree**
- Entity and relation type distributions
- Average clustering coefficient
- Number of connected components
- Largest component size
- Top 10 central nodes (by degree centrality)
- Top entities by degree

### 7. Visualization
- Output file path and size
- Nodes and edges visualized
- Visualization type

### 8. Execution Time
- **Total execution time** (seconds and minutes)
- **Stage-by-stage breakdown**:
  - Data loading
  - Preprocessing
  - NER extraction
  - Relation extraction
  - Knowledge graph construction
  - Visualization
- Percentage of time spent per stage

### 9. Summary
Quick overview with key statistics:
- Pipeline status
- Total documents processed
- Total entities and unique entities
- Total relations
- Knowledge graph size (nodes and edges)
- Average processing time per document

## Sample Metrics Output

```json
{
  "summary": {
    "pipeline_status": "completed",
    "total_documents_processed": 2,
    "total_entities_extracted": 1026,
    "unique_entities": 633,
    "total_relations_extracted": 3416,
    "knowledge_graph_nodes": 641,
    "knowledge_graph_edges": 3354,
    "total_execution_time_minutes": 3.19,
    "avg_processing_time_per_doc_seconds": 95.75
  },
  "ner_extraction": {
    "entity_type_distribution": {
      "PERSON": 881,
      "LOC": 101,
      "ORG": 26,
      "OTHER": 14,
      "EVENT": 4
    },
    "top_20_entities": [
      {"entity": "Raden Abimanyu", "count": 45},
      {"entity": "Prabu Kresna", "count": 38},
      ...
    ]
  },
  "knowledge_graph": {
    "density": 0.0082,
    "avg_degree": 10.46,
    "avg_clustering_coefficient": 0.34
  }
}
```

## Usage

### Automatic Collection (Default)

Metrics are automatically collected when you run the pipeline:

```bash
python pipeline.py
```

### Programmatic Access

```python
from pipeline import WayangPipeline
from metrics import generate_metrics_report
import json

# Run pipeline with metrics
pipeline = WayangPipeline()
pipeline.run_full_pipeline()

# Access metrics programmatically
with open('output/pipeline_metrics.json') as f:
    metrics = json.load(f)

# Get specific metrics
total_entities = metrics['summary']['total_entities_extracted']
entity_types = metrics['ner_extraction']['entity_type_distribution']
graph_density = metrics['knowledge_graph']['density']

print(f"Extracted {total_entities} entities")
print(f"Graph density: {graph_density:.4f}")
```

### Custom Metrics Analysis

```python
from metrics import MetricsCollector

# Create custom collector
metrics = MetricsCollector()

# Start tracking
metrics.start_pipeline({'custom': 'config'})

# Record stages manually
metrics.record_data_loading(dataframe)
metrics.record_ner_extraction(dataframe_with_entities)
# ... etc

# Finalize
metrics.finalize_metrics()
metrics.print_summary()
metrics.save_metrics('custom_metrics.json')
```

### Generate HTML Report

```python
from metrics import generate_metrics_report

# Generate report from JSON
generate_metrics_report(
    'output/pipeline_metrics.json',
    'output/custom_report.html'
)
```

## HTML Dashboard Features

The HTML report (`pipeline_metrics.html`) includes:

✨ **Visual Summary Cards**
- Status badge
- Execution time
- Documents processed
- Entities extracted

📊 **Detailed Tables**
- Entity type distribution with percentages
- Relation type distribution with percentages
- Top entities by frequency
- Execution time breakdown

📈 **Knowledge Graph Metrics**
- Network statistics (nodes, edges, density)
- Centrality measures
- Clustering coefficients
- Component analysis

⏱️ **Performance Analysis**
- Stage execution times
- Percentage breakdown
- Performance bottleneck identification

## Interpreting Metrics

### NER Performance
- **High unique entities / total entities ratio** → Good entity diversity
- **Low entities per document** → May need tuning or better patterns
- **Unbalanced entity types** → Check if specific types are under-represented

### Relation Extraction
- **Low confidence scores** → Review relation patterns
- **High associated_with relations** → May need more specific patterns
- **Few dynamic labels** → Check dynamic labeler configuration

### Knowledge Graph
- **Low density (0.001-0.01)** → Typical for large sparse graphs
- **High clustering coefficient** → Strong local communities
- **Multiple components** → Disconnected subgraphs exist
- **High average degree** → Entities are well-connected

### Performance
- **Slow relation extraction** → Most computationally intensive stage
- **Long NER extraction** → Consider faster model or caching
- **High memory usage** → Process in batches for large datasets

## Best Practices

1. **Save metrics for each run** - Use timestamps in filenames
2. **Compare metrics across experiments** - Track improvements
3. **Monitor execution time** - Identify bottlenecks
4. **Check entity coverage** - Ensure all entity types are extracted
5. **Validate relation quality** - Review confidence scores
6. **Analyze graph structure** - Check connectivity and density

## Example Analysis Workflow

```python
import json
import pandas as pd

# Load multiple metric files
runs = []
for file in ['run1.json', 'run2.json', 'run3.json']:
    with open(file) as f:
        runs.append(json.load(f))

# Compare performance
comparison = pd.DataFrame([
    {
        'run': i+1,
        'entities': r['summary']['total_entities_extracted'],
        'relations': r['summary']['total_relations_extracted'],
        'time': r['summary']['total_execution_time_minutes']
    }
    for i, r in enumerate(runs)
])

print(comparison)
```

## Troubleshooting

**Q: Metrics file not generated**  
A: Ensure pipeline completed successfully without errors

**Q: Missing metrics sections**  
A: Some stages may have been skipped or failed

**Q: Execution times show 0.0%**  
A: Very fast execution; times rounded to 0

**Q: High memory usage reported**  
A: Consider processing in batches or reducing dataset size

## Integration with External Tools

### Export to CSV

```python
import json
import pandas as pd

with open('output/pipeline_metrics.json') as f:
    metrics = json.load(f)

# Convert entity distribution to CSV
entity_dist = pd.DataFrame([
    {'entity_type': k, 'count': v}
    for k, v in metrics['ner_extraction']['entity_type_distribution'].items()
])
entity_dist.to_csv('entity_distribution.csv', index=False)
```

### Dashboard Integration

The JSON metrics can be easily integrated into:
- Grafana dashboards
- Jupyter notebooks
- Web analytics platforms
- CI/CD pipelines for automated quality checks

---

**For more information, see the main README.md or run:**
```bash
python test_metrics.py
```
