#!/usr/bin/env python3
"""
Google Colab Runner for NLP Knowledge Graph Pipeline
This script is specifically designed to run the NLP pipeline in Google Colab environment.
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, description):
    """Run a command and handle output"""
    logger.info(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main execution function for Google Colab"""
    
    print("🚀 Starting NLP Knowledge Graph Pipeline in Google Colab")
    print("=" * 70)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Step 1: Install dependencies
    print("\n📦 Installing Dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    # Step 2: Download spaCy model
    print("\n🌐 Downloading spaCy Model...")
    if not run_command("python -m spacy download xx_ent_wiki_sm", "Downloading spaCy multilingual model"):
        return False
    
    # Step 3: Train NER model
    print("\n🤖 Training NER Model...")
    if not run_command("python ner_trainer.py", "Training custom NER model"):
        return False
    
    # Step 4: Evaluate models
    print("\n📊 Evaluating Models...")
    if not run_command("python compare_ner_models.py", "Comparing NER models"):
        return False
    
    # Step 5: Build knowledge graph
    print("\n🕸️ Building Knowledge Graph...")
    if not run_command("python build_knowledge_graph.py", "Building knowledge graph"):
        return False
    
    print("\n" + "=" * 70)
    print("🎉 Pipeline completed successfully!")
    print("=" * 70)
    
    # Show results
    output_dir = current_dir / "output"
    if output_dir.exists():
        print("\n📋 Generated Files:")
        for file_path in output_dir.glob("*.html"):
            print(f"  🔗 {file_path.name}")
        for file_path in output_dir.glob("*.json"):
            print(f"  📄 {file_path.name}")
    
    print("\n💡 To view results in Colab:")
    print("   1. Navigate to the 'output' folder in the file browser")
    print("   2. Download the HTML files to view visualizations")
    print("   3. Or use: from google.colab import files; files.download('output/knowledge_graph.html')")

if __name__ == "__main__":
    main()