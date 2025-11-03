"""
Test and Example Script for Wayang NER System
Author: Ahmad Reza Adrian

This script demonstrates the functionality of each module
and provides test cases for validation.
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_preprocessing():
    """Test the preprocessing module."""
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Text Preprocessing")
    logger.info("="*60)
    
    from preprocessing import TextPreprocessor
    
    preprocessor = TextPreprocessor()
    
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra.    Ia gugur dalam perang Bharatayudha.
    Arjuna merupakan ksatria   terkuat di Pandawa.
    """
    
    result = preprocessor.preprocess(sample_text)
    
    print(f"\n📝 Original text length: {len(result['original'])} characters")
    print(f"✅ Cleaned text length: {len(result['cleaned'])} characters")
    print(f"📊 Sentence count: {result['sentence_count']}")
    print(f"\nSentences:")
    for i, sent in enumerate(result['sentences'], 1):
        print(f"  {i}. {sent}")
    
    return True


def test_ner():
    """Test the NER module."""
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Named Entity Recognition")
    logger.info("="*60)
    
    from ner_extraction import WayangNER
    
    # Use rule-based only for testing (faster, no model download needed)
    ner = WayangNER(model_type="rule-based")
    
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra. Ia gugur dalam perang Bharatayudha.
    Prabu Kresna memerintah di Kerajaan Dwarawati. Raden Samba adalah putra mahkota.
    Pandawa bertempur melawan Kurawa.
    """
    
    entities = ner.extract_entities_rule_based(sample_text)
    
    print(f"\n✅ Found {len(entities)} entities:")
    
    # Group by type
    by_type = {}
    for entity in entities:
        etype = entity['type']
        if etype not in by_type:
            by_type[etype] = []
        by_type[etype].append(entity['text'])
    
    for etype, names in sorted(by_type.items()):
        print(f"\n  {etype}:")
        for name in sorted(set(names)):
            print(f"    - {name}")
    
    return True


def test_relation_extraction():
    """Test the relation extraction module."""
    logger.info("\n" + "="*60)
    logger.info("TEST 3: Relation Extraction")
    logger.info("="*60)
    
    from relation_extraction import RelationExtractor
    
    extractor = RelationExtractor()
    
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra. Ia gugur dalam perang Bharatayudha.
    Arjuna menikah dengan Subadra. Prabu Kresna memerintah di Kerajaan Dwarawati.
    """
    
    # Sample entities
    entities = [
        {'text': 'Abimanyu', 'type': 'PERSON', 'start': 0, 'end': 8},
        {'text': 'Arjuna', 'type': 'PERSON', 'start': 24, 'end': 30},
        {'text': 'Subadra', 'type': 'PERSON', 'start': 35, 'end': 42},
        {'text': 'Bharatayudha', 'type': 'EVENT', 'start': 65, 'end': 77},
        {'text': 'Prabu Kresna', 'type': 'PERSON', 'start': 110, 'end': 122},
        {'text': 'Kerajaan Dwarawati', 'type': 'LOC', 'start': 139, 'end': 157}
    ]
    
    relations = extractor.extract_relations_from_entities(sample_text, entities)
    
    print(f"\n✅ Found {len(relations)} relations:")
    for relation in relations:
        print(f"\n  ({relation['subject']}) -[{relation['relation']}]-> ({relation['object']})")
        print(f"    Type: {relation['subject_type']} → {relation['object_type']}")
        print(f"    Confidence: {relation['confidence']:.2f}")
        print(f"    Context: \"{relation['context'][:60]}...\"")
    
    return True


def test_knowledge_graph():
    """Test the knowledge graph builder."""
    logger.info("\n" + "="*60)
    logger.info("TEST 4: Knowledge Graph Construction")
    logger.info("="*60)
    
    from graph_builder import KnowledgeGraph
    
    kg = KnowledgeGraph()
    
    # Add sample entities
    entities_data = [
        ('Abimanyu', 'PERSON'),
        ('Arjuna', 'PERSON'),
        ('Subadra', 'PERSON'),
        ('Kresna', 'PERSON'),
        ('Bharatayudha', 'EVENT'),
        ('Dwarawati', 'LOC'),
        ('Pandawa', 'ORG'),
        ('Kurawa', 'ORG')
    ]
    
    for name, etype in entities_data:
        kg.add_entity(name, etype)
    
    # Add sample relations
    relations_data = [
        ('Abimanyu', 'child_of', 'Arjuna', 0.9),
        ('Abimanyu', 'child_of', 'Subadra', 0.9),
        ('Abimanyu', 'died_in', 'Bharatayudha', 0.85),
        ('Arjuna', 'married_to', 'Subadra', 0.8),
        ('Kresna', 'ruled_in', 'Dwarawati', 0.95),
        ('Arjuna', 'associated_with', 'Pandawa', 0.7),
        ('Pandawa', 'fought_with', 'Kurawa', 0.9)
    ]
    
    for subj, rel, obj, conf in relations_data:
        kg.add_relation(subj, rel, obj, confidence=conf)
    
    # Get statistics
    stats = kg.get_statistics()
    
    print(f"\n📊 Graph Statistics:")
    print(f"  Nodes: {stats['total_nodes']}")
    print(f"  Edges: {stats['total_edges']}")
    print(f"  Density: {stats['density']:.4f}")
    print(f"  Connected: {stats['is_connected']}")
    
    print(f"\n📈 Entity Type Distribution:")
    for etype, count in sorted(stats['entity_type_distribution'].items()):
        print(f"  {etype}: {count}")
    
    print(f"\n🔗 Relation Type Distribution:")
    for rtype, count in sorted(stats['relation_type_distribution'].items()):
        print(f"  {rtype}: {count}")
    
    print(f"\n⭐ Top Entities:")
    for entity_info in stats['top_entities'][:5]:
        print(f"  {entity_info['entity']}: {entity_info['degree']} connections")
    
    # Test entity info
    print(f"\n🔍 Entity Details: Abimanyu")
    info = kg.get_entity_info('Abimanyu')
    print(f"  Type: {info['type']}")
    print(f"  Degree: {info['degree']}")
    print(f"  Outgoing relations: {len(info['outgoing_relations'])}")
    print(f"  Incoming relations: {len(info['incoming_relations'])}")
    
    # Export to JSON
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    json_path = output_dir / 'test_graph.json'
    kg.to_json(str(json_path))
    print(f"\n💾 Graph exported to: {json_path}")
    
    return True


def test_visualization():
    """Test the visualization module."""
    logger.info("\n" + "="*60)
    logger.info("TEST 5: Graph Visualization")
    logger.info("="*60)
    
    from graph_builder import KnowledgeGraph
    from visualization import GraphVisualizer
    
    # Create sample graph
    kg = KnowledgeGraph()
    
    entities_data = [
        ('Abimanyu', 'PERSON'),
        ('Arjuna', 'PERSON'),
        ('Subadra', 'PERSON'),
        ('Kresna', 'PERSON'),
        ('Baladewa', 'PERSON'),
        ('Bharatayudha', 'EVENT'),
        ('Dwarawati', 'LOC'),
        ('Hastina', 'LOC'),
        ('Pandawa', 'ORG')
    ]
    
    for name, etype in entities_data:
        kg.add_entity(name, etype)
    
    relations_data = [
        ('Abimanyu', 'child_of', 'Arjuna'),
        ('Abimanyu', 'child_of', 'Subadra'),
        ('Arjuna', 'married_to', 'Subadra'),
        ('Arjuna', 'associated_with', 'Pandawa'),
        ('Abimanyu', 'died_in', 'Bharatayudha'),
        ('Kresna', 'ruled_in', 'Dwarawati'),
        ('Kresna', 'sibling_of', 'Baladewa'),
        ('Baladewa', 'ruled_in', 'Hastina')
    ]
    
    for subj, rel, obj in relations_data:
        kg.add_relation(subj, rel, obj)
    
    # Create visualization
    visualizer = GraphVisualizer()
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    html_path = output_dir / 'test_visualization.html'
    visualizer.visualize_from_knowledge_graph(kg, str(html_path))
    
    print(f"\n✅ Visualization created: {html_path}")
    print(f"📱 Open this file in a web browser to view the interactive graph")
    
    return True


def test_mini_pipeline():
    """Test a mini pipeline with sample data."""
    logger.info("\n" + "="*60)
    logger.info("TEST 6: Mini Pipeline")
    logger.info("="*60)
    
    from preprocessing import TextPreprocessor
    from ner_extraction import WayangNER
    from relation_extraction import RelationExtractor
    from graph_builder import KnowledgeGraph
    from visualization import GraphVisualizer
    
    # Sample text
    sample_texts = [
        """Abimanyu adalah putra Arjuna dan Subadra. 
        Ia merupakan ksatria muda yang gagah berani. 
        Abimanyu gugur dalam perang Bharatayudha.""",
        
        """Prabu Kresna memerintah di Kerajaan Dwarawati. 
        Kresna adalah kakak Subadra. 
        Arjuna menikah dengan Subadra.""",
        
        """Pandawa bertempur melawan Kurawa dalam perang Bharatayudha. 
        Arjuna adalah salah satu ksatria Pandawa terkuat."""
    ]
    
    # Initialize components
    preprocessor = TextPreprocessor()
    ner = WayangNER(model_type="rule-based")
    extractor = RelationExtractor()
    kg = KnowledgeGraph()
    
    print("\n🔄 Processing texts...")
    
    all_entities = []
    all_relations = []
    
    for i, text in enumerate(sample_texts, 1):
        # Preprocess
        result = preprocessor.preprocess(text)
        clean_text = result['normalized']
        
        # Extract entities
        entities = ner.extract_entities(clean_text)
        all_entities.extend(entities)
        
        # Extract relations
        relations = extractor.extract_relations_from_entities(clean_text, entities)
        all_relations.extend(relations)
        
        print(f"  Text {i}: {len(entities)} entities, {len(relations)} relations")
    
    # Build graph
    print(f"\n🏗️  Building knowledge graph...")
    for entity in all_entities:
        kg.add_entity(entity['text'], entity['type'])
    
    for relation in all_relations:
        kg.add_relation(
            relation['subject'],
            relation['relation'],
            relation['object'],
            confidence=relation.get('confidence', 1.0)
        )
    
    stats = kg.get_statistics()
    print(f"  Graph: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    
    # Visualize
    visualizer = GraphVisualizer()
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    html_path = output_dir / 'mini_pipeline_graph.html'
    visualizer.visualize_from_knowledge_graph(kg, str(html_path))
    
    print(f"\n✅ Mini pipeline complete!")
    print(f"📊 Results: {len(all_entities)} entities, {len(all_relations)} relations")
    print(f"📱 Visualization: {html_path}")
    
    return True


def run_all_tests():
    """Run all test cases."""
    logger.info("\n" + "🧪 "*30)
    logger.info("WAYANG NER SYSTEM - TEST SUITE")
    logger.info("🧪 "*30)
    
    tests = [
        ("Preprocessing", test_preprocessing),
        ("Named Entity Recognition", test_ner),
        ("Relation Extraction", test_relation_extraction),
        ("Knowledge Graph", test_knowledge_graph),
        ("Visualization", test_visualization),
        ("Mini Pipeline", test_mini_pipeline)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "✅ PASSED" if success else "❌ FAILED"))
        except Exception as e:
            logger.error(f"Error in {test_name}: {e}", exc_info=True)
            results.append((test_name, f"❌ ERROR: {str(e)}"))
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    for test_name, result in results:
        print(f"  {test_name:<30} {result}")
    
    passed = sum(1 for _, r in results if "PASSED" in r)
    total = len(results)
    
    logger.info("\n" + "="*60)
    logger.info(f"RESULT: {passed}/{total} tests passed")
    logger.info("="*60)


if __name__ == "__main__":
    run_all_tests()
