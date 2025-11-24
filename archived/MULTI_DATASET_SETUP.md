# Multi-Dataset Setup Documentation

## Overview

The project has been updated to support multiple wayang story datasets. The system now automatically loads and merges data from different sources.

## Changes Made

### 1. Data Organization
- **Moved** `wayang.csv` → `data/wayang_stories_dataset.csv`
- **Added** `data/sitija_takon_bapa_dataset.csv` 
- Both datasets are now in the `data/` folder for better organization

### 2. Updated Files

#### `config.py`
- Added `DATASET_PATHS` list for multiple datasets
- Added `DATASET_COLUMNS` mapping for different column structures
- Each dataset can have different column names (e.g., "isi_teks" vs "Content")

#### `preprocessing.py`
- Added `load_multiple_datasets()` function
- Automatically standardizes column names across datasets
- Merges datasets with `source_dataset` tracking

#### `pipeline.py`
- Added `use_multiple_datasets` parameter (default: True)
- Supports both multiple and single dataset modes
- Command-line options for `--datasets` and `--single-dataset`

### 3. Dataset Structure

#### wayang_stories_dataset.csv
- **Columns**: `judul`, `tgl_posting`, `pengarang`, `ringkasan`, `isi_teks`, etc.
- **Text column**: `isi_teks`
- **Source**: wayang_stories

#### sitija_takon_bapa_dataset.csv
- **Columns**: `Title`, `Content`
- **Text column**: `Content`
- **Source**: sitija_takon_bapa

Both are automatically merged into standardized columns:
- `text` - Main story text
- `title` - Story title
- `source_dataset` - Origin dataset identifier

## Usage

### Default (Multiple Datasets)
```bash
# Automatically loads both datasets
python pipeline.py
```

### Single Dataset Mode
```bash
# Use only one dataset
python pipeline.py --single-dataset --dataset data/wayang_stories_dataset.csv
```

### Custom Multiple Datasets
```bash
# Specify custom dataset paths
python pipeline.py --datasets data/dataset1.csv data/dataset2.csv
```

### Programmatic Usage
```python
from pipeline import WayangPipeline

# Use multiple datasets (default)
pipeline = WayangPipeline(
    use_multiple_datasets=True,
    output_dir='output',
    ner_model_type='spacy'
)

# Use single dataset
pipeline = WayangPipeline(
    dataset_path='data/wayang_stories_dataset.csv',
    use_multiple_datasets=False
)

pipeline.run_full_pipeline()
```

## Testing

Run the test suite to verify multi-dataset functionality:

```bash
python test_multiple_datasets.py
```

This will:
1. Load both datasets
2. Verify column standardization
3. Test preprocessing
4. Initialize the full pipeline

## Adding New Datasets

To add a new dataset:

1. **Place CSV in `data/` folder**
2. **Update `config.py`**:
   ```python
   DATASET_PATHS = [
       DATA_DIR / "wayang_stories_dataset.csv",
       DATA_DIR / "sitija_takon_bapa_dataset.csv",
       DATA_DIR / "your_new_dataset.csv"  # Add here
   ]
   
   DATASET_COLUMNS = {
       # ... existing mappings ...
       "your_new_dataset.csv": {
           "text": "content_column_name",
           "title": "title_column_name",
           "source": "your_dataset_name"
       }
   }
   ```
3. **Run pipeline** - New dataset will be automatically included

## Benefits

✅ **Unified processing** - All datasets processed with same NER and relation extraction  
✅ **Source tracking** - Each entity/relation tagged with source dataset  
✅ **Flexible** - Easy to add/remove datasets  
✅ **Backward compatible** - Single dataset mode still works  
✅ **Better organization** - All data files in `data/` folder  

## Output

The merged knowledge graph will contain:
- Entities from all datasets
- Relations from all datasets
- `source_dataset` metadata for tracing back to origin

Example statistics output:
```
Loading 2 datasets...
Loaded 1 records from wayang_stories_dataset.csv
Loaded 1 records from sitija_takon_bapa_dataset.csv
Successfully merged 2 total records from 2 datasets
  - wayang_stories: 1 records
  - sitija_takon_bapa: 1 records
```

## Notes

- The original CSV files contain long narrative texts as single records
- Each "row" is a complete story document
- Multi-line field values are properly handled with CSV quoting
- Column names are automatically standardized during loading
