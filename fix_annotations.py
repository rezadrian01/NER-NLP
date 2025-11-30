#!/usr/bin/env python3
"""
Automatic Annotation Boundary Fixer

This script automatically fixes boundary errors in manual annotations by:
1. Detecting entities with trailing/leading spaces, punctuation, or mid-word cuts
2. Automatically correcting the boundaries to proper entity spans
3. Generating corrected manual_annotations.py file
"""

import re
from scripts.manual_annotations import MANUAL_ANNOTATIONS

def fix_entity_boundaries(text, entities):
    """
    Fix entity boundary errors automatically.
    
    Args:
        text (str): The source text
        entities (list): List of (start, end, label) tuples
        
    Returns:
        list: Corrected entities
    """
    fixed_entities = []
    
    for start, end, label in entities:
        original_entity = text[start:end]
        
        # Find the actual entity boundaries by expanding/contracting
        fixed_start = start
        fixed_end = end
        
        # Expand backwards if we're in the middle of a word
        while fixed_start > 0 and text[fixed_start-1].isalnum():
            fixed_start -= 1
            
        # Expand forwards if we're in the middle of a word  
        while fixed_end < len(text) and text[fixed_end].isalnum():
            fixed_end += 1
            
        # Get the expanded text
        expanded_text = text[fixed_start:fixed_end]
        
        # Now find the actual entity within this expanded text
        # Remove punctuation and spaces from original entity for matching
        clean_original = re.sub(r'[^\w\s]', '', original_entity).strip()
        
        # Find the best match within expanded text
        words = expanded_text.split()
        best_match = ""
        best_start = fixed_start
        best_end = fixed_start
        
        # Try to find the entity by matching words
        for i in range(len(words)):
            for j in range(i+1, len(words)+1):
                candidate = ' '.join(words[i:j])
                candidate_clean = re.sub(r'[^\w\s]', '', candidate).strip()
                
                # Check if this candidate matches our original entity
                if candidate_clean.lower() == clean_original.lower():
                    # Calculate the position of this candidate in the original text
                    prefix = ' '.join(words[:i])
                    candidate_start = fixed_start + len(prefix) + (1 if prefix else 0)
                    candidate_end = candidate_start + len(candidate)
                    
                    if len(candidate) > len(best_match):
                        best_match = candidate
                        best_start = candidate_start
                        best_end = candidate_end
        
        # If we found a good match, use it
        if best_match and best_match.strip():
            fixed_entities.append((best_start, best_end, label))
            print(f"Fixed: '{original_entity}' -> '{best_match}' [{label}]")
        else:
            # Fallback: just clean up the original boundaries
            clean_text = original_entity.strip(' \t.,!?;:')
            if clean_text:
                # Find where this clean text starts in the original text
                clean_start = text.find(clean_text, start-5, end+5)
                if clean_start != -1:
                    clean_end = clean_start + len(clean_text)
                    fixed_entities.append((clean_start, clean_end, label))
                    print(f"Cleaned: '{original_entity}' -> '{clean_text}' [{label}]")
                else:
                    # Keep original if we can't fix it
                    fixed_entities.append((start, end, label))
                    print(f"Kept: '{original_entity}' [{label}] (couldn't fix)")
            else:
                print(f"Skipped empty entity: '{original_entity}' [{label}]")
    
    return fixed_entities

def main():
    """Fix all annotation boundaries and generate new manual_annotations.py"""
    
    print("="*60)
    print("Fixing Manual Annotation Boundaries")
    print("="*60)
    
    fixed_annotations = []
    total_fixes = 0
    
    for i, (text, entities) in enumerate(MANUAL_ANNOTATIONS):
        print(f"\nProcessing example {i+1}: {text[:50]}...")
        
        # Check if this example needs fixing
        needs_fixing = False
        for start, end, label in entities:
            entity_text = text[start:end]
            if (entity_text != entity_text.strip() or 
                entity_text.endswith('.') or entity_text.endswith(',') or
                (start > 0 and text[start-1].isalnum()) or
                (end < len(text) and text[end].isalnum())):
                needs_fixing = True
                break
        
        if needs_fixing:
            fixed_entities = fix_entity_boundaries(text, entities)
            fixed_annotations.append((text, fixed_entities))
            total_fixes += 1
        else:
            fixed_annotations.append((text, entities))
            print("  No fixes needed")
    
    print(f"\n{'='*60}")
    print(f"Fixed {total_fixes} examples out of {len(MANUAL_ANNOTATIONS)}")
    print(f"{'='*60}")
    
    # Generate the new manual_annotations.py file
    output_lines = [
        '"""',
        'Manual Entity Annotations for Wayang Stories',
        'Author: Kelompok 1',
        '',
        'This module contains manually curated entity annotations for training a high-quality NER model.',
        'Entities are hardcoded with exact character positions for maximum accuracy.',
        '"""',
        '',
        '# Manual annotations: List of (text, entities) tuples',
        '# entities format: [(start_pos, end_pos, label), ...]',
        '',
        'MANUAL_ANNOTATIONS = ['
    ]
    
    for i, (text, entities) in enumerate(fixed_annotations):
        # Add comment for story sections
        if i == 0:
            output_lines.append('    # Story 1: Abimanyu Rabi')
        elif i == 5:
            output_lines.append('    # Story 2: Sitija Takon Bapa')
        elif i == 29:
            output_lines.append('    # Additional training examples with common patterns')
        
        output_lines.append('    (')
        output_lines.append(f'        "{text}",')
        output_lines.append(f'        {entities}')
        output_lines.append('    ),')
    
    output_lines.extend([
        ']',
        '',
        '',
        'def get_manual_annotations():',
        '    """',
        '    Get manually curated annotations.',
        '    ',
        '    Returns:',
        '        List of (text, {\'entities\': [(start, end, label)]}) tuples',
        '    """',
        '    formatted_annotations = []',
        '    for text, entities in MANUAL_ANNOTATIONS:',
        '        formatted_annotations.append((text, {\'entities\': entities}))',
        '    return formatted_annotations',
        '',
        '',
        'def get_annotation_statistics():',
        '    """',
        '    Get statistics about the manual annotations.',
        '    ',
        '    Returns:',
        '        Dictionary with statistics',
        '    """',
        '    total_examples = len(MANUAL_ANNOTATIONS)',
        '    total_entities = sum(len(entities) for _, entities in MANUAL_ANNOTATIONS)',
        '    ',
        '    entity_counts = {}',
        '    for _, entities in MANUAL_ANNOTATIONS:',
        '        for _, _, label in entities:',
        '            entity_counts[label] = entity_counts.get(label, 0) + 1',
        '    ',
        '    return {',
        '        \'total_examples\': total_examples,',
        '        \'total_entities\': total_entities,',
        '        \'avg_entities_per_example\': total_entities / total_examples if total_examples > 0 else 0,',
        '        \'entity_distribution\': entity_counts',
        '    }',
        '',
        '',
        'if __name__ == "__main__":',
        '    stats = get_annotation_statistics()',
        '    print("="*60)',
        '    print("Manual Annotations Statistics")',
        '    print("="*60)',
        '    print(f"Total examples: {stats[\'total_examples\']}")',
        '    print(f"Total entities: {stats[\'total_entities\']}")',
        '    print(f"Avg entities per example: {stats[\'avg_entities_per_example\']:.2f}")',
        '    print("\\nEntity distribution:")',
        '    for label, count in sorted(stats[\'entity_distribution\'].items()):',
        '        print(f"  {label}: {count}")',
        ''
    ])
    
    # Write the fixed annotations
    with open('scripts/manual_annotations_fixed.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\n✅ Fixed annotations saved to: scripts/manual_annotations_fixed.py")
    print(f"📝 Total examples: {len(fixed_annotations)}")
    print(f"🔧 Examples fixed: {total_fixes}")
    
    return fixed_annotations

if __name__ == "__main__":
    main()