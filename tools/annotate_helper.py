#!/usr/bin/env python3
"""
Annotation Helper Script
Helps you find exact character positions for entity annotations
"""

def find_entities(text, entities):
    """
    Find character positions for entities in text.
    
    Args:
        text: The sentence text
        entities: List of (entity_text, label) tuples
    
    Returns:
        List of (start, end, label) tuples
    """
    annotations = []
    print(f"\n{'='*60}")
    print(f"Text: {text}")
    print(f"{'='*60}\n")
    
    for entity, label in entities:
        start = text.find(entity)
        if start == -1:
            print(f"⚠️  Entity not found: '{entity}'")
            print(f"    Make sure the text exactly matches!")
            continue
        end = start + len(entity)
        annotations.append((start, end, label))
        print(f"✓ ({start}, {end}, '{label}'),  # {entity}")
    
    print(f"\n{'='*60}")
    print("# Full annotation for manual_annotations.py:")
    print(f"{'='*60}")
    print(f'(')
    print(f'    "{text}",')
    print(f'    {annotations}')
    print(f'),')
    print(f"{'='*60}\n")
    
    return annotations


def interactive_annotate():
    """Interactive annotation mode"""
    print("="*60)
    print("Interactive Annotation Helper")
    print("="*60)
    print("\nInstructions:")
    print("1. Enter your sentence")
    print("2. Enter entities one by one (entity text, label)")
    print("3. Type 'done' when finished")
    print("4. Copy the output to manual_annotations.py")
    print()
    
    text = input("Enter sentence: ").strip()
    
    entities = []
    print("\nNow enter entities (format: entity_text, LABEL)")
    print("Example: Raden Arjuna, PERSON")
    print("Type 'done' when finished\n")
    
    while True:
        entity_input = input("Entity: ").strip()
        if entity_input.lower() == 'done':
            break
        
        if ',' not in entity_input:
            print("❌ Invalid format. Use: entity_text, LABEL")
            continue
        
        entity_text, label = entity_input.rsplit(',', 1)
        entity_text = entity_text.strip()
        label = label.strip().upper()
        
        if label not in ['PERSON', 'LOC', 'ORG', 'EVENT']:
            print(f"⚠️  Warning: '{label}' is not a standard label")
            print("   Standard labels: PERSON, LOC, ORG, EVENT")
            confirm = input("   Continue anyway? (y/n): ")
            if confirm.lower() != 'y':
                continue
        
        entities.append((entity_text, label))
    
    if entities:
        find_entities(text, entities)
    else:
        print("\n❌ No entities added!")


def batch_annotate_examples():
    """Batch annotate multiple examples"""
    print("="*60)
    print("Batch Annotation Examples")
    print("="*60)
    
    # Example 1
    text1 = "Raden Werkudara mengalahkan Prabu Duryudana dalam Perang Bharatayudha."
    entities1 = [
        ("Raden Werkudara", "PERSON"),
        ("Prabu Duryudana", "PERSON"),
        ("Perang Bharatayudha", "EVENT")
    ]
    find_entities(text1, entities1)
    
    # Example 2
    text2 = "Dewi Srikandi memanah pasukan Kurawa dari Kerajaan Mandraka."
    entities2 = [
        ("Dewi Srikandi", "PERSON"),
        ("Kurawa", "ORG"),
        ("Kerajaan Mandraka", "LOC")
    ]
    find_entities(text2, entities2)
    
    # Example 3
    text3 = "Prabu Salya memimpin pasukan dari Kerajaan Mandraka."
    entities3 = [
        ("Prabu Salya", "PERSON"),
        ("Kerajaan Mandraka", "LOC")
    ]
    find_entities(text3, entities3)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--batch':
        # Run batch examples
        batch_annotate_examples()
    else:
        # Run interactive mode
        try:
            interactive_annotate()
        except KeyboardInterrupt:
            print("\n\n👋 Bye!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
