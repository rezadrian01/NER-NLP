"""
Complete NER Evaluation Pipeline
This script runs the entire evaluation workflow:
1. Create training data from manual annotations
2. Train custom NER model
3. Compare models and generate reports
"""

import subprocess
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define script paths
SCRIPTS_DIR = Path(__file__).parent / "scripts"
EVALUATION_DIR = Path(__file__).parent / "evaluation"


def run_step(step_name: str, script_path: str) -> bool:
    """
    Run a Python script and check if it succeeds.
    
    Args:
        step_name: Name of the step for logging
        script_path: Path to Python script
        
    Returns:
        True if successful, False otherwise
    """
    logger.info("="*70)
    logger.info(f"STEP: {step_name}")
    logger.info("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False,
            text=True
        )
        logger.info(f"✅ {step_name} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {step_name} failed with error code {e.returncode}\n")
        return False
    except Exception as e:
        logger.error(f"❌ {step_name} failed: {e}\n")
        return False


def main():
    """
    Run the complete workflow.
    """
    print("\n" + "="*70)
    print("NER MODEL EVALUATION WORKFLOW")
    print("="*70)
    print("\nThis workflow will:")
    print("  1. Extract training data from your dataset")
    print("  2. Train a custom NER model")
    print("  3. Evaluate both spaCy and custom models")
    print("  4. Generate comparison reports (JSON + HTML)")
    print("\nEstimated time: 5-15 minutes depending on dataset size")
    print("="*70)
    
    # Ask for confirmation
    response = input("\nContinue? (y/n): ").strip().lower()
    if response != 'y':
        print("Workflow cancelled.")
        return
    
    # Define workflow steps
    steps = [
        ("Create Training Data", str(SCRIPTS_DIR / "create_manual_training_data.py")),
        ("Train Custom NER Model", str(EVALUATION_DIR / "ner_trainer.py")),
        ("Compare Models and Generate Reports", str(EVALUATION_DIR / "compare_ner_models.py"))
    ]
    
    # Execute workflow
    start_time = __import__('time').time()
    
    for step_name, script_path in steps:
        success = run_step(step_name, script_path)
        if not success:
            logger.error(f"\n❌ Workflow stopped at: {step_name}")
            logger.error("Please fix the errors and try again.")
            return
    
    # Calculate duration
    duration = __import__('time').time() - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    
    # Success message
    print("\n" + "="*70)
    print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nTotal time: {minutes}m {seconds}s")
    print("\n📊 Generated files:")
    print("  - models/train_data.json (training data)")
    print("  - models/test_data.json (test data)")
    print("  - models/custom_ner_model/ (trained model)")
    print("  - output/ner_evaluation_comparison.json (detailed metrics)")
    print("  - output/ner_evaluation_comparison.html (visual report)")
    print("\n🎯 Next steps:")
    print("  - Open output/ner_evaluation_comparison.html in your browser")
    print("  - Review the comparison metrics")
    print("  - Use the better model in your pipeline")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
