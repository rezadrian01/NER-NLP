"""
Test Metrics Collection
Author: Ahmad Reza Adrian

This script tests the metrics collection functionality.
"""

import logging
from pathlib import Path
from pipeline import WayangPipeline
from metrics import generate_metrics_report

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_metrics_collection():
    """Test the complete pipeline with metrics collection."""
    logger.info("=" * 60)
    logger.info("TESTING METRICS COLLECTION")
    logger.info("=" * 60)
    
    try:
        # Create pipeline
        pipeline = WayangPipeline(
            use_multiple_datasets=True,
            output_dir='output',
            ner_model_type='spacy'
        )
        
        # Run full pipeline with metrics
        pipeline.run_full_pipeline(max_vis_nodes=100, light_mode=True)
        
        logger.info("\n" + "=" * 60)
        logger.info("METRICS TEST COMPLETED!")
        logger.info("=" * 60)
        logger.info("\nGenerated files:")
        logger.info("  - output/pipeline_metrics.json")
        logger.info("  - output/pipeline_metrics.html")
        logger.info("\nOpen pipeline_metrics.html in your browser to view the report!")
        
    except Exception as e:
        logger.error(f"Error during metrics test: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    test_metrics_collection()
