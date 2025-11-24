"""
Quick test to regenerate knowledge graph with dynamic labels
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from preprocessing import TextPreprocessor, load_dataset
from ner_extraction import WayangNER
from relation_extraction import RelationExtractor
from graph_builder import KnowledgeGraph
from visualization import GraphVisualizer
import pandas as pd

def quick_test():
    """Test with a small subset of data."""
    
    print("\n" + "="*70)
    print("QUICK TEST: Dynamic Labels on Wayang Dataset")
    print("="*70)
    
    # Load just first 10 documents for quick test
    print("\n📂 Loading dataset...")
    df = load_dataset('wayang.csv')
    df_sample = df.head(10).copy()
    print(f"   Using {len(df_sample)} documents for testing")
    
    # Preprocess
    print("\n🔧 Preprocessing...")
    preprocessor = TextPreprocessor()
    df_sample = preprocessor.preprocess_dataframe(df_sample, 'isi_teks')
    print(f"   Preprocessed {df_sample['sentence_count'].sum()} sentences")
    
    # Extract entities
    print("\n🏷️  Extracting entities...")
    ner_extractor = WayangNER(model_type='spacy', model_name='xx_ent_wiki_sm')
    df_sample = ner_extractor.process_dataframe(df_sample, 'normalized_text')
    total_entities = df_sample['entity_count'].sum()
    print(f"   Extracted {total_entities} entities")
    
    # Extract relations WITH DYNAMIC LABELS
    print("\n🔗 Extracting relations with dynamic labels...")
    rel_extractor = RelationExtractor(use_dynamic_labels=True)  # Enable dynamic labels!
    df_sample = rel_extractor.process_dataframe(df_sample, 'normalized_text', 'entities')
    total_relations = df_sample['relation_count'].sum()
    print(f"   Extracted {total_relations} relations")
    
    # Check if dynamic labels were generated
    sample_relations = []
    for relations in df_sample['relations']:
        if relations:
            sample_relations.extend(relations[:2])  # Get first 2 from each doc
            if len(sample_relations) >= 5:
                break
    
    print("\n✨ Sample Dynamic Labels:")
    for i, rel in enumerate(sample_relations[:5], 1):
        dynamic_label = rel.get('dynamic_label', 'N/A')
        static_label = rel.get('relation', 'N/A')
        print(f"   {i}. {rel['subject']} → {rel['object']}")
        print(f"      Static: {static_label}")
        print(f"      Dynamic: {dynamic_label if dynamic_label else '(none)'}")
    
    # Build knowledge graph
    print("\n🕸️  Building knowledge graph...")
    kg = KnowledgeGraph()
    kg.build_from_dataframe(df_sample, 'entities', 'relations')
    print(f"   Graph: {kg.graph.number_of_nodes()} nodes, {kg.graph.number_of_edges()} edges")
    
    # Count how many edges have dynamic labels
    edges_with_dynamic = 0
    for _, _, data in kg.graph.edges(data=True):
        if data.get('dynamic_labels'):
            edges_with_dynamic += 1
    
    print(f"   Edges with dynamic labels: {edges_with_dynamic}/{kg.graph.number_of_edges()}")
    
    # Visualize
    print("\n🎨 Creating visualization...")
    visualizer = GraphVisualizer()
    output_file = 'output/quick_test_dynamic.html'
    visualizer.visualize_from_knowledge_graph(
        kg, 
        output_file,
        max_nodes=30,  # Limit for readability
        one_level_per_node=True  # Light mode
    )
    print(f"   ✅ Visualization saved: {output_file}")
    
    # Show some edge examples with dynamic labels
    print("\n📊 Sample Edge Labels in Graph:")
    edge_count = 0
    for source, target, data in kg.graph.edges(data=True):
        if edge_count >= 8:
            break
        dynamic_labels = data.get('dynamic_labels', [])
        if dynamic_labels:  # Only show edges with dynamic labels
            static_labels = data.get('relations', [])
            print(f"\n   {source} → {target}")
            print(f"      Static: {', '.join(static_labels)}")
            print(f"      ✨ Dynamic: {', '.join(dynamic_labels)}")
            edge_count += 1
    
    print("\n" + "="*70)
    print("✅ QUICK TEST COMPLETE!")
    print("="*70)
    print(f"\nOpen {output_file} in your browser to see dynamic labels in action!")
    print("Dynamic labels are extracted from the actual text context using:")
    print("  • Indonesian action verbs (membunuh, menikah, memerintah, etc.)")
    print("  • Relationship nouns (putra, murid, raja, musuh, etc.)")
    print("  • Dependency parsing and preposition analysis")
    print()


if __name__ == "__main__":
    quick_test()
