"""
Metrics Collection and Reporting Module
Author: Ahmad Reza Adrian

This module collects and reports detailed metrics for the NER pipeline.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from collections import Counter
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collects and reports metrics for the entire NER pipeline.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics = {
            'pipeline_info': {},
            'data_loading': {},
            'preprocessing': {},
            'ner_extraction': {},
            'relation_extraction': {},
            'knowledge_graph': {},
            'visualization': {},
            'execution_time': {},
            'summary': {}
        }
        self.start_time = None
        self.stage_times = {}
    
    def start_pipeline(self, config: Dict[str, Any]):
        """
        Record pipeline start and configuration.
        
        Args:
            config: Pipeline configuration dictionary
        """
        self.start_time = datetime.now()
        self.metrics['pipeline_info'] = {
            'start_time': self.start_time.isoformat(),
            'configuration': config
        }
        logger.info("Metrics collection started")
    
    def record_data_loading(self, df: pd.DataFrame):
        """
        Record data loading metrics.
        
        Args:
            df: Loaded DataFrame
        """
        stage_start = datetime.now()
        
        # Count records by source
        source_counts = {}
        if 'source_dataset' in df.columns:
            source_counts = df['source_dataset'].value_counts().to_dict()
        
        self.metrics['data_loading'] = {
            'total_documents': len(df),
            'columns': list(df.columns),
            'source_distribution': source_counts,
            'has_source_tracking': 'source_dataset' in df.columns,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        
        self.stage_times['data_loading'] = (datetime.now() - stage_start).total_seconds()
        logger.info("Data loading metrics recorded")
    
    def record_preprocessing(self, df: pd.DataFrame):
        """
        Record preprocessing metrics.
        
        Args:
            df: Preprocessed DataFrame
        """
        stage_start = datetime.now()
        
        # Calculate text statistics
        text_col = 'normalized_text' if 'normalized_text' in df.columns else 'text'
        
        self.metrics['preprocessing'] = {
            'total_documents': len(df),
            'total_sentences': int(df['sentence_count'].sum()) if 'sentence_count' in df.columns else 0,
            'avg_sentences_per_doc': float(df['sentence_count'].mean()) if 'sentence_count' in df.columns else 0,
            'avg_text_length': float(df[text_col].str.len().mean()) if text_col in df.columns else 0,
            'min_text_length': int(df[text_col].str.len().min()) if text_col in df.columns else 0,
            'max_text_length': int(df[text_col].str.len().max()) if text_col in df.columns else 0,
            'total_characters': int(df[text_col].str.len().sum()) if text_col in df.columns else 0
        }
        
        # Add source-specific stats if available
        if 'source_dataset' in df.columns:
            source_stats = {}
            for source in df['source_dataset'].unique():
                source_df = df[df['source_dataset'] == source]
                source_stats[source] = {
                    'documents': len(source_df),
                    'sentences': int(source_df['sentence_count'].sum()) if 'sentence_count' in source_df.columns else 0,
                    'avg_text_length': float(source_df[text_col].str.len().mean()) if text_col in source_df.columns else 0
                }
            self.metrics['preprocessing']['source_statistics'] = source_stats
        
        self.stage_times['preprocessing'] = (datetime.now() - stage_start).total_seconds()
        logger.info("Preprocessing metrics recorded")
    
    def record_ner_extraction(self, df: pd.DataFrame):
        """
        Record NER extraction metrics.
        
        Args:
            df: DataFrame with entities
        """
        stage_start = datetime.now()
        
        # Collect all entities
        all_entities = []
        for entities in df['entities']:
            all_entities.extend(entities)
        
        # Entity type distribution
        entity_types = Counter(e['type'] for e in all_entities)
        
        # Entity extraction method distribution
        entity_methods = Counter(e.get('method', 'unknown') for e in all_entities)
        
        # Unique entities
        unique_entities = len(set(e['text'].lower() for e in all_entities))
        
        # Average entities per document
        avg_entities = df['entity_count'].mean() if 'entity_count' in df.columns else 0
        
        self.metrics['ner_extraction'] = {
            'total_entities': len(all_entities),
            'unique_entities': unique_entities,
            'avg_entities_per_doc': float(avg_entities),
            'min_entities_per_doc': int(df['entity_count'].min()) if 'entity_count' in df.columns else 0,
            'max_entities_per_doc': int(df['entity_count'].max()) if 'entity_count' in df.columns else 0,
            'entity_type_distribution': dict(entity_types),
            'entity_method_distribution': dict(entity_methods),
            'documents_with_entities': int((df['entity_count'] > 0).sum()) if 'entity_count' in df.columns else 0,
            'documents_without_entities': int((df['entity_count'] == 0).sum()) if 'entity_count' in df.columns else 0
        }
        
        # Add top entities
        entity_counter = Counter(e['text'] for e in all_entities)
        top_entities = [{'entity': k, 'count': v} for k, v in entity_counter.most_common(20)]
        self.metrics['ner_extraction']['top_20_entities'] = top_entities
        
        # Source-specific stats if available
        if 'source_dataset' in df.columns:
            source_stats = {}
            for source in df['source_dataset'].unique():
                source_df = df[df['source_dataset'] == source]
                source_entities = []
                for entities in source_df['entities']:
                    source_entities.extend(entities)
                
                source_stats[source] = {
                    'total_entities': len(source_entities),
                    'unique_entities': len(set(e['text'].lower() for e in source_entities)),
                    'avg_entities_per_doc': float(source_df['entity_count'].mean()) if 'entity_count' in source_df.columns else 0,
                    'entity_types': dict(Counter(e['type'] for e in source_entities))
                }
            self.metrics['ner_extraction']['source_statistics'] = source_stats
        
        self.stage_times['ner_extraction'] = (datetime.now() - stage_start).total_seconds()
        logger.info("NER extraction metrics recorded")
    
    def record_relation_extraction(self, df: pd.DataFrame):
        """
        Record relation extraction metrics.
        
        Args:
            df: DataFrame with relations
        """
        stage_start = datetime.now()
        
        # Collect all relations
        all_relations = []
        for relations in df['relations']:
            all_relations.extend(relations)
        
        # Relation type distribution
        relation_types = Counter(r['relation'] for r in all_relations)
        
        # Average confidence
        avg_confidence = sum(r.get('confidence', 1.0) for r in all_relations) / len(all_relations) if all_relations else 0
        
        # Count relations with dynamic labels
        dynamic_labels_count = sum(1 for r in all_relations if r.get('dynamic_label'))
        
        # Entity type pairs
        entity_pairs = Counter((r['subject_type'], r['object_type']) for r in all_relations if 'subject_type' in r and 'object_type' in r)
        
        self.metrics['relation_extraction'] = {
            'total_relations': len(all_relations),
            'avg_relations_per_doc': float(df['relation_count'].mean()) if 'relation_count' in df.columns else 0,
            'min_relations_per_doc': int(df['relation_count'].min()) if 'relation_count' in df.columns else 0,
            'max_relations_per_doc': int(df['relation_count'].max()) if 'relation_count' in df.columns else 0,
            'relation_type_distribution': dict(relation_types),
            'avg_confidence': float(avg_confidence),
            'relations_with_dynamic_labels': dynamic_labels_count,
            'dynamic_label_percentage': float(dynamic_labels_count / len(all_relations) * 100) if all_relations else 0,
            'documents_with_relations': int((df['relation_count'] > 0).sum()) if 'relation_count' in df.columns else 0,
            'documents_without_relations': int((df['relation_count'] == 0).sum()) if 'relation_count' in df.columns else 0,
            'top_entity_type_pairs': [{'pair': f"{k[0]}-{k[1]}", 'count': v} for k, v in entity_pairs.most_common(10)]
        }
        
        # Top relation patterns
        relation_patterns = Counter()
        for r in all_relations:
            pattern = f"{r['subject']} -{r['relation']}-> {r['object']}"
            relation_patterns[pattern] += 1
        
        self.metrics['relation_extraction']['top_10_relation_patterns'] = [
            {'pattern': k, 'count': v} for k, v in relation_patterns.most_common(10)
        ]
        
        # Source-specific stats if available
        if 'source_dataset' in df.columns:
            source_stats = {}
            for source in df['source_dataset'].unique():
                source_df = df[df['source_dataset'] == source]
                source_relations = []
                for relations in source_df['relations']:
                    source_relations.extend(relations)
                
                source_stats[source] = {
                    'total_relations': len(source_relations),
                    'avg_relations_per_doc': float(source_df['relation_count'].mean()) if 'relation_count' in source_df.columns else 0,
                    'relation_types': dict(Counter(r['relation'] for r in source_relations))
                }
            self.metrics['relation_extraction']['source_statistics'] = source_stats
        
        self.stage_times['relation_extraction'] = (datetime.now() - stage_start).total_seconds()
        logger.info("Relation extraction metrics recorded")
    
    def record_knowledge_graph(self, knowledge_graph):
        """
        Record knowledge graph metrics.
        
        Args:
            knowledge_graph: KnowledgeGraph instance
        """
        stage_start = datetime.now()
        
        # Get graph statistics
        stats = knowledge_graph.get_statistics()
        
        # Add additional graph metrics
        import networkx as nx
        
        # Degree centrality
        degree_centrality = nx.degree_centrality(knowledge_graph.graph)
        top_central_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Clustering coefficient
        clustering = nx.clustering(knowledge_graph.graph.to_undirected())
        avg_clustering = sum(clustering.values()) / len(clustering) if clustering else 0
        
        # Connected components
        weak_components = list(nx.weakly_connected_components(knowledge_graph.graph))
        largest_component_size = len(max(weak_components, key=len)) if weak_components else 0
        
        self.metrics['knowledge_graph'] = {
            'total_nodes': stats['total_nodes'],
            'total_edges': stats['total_edges'],
            'density': float(stats['density']),
            'is_weakly_connected': stats['is_connected'],
            'entity_type_distribution': stats['entity_type_distribution'],
            'relation_type_distribution': stats['relation_type_distribution'],
            'avg_degree': float(sum(dict(knowledge_graph.graph.degree()).values()) / stats['total_nodes']) if stats['total_nodes'] > 0 else 0,
            'avg_clustering_coefficient': float(avg_clustering),
            'number_of_components': len(weak_components),
            'largest_component_size': largest_component_size,
            'top_10_central_nodes': [{'node': k, 'centrality': float(v)} for k, v in top_central_nodes],
            'top_entities_by_degree': stats.get('top_entities', [])
        }
        
        self.stage_times['knowledge_graph'] = (datetime.now() - stage_start).total_seconds()
        logger.info("Knowledge graph metrics recorded")
    
    def record_visualization(self, viz_path: str, node_count: int, edge_count: int):
        """
        Record visualization metrics.
        
        Args:
            viz_path: Path to visualization file
            node_count: Number of nodes visualized
            edge_count: Number of edges visualized
        """
        stage_start = datetime.now()
        
        viz_path_obj = Path(viz_path)
        file_size = viz_path_obj.stat().st_size / (1024 * 1024) if viz_path_obj.exists() else 0
        
        self.metrics['visualization'] = {
            'output_file': str(viz_path),
            'file_size_mb': float(file_size),
            'nodes_visualized': node_count,
            'edges_visualized': edge_count,
            'visualization_type': 'interactive_html'
        }
        
        self.stage_times['visualization'] = (datetime.now() - stage_start).total_seconds()
        logger.info("Visualization metrics recorded")
    
    def finalize_metrics(self):
        """Calculate final summary metrics."""
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds() if self.start_time else 0
        
        self.metrics['execution_time'] = {
            'total_seconds': float(total_time),
            'total_minutes': float(total_time / 60),
            'stage_breakdown_seconds': {k: float(v) for k, v in self.stage_times.items()},
            'stage_breakdown_percentage': {
                k: float(v / total_time * 100) if total_time > 0 else 0 
                for k, v in self.stage_times.items()
            }
        }
        
        self.metrics['pipeline_info']['end_time'] = end_time.isoformat()
        self.metrics['pipeline_info']['duration_seconds'] = float(total_time)
        
        # Summary statistics
        self.metrics['summary'] = {
            'pipeline_status': 'completed',
            'total_documents_processed': self.metrics['data_loading'].get('total_documents', 0),
            'total_entities_extracted': self.metrics['ner_extraction'].get('total_entities', 0),
            'unique_entities': self.metrics['ner_extraction'].get('unique_entities', 0),
            'total_relations_extracted': self.metrics['relation_extraction'].get('total_relations', 0),
            'knowledge_graph_nodes': self.metrics['knowledge_graph'].get('total_nodes', 0),
            'knowledge_graph_edges': self.metrics['knowledge_graph'].get('total_edges', 0),
            'total_execution_time_minutes': float(total_time / 60),
            'avg_processing_time_per_doc_seconds': float(total_time / self.metrics['data_loading'].get('total_documents', 1))
        }
        
        logger.info("Pipeline metrics finalized")
    
    def save_metrics(self, output_path: str):
        """
        Save metrics to JSON file.
        
        Args:
            output_path: Path to save metrics JSON
        """
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Metrics saved to {output_path}")
    
    def print_summary(self):
        """Print a human-readable summary of metrics."""
        print("\n" + "=" * 80)
        print("PIPELINE METRICS SUMMARY")
        print("=" * 80)
        
        summary = self.metrics['summary']
        print(f"\n📊 Overall Statistics:")
        print(f"  Status: {summary['pipeline_status'].upper()}")
        print(f"  Execution Time: {summary['total_execution_time_minutes']:.2f} minutes")
        print(f"  Documents Processed: {summary['total_documents_processed']}")
        print(f"  Avg Time per Document: {summary['avg_processing_time_per_doc_seconds']:.2f} seconds")
        
        print(f"\n🏷️  Entity Extraction:")
        print(f"  Total Entities: {summary['total_entities_extracted']}")
        print(f"  Unique Entities: {summary['unique_entities']}")
        print(f"  Avg per Document: {self.metrics['ner_extraction']['avg_entities_per_doc']:.2f}")
        
        print(f"\n🔗 Relation Extraction:")
        print(f"  Total Relations: {summary['total_relations_extracted']}")
        print(f"  Avg per Document: {self.metrics['relation_extraction']['avg_relations_per_doc']:.2f}")
        print(f"  Avg Confidence: {self.metrics['relation_extraction']['avg_confidence']:.2f}")
        
        print(f"\n📈 Knowledge Graph:")
        print(f"  Nodes: {summary['knowledge_graph_nodes']}")
        print(f"  Edges: {summary['knowledge_graph_edges']}")
        print(f"  Density: {self.metrics['knowledge_graph']['density']:.4f}")
        print(f"  Avg Degree: {self.metrics['knowledge_graph']['avg_degree']:.2f}")
        
        print(f"\n⏱️  Stage Execution Times:")
        for stage, seconds in self.stage_times.items():
            percentage = self.metrics['execution_time']['stage_breakdown_percentage'][stage]
            print(f"  {stage:25s}: {seconds:6.2f}s ({percentage:5.1f}%)")
        
        print("\n" + "=" * 80 + "\n")


def generate_metrics_report(metrics_path: str, output_html_path: str = None):
    """
    Generate an HTML report from metrics JSON.
    
    Args:
        metrics_path: Path to metrics JSON file
        output_html_path: Optional path for HTML report
    """
    with open(metrics_path, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    if output_html_path is None:
        output_html_path = Path(metrics_path).parent / 'metrics_report.html'
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pipeline Metrics Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .metric-card h3 {{ margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.9; }}
        .metric-card .value {{ font-size: 2em; font-weight: bold; }}
        .metric-card .unit {{ font-size: 0.8em; opacity: 0.8; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; font-weight: 600; }}
        tr:hover {{ background: #f5f5f5; }}
        .chart-bar {{ background: #3498db; height: 20px; border-radius: 3px; margin: 5px 0; }}
        .status-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; background: #27ae60; color: white; font-weight: bold; }}
        .section {{ margin: 30px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Wayang NER Pipeline - Metrics Report</h1>
        
        <div class="section">
            <h2>📊 Pipeline Summary</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>Status</h3>
                    <div class="value">✓</div>
                    <div class="unit">COMPLETED</div>
                </div>
                <div class="metric-card">
                    <h3>Execution Time</h3>
                    <div class="value">{metrics['summary']['total_execution_time_minutes']:.2f}</div>
                    <div class="unit">minutes</div>
                </div>
                <div class="metric-card">
                    <h3>Documents</h3>
                    <div class="value">{metrics['summary']['total_documents_processed']}</div>
                    <div class="unit">processed</div>
                </div>
                <div class="metric-card">
                    <h3>Entities</h3>
                    <div class="value">{metrics['summary']['total_entities_extracted']}</div>
                    <div class="unit">extracted</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🏷️ Named Entity Recognition</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Entities</td><td>{metrics['ner_extraction']['total_entities']}</td></tr>
                <tr><td>Unique Entities</td><td>{metrics['ner_extraction']['unique_entities']}</td></tr>
                <tr><td>Avg per Document</td><td>{metrics['ner_extraction']['avg_entities_per_doc']:.2f}</td></tr>
                <tr><td>Documents with Entities</td><td>{metrics['ner_extraction']['documents_with_entities']}</td></tr>
            </table>
            
            <h3>Entity Type Distribution</h3>
            <table>
                <tr><th>Type</th><th>Count</th><th>Percentage</th></tr>
"""
    
    total_entities = metrics['ner_extraction']['total_entities']
    for entity_type, count in sorted(metrics['ner_extraction']['entity_type_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_entities * 100) if total_entities > 0 else 0
        html_content += f"                <tr><td>{entity_type}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>\n"
    
    html_content += """            </table>
        </div>
        
        <div class="section">
            <h2>🔗 Relation Extraction</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
"""
    
    html_content += f"""                <tr><td>Total Relations</td><td>{metrics['relation_extraction']['total_relations']}</td></tr>
                <tr><td>Avg per Document</td><td>{metrics['relation_extraction']['avg_relations_per_doc']:.2f}</td></tr>
                <tr><td>Avg Confidence</td><td>{metrics['relation_extraction']['avg_confidence']:.2f}</td></tr>
                <tr><td>With Dynamic Labels</td><td>{metrics['relation_extraction']['relations_with_dynamic_labels']} ({metrics['relation_extraction']['dynamic_label_percentage']:.1f}%)</td></tr>
            </table>
            
            <h3>Relation Type Distribution</h3>
            <table>
                <tr><th>Relation</th><th>Count</th><th>Percentage</th></tr>
"""
    
    total_relations = metrics['relation_extraction']['total_relations']
    for rel_type, count in sorted(metrics['relation_extraction']['relation_type_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_relations * 100) if total_relations > 0 else 0
        html_content += f"                <tr><td>{rel_type}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>\n"
    
    html_content += f"""            </table>
        </div>
        
        <div class="section">
            <h2>📈 Knowledge Graph</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <h3>Nodes</h3>
                    <div class="value">{metrics['knowledge_graph']['total_nodes']}</div>
                </div>
                <div class="metric-card">
                    <h3>Edges</h3>
                    <div class="value">{metrics['knowledge_graph']['total_edges']}</div>
                </div>
                <div class="metric-card">
                    <h3>Density</h3>
                    <div class="value">{metrics['knowledge_graph']['density']:.4f}</div>
                </div>
                <div class="metric-card">
                    <h3>Avg Degree</h3>
                    <div class="value">{metrics['knowledge_graph']['avg_degree']:.2f}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>⏱️ Execution Time Breakdown</h2>
            <table>
                <tr><th>Stage</th><th>Time (seconds)</th><th>Percentage</th></tr>
"""
    
    for stage, seconds in metrics['execution_time']['stage_breakdown_seconds'].items():
        percentage = metrics['execution_time']['stage_breakdown_percentage'][stage]
        html_content += f"                <tr><td>{stage.replace('_', ' ').title()}</td><td>{seconds:.2f}s</td><td>{percentage:.1f}%</td></tr>\n"
    
    html_content += f"""            </table>
        </div>
        
        <div class="section">
            <p style="text-align: center; color: #7f8c8d; margin-top: 50px;">
                Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                Wayang NER and Knowledge Graph Builder
            </p>
        </div>
    </div>
</body>
</html>"""
    
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"HTML report generated: {output_html_path}")
    return output_html_path
