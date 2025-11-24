"""
Main Pipeline for Wayang NER and Knowledge Graph Builder
Author: Ahmad Reza Adrian

This module orchestrates the complete pipeline from data loading
to knowledge graph construction and visualization.
"""

import logging
import argparse
from pathlib import Path
import json

import pandas as pd

from config import DATASET_PATH, DATASET_PATHS, DATASET_COLUMNS, OUTPUT_DIR, TEXT_COLUMN
from preprocessing import TextPreprocessor, load_dataset, load_multiple_datasets
from ner_extraction import WayangNER
from relation_extraction import RelationExtractor
from graph_builder import KnowledgeGraph
from visualization import GraphVisualizer
from metrics import MetricsCollector, generate_metrics_report

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WayangPipeline:
    """
    End-to-end pipeline for Wayang NER and Knowledge Graph construction.
    """
    
    def __init__(self, 
                 dataset_path: str = None,
                 dataset_paths: list = None,
                 use_multiple_datasets: bool = True,
                 output_dir: str = None,
                 ner_model_type: str = "spacy"):
        """
        Initialize pipeline.
        
        Args:
            dataset_path: Path to single dataset (deprecated, use dataset_paths)
            dataset_paths: List of paths to datasets (default: all configured datasets)
            use_multiple_datasets: Whether to load multiple datasets (default: True)
            output_dir: Directory for output files
            ner_model_type: Type of NER model ('spacy' or 'transformers')
        """
        self.dataset_path = dataset_path or DATASET_PATH
        self.dataset_paths = dataset_paths or DATASET_PATHS
        self.use_multiple_datasets = use_multiple_datasets
        self.output_dir = Path(output_dir or OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize components
        logger.info("Initializing pipeline components...")
        self.preprocessor = TextPreprocessor()
        self.ner = WayangNER(model_type=ner_model_type)
        self.relation_extractor = RelationExtractor()
        self.knowledge_graph = KnowledgeGraph()
        self.visualizer = GraphVisualizer()
        self.metrics = MetricsCollector()
        
        self.df = None
    
    def load_data(self):
        """Load the wayang dataset(s)."""
        logger.info("=" * 60)
        logger.info("STEP 1: Loading Dataset(s)")
        logger.info("=" * 60)
        
        if self.use_multiple_datasets:
            # Load and merge multiple datasets
            self.df = load_multiple_datasets(
                [str(path) for path in self.dataset_paths],
                DATASET_COLUMNS
            )
            logger.info(f"Loaded {len(self.df)} documents from {len(self.dataset_paths)} datasets")
        else:
            # Load single dataset (legacy behavior)
            self.df = load_dataset(str(self.dataset_path))
            # Add source_dataset column for consistency
            self.df['source_dataset'] = 'single_dataset'
            # Rename text column to 'text' for consistency
            if TEXT_COLUMN in self.df.columns:
                self.df['text'] = self.df[TEXT_COLUMN]
            logger.info(f"Loaded {len(self.df)} documents from single dataset")
        
        # Record metrics
        self.metrics.record_data_loading(self.df)
        
        return self.df
    
    def preprocess(self):
        """Preprocess all texts."""
        logger.info("=" * 60)
        logger.info("STEP 2: Preprocessing")
        logger.info("=" * 60)
        
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Use 'text' column which is now standardized across all datasets
        text_col = 'text' if 'text' in self.df.columns else TEXT_COLUMN
        self.df = self.preprocessor.preprocess_dataframe(self.df, text_col)
        
        # Save preprocessed data
        preprocessed_path = self.output_dir / "preprocessed_data.csv"
        self.df.to_csv(preprocessed_path, index=False, encoding='utf-8')
        logger.info(f"Preprocessed data saved to {preprocessed_path}")
        
        # Record metrics
        self.metrics.record_preprocessing(self.df)
        
        return self.df
    
    def extract_entities(self):
        """Extract named entities."""
        logger.info("=" * 60)
        logger.info("STEP 3: Named Entity Recognition")
        logger.info("=" * 60)
        
        if self.df is None or 'normalized_text' not in self.df.columns:
            raise ValueError("Data not preprocessed. Call preprocess() first.")
        
        self.df = self.ner.process_dataframe(self.df, text_column='normalized_text')
        
        # Log statistics
        total_entities = self.df['entity_count'].sum()
        logger.info(f"Total entities extracted: {total_entities}")
        
        # Entity type distribution
        all_entities = []
        for entities in self.df['entities']:
            all_entities.extend(entities)
        
        entity_types = {}
        for entity in all_entities:
            etype = entity['type']
            entity_types[etype] = entity_types.get(etype, 0) + 1
        
        logger.info("Entity type distribution:")
        for etype, count in sorted(entity_types.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {etype}: {count}")
        
        # Record metrics
        self.metrics.record_ner_extraction(self.df)
        
        return self.df
    
    def extract_relations(self):
        """Extract relations between entities."""
        logger.info("=" * 60)
        logger.info("STEP 4: Relation Extraction")
        logger.info("=" * 60)
        
        if self.df is None or 'entities' not in self.df.columns:
            raise ValueError("Entities not extracted. Call extract_entities() first.")
        
        self.df = self.relation_extractor.process_dataframe(
            self.df,
            text_column='normalized_text',
            entities_column='entities'
        )
        
        # Log statistics
        total_relations = self.df['relation_count'].sum()
        logger.info(f"Total relations extracted: {total_relations}")
        
        # Relation type distribution
        all_relations = []
        for relations in self.df['relations']:
            all_relations.extend(relations)
        
        relation_types = {}
        for relation in all_relations:
            rtype = relation['relation']
            relation_types[rtype] = relation_types.get(rtype, 0) + 1
        
        logger.info("Relation type distribution:")
        for rtype, count in sorted(relation_types.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {rtype}: {count}")
        
        # Record metrics
        self.metrics.record_relation_extraction(self.df)
        
        return self.df
    
    def build_knowledge_graph(self):
        """Build the knowledge graph."""
        logger.info("=" * 60)
        logger.info("STEP 5: Knowledge Graph Construction")
        logger.info("=" * 60)
        
        if self.df is None or 'relations' not in self.df.columns:
            raise ValueError("Relations not extracted. Call extract_relations() first.")
        
        self.knowledge_graph.build_from_dataframe(
            self.df,
            entities_column='entities',
            relations_column='relations'
        )
        
        # Get and log statistics
        stats = self.knowledge_graph.get_statistics()
        logger.info(f"Knowledge Graph Statistics:")
        logger.info(f"  Nodes: {stats['total_nodes']}")
        logger.info(f"  Edges: {stats['total_edges']}")
        logger.info(f"  Density: {stats['density']:.4f}")
        logger.info(f"  Is connected: {stats['is_connected']}")
        
        # Save graph to JSON
        json_path = self.output_dir / "knowledge_graph.json"
        self.knowledge_graph.to_json(str(json_path))
        
        # Record metrics
        self.metrics.record_knowledge_graph(self.knowledge_graph)
        
        return self.knowledge_graph
    
    def visualize_graph(self, max_nodes: int = 100, light_mode: bool = True):
        """Create interactive visualization.
        
        Args:
            max_nodes: Maximum nodes to display
            light_mode: If True, uses optimized 1-level visualization (recommended for large graphs)
        """
        logger.info("=" * 60)
        logger.info("STEP 6: Graph Visualization")
        logger.info("=" * 60)
        
        if self.knowledge_graph is None or self.knowledge_graph.graph.number_of_nodes() == 0:
            raise ValueError("Knowledge graph not built. Call build_knowledge_graph() first.")
        
        total_nodes = self.knowledge_graph.graph.number_of_nodes()
        total_edges = self.knowledge_graph.graph.number_of_edges()
        
        logger.info(f"Total graph size: {total_nodes} nodes, {total_edges} edges")
        
        # Generate visualization
        html_path = self.output_dir / "knowledge_graph.html"
        
        if light_mode and total_nodes > 50:
            # Use hub visualization for large graphs
            logger.info("Using optimized hub visualization (1-level connections)...")
            self.visualizer.visualize_hub_network(
                self.knowledge_graph,
                output_path=str(html_path),
                top_entities=max_nodes
            )
        else:
            # Use standard visualization
            self.visualizer.visualize_from_knowledge_graph(
                self.knowledge_graph,
                output_path=str(html_path),
                max_nodes=max_nodes,
                one_level_per_node=light_mode
            )
        
        logger.info(f"Visualization saved to {html_path}")
        logger.info(f"Open {html_path} in a web browser to explore the graph")
        
        # Record metrics
        self.metrics.record_visualization(
            str(html_path),
            self.knowledge_graph.graph.number_of_nodes(),
            self.knowledge_graph.graph.number_of_edges()
        )
        
        return str(html_path)
    
    def run_full_pipeline(self, max_vis_nodes: int = 100, light_mode: bool = True):
        """
        Run the complete pipeline.
        
        Args:
            max_vis_nodes: Maximum nodes to display in visualization
            light_mode: Use optimized visualization (recommended for large graphs)
        """
        logger.info("=" * 60)
        logger.info("WAYANG NER AND KNOWLEDGE GRAPH BUILDER")
        logger.info("=" * 60)
        
        # Start metrics collection
        self.metrics.start_pipeline({
            'use_multiple_datasets': self.use_multiple_datasets,
            'ner_model_type': self.ner.model_type,
            'max_vis_nodes': max_vis_nodes,
            'light_mode': light_mode
        })
        
        # Run all steps
        self.load_data()
        self.preprocess()
        self.extract_entities()
        self.extract_relations()
        self.build_knowledge_graph()
        self.visualize_graph(max_nodes=max_vis_nodes, light_mode=light_mode)
        
        # Finalize and save metrics
        self.metrics.finalize_metrics()
        
        metrics_json_path = self.output_dir / "pipeline_metrics.json"
        self.metrics.save_metrics(str(metrics_json_path))
        
        # Generate HTML report
        metrics_html_path = self.output_dir / "pipeline_metrics.html"
        generate_metrics_report(str(metrics_json_path), str(metrics_html_path))
        
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info(f"Output files saved to: {self.output_dir}")
        logger.info(f"  - preprocessed_data.csv")
        logger.info(f"  - knowledge_graph.json")
        logger.info(f"  - knowledge_graph.html")
        logger.info(f"  - pipeline_metrics.json")
        logger.info(f"  - pipeline_metrics.html")
        
        # Print metrics summary
        self.metrics.print_summary()
    
    def get_entity_info(self, entity_name: str):
        """
        Get detailed information about an entity.
        
        Args:
            entity_name: Name of the entity
            
        Returns:
            Dictionary with entity information
        """
        return self.knowledge_graph.get_entity_info(entity_name)
    
    def create_subgraph_visualization(self, entity_name: str, depth: int = 1):
        """
        Create visualization of subgraph around an entity.
        
        Args:
            entity_name: Central entity
            depth: Neighborhood depth
            
        Returns:
            Path to HTML file
        """
        safe_name = entity_name.replace(' ', '_').lower()
        output_path = self.output_dir / f"subgraph_{safe_name}.html"
        
        return self.visualizer.create_subgraph_visualization(
            self.knowledge_graph,
            entity_name,
            depth=depth,
            output_path=str(output_path)
        )


def main():
    """
    Main function for command-line usage.
    """
    parser = argparse.ArgumentParser(description="Wayang NER and Knowledge Graph Builder")
    parser.add_argument('--dataset', type=str, default=None,
                       help='Path to single dataset (legacy mode)')
    parser.add_argument('--datasets', nargs='+', default=None,
                       help='Paths to multiple datasets')
    parser.add_argument('--single-dataset', action='store_true',
                       help='Use single dataset mode (default: multiple datasets)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output directory')
    parser.add_argument('--ner-model', type=str, default='spacy',
                       choices=['spacy', 'transformers'],
                       help='NER model type')
    parser.add_argument('--max-nodes', type=int, default=100,
                       help='Maximum nodes in visualization')
    parser.add_argument('--light-mode', action='store_true', default=True,
                       help='Use optimized visualization (default: True)')
    parser.add_argument('--full-mode', action='store_true',
                       help='Show all connections (may be slow for large graphs)')
    
    args = parser.parse_args()
    
    # Determine light mode
    light_mode = not args.full_mode
    
    # Determine dataset mode
    use_multiple = not args.single_dataset
    
    # Create and run pipeline
    pipeline = WayangPipeline(
        dataset_path=args.dataset,
        dataset_paths=args.datasets,
        use_multiple_datasets=use_multiple,
        output_dir=args.output,
        ner_model_type=args.ner_model
    )
    
    pipeline.run_full_pipeline(max_vis_nodes=args.max_nodes, light_mode=light_mode)


if __name__ == "__main__":
    main()
