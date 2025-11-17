"""
Test Dynamic Relation Labeling
Demonstrates how context-based dynamic labels are generated
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dynamic_relation_labeler import DynamicRelationLabeler
from graph_builder import KnowledgeGraph
from visualization import GraphVisualizer

def test_dynamic_labeling():
    """Test dynamic relation labeling with various examples."""
    
    print("\n" + "="*70)
    print("TESTING DYNAMIC RELATION LABELING")
    print("="*70)
    
    # Initialize the dynamic labeler
    labeler = DynamicRelationLabeler()
    
    # Test cases with real wayang story contexts
    test_cases = [
        {
            'subject': 'Abimanyu',
            'object': 'Arjuna',
            'context': 'Abimanyu adalah putra Arjuna yang gagah berani dan terkenal di medan perang',
            'relation': 'child_of'
        },
        {
            'subject': 'Arjuna',
            'object': 'Subadra',
            'context': 'Arjuna menikah dengan Subadra setelah memperoleh restu dari Prabu Kresna',
            'relation': 'married_to'
        },
        {
            'subject': 'Bima',
            'object': 'Dursasana',
            'context': 'Bima membunuh Dursasana dalam pertempuran sengit di Bharatayudha',
            'relation': 'killed'
        },
        {
            'subject': 'Prabu Kresna',
            'object': 'Dwarawati',
            'context': 'Prabu Kresna memerintah di Kerajaan Dwarawati dengan bijaksana',
            'relation': 'ruled_in'
        },
        {
            'subject': 'Gatotkaca',
            'object': 'Abimanyu',
            'context': 'Gatotkaca bertempur melawan Abimanyu di medan Kurukshetra',
            'relation': 'fought_with'
        },
        {
            'subject': 'Werkudara',
            'object': 'Pandawa',
            'context': 'Werkudara adalah salah satu ksatria Pandawa yang terkuat',
            'relation': 'member_of'
        },
        {
            'subject': 'Srikandi',
            'object': 'Arjuna',
            'context': 'Srikandi adalah murid Arjuna yang belajar ilmu memanah',
            'relation': 'student_of'
        },
        {
            'subject': 'Yudhistira',
            'object': 'Indraprastha',
            'context': 'Yudhistira bertahta di istana Indraprastha sebagai raja yang adil',
            'relation': 'ruled_in'
        },
        {
            'subject': 'Karna',
            'object': 'Kunti',
            'context': 'Karna dilahirkan oleh Kunti sebelum perkawinannya dengan Pandu',
            'relation': 'child_of'
        },
        {
            'subject': 'Pandawa',
            'object': 'Kurawa',
            'context': 'Pandawa dan Kurawa adalah sepupu yang saling bermusuhan',
            'relation': 'rival_of'
        }
    ]
    
    print("\n📋 Testing Dynamic Label Generation:\n")
    
    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['subject']} ⟷ {test['object']}")
        print(f"   Context: {test['context'][:70]}...")
        
        # Generate dynamic label
        dynamic_label = labeler.extract_relation_label(
            test['subject'],
            test['object'],
            test['context'],
            test['relation']
        )
        
        print(f"   Static relation:  {test['relation']}")
        print(f"   ✨ Dynamic label:  '{dynamic_label}'")
        print()
        
        results.append({
            **test,
            'dynamic_label': dynamic_label
        })
    
    # Show statistics
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)
    
    stats = labeler.get_statistics()
    print(f"Total labels cached: {stats['total_cached_labels']}")
    print(f"Unique dynamic labels: {stats['unique_labels']}")
    print(f"\nMost common labels:")
    for label, count in stats['most_common_labels'][:5]:
        print(f"  - '{label}': {count}x")
    
    # Create a small knowledge graph with dynamic labels
    print("\n" + "="*70)
    print("CREATING VISUALIZATION WITH DYNAMIC LABELS")
    print("="*70)
    
    kg = KnowledgeGraph()
    
    # Add entities and relations with dynamic labels
    for result in results:
        kg.add_entity(result['subject'], 'PERSON')
        kg.add_entity(result['object'], 'PERSON' if result['object'] != 'Dwarawati' and result['object'] != 'Indraprastha' else 'LOC')
        kg.add_relation(
            result['subject'],
            result['relation'],
            result['object'],
            confidence=0.9,
            context=result['context'],
            dynamic_label=result['dynamic_label']
        )
    
    # Visualize
    visualizer = GraphVisualizer()
    output_file = 'output/test_dynamic_labels_new.html'
    visualizer.visualize_from_knowledge_graph(kg, output_file)
    
    print(f"\n✅ Visualization created: {output_file}")
    print(f"   Nodes: {kg.graph.number_of_nodes()}")
    print(f"   Edges: {kg.graph.number_of_edges()}")
    
    # Show edge details
    print("\n📊 Edge Labels in Graph:")
    for source, target, data in kg.graph.edges(data=True):
        dynamic_labels = data.get('dynamic_labels', [])
        static_relations = data.get('relations', [])
        print(f"   {source} → {target}")
        print(f"      Static: {', '.join(static_relations)}")
        if dynamic_labels:
            print(f"      ✨ Dynamic: {', '.join(dynamic_labels)}")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)
    print("\nDynamic labels are generated based on:")
    print("  1. Verb extraction (membunuh, menikah, memerintah, etc.)")
    print("  2. Noun relationships (putra, murid, raja, etc.)")
    print("  3. Dependency parsing (when spaCy available)")
    print("  4. Preposition analysis (di, dengan, oleh, etc.)")
    print("  5. TF-IDF of context words")
    print("\nThe labels adapt to the actual text context, making them more")
    print("meaningful and specific than generic static labels!")
    print()


if __name__ == "__main__":
    test_dynamic_labeling()
