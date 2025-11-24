"""
Create Training Data for Custom NER Model
Author: Ahmad Reza Adrian

This module extracts entity annotations from the existing dataset
and converts them into spaCy training format.
"""

import pandas as pd
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any
import logging
from config import DATA_DIR, MODELS_DIR, OUTPUT_DIR

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AnnotationExtractor:
    """
    Extract entity annotations from text using rule-based patterns.
    These annotations will be used as ground truth for training.
    """
    
    def __init__(self):
        """Initialize annotation extractor with entity patterns."""
        self.entity_patterns = self._init_patterns()
    
    def _init_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize comprehensive entity patterns for wayang texts.
        
        Returns:
            Dictionary mapping entity types to regex patterns
        """
        return {
            'PERSON': [
                # Titles with names
                r'\b(?:Raden|Dewi|Prabu|Arya|Patih|Pandita|Begawan|Adipati|Emban|Senapati)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                
                # Known characters (comprehensive list)
                r'\bAbimanyu\b', r'\bArjuna\b', r'\bSubadra\b', r'\bSumbadra\b',
                r'\bKresna\b', r'\bKrisna\b', r'\bBaladewa\b', r'\bBaladeva\b',
                r'\bDuryudana\b', r'\bBima\b', r'\bYudistira\b', r'\bYudhishthira\b',
                r'\bNakula\b', r'\bSadewa\b', r'\bSahadewa\b',
                r'\bKunthi\b', r'\bKunti\b', r'\bDrupadi\b', r'\bDraupadi\b',
                r'\bSangkuni\b', r'\bShakuni\b', r'\bKarna\b',
                r'\bDurna\b', r'\bDrona\b', r'\bBisma\b', r'\bBhishma\b',
                r'\bSalya\b', r'\bSrikandi\b', r'\bShikandi\b',
                r'\bGathutkaca\b', r'\bGhatotkaca\b', r'\bAntasena\b',
                r'\bWerkudara\b', r'\bSembadra\b', r'\bSitisundari\b',
                r'\bSitija\b', r'\bLarasati\b', r'\bPregiwa\b', r'\bPragiwaksana\b',
                r'\bLesmana\b', r'\bMandura\b', r'\bManuhara\b',
                r'\bSamba\b', r'\bSatyaki\b', r'\bUtara\b', r'\bUttara\b',
                r'\bWijaya\b', r'\bJanaka\b', r'\bAswatama\b', r'\bAshwatthama\b',
                r'\bJayadrata\b', r'\bBurisrawa\b', r'\bKripasarpa\b',
            ],
            'LOC': [
                # Kingdoms
                r'\b(?:Kerajaan|Negara)\s+[A-Z][a-z]+\b',
                r'\bDwarawati\b', r'\bDwaraka\b', r'\bHastina\b', r'\bHastinapura\b',
                r'\bMandura\b', r'\bAmarta\b', r'\bIndraprastha\b', r'\bIndraprasta\b',
                r'\bAlengka\b', r'\bLanka\b', r'\bMadukara\b', r'\bNgastina\b',
                r'\bWirata\b', r'\bVirata\b', r'\bMatswapati\b', r'\bMatsya\b',
                r'\bAwangga\b', r'\bAnga\b', r'\bSalya\b',
                
                # Palaces and places
                r'\b(?:Istana|Pura|Balai|Pendopo)\s+[A-Z][a-z]+\b',
                r'\b(?:Kahyangan)\s+[A-Z][a-z]+\b',
            ],
            'EVENT': [
                # Wars and battles
                r'\b(?:Perang|Pertempuran)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                r'\bBharatayudha\b', r'\bBharata\s+Yudha\b', r'\bMahabharata\b',
                r'\bBrubuh\b', r'\bKurukshetra\b',
                
                # Events
                r'\b(?:Upacara|Pesta|Pernikahan|Sayembara)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            ],
            'ORG': [
                # Factions
                r'\bPandawa\b', r'\bPandava\b',
                r'\bKurawa\b', r'\bKaurava\b',
                r'\bPunakawan\b',
            ]
        }
    
    def extract_annotations(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Extract entity annotations from text.
        
        Args:
            text: Input text
            
        Returns:
            List of (start, end, label) tuples
        """
        annotations = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    start, end = match.span()
                    annotations.append((start, end, entity_type))
        
        # Remove overlapping annotations (keep longest match)
        annotations = self._remove_overlaps(annotations)
        
        return sorted(annotations, key=lambda x: x[0])
    
    def _remove_overlaps(self, annotations: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        """
        Remove overlapping annotations, keeping longer matches.
        
        Args:
            annotations: List of (start, end, label) tuples
            
        Returns:
            Non-overlapping annotations
        """
        if not annotations:
            return []
        
        # Sort by start position, then by length (descending)
        sorted_annots = sorted(annotations, key=lambda x: (x[0], -(x[1] - x[0])))
        
        result = []
        for annot in sorted_annots:
            start, end, label = annot
            
            # Check if overlaps with any existing annotation
            overlaps = False
            for existing_start, existing_end, _ in result:
                if not (end <= existing_start or start >= existing_end):
                    overlaps = True
                    break
            
            if not overlaps:
                result.append(annot)
        
        return result
    
    def create_spacy_format(self, text: str) -> Tuple[str, Dict[str, List[Tuple[int, int, str]]]]:
        """
        Create spaCy training format from text.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (text, {"entities": [(start, end, label)]})
        """
        annotations = self.extract_annotations(text)
        return (text, {"entities": annotations})
    
    def process_dataset(self, dataset_paths: List[Path], text_column: str = 'text') -> List[Tuple[str, Dict]]:
        """
        Process multiple datasets and create training data.
        
        Args:
            dataset_paths: List of paths to CSV datasets
            text_column: Name of text column
            
        Returns:
            List of training examples in spaCy format
        """
        training_data = []
        
        logger.info(f"Processing {len(dataset_paths)} datasets...")
        
        for dataset_path in dataset_paths:
            logger.info(f"Loading {dataset_path.name}...")
            df = pd.read_csv(dataset_path, quoting=1)
            
            # Handle different column names
            if text_column not in df.columns:
                if 'isi_teks' in df.columns:
                    text_column = 'isi_teks'
                elif 'Text' in df.columns:
                    text_column = 'Text'
                elif 'Content' in df.columns:
                    text_column = 'Content'
                else:
                    logger.warning(f"Could not find text column in {dataset_path.name}")
                    logger.warning(f"Available columns: {list(df.columns)}")
                    continue
            
            for idx, row in df.iterrows():
                text = row[text_column]
                if pd.notna(text) and len(str(text).strip()) > 0:
                    example = self.create_spacy_format(str(text))
                    if example[1]['entities']:  # Only add if entities found
                        training_data.append(example)
                
                if (idx + 1) % 10 == 0:
                    logger.info(f"  Processed {idx + 1}/{len(df)} rows")
        
        logger.info(f"Created {len(training_data)} training examples")
        
        return training_data
    
    def save_training_data(self, training_data: List[Tuple[str, Dict]], output_path: Path):
        """
        Save training data to JSON file.
        
        Args:
            training_data: List of training examples
            output_path: Path to save JSON file
        """
        # Convert to serializable format
        serializable_data = []
        for text, annotations in training_data:
            serializable_data.append({
                'text': text,
                'entities': annotations['entities']
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved training data to {output_path}")
    
    def split_train_test(self, training_data: List[Tuple[str, Dict]], test_size: float = 0.2) -> Tuple[List, List]:
        """
        Split data into training and test sets.
        
        Args:
            training_data: Full dataset
            test_size: Proportion for test set (default 0.2)
            
        Returns:
            Tuple of (train_data, test_data)
        """
        import random
        
        # Shuffle data
        data_copy = training_data.copy()
        random.seed(42)  # For reproducibility
        random.shuffle(data_copy)
        
        # Split
        split_idx = int(len(data_copy) * (1 - test_size))
        train_data = data_copy[:split_idx]
        test_data = data_copy[split_idx:]
        
        logger.info(f"Split: {len(train_data)} train, {len(test_data)} test")
        
        return train_data, test_data


def main():
    """
    Main function to create training data.
    """
    logger.info("="*60)
    logger.info("Creating Training Data for Custom NER Model")
    logger.info("="*60)
    
    # Initialize extractor
    extractor = AnnotationExtractor()
    
    # Define dataset paths
    dataset_paths = [
        DATA_DIR / "wayang_stories_dataset.csv",
        DATA_DIR / "sitija_takon_bapa_dataset.csv"
    ]
    
    # Process datasets
    training_data = extractor.process_dataset(dataset_paths)
    
    # Split into train and test
    train_data, test_data = extractor.split_train_test(training_data, test_size=0.2)
    
    # Save to files
    models_dir = Path(MODELS_DIR)
    models_dir.mkdir(exist_ok=True)
    
    extractor.save_training_data(train_data, models_dir / "train_data.json")
    extractor.save_training_data(test_data, models_dir / "test_data.json")
    extractor.save_training_data(training_data, models_dir / "full_data.json")
    
    # Print statistics
    total_entities = sum(len(example[1]['entities']) for example in training_data)
    entity_types = {}
    for _, annotations in training_data:
        for _, _, label in annotations['entities']:
            entity_types[label] = entity_types.get(label, 0) + 1
    
    logger.info("\n" + "="*60)
    logger.info("Statistics:")
    logger.info(f"  Total examples: {len(training_data)}")
    logger.info(f"  Training examples: {len(train_data)}")
    logger.info(f"  Test examples: {len(test_data)}")
    logger.info(f"  Total entities: {total_entities}")
    logger.info(f"  Avg entities per example: {total_entities/len(training_data):.2f}")
    logger.info("\nEntity distribution:")
    for label, count in sorted(entity_types.items()):
        logger.info(f"  {label}: {count}")
    logger.info("="*60)
    
    logger.info("\n✅ Training data created successfully!")
    logger.info(f"   Files saved in: {models_dir}")


if __name__ == "__main__":
    main()
