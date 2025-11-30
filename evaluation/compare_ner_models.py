"""
NER Model Comparison Tool
Author: Kelompok 1

Compares two NER models side-by-side with comprehensive metrics.
"""

import spacy
import json
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, Any
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ner_evaluator import NEREvaluator
from config import MODELS_DIR, OUTPUT_DIR

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ModelComparison:
    """
    Compare two NER models and generate reports.
    """
    
    def __init__(self):
        """Initialize model comparison."""
        self.models = {}
        self.evaluations = {}
        self.test_data = []
    
    def load_test_data(self, test_data_path: Path):
        """
        Load test data.
        
        Args:
            test_data_path: Path to test data JSON
        """
        logger.info(f"Loading test data from {test_data_path}...")
        
        with open(test_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both dict and tuple/list formats
        test_data = []
        for item in data:
            if isinstance(item, dict):
                test_data.append((item['text'], {'entities': item['entities']}))
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                # Data is already in (text, {'entities': [...]}) format
                test_data.append((item[0], item[1]))
            else:
                logger.warning(f"Skipping invalid item format: {type(item)}")
        
        self.test_data = test_data
        logger.info(f"Loaded {len(self.test_data)} test examples")
    
    def load_model(self, model_name: str, model_path: str):
        """
        Load a spaCy model.
        
        Args:
            model_name: Name identifier for the model
            model_path: Path or name of spaCy model
        """
        logger.info(f"Loading model: {model_name} from {model_path}")
        
        try:
            nlp = spacy.load(model_path)
            self.models[model_name] = nlp
            logger.info(f"✅ Successfully loaded {model_name}")
        except Exception as e:
            logger.error(f"❌ Failed to load {model_name}: {e}")
            raise
    
    def evaluate_model(self, model_name: str):
        """
        Evaluate a loaded model.
        
        Args:
            model_name: Name identifier for the model
        """
        if model_name not in self.models:
            logger.error(f"Model {model_name} not loaded")
            return
        
        logger.info(f"\n{'='*70}")
        logger.info(f"Evaluating: {model_name}")
        logger.info(f"{'='*70}")
        
        evaluator = NEREvaluator(model_name)
        results = evaluator.evaluate(self.models[model_name], self.test_data)
        evaluator.print_summary()
        
        self.evaluations[model_name] = results
    
    def generate_comparison_report(self) -> Dict[str, Any]:
        """
        Generate comparison report.
        
        Returns:
            Dictionary with comparison data
        """
        if len(self.evaluations) < 2:
            logger.warning("Need at least 2 models to compare")
            return {}
        
        model_names = list(self.evaluations.keys())
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_data_size': len(self.test_data),
            'models': model_names,
            'comparison': {},
            'model_details': {}
        }
        
        # Extract key metrics for comparison
        for model_name in model_names:
            eval_results = self.evaluations[model_name]
            metrics = eval_results['metrics']
            
            report['model_details'][model_name] = {
                'exact_match': metrics['exact_match'],
                'partial_match': metrics['partial_match'],
                'macro_f1': metrics['macro_f1'],
                'micro_f1': metrics['micro_f1'],
                'per_label_f1': {
                    label: metrics_data['f1'] 
                    for label, metrics_data in eval_results['per_label_metrics'].items()
                }
            }
        
        # Calculate differences
        model1, model2 = model_names[0], model_names[1]
        m1_metrics = report['model_details'][model1]
        m2_metrics = report['model_details'][model2]
        
        report['comparison'] = {
            'exact_match_f1_diff': m1_metrics['exact_match']['f1'] - m2_metrics['exact_match']['f1'],
            'partial_match_f1_diff': m1_metrics['partial_match']['f1'] - m2_metrics['partial_match']['f1'],
            'macro_f1_diff': m1_metrics['macro_f1'] - m2_metrics['macro_f1'],
            'micro_f1_diff': m1_metrics['micro_f1'] - m2_metrics['micro_f1'],
            'winner': model1 if m1_metrics['micro_f1'] > m2_metrics['micro_f1'] else model2
        }
        
        return report
    
    def save_json_report(self, report: Dict[str, Any], output_path: Path):
        """
        Save comparison report as JSON.
        
        Args:
            report: Comparison report
            output_path: Path to save JSON file
        """
        # Include full evaluation results
        full_report = {
            **report,
            'full_evaluations': self.evaluations
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 JSON report saved to {output_path}")
    
    def generate_html_report(self, report: Dict[str, Any], output_path: Path):
        """
        Generate HTML report with visualizations.
        
        Args:
            report: Comparison report
            output_path: Path to save HTML file
        """
        model_names = report['models']
        m1, m2 = model_names[0], model_names[1]
        
        # Extract metrics for easier access
        m1_data = report['model_details'][m1]
        m2_data = report['model_details'][m2]
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NER Model Comparison Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .winner-banner {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}
        
        .metric-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .metric-row:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            font-weight: 600;
            color: #555;
        }}
        
        .metric-value {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }}
        
        .metric-value.good {{
            color: #38ef7d;
        }}
        
        .metric-value.medium {{
            color: #ffa726;
        }}
        
        .metric-value.poor {{
            color: #ef5350;
        }}
        
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .comparison-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .comparison-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .comparison-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .comparison-table .model-col {{
            font-weight: 600;
        }}
        
        .better {{
            background: #e8f5e9;
            font-weight: bold;
            color: #2e7d32;
        }}
        
        .worse {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .diff-positive {{
            color: #2e7d32;
            font-weight: bold;
        }}
        
        .diff-negative {{
            color: #c62828;
            font-weight: bold;
        }}
        
        .bar-chart {{
            margin: 20px 0;
        }}
        
        .bar-item {{
            margin: 15px 0;
        }}
        
        .bar-label {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #555;
        }}
        
        .bar-container {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .bar {{
            height: 30px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            transition: width 0.3s ease;
        }}
        
        .bar.model2 {{
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        .info-box strong {{
            color: #1976d2;
        }}
        
        .legend {{
            display: flex;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .legend-color {{
            width: 30px;
            height: 20px;
            border-radius: 3px;
        }}
        
        .legend-color.model1 {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }}
        
        .legend-color.model2 {{
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 NER Model Comparison Report</h1>
            <div class="subtitle">Indonesian Wayang Stories Named Entity Recognition</div>
            <div style="margin-top: 15px; font-size: 0.9em;">
                Generated: {report['timestamp']}<br>
                Test Examples: {report['test_data_size']}
            </div>
        </div>
        
        <div class="content">
            <!-- Winner Banner -->
            <div class="winner-banner">
                🏆 Best Model: {report['comparison']['winner']}
                <div style="font-size: 0.7em; margin-top: 10px; opacity: 0.9;">
                    Based on Micro F1 Score
                </div>
            </div>
            
            <!-- Summary Metrics -->
            <div class="section">
                <h2 class="section-title">📊 Overall Metrics Comparison</h2>
                
                <div class="info-box">
                    <strong>Test Dataset:</strong> {report['test_data_size']} examples<br>
                    <strong>Models Compared:</strong> {m1} vs {m2}
                </div>
                
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th class="model-col">{m1}</th>
                            <th class="model-col">{m2}</th>
                            <th>Difference</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Exact Match F1</td>
                            <td class="{'better' if m1_data['exact_match']['f1'] > m2_data['exact_match']['f1'] else ''}">{m1_data['exact_match']['f1']:.4f}</td>
                            <td class="{'better' if m2_data['exact_match']['f1'] > m1_data['exact_match']['f1'] else ''}">{m2_data['exact_match']['f1']:.4f}</td>
                            <td class="{'diff-positive' if report['comparison']['exact_match_f1_diff'] > 0 else 'diff-negative'}">{report['comparison']['exact_match_f1_diff']:+.4f}</td>
                        </tr>
                        <tr>
                            <td>Exact Match Precision</td>
                            <td>{m1_data['exact_match']['precision']:.4f}</td>
                            <td>{m2_data['exact_match']['precision']:.4f}</td>
                            <td>{m1_data['exact_match']['precision'] - m2_data['exact_match']['precision']:+.4f}</td>
                        </tr>
                        <tr>
                            <td>Exact Match Recall</td>
                            <td>{m1_data['exact_match']['recall']:.4f}</td>
                            <td>{m2_data['exact_match']['recall']:.4f}</td>
                            <td>{m1_data['exact_match']['recall'] - m2_data['exact_match']['recall']:+.4f}</td>
                        </tr>
                        <tr>
                            <td>Partial Match F1</td>
                            <td class="{'better' if m1_data['partial_match']['f1'] > m2_data['partial_match']['f1'] else ''}">{m1_data['partial_match']['f1']:.4f}</td>
                            <td class="{'better' if m2_data['partial_match']['f1'] > m1_data['partial_match']['f1'] else ''}">{m2_data['partial_match']['f1']:.4f}</td>
                            <td class="{'diff-positive' if report['comparison']['partial_match_f1_diff'] > 0 else 'diff-negative'}">{report['comparison']['partial_match_f1_diff']:+.4f}</td>
                        </tr>
                        <tr>
                            <td>Macro F1</td>
                            <td class="{'better' if m1_data['macro_f1'] > m2_data['macro_f1'] else ''}">{m1_data['macro_f1']:.4f}</td>
                            <td class="{'better' if m2_data['macro_f1'] > m1_data['macro_f1'] else ''}">{m2_data['macro_f1']:.4f}</td>
                            <td class="{'diff-positive' if report['comparison']['macro_f1_diff'] > 0 else 'diff-negative'}">{report['comparison']['macro_f1_diff']:+.4f}</td>
                        </tr>
                        <tr>
                            <td><strong>Micro F1</strong></td>
                            <td class="{'better' if m1_data['micro_f1'] > m2_data['micro_f1'] else ''}"><strong>{m1_data['micro_f1']:.4f}</strong></td>
                            <td class="{'better' if m2_data['micro_f1'] > m1_data['micro_f1'] else ''}"><strong>{m2_data['micro_f1']:.4f}</strong></td>
                            <td class="{'diff-positive' if report['comparison']['micro_f1_diff'] > 0 else 'diff-negative'}"><strong>{report['comparison']['micro_f1_diff']:+.4f}</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Per-Label Comparison -->
            <div class="section">
                <h2 class="section-title">🏷️ Per-Label F1 Scores</h2>
                
                <div class="legend">
                    <div class="legend-item">
                        <div class="legend-color model1"></div>
                        <span>{m1}</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color model2"></div>
                        <span>{m2}</span>
                    </div>
                </div>
                
                <div class="bar-chart">
"""
        
        # Add per-label bars
        all_labels = set(list(m1_data['per_label_f1'].keys()) + list(m2_data['per_label_f1'].keys()))
        for label in sorted(all_labels):
            m1_score = m1_data['per_label_f1'].get(label, 0.0)
            m2_score = m2_data['per_label_f1'].get(label, 0.0)
            
            html_content += f"""
                    <div class="bar-item">
                        <div class="bar-label">{label}</div>
                        <div class="bar-container">
                            <div style="width: 150px;">{m1}:</div>
                            <div class="bar" style="width: {m1_score * 300}px;">{m1_score:.3f}</div>
                        </div>
                        <div class="bar-container">
                            <div style="width: 150px;">{m2}:</div>
                            <div class="bar model2" style="width: {m2_score * 300}px;">{m2_score:.3f}</div>
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
            
            <!-- Detailed Metrics -->
            <div class="section">
                <h2 class="section-title">📈 Detailed Model Metrics</h2>
                
                <div class="metrics-grid">
"""
        
        # Add detailed metric cards for each model
        for model_name in [m1, m2]:
            model_data = report['model_details'][model_name]
            
            html_content += f"""
                    <div class="metric-card">
                        <h3>{model_name}</h3>
                        <div class="metric-row">
                            <span class="metric-label">Exact TP:</span>
                            <span class="metric-value">{model_data['exact_match']['tp']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Exact FP:</span>
                            <span class="metric-value">{model_data['exact_match']['fp']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Exact FN:</span>
                            <span class="metric-value">{model_data['exact_match']['fn']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Partial TP:</span>
                            <span class="metric-value">{model_data['partial_match']['tp']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Partial FP:</span>
                            <span class="metric-value">{model_data['partial_match']['fp']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Partial FN:</span>
                            <span class="metric-value">{model_data['partial_match']['fn']}</span>
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
            
            <!-- Interpretation Guide -->
            <div class="section">
                <h2 class="section-title">📖 Metrics Interpretation</h2>
                
                <div class="info-box">
                    <strong>Exact Match:</strong> Entity boundaries and type must match exactly<br>
                    <strong>Partial Match:</strong> Overlapping entities with same type count as matches<br>
                    <strong>Macro F1:</strong> Average F1 across all entity types (treats all types equally)<br>
                    <strong>Micro F1:</strong> F1 calculated from total TP, FP, FN (weighted by frequency)<br>
                    <strong>TP (True Positive):</strong> Correctly predicted entities<br>
                    <strong>FP (False Positive):</strong> Incorrectly predicted entities<br>
                    <strong>FN (False Negative):</strong> Missed entities
                </div>
            </div>
        </div>
        
        <div class="footer">
            <strong>Wayang NER Evaluation System</strong><br>
            Generated by compare_ner_models.py | Kelompok 1
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"📊 HTML report saved to {output_path}")
    
    def print_comparison_summary(self, report: Dict[str, Any]):
        """
        Print comparison summary to console.
        
        Args:
            report: Comparison report
        """
        print("\n" + "="*70)
        print("MODEL COMPARISON SUMMARY")
        print("="*70)
        
        print(f"\n🏆 Winner: {report['comparison']['winner']}")
        print(f"   (Based on Micro F1 Score)")
        
        print(f"\n📊 Key Differences:")
        print(f"   Exact Match F1:   {report['comparison']['exact_match_f1_diff']:+.4f}")
        print(f"   Partial Match F1: {report['comparison']['partial_match_f1_diff']:+.4f}")
        print(f"   Macro F1:         {report['comparison']['macro_f1_diff']:+.4f}")
        print(f"   Micro F1:         {report['comparison']['micro_f1_diff']:+.4f}")
        
        print("\n" + "="*70)


def main():
    """
    Main function to compare models.
    """
    logger.info("="*70)
    logger.info("NER Model Comparison")
    logger.info("="*70)
    
    # Setup paths
    models_dir = Path(MODELS_DIR)
    output_dir = Path(OUTPUT_DIR)
    
    test_data_path = models_dir / "test_data.json"
    custom_model_path = models_dir / "custom_ner_model"
    
    # Check if files exist
    if not test_data_path.exists():
        logger.error(f"Test data not found: {test_data_path}")
        logger.error("Please run 'python create_training_data.py' first")
        return
    
    if not custom_model_path.exists():
        logger.error(f"Custom model not found: {custom_model_path}")
        logger.error("Please run 'python ner_trainer.py' first")
        return
    
    # Initialize comparison
    comparison = ModelComparison()
    
    # Load test data
    comparison.load_test_data(test_data_path)
    
    # Load models
    logger.info("\n" + "="*70)
    logger.info("Loading Models")
    logger.info("="*70)
    
    comparison.load_model("spaCy Multilingual (xx_ent_wiki_sm)", "xx_ent_wiki_sm")
    comparison.load_model("Custom Trained Model", str(custom_model_path))
    
    # Evaluate both models
    logger.info("\n" + "="*70)
    logger.info("Running Evaluations")
    logger.info("="*70)
    
    comparison.evaluate_model("spaCy Multilingual (xx_ent_wiki_sm)")
    comparison.evaluate_model("Custom Trained Model")
    
    # Generate comparison report
    logger.info("\n" + "="*70)
    logger.info("Generating Comparison Report")
    logger.info("="*70)
    
    report = comparison.generate_comparison_report()
    
    # Save reports
    output_dir.mkdir(exist_ok=True, parents=True)
    
    json_path = output_dir / "ner_evaluation_comparison.json"
    html_path = output_dir / "ner_evaluation_comparison.html"
    
    comparison.save_json_report(report, json_path)
    comparison.generate_html_report(report, html_path)
    
    # Print summary
    comparison.print_comparison_summary(report)
    
    logger.info("\n" + "="*70)
    logger.info("✅ Comparison Complete!")
    logger.info("="*70)
    logger.info(f"\nReports saved:")
    logger.info(f"  📄 JSON: {json_path}")
    logger.info(f"  📊 HTML: {html_path}")
    logger.info(f"\nOpen the HTML file in your browser to view the interactive report.")


if __name__ == "__main__":
    main()
