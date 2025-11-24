"""
Text Preprocessing Module for Wayang NER System
Author: Ahmad Reza Adrian

This module handles text cleaning, normalization, and sentence segmentation
for Indonesian wayang narrative texts.
"""

import re
import logging
from typing import List, Dict, Any
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextPreprocessor:
    """
    Preprocessor for Indonesian wayang texts.
    Handles cleaning, normalization, and sentence segmentation.
    """
    
    def __init__(self):
        """Initialize the preprocessor with cleaning patterns."""
        # Patterns for text cleaning
        self.patterns = {
            'extra_whitespace': re.compile(r'\s+'),
            'special_chars': re.compile(r'[^\w\s\.\,\;\:\!\?\-\(\)]'),
            'multiple_periods': re.compile(r'\.{2,}'),
        }
        
    def clean_text(self, text: str) -> str:
        """
        Clean raw text by removing extra whitespace and special characters.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ""
            
        # Remove extra whitespace
        text = self.patterns['extra_whitespace'].sub(' ', text)
        
        # Normalize multiple periods
        text = self.patterns['multiple_periods'].sub('.', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for better processing.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to proper spacing around punctuation
        text = re.sub(r'\s*([.,;:!?])\s*', r'\1 ', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Segment text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence segmentation based on punctuation
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def preprocess(self, text: str) -> Dict[str, Any]:
        """
        Complete preprocessing pipeline.
        
        Args:
            text: Raw input text
            
        Returns:
            Dictionary containing cleaned text and sentences
        """
        # Clean text
        cleaned = self.clean_text(text)
        
        # Normalize
        normalized = self.normalize_text(cleaned)
        
        # Segment sentences
        sentences = self.segment_sentences(normalized)
        
        return {
            'original': text,
            'cleaned': cleaned,
            'normalized': normalized,
            'sentences': sentences,
            'sentence_count': len(sentences)
        }
    
    def preprocess_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Preprocess all texts in a DataFrame.
        
        Args:
            df: Input DataFrame
            text_column: Name of the column containing text
            
        Returns:
            DataFrame with preprocessed columns added
        """
        logger.info(f"Preprocessing {len(df)} documents...")
        
        # Apply preprocessing to each row
        results = df[text_column].apply(lambda x: self.preprocess(x) if pd.notna(x) else {})
        
        # Extract components
        df['cleaned_text'] = results.apply(lambda x: x.get('cleaned', ''))
        df['normalized_text'] = results.apply(lambda x: x.get('normalized', ''))
        df['sentences'] = results.apply(lambda x: x.get('sentences', []))
        df['sentence_count'] = results.apply(lambda x: x.get('sentence_count', 0))
        
        logger.info(f"Preprocessing complete. Total sentences: {df['sentence_count'].sum()}")
        
        return df


def load_dataset(filepath: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Load the wayang dataset from CSV.
    
    Args:
        filepath: Path to CSV file
        encoding: Text encoding (default: utf-8)
        
    Returns:
        DataFrame with loaded data
    """
    logger.info(f"Loading dataset from {filepath}...")
    
    try:
        df = pd.read_csv(filepath, encoding=encoding)
        logger.info(f"Successfully loaded {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise


def load_multiple_datasets(filepaths: list, column_mapping: dict, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Load and merge multiple datasets from CSV files.
    
    Args:
        filepaths: List of paths to CSV files
        column_mapping: Dictionary mapping dataset names to their column configurations
        encoding: Text encoding (default: utf-8)
        
    Returns:
        Merged DataFrame with standardized columns
    """
    from pathlib import Path
    
    logger.info(f"Loading {len(filepaths)} datasets...")
    
    all_dataframes = []
    
    for filepath in filepaths:
        try:
            # Read CSV with proper handling of multi-line quoted fields
            df = pd.read_csv(filepath, encoding=encoding, quoting=1)  # QUOTE_ALL
            filename = Path(filepath).name
            
            # Get column mapping for this dataset
            if filename in column_mapping:
                cols = column_mapping[filename]
                
                # Create standardized dataframe
                standardized_df = pd.DataFrame()
                standardized_df['text'] = df[cols['text']]
                standardized_df['title'] = df[cols['title']] if 'title' in cols else ''
                standardized_df['source_dataset'] = cols['source']
                
                all_dataframes.append(standardized_df)
                logger.info(f"Loaded {len(df)} records from {filename}")
            else:
                logger.warning(f"No column mapping found for {filename}, skipping...")
        
        except Exception as e:
            logger.error(f"Error loading dataset {filepath}: {e}")
            continue
    
    if not all_dataframes:
        raise ValueError("No datasets could be loaded successfully")
    
    # Merge all dataframes
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    logger.info(f"Successfully merged {len(merged_df)} total records from {len(all_dataframes)} datasets")
    
    # Log dataset distribution
    for source in merged_df['source_dataset'].unique():
        count = len(merged_df[merged_df['source_dataset'] == source])
        logger.info(f"  - {source}: {count} records")
    
    return merged_df


def main():
    """
    Main function for testing preprocessing module.
    """
    # Test data
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra. Ia gugur dalam perang Bharatayudha.
    Arjuna merupakan ksatria terkuat di Pandawa.
    """
    
    # Initialize preprocessor
    preprocessor = TextPreprocessor()
    
    # Preprocess sample
    result = preprocessor.preprocess(sample_text)
    
    print("=== Preprocessing Results ===")
    print(f"Original length: {len(result['original'])} chars")
    print(f"Cleaned text: {result['cleaned'][:100]}...")
    print(f"Sentence count: {result['sentence_count']}")
    print(f"Sentences: {result['sentences']}")


if __name__ == "__main__":
    main()
