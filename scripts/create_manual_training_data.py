"""
Create Training Data from Manual Annotations
This module splits manually annotated data into train/test sets for NER model training.
"""

import json
import random
from pathlib import Path
from typing import List, Tuple, Dict
from manual_annotations import get_manual_annotations, get_annotation_statistics


def split_train_test(annotations: List[Tuple], train_ratio: float = 0.8, seed: int = 42):
    """
    Split annotations into training and test sets.
    
    Args:
        annotations: List of (text, entities) tuples
        train_ratio: Proportion of data for training (default 0.8)
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (train_data, test_data)
    """
    random.seed(seed)
    shuffled = annotations.copy()
    random.shuffle(shuffled)
    
    split_idx = int(len(shuffled) * train_ratio)
    train_data = shuffled[:split_idx]
    test_data = shuffled[split_idx:]
    
    return train_data, test_data


def save_training_data(train_data: List[Tuple], test_data: List[Tuple], output_dir: str = "models"):
    """
    Save training and test data to JSON files.
    
    Args:
        train_data: Training examples
        test_data: Test examples
        output_dir: Directory to save files
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save training data
    train_file = output_path / "train_data.json"
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(train_data)} training examples to {train_file}")
    
    # Save test data
    test_file = output_path / "test_data.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(test_data)} test examples to {test_file}")
    
    # Save full data
    full_file = output_path / "full_data.json"
    full_data = train_data + test_data
    with open(full_file, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(full_data)} total examples to {full_file}")
    
    return train_file, test_file, full_file


def print_statistics(train_data: List[Tuple], test_data: List[Tuple]):
    """Print statistics about the datasets."""
    def count_entities(data):
        entity_counts = {}
        total = 0
        for _, entities_dict in data:
            entities = entities_dict['entities']
            for _, _, label in entities:
                entity_counts[label] = entity_counts.get(label, 0) + 1
                total += 1
        return entity_counts, total
    
    train_counts, train_total = count_entities(train_data)
    test_counts, test_total = count_entities(test_data)
    
    print("\n" + "="*60)
    print("Dataset Statistics")
    print("="*60)
    print(f"\nTraining Set:")
    print(f"  Examples: {len(train_data)}")
    print(f"  Total entities: {train_total}")
    print(f"  Entity distribution:")
    for label, count in sorted(train_counts.items()):
        print(f"    {label}: {count}")
    
    print(f"\nTest Set:")
    print(f"  Examples: {len(test_data)}")
    print(f"  Total entities: {test_total}")
    print(f"  Entity distribution:")
    for label, count in sorted(test_counts.items()):
        print(f"    {label}: {count}")
    
    print(f"\nTotal:")
    print(f"  Examples: {len(train_data) + len(test_data)}")
    print(f"  Total entities: {train_total + test_total}")


def main():
    """Main function to create training data from manual annotations."""
    print("="*60)
    print("Creating Training Data from Manual Annotations")
    print("="*60)
    
    # Get manual annotations
    annotations = get_manual_annotations()
    stats = get_annotation_statistics()
    
    print(f"\nLoaded {stats['total_examples']} manually annotated examples")
    print(f"Total entities: {stats['total_entities']}")
    print(f"Avg entities per example: {stats['avg_entities_per_example']:.2f}")
    
    # Split into train/test
    train_data, test_data = split_train_test(annotations, train_ratio=0.8)
    
    # Save to files
    print("\nSaving datasets...")
    save_training_data(train_data, test_data)
    
    # Print statistics
    print_statistics(train_data, test_data)
    
    print("\n" + "="*60)
    print("✓ Training data created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Train custom model: python ner_trainer.py")
    print("2. Compare models: python compare_ner_models.py")


if __name__ == "__main__":
    main()
