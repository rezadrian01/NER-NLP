# How to Expand Manual Annotations

This guide shows you how to add more manual annotations to improve the NER model performance.

## Current Status

- **Current Examples:** 45 sentences
- **Training Set:** 36 examples
- **Test Set:** 9 examples
- **Custom Model F1:** 0.2308 (Exact), 0.9434 (Partial)

## Goal

- **Target Examples:** 200+ sentences
- **Expected F1:** 0.70+ (Exact), 0.95+ (Partial)

## How to Add Annotations

### Step 1: Open the Annotation File

```bash
nano manual_annotations.py
# or use your favorite editor
```

### Step 2: Add New Annotations

Add new tuples to the `MANUAL_ANNOTATIONS` list following this format:

```python
(
    "Your sentence text here.",
    [(start_pos, end_pos, 'LABEL'), ...]
),
```

### Step 3: Find Character Positions

Use Python to find exact character positions:

```python
text = "Prabu Kresna memerintah di Kerajaan Dwarawati."
entity = "Prabu Kresna"
start = text.find(entity)
end = start + len(entity)
print(f"({start}, {end}, 'PERSON')")  # Output: (0, 12, 'PERSON')
```

### Step 4: Example Annotation

**Original Text:**
```
Raden Werkudara mengalahkan Prabu Duryudana dalam Perang Bharatayudha.
```

**Find Positions:**
```python
text = "Raden Werkudara mengalahkan Prabu Duryudana dalam Perang Bharatayudha."

# Find each entity
entities = [
    "Raden Werkudara",  # Character
    "Prabu Duryudana",  # Character
    "Perang Bharatayudha"  # Event
]

for entity in entities:
    start = text.find(entity)
    end = start + len(entity)
    print(f'({start}, {end}, \'LABEL\'),  # {entity}')

# Output:
# (0, 16, 'PERSON'),  # Raden Werkudara
# (29, 45, 'PERSON'),  # Prabu Duryudana
# (52, 72, 'EVENT'),  # Perang Bharatayudha
```

**Add to `manual_annotations.py`:**
```python
(
    "Raden Werkudara mengalahkan Prabu Duryudana dalam Perang Bharatayudha.",
    [(0, 16, 'PERSON'), (29, 45, 'PERSON'), (52, 72, 'EVENT')]
),
```

## Entity Labels

Use these labels consistently:

1. **PERSON** - Character names
   - Examples: Raden Arjuna, Prabu Kresna, Dewi Srikandi
   
2. **LOC** - Locations
   - Examples: Kerajaan Dwarawati, Kahyangan Suralaya, Gunung Jamurdipa
   
3. **ORG** - Organizations/Groups
   - Examples: Pandawa, Kurawa
   
4. **EVENT** - Named events
   - Examples: Perang Bharatayudha, Pertempuran Brubuh

## Quick Annotation Script

Save this as `annotate_helper.py`:

```python
#!/usr/bin/env python3
"""Helper script to find entity positions"""

def find_entities(text, entities):
    """Find character positions for entities in text"""
    annotations = []
    for entity, label in entities:
        start = text.find(entity)
        if start == -1:
            print(f"⚠️  Entity not found: {entity}")
            continue
        end = start + len(entity)
        annotations.append((start, end, label))
        print(f"({start}, {end}, '{label}'),  # {entity}")
    
    print("\n# Full annotation:")
    print(f'("{text}",')
    print(f"    {annotations}")
    print("),")

# Example usage
if __name__ == "__main__":
    text = "Raden Werkudara mengalahkan Prabu Duryudana dalam Perang Bharatayudha."
    entities = [
        ("Raden Werkudara", "PERSON"),
        ("Prabu Duryudana", "PERSON"),
        ("Perang Bharatayudha", "EVENT")
    ]
    find_entities(text, entities)
```

**Usage:**
```bash
python annotate_helper.py
```

## Annotation Tips

### 1. Extract Sentences from Stories

```python
# Read the story
with open('data/wayang_stories.csv', 'r') as f:
    df = pd.read_csv(f)

story_text = df.iloc[0]['isi_teks']

# Split into sentences
import re
sentences = re.split(r'[.!?]+', story_text)

# Annotate each sentence
for sentence in sentences[:10]:  # First 10 sentences
    sentence = sentence.strip()
    if len(sentence) > 20:  # Skip very short sentences
        print(f"\nSentence: {sentence}")
        # Manually identify entities and use annotate_helper.py
```

### 2. Focus on Diverse Examples

- Mix of PERSON, LOC, ORG, EVENT
- Short and long sentences
- Single and multiple entities
- Different story contexts

### 3. Verify Positions

Always verify your annotations work:

```python
text = "Raden Arjuna berperang melawan Kurawa."
entities = [(0, 12, 'PERSON'), (31, 37, 'ORG')]

# Verify
for start, end, label in entities:
    print(f"{text[start:end]} -> {label}")

# Output:
# Raden Arjuna -> PERSON
# Kurawa -> ORG
```

## Re-train After Adding Annotations

1. **Update annotations** in `manual_annotations.py`
2. **Regenerate training data:**
   ```bash
   python create_manual_training_data.py
   ```

3. **Train the model:**
   ```bash
   python ner_trainer.py
   ```

4. **Compare performance:**
   ```bash
   python compare_ner_models.py
   ```

5. **View report:**
   ```bash
   xdg-open output/ner_evaluation_comparison.html
   ```

## Example: Adding 10 New Annotations

```python
# Add these to MANUAL_ANNOTATIONS list in manual_annotations.py

(
    "Raden Werkudara adalah ksatria terkuat Pandawa.",
    [(0, 16, 'PERSON'), (39, 46, 'ORG')]
),
(
    "Dewi Srikandi memanah pasukan Kurawa dari Kerajaan Mandraka.",
    [(0, 15, 'PERSON'), (31, 37, 'ORG'), (43, 61, 'LOC')]
),
(
    "Prabu Salya memimpin pasukan dari Kerajaan Mandraka.",
    [(0, 11, 'PERSON'), (34, 52, 'LOC')]
),
(
    "Raden Karna adalah anak Prabu Kunthi yang dibuang ke sungai.",
    [(0, 11, 'PERSON'), (24, 36, 'PERSON')]
),
(
    "Begawan Durna mengajarkan ilmu perang kepada Pandawa dan Kurawa.",
    [(0, 13, 'PERSON'), (46, 53, 'ORG'), (58, 64, 'ORG')]
),
(
    "Prabu Pandu adalah ayah para Pandawa yang meninggal di hutan.",
    [(0, 11, 'PERSON'), (29, 36, 'ORG')]
),
(
    "Dewi Drupadi menjadi istri kelima Pandawa bersaudara.",
    [(0, 13, 'PERSON'), (35, 42, 'ORG')]
),
(
    "Prabu Baladewa adalah kakak Prabu Kresna dari Dwarawati.",
    [(0, 14, 'PERSON'), (28, 40, 'PERSON'), (46, 56, 'LOC')]
),
(
    "Raden Janaka adalah putra Raden Kresna dan Dewi Rukmini.",
    [(0, 12, 'PERSON'), (26, 38, 'PERSON'), (43, 56, 'PERSON')]
),
(
    "Kerajaan Hastina dikuasai oleh Kurawa sebelum Perang Bharatayudha.",
    [(0, 16, 'LOC'), (31, 37, 'ORG'), (47, 67, 'EVENT')]
),
```

## Tracking Progress

Check statistics after adding annotations:

```bash
python manual_annotations.py
```

Output will show:
```
============================================================
Manual Annotations Statistics
============================================================
Total examples: 55
Total entities: 147
Avg entities per example: 2.67

Entity distribution:
  EVENT: 4
  LOC: 24
  ORG: 17
  PERSON: 102
```

## Quality Checklist

✅ Entity positions are exact (no off-by-one errors)  
✅ Labels are consistent (PERSON not PER)  
✅ Text has proper punctuation  
✅ All entities in sentence are annotated  
✅ No overlapping entities  
✅ Text matches original source  

## Target Milestones

- [ ] 100 examples (Current: 45)
- [ ] 150 examples
- [ ] 200 examples
- [ ] 300 examples (Production-ready)

Track your progress and re-evaluate the model after each milestone!

---

**Good luck annotating! 🎯**
