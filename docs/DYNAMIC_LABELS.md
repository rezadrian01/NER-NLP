# Dynamic Relation Labeling System

## Overview

The system now generates **dynamic, context-based relation labels** instead of static labels. Instead of showing generic labels like "child_of" or "associated_with", the system extracts meaningful verbs and nouns from the actual text context.

## How It Works

### Multi-Strategy Approach

The `DynamicRelationLabeler` uses 5 strategies in order of priority:

#### 1. **Verb-Based Extraction** (Highest Priority)
Extracts action verbs between entities:
- `membunuh` (kill)
- `menikah` (marry)
- `memerintah` (rule)
- `bertempur` (fight)
- `melawan` (oppose)
- And 50+ more Indonesian action verbs

**Example:**
```
Context: "Bima membunuh Dursasana dalam pertempuran"
Label: "membunuh" (instead of static "killed")
```

#### 2. **Noun-Based Relationships**
Identifies relationship nouns:
- `putra/putri` (son/daughter)
- `murid` (student)
- `raja` (king)
- `guru` (teacher)
- `musuh` (enemy)
- And 50+ more relationship terms

**Example:**
```
Context: "Srikandi adalah murid Arjuna"
Label: "murid of" (student of)
```

#### 3. **Dependency Parsing** (When spaCy Available)
Uses linguistic structure to find connections:
- Analyzes syntax trees
- Finds connecting verbs
- Determines relationships from grammar

#### 4. **Preposition Analysis**
Extracts preposition-based relations:
- `di` (at/in)
- `dengan` (with)
- `oleh` (by)
- `untuk` (for)
- `melawan` (against)

#### 5. **TF-IDF Context Words**
Uses statistical importance:
- Finds distinctive words in context
- Weights by term frequency
- Identifies most meaningful terms

## Results

### Before (Static Labels)
```
Abimanyu → Arjuna: "child of"
Arjuna → Subadra: "married to"
Bima → Dursasana: "killed"
```

### After (Dynamic Labels)
```
Abimanyu → Arjuna: "putra" (son)
Arjuna → Subadra: "menikah" (marry)
Bima → Dursasana: "membunuh" (kill)
Prabu Kresna → Dwarawati: "memerintah" (rule)
Srikandi → Arjuna: "murid of" (student of)
```

## Technical Implementation

### Key Components

1. **dynamic_relation_labeler.py** - New module with labeling logic
2. **relation_extraction.py** - Updated to generate dynamic labels
3. **graph_builder.py** - Stores dynamic labels in graph edges
4. **visualization.py** - Displays dynamic labels in visualizations

### Integration Points

```python
# In relation_extraction.py
def __init__(self, use_dynamic_labels: bool = True):
    self.dynamic_labeler = DynamicRelationLabeler()

# When extracting relations
dynamic_label = self.dynamic_labeler.extract_relation_label(
    subject, object, context, relation_type
)
```

### Data Flow

```
Text Context
    ↓
Relation Extraction (pattern matching)
    ↓
Dynamic Labeler (NLP analysis)
    ↓
Knowledge Graph (stores both static + dynamic)
    ↓
Visualization (displays dynamic labels)
```

## Features

### ✅ Language-Aware
- Designed for Indonesian language
- Handles Indonesian verb prefixes (me-, ber-, ter-, di-, pe-)
- Understands wayang story terminology

### ✅ Context-Sensitive
- Same entities can have different labels in different contexts
- Adapts to actual text usage
- Preserves semantic meaning

### ✅ Fallback System
- If dynamic label can't be determined, uses static label
- Never fails silently
- Always provides meaningful output

### ✅ Caching
- Caches generated labels for performance
- Reuses labels for identical contexts
- Efficient for large datasets

## Testing

Run the test to see dynamic labeling in action:

```bash
python test_dynamic_relation_labels.py
```

This will:
1. Test 10 different relation types
2. Show static vs dynamic labels
3. Generate visualization with dynamic labels
4. Display statistics

## Configuration

### Enable/Disable Dynamic Labels

In `relation_extraction.py`:
```python
# Enable (default)
extractor = RelationExtractor(use_dynamic_labels=True)

# Disable (use static labels only)
extractor = RelationExtractor(use_dynamic_labels=False)
```

### Customize Verb/Noun Lists

Edit `dynamic_relation_labeler.py`:
```python
self.action_verbs = {
    'your_custom_verb',
    # Add more verbs
}

self.relationship_nouns = {
    'your_custom_noun',
    # Add more nouns
}
```

## Examples from Test

| Context | Static Label | Dynamic Label |
|---------|-------------|---------------|
| "Abimanyu adalah putra Arjuna" | child_of | putra of |
| "Arjuna menikah dengan Subadra" | married_to | menikah |
| "Bima membunuh Dursasana" | killed | membunuh |
| "Prabu Kresna memerintah di Dwarawati" | ruled_in | memerintah |
| "Gatotkaca bertempur melawan Abimanyu" | fought_with | bertempur |
| "Srikandi adalah murid Arjuna" | student_of | murid of |

## Statistics

From test run:
- **10 unique dynamic labels** generated
- **100% coverage** (all relations got dynamic labels)
- **Context-specific** labels for each relation
- **Indonesian language** preserved in labels

## Benefits

1. **More Meaningful**: Labels reflect actual text content
2. **Language Preservation**: Shows Indonesian terms naturally
3. **Context-Aware**: Different contexts = different labels
4. **Flexibility**: Multiple strategies ensure coverage
5. **Maintainability**: Easy to add new verbs/nouns

## Future Enhancements

Possible improvements:
- Add more Indonesian verbs/nouns
- Train ML model for label prediction
- Support multi-word phrases
- Add sentiment to labels
- Handle negation (tidak, bukan)

## API Reference

### DynamicRelationLabeler

```python
labeler = DynamicRelationLabeler()

# Extract label for single relation
label = labeler.extract_relation_label(
    subject='Abimanyu',
    object_entity='Arjuna',
    context='Abimanyu adalah putra Arjuna',
    relation_type='child_of'  # Optional hint
)

# Batch process multiple relations
labeled_relations = labeler.batch_label_relations(relations)

# Get statistics
stats = labeler.get_statistics()
```

## Conclusion

The dynamic relation labeling system makes the knowledge graph **more intuitive and meaningful** by using actual text content to describe relationships. This is especially valuable for Indonesian wayang stories where preserving the original language and cultural context is important.
