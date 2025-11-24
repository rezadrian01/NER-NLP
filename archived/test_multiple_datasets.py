"""
Test script for loading and processing multiple datasets
Author: Ahmad Reza Adrian

This script tests the new multi-dataset functionality.
"""

import logging
from pathlib import Path
from config import DATASET_PATHS, DATASET_COLUMNS, OUTPUT_DIR
from preprocessing import load_multiple_datasets, TextPreprocessor

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_load_multiple_datasets():
    """Test loading multiple datasets."""
    logger.info("=" * 60)
    logger.info("TEST: Loading Multiple Datasets")
    logger.info("=" * 60)
    
    try:
        # Load datasets
        df = load_multiple_datasets(
            [str(path) for path in DATASET_PATHS],
            DATASET_COLUMNS
        )
        
        # Display statistics
        logger.info(f"\nDataset Statistics:")
        logger.info(f"  Total records: {len(df)}")
        logger.info(f"  Columns: {list(df.columns)}")
        logger.info(f"\nSource distribution:")
        print(df['source_dataset'].value_counts())
        
        # Show sample data
        logger.info(f"\nSample data (first 3 rows):")
        for idx, row in df.head(3).iterrows():
            logger.info(f"\n  Row {idx}:")
            logger.info(f"    Source: {row['source_dataset']}")
            logger.info(f"    Title: {row['title']}")
            logger.info(f"    Text (first 100 chars): {row['text'][:100]}...")
        
        logger.info("\n✓ Multiple datasets loaded successfully!")
        return df
        
    except Exception as e:
        logger.error(f"✗ Error loading datasets: {e}")
        raise


def test_preprocess_multiple_datasets():
    """Test preprocessing on multiple datasets."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Preprocessing Multiple Datasets")
    logger.info("=" * 60)
    
    try:
        # Load datasets
        df = load_multiple_datasets(
            [str(path) for path in DATASET_PATHS],
            DATASET_COLUMNS
        )
        
        # Preprocess
        preprocessor = TextPreprocessor()
        df = preprocessor.preprocess_dataframe(df, 'text')
        
        # Display results
        logger.info(f"\nPreprocessing results:")
        logger.info(f"  Total sentences: {df['sentence_count'].sum()}")
        logger.info(f"  Average sentences per document: {df['sentence_count'].mean():.2f}")
        
        # Show samples by source
        for source in df['source_dataset'].unique():
            source_df = df[df['source_dataset'] == source]
            logger.info(f"\n  {source}:")
            logger.info(f"    Records: {len(source_df)}")
            logger.info(f"    Total sentences: {source_df['sentence_count'].sum()}")
            logger.info(f"    Avg sentence length: {source_df['normalized_text'].str.len().mean():.0f} chars")
        
        logger.info("\n✓ Preprocessing completed successfully!")
        return df
        
    except Exception as e:
        logger.error(f"✗ Error preprocessing: {e}")
        raise


def test_full_pipeline():
    """Test full pipeline with multiple datasets."""
    logger.info("\n" + "=" * 60)
    logger.info("TEST: Full Pipeline with Multiple Datasets")
    logger.info("=" * 60)
    
    try:
        from pipeline import WayangPipeline
        
        # Create pipeline
        pipeline = WayangPipeline(
            use_multiple_datasets=True,
            output_dir='output',
            ner_model_type='spacy'
        )
        
        # Load data
        df = pipeline.load_data()
        
        # Quick stats
        logger.info(f"\n✓ Pipeline initialized and data loaded!")
        logger.info(f"  Total documents: {len(df)}")
        logger.info(f"  Sources: {df['source_dataset'].unique().tolist()}")
        
        return pipeline
        
    except Exception as e:
        logger.error(f"✗ Error in pipeline: {e}")
        raise


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("MULTIPLE DATASETS TEST SUITE")
    logger.info("=" * 60)
    
    # Test 1: Load datasets
    df = test_load_multiple_datasets()
    
    # Test 2: Preprocess
    df = test_preprocess_multiple_datasets()
    
    # Test 3: Full pipeline
    pipeline = test_full_pipeline()
    
    logger.info("\n" + "=" * 60)
    logger.info("ALL TESTS PASSED! ✓")
    logger.info("=" * 60)
    logger.info("\nYou can now run the full pipeline with:")
    logger.info("  python pipeline.py")


if __name__ == "__main__":
    main()
