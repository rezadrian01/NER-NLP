"""
NER Model Evaluator
Author: Ahmad Reza Adrian

This module provides comprehensive evaluation metrics for NER models:
- Precision, Recall, F1 Score
- Exact Match (entity-level)
- Partial Match (token-level)
- Per-label Metrics (Macro F1)
- Micro F1
- Confusion Matrix
"""

import spacy
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NEREvaluator:
    """
    Comprehensive NER Model Evaluator
    Author: Kelompok 1
    
    Provides detailed evaluation metrics for Named Entity Recognition models.
    """
    
    def __init__(self, model_name: str):
        """
        Initialize evaluator.
        
        Args:
            model_name: Name/description of the model being evaluated
        """
        self.model_name = model_name
        self.results = {
            'model_name': model_name,
            'metrics': {},
            'per_label_metrics': {},
            'confusion_matrix': defaultdict(lambda: defaultdict(int)),
            'examples': []
        }
        
        # Label mapping for spaCy multilingual model compatibility
        self.label_mapping = {
            'PER': 'PERSON',  # spaCy multilingual uses 'PER', we use 'PERSON'
            'PERSON': 'PERSON',  # Keep our custom labels as-is
            'LOC': 'LOC',
            'ORG': 'ORG', 
            'EVENT': 'EVENT',
            'MISC': 'EVENT'  # Map MISC to EVENT as fallback
        }
    
    def normalize_label(self, label: str) -> str:
        """
        Normalize entity labels for comparison.
        
        Args:
            label: Original label
            
        Returns:
            Normalized label
        """
        return self.label_mapping.get(label, label)
    
    def predict(self, nlp, text: str) -> List[Tuple[int, int, str]]:
        """
        Get predictions from a spaCy model with normalized labels.
        
        Args:
            nlp: spaCy model
            text: Input text
            
        Returns:
            List of (start, end, normalized_label) tuples
        """
        doc = nlp(text)
        return [(ent.start_char, ent.end_char, self.normalize_label(ent.label_)) for ent in doc.ents]
    
    def calculate_exact_match(self, 
                             true_entities: List[Tuple[int, int, str]], 
                             pred_entities: List[Tuple[int, int, str]]) -> Dict[str, int]:
        """
        Calculate exact match metrics (entity boundaries and type must match exactly).
        
        Args:
            true_entities: Ground truth entities
            pred_entities: Predicted entities
            
        Returns:
            Dictionary with TP, FP, FN counts
        """
        # Convert to tuples if they're lists (from JSON loading)
        true_entities = [tuple(e) if isinstance(e, list) else e for e in true_entities]
        pred_entities = [tuple(e) if isinstance(e, list) else e for e in pred_entities]
        
        # Normalize labels in both sets
        true_normalized = [(start, end, self.normalize_label(label)) for start, end, label in true_entities]
        pred_normalized = [(start, end, self.normalize_label(label)) for start, end, label in pred_entities]
        
        true_set = set(true_normalized)
        pred_set = set(pred_normalized)
        
        tp = len(true_set & pred_set)  # True positives
        fp = len(pred_set - true_set)  # False positives
        fn = len(true_set - pred_set)  # False negatives
        
        return {'tp': tp, 'fp': fp, 'fn': fn}
    
    def calculate_partial_match(self,
                                true_entities: List[Tuple[int, int, str]],
                                pred_entities: List[Tuple[int, int, str]]) -> Dict[str, int]:
        """
        Calculate partial match metrics (overlapping boundaries count as match).
        
        Args:
            true_entities: Ground truth entities
            pred_entities: Predicted entities
            
        Returns:
            Dictionary with TP, FP, FN counts
        """
        # Convert to tuples if they're lists (from JSON loading)
        true_entities = [tuple(e) if isinstance(e, list) else e for e in true_entities]
        pred_entities = [tuple(e) if isinstance(e, list) else e for e in pred_entities]
        
        tp = 0
        fp = 0
        matched_true = set()
        matched_pred = set()
        
        # Find partial matches
        for i, (pred_start, pred_end, pred_label) in enumerate(pred_entities):
            found_match = False
            for j, (true_start, true_end, true_label) in enumerate(true_entities):
                # Normalize labels before comparison
                normalized_pred_label = self.normalize_label(pred_label)
                normalized_true_label = self.normalize_label(true_label)
                
                # Check if there's overlap and normalized labels match
                if (normalized_pred_label == normalized_true_label and 
                    not (pred_end <= true_start or pred_start >= true_end)):
                    tp += 1
                    matched_true.add(j)
                    matched_pred.add(i)
                    found_match = True
                    break
            
            if not found_match:
                fp += 1
        
        # Count false negatives (unmatched true entities)
        fn = len(true_entities) - len(matched_true)
        
        return {'tp': tp, 'fp': fp, 'fn': fn}
    
    def calculate_type_match(self,
                           true_entities: List[Tuple[int, int, str]],
                           pred_entities: List[Tuple[int, int, str]]) -> Dict[str, int]:
        """
        Calculate type-only match (boundaries match but label may differ).
        
        Args:
            true_entities: Ground truth entities
            pred_entities: Predicted entities
            
        Returns:
            Dictionary with correct/incorrect label counts
        """
        # Convert to tuples if they're lists (from JSON loading)
        true_entities = [tuple(e) if isinstance(e, list) else e for e in true_entities]
        pred_entities = [tuple(e) if isinstance(e, list) else e for e in pred_entities]
        
        correct_type = 0
        wrong_type = 0
        
        for pred_start, pred_end, pred_label in pred_entities:
            for true_start, true_end, true_label in true_entities:
                # If boundaries match exactly
                if pred_start == true_start and pred_end == true_end:
                    if pred_label == true_label:
                        correct_type += 1
                    else:
                        wrong_type += 1
                        # Update confusion matrix
                        self.results['confusion_matrix'][true_label][pred_label] += 1
                    break
        
        return {'correct_type': correct_type, 'wrong_type': wrong_type}
    
    def calculate_precision_recall_f1(self, tp: int, fp: int, fn: int) -> Dict[str, float]:
        """
        Calculate precision, recall, and F1 score.
        
        Args:
            tp: True positives
            fp: False positives
            fn: False negatives
            
        Returns:
            Dictionary with precision, recall, f1
        """
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def calculate_per_label_metrics(self, 
                                   true_entities: List[Tuple[int, int, str]], 
                                   pred_entities: List[Tuple[int, int, str]]) -> Dict[str, Dict]:
        """
        Calculate metrics for each entity label.
        
        Args:
            true_entities: Ground truth entities
            pred_entities: Predicted entities
            
        Returns:
            Dictionary mapping labels to their metrics
        """
        # Convert to tuples if they're lists (from JSON loading)
        true_entities = [tuple(e) if isinstance(e, list) else e for e in true_entities]
        pred_entities = [tuple(e) if isinstance(e, list) else e for e in pred_entities]
        
        # Normalize labels
        true_normalized = [(start, end, self.normalize_label(label)) for start, end, label in true_entities]
        pred_normalized = [(start, end, self.normalize_label(label)) for start, end, label in pred_entities]
        
        label_stats = defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0})
        
        true_set = set(true_normalized)
        pred_set = set(pred_normalized)
        
        # True positives and false negatives
        for entity in true_set:
            label = entity[2]  # normalized label
            if entity in pred_set:
                label_stats[label]['tp'] += 1
            else:
                label_stats[label]['fn'] += 1
        
        # False positives
        for entity in pred_set:
            label = entity[2]  # normalized label
            if entity not in true_set:
                label_stats[label]['fp'] += 1
        
        # Calculate metrics for each label
        label_metrics = {}
        for label, stats in label_stats.items():
            metrics = self.calculate_precision_recall_f1(
                stats['tp'], stats['fp'], stats['fn']
            )
            metrics.update(stats)
            label_metrics[label] = metrics
        
        return label_metrics
    
    def calculate_macro_micro_f1(self, per_label_metrics: Dict[str, Dict]) -> Dict[str, float]:
        """
        Calculate macro and micro F1 scores.
        
        Args:
            per_label_metrics: Metrics for each label
            
        Returns:
            Dictionary with macro_f1 and micro_f1
        """
        # Macro F1: average of per-label F1 scores
        f1_scores = [metrics['f1'] for metrics in per_label_metrics.values()]
        macro_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
        
        # Micro F1: calculate from total TP, FP, FN
        total_tp = sum(metrics['tp'] for metrics in per_label_metrics.values())
        total_fp = sum(metrics['fp'] for metrics in per_label_metrics.values())
        total_fn = sum(metrics['fn'] for metrics in per_label_metrics.values())
        
        micro_metrics = self.calculate_precision_recall_f1(total_tp, total_fp, total_fn)
        micro_f1 = micro_metrics['f1']
        
        return {
            'macro_f1': macro_f1,
            'micro_f1': micro_f1,
            'micro_precision': micro_metrics['precision'],
            'micro_recall': micro_metrics['recall']
        }
    
    def evaluate(self, nlp, test_data: List[Tuple[str, Dict]]) -> Dict[str, Any]:
        """
        Run comprehensive evaluation on test data.
        
        Args:
            nlp: spaCy model to evaluate
            test_data: List of (text, annotations) tuples
            
        Returns:
            Dictionary with all evaluation metrics
        """
        logger.info(f"Evaluating {self.model_name} on {len(test_data)} examples...")
        
        # Accumulate counts
        exact_match_total = {'tp': 0, 'fp': 0, 'fn': 0}
        partial_match_total = {'tp': 0, 'fp': 0, 'fn': 0}
        type_match_total = {'correct_type': 0, 'wrong_type': 0}
        
        all_true_entities = []
        all_pred_entities = []
        
        for idx, (text, annotations) in enumerate(test_data):
            # Get predictions
            pred_entities = self.predict(nlp, text)
            true_entities = annotations.get('entities', [])
            
            # Store for per-label metrics
            all_true_entities.extend(true_entities)
            all_pred_entities.extend(pred_entities)
            
            # Calculate exact match
            exact = self.calculate_exact_match(true_entities, pred_entities)
            for key in exact:
                exact_match_total[key] += exact[key]
            
            # Calculate partial match
            partial = self.calculate_partial_match(true_entities, pred_entities)
            for key in partial:
                partial_match_total[key] += partial[key]
            
            # Calculate type match
            type_match = self.calculate_type_match(true_entities, pred_entities)
            for key in type_match:
                type_match_total[key] += type_match[key]
            
            # Store example if interesting (has predictions or ground truth)
            if len(self.results['examples']) < 10 and (pred_entities or true_entities):
                self.results['examples'].append({
                    'text': text[:200] + '...' if len(text) > 200 else text,
                    'true_entities': true_entities,
                    'pred_entities': pred_entities,
                    'exact_match': exact,
                    'partial_match': partial
                })
            
            if (idx + 1) % 20 == 0:
                logger.info(f"  Processed {idx + 1}/{len(test_data)} examples")
        
        # Calculate overall metrics
        exact_metrics = self.calculate_precision_recall_f1(
            exact_match_total['tp'], exact_match_total['fp'], exact_match_total['fn']
        )
        
        partial_metrics = self.calculate_precision_recall_f1(
            partial_match_total['tp'], partial_match_total['fp'], partial_match_total['fn']
        )
        
        # Per-label metrics
        per_label = self.calculate_per_label_metrics(all_true_entities, all_pred_entities)
        
        # Macro/Micro F1
        macro_micro = self.calculate_macro_micro_f1(per_label)
        
        # Store results
        self.results['metrics'] = {
            'exact_match': {
                **exact_match_total,
                **exact_metrics
            },
            'partial_match': {
                **partial_match_total,
                **partial_metrics
            },
            'type_match': type_match_total,
            **macro_micro
        }
        
        self.results['per_label_metrics'] = per_label
        
        # Convert confusion matrix to regular dict for JSON serialization
        self.results['confusion_matrix'] = {
            k: dict(v) for k, v in self.results['confusion_matrix'].items()
        }
        
        logger.info(f"✅ Evaluation complete for {self.model_name}")
        
        return self.results
    
    def print_summary(self):
        """Print evaluation summary to console."""
        print("\n" + "="*70)
        print(f"Evaluation Results: {self.model_name}")
        print("="*70)
        
        metrics = self.results['metrics']
        
        print("\n📊 Overall Metrics:")
        print(f"  Exact Match:")
        print(f"    Precision: {metrics['exact_match']['precision']:.4f}")
        print(f"    Recall:    {metrics['exact_match']['recall']:.4f}")
        print(f"    F1 Score:  {metrics['exact_match']['f1']:.4f}")
        
        print(f"\n  Partial Match:")
        print(f"    Precision: {metrics['partial_match']['precision']:.4f}")
        print(f"    Recall:    {metrics['partial_match']['recall']:.4f}")
        print(f"    F1 Score:  {metrics['partial_match']['f1']:.4f}")
        
        print(f"\n  Aggregate Metrics:")
        print(f"    Macro F1:       {metrics['macro_f1']:.4f}")
        print(f"    Micro F1:       {metrics['micro_f1']:.4f}")
        print(f"    Micro Precision: {metrics['micro_precision']:.4f}")
        print(f"    Micro Recall:    {metrics['micro_recall']:.4f}")
        
        print("\n📋 Per-Label F1 Scores:")
        for label, label_metrics in sorted(self.results['per_label_metrics'].items()):
            print(f"  {label:10s}: {label_metrics['f1']:.4f} "
                  f"(P: {label_metrics['precision']:.3f}, "
                  f"R: {label_metrics['recall']:.3f})")
        
        print("\n" + "="*70)
    
    def save_results(self, output_path: Path):
        """
        Save evaluation results to JSON file.
        
        Args:
            output_path: Path to save results
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {output_path}")


def main():
    """
    Test the evaluator on a sample model.
    """
    import sys
    import os
    
    # Add parent directory to path to import config
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import MODELS_DIR
    
    logger.info("Testing NER Evaluator...")
    
    # Load test data
    test_data_path = Path(MODELS_DIR) / "test_data.json"
    if not test_data_path.exists():
        logger.error(f"Test data not found at {test_data_path}")
        return
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_data = [(item['text'], {'entities': item['entities']}) for item in data]
    
    # Load model
    try:
        nlp = spacy.load("xx_ent_wiki_sm")
    except:
        logger.error("spaCy model not found. Please download it first.")
        return
    
    # Evaluate
    evaluator = NEREvaluator("Test Model")
    results = evaluator.evaluate(nlp, test_data[:10])  # Test on first 10 examples
    evaluator.print_summary()


if __name__ == "__main__":
    main()
