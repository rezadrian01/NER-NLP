"""
Custom NER Model Trainer
Author: Ahmad Reza Adrian

This module trains a custom spaCy NER model using annotated data
from the wayang stories dataset.
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import json
import random
from pathlib import Path
import logging
from typing import List, Tuple, Dict
from config import MODELS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CustomNERTrainer:
    """
    Train a custom spaCy NER model for Indonesian wayang texts.
    """
    
    def __init__(self, base_model: str = "xx_ent_wiki_sm"):
        """
        Initialize trainer.
        
        Args:
            base_model: Base spaCy model to start from
        """
        self.base_model = base_model
        self.nlp = None
        self.ner = None
    
    def load_training_data(self, train_path: Path) -> List[Tuple[str, Dict]]:
        """
        Load training data from JSON file.
        
        Args:
            train_path: Path to training data JSON
            
        Returns:
            List of (text, annotations) tuples
        """
        logger.info(f"Loading training data from {train_path}...")
        
        with open(train_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        training_data = []
        for item in data:
            # Handle both dict and tuple/list formats
            if isinstance(item, dict):
                text = item['text']
                entities = item['entities']
                training_data.append((text, {'entities': entities}))
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                # Data is already in (text, {'entities': [...]}) format
                text, entities_dict = item
                training_data.append((text, entities_dict))
            else:
                logger.warning(f"Skipping invalid item format: {type(item)}")
                continue
        
        logger.info(f"Loaded {len(training_data)} training examples")
        
        return training_data
    
    def setup_model(self):
        """
        Setup spaCy model for training.
        """
        logger.info(f"Setting up model from {self.base_model}...")
        
        try:
            # Load base model
            self.nlp = spacy.load(self.base_model)
            logger.info(f"Loaded base model: {self.base_model}")
        except OSError:
            logger.info(f"Base model not found. Creating blank 'id' model...")
            self.nlp = spacy.blank("id")  # Indonesian
        
        # Get or create NER component
        if "ner" not in self.nlp.pipe_names:
            self.ner = self.nlp.add_pipe("ner")
            logger.info("Added NER pipeline component")
        else:
            self.ner = self.nlp.get_pipe("ner")
            logger.info("Using existing NER pipeline component")
    
    def add_labels(self, training_data: List[Tuple[str, Dict]]):
        """
        Add entity labels to NER component.
        
        Args:
            training_data: Training data with entity annotations
        """
        logger.info("Adding entity labels...")
        
        labels = set()
        for _, annotations in training_data:
            for ent in annotations.get('entities', []):
                labels.add(ent[2])
        
        for label in labels:
            self.ner.add_label(label)
            logger.info(f"  Added label: {label}")
    
    def train(self, 
              training_data: List[Tuple[str, Dict]], 
              n_iter: int = 30,
              dropout: float = 0.2,
              batch_size: int = 8) -> Dict[str, List[float]]:
        """
        Train the NER model.
        
        Args:
            training_data: Training data
            n_iter: Number of training iterations
            dropout: Dropout rate
            batch_size: Batch size for training
            
        Returns:
            Dictionary of training losses per iteration
        """
        logger.info(f"Starting training for {n_iter} iterations...")
        logger.info(f"  Batch size: {batch_size}")
        logger.info(f"  Dropout: {dropout}")
        
        # Get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        
        losses_history = {'ner': []}
        
        with self.nlp.disable_pipes(*other_pipes):
            # Initialize optimizer
            optimizer = self.nlp.begin_training()
            
            for iteration in range(n_iter):
                random.shuffle(training_data)
                losses = {}
                
                # Create batches with compounding batch size
                batches = minibatch(training_data, size=compounding(4.0, batch_size, 1.001))
                
                for batch in batches:
                    examples = []
                    for text, annotations in batch:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        examples.append(example)
                    
                    self.nlp.update(examples, 
                                   drop=dropout,
                                   losses=losses,
                                   sgd=optimizer)
                
                losses_history['ner'].append(losses.get('ner', 0))
                
                if (iteration + 1) % 5 == 0 or iteration == 0:
                    logger.info(f"  Iteration {iteration + 1}/{n_iter} - Loss: {losses.get('ner', 0):.4f}")
        
        logger.info("✅ Training complete!")
        
        return losses_history
    
    def save_model(self, output_dir: Path):
        """
        Save trained model to disk.
        
        Args:
            output_dir: Directory to save model
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        self.nlp.to_disk(output_dir)
        logger.info(f"✅ Model saved to {output_dir}")
    
    def evaluate_on_sample(self, test_data: List[Tuple[str, Dict]], n_samples: int = 5):
        """
        Evaluate model on sample texts.
        
        Args:
            test_data: Test data
            n_samples: Number of samples to display
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Sample Predictions (first {n_samples} examples):")
        logger.info(f"{'='*60}")
        
        for i, (text, annotations) in enumerate(test_data[:n_samples]):
            doc = self.nlp(text)
            
            true_entities = annotations.get('entities', [])
            pred_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
            
            logger.info(f"\nExample {i+1}:")
            logger.info(f"  Text: {text[:100]}{'...' if len(text) > 100 else ''}")
            logger.info(f"  True entities: {len(true_entities)}")
            for start, end, label in true_entities[:5]:
                logger.info(f"    - {text[start:end]} [{label}]")
            logger.info(f"  Predicted entities: {len(pred_entities)}")
            for start, end, label in pred_entities[:5]:
                logger.info(f"    - {text[start:end]} [{label}]")


def main():
    """
    Main function to train custom NER model.
    """
    logger.info("="*60)
    logger.info("Training Custom NER Model for Wayang Stories")
    logger.info("="*60)
    
    # Paths
    models_dir = Path(MODELS_DIR)
    train_data_path = models_dir / "train_data.json"
    test_data_path = models_dir / "test_data.json"
    output_model_path = models_dir / "custom_ner_model"
    
    # Check if training data exists
    if not train_data_path.exists():
        logger.error(f"Training data not found at {train_data_path}")
        logger.error("Please run 'python create_training_data.py' first")
        return
    
    # Initialize trainer
    trainer = CustomNERTrainer(base_model="xx_ent_wiki_sm")
    
    # Load data
    training_data = trainer.load_training_data(train_data_path)
    test_data = trainer.load_training_data(test_data_path) if test_data_path.exists() else []
    
    # Setup model
    trainer.setup_model()
    
    # Add labels
    trainer.add_labels(training_data)
    
    # Train model
    losses = trainer.train(training_data, n_iter=30, dropout=0.2, batch_size=8)
    
    # Show sample predictions
    if test_data:
        trainer.evaluate_on_sample(test_data, n_samples=5)
    
    # Save model
    trainer.save_model(output_model_path)
    
    logger.info("\n" + "="*60)
    logger.info("Training Complete!")
    logger.info(f"Model saved to: {output_model_path}")
    logger.info("="*60)
    logger.info("\nNext steps:")
    logger.info("  1. Run 'python compare_ner_models.py' to evaluate both models")
    logger.info("  2. Check the evaluation report in output/ner_evaluation_report.html")


if __name__ == "__main__":
    main()
