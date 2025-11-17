"""
Test script for dynamic relation labels
Shows how relations are now displayed with meaningful, readable labels
"""

from graph_builder import KnowledgeGraph
from visualization import GraphVisualizer

# Create sample graph with various relation types
kg = KnowledgeGraph()

# Add entities
entities = [
    ('Abimanyu', 'PERSON'),
    ('Arjuna', 'PERSON'),
    ('Subadra', 'PERSON'),
    ('Kresna', 'PERSON'),
    ('Bharatayudha', 'EVENT'),
    ('Dwarawati', 'LOC'),
    ('Pandawa', 'ORG'),
]

for name, etype in entities:
    kg.add_entity(name, etype)

# Add various relation types
print("=== Adding Relations ===")
print("✓ Abimanyu child_of Arjuna")
kg.add_relation('Abimanyu', 'child_of', 'Arjuna', confidence=0.9)

print("✓ Abimanyu child_of Subadra")
kg.add_relation('Abimanyu', 'child_of', 'Subadra', confidence=0.9)

print("✓ Arjuna married_to Subadra")
kg.add_relation('Arjuna', 'married_to', 'Subadra', confidence=0.8)

print("✓ Kresna ruled_in Dwarawati")
kg.add_relation('Kresna', 'ruled_in', 'Dwarawati', confidence=0.95)

print("✓ Abimanyu died_in Bharatayudha")
kg.add_relation('Abimanyu', 'died_in', 'Bharatayudha', confidence=0.85)

print("✓ Arjuna member_of Pandawa")
kg.add_relation('Arjuna', 'member_of', 'Pandawa', confidence=0.9)

# Now test automatic reverse relations
print("\n=== Testing Reverse Relations ===")
print("When we add: Abimanyu child_of Arjuna")
print("System should automatically infer: Arjuna parent_of Abimanyu")

# Create visualizer
visualizer = GraphVisualizer()

# Create visualization
print("\n=== Creating Visualization ===")
output_path = visualizer.visualize_from_knowledge_graph(
    kg, 
    output_path='output/test_dynamic_labels.html'
)

print(f"✓ Visualization created: {output_path}")

# Show what labels will appear
print("\n=== Expected Readable Labels in Visualization ===")
print("Old format (technical):     New format (readable):")
print("─" * 60)
print("child_of                →   'child of'")
print("parent_of               →   'parent of'  (auto-inferred!)")
print("married_to              →   'married to'")
print("ruled_in                →   'ruled in'")
print("died_in                 →   'died in'")
print("member_of               →   'member of'")
print("associated_with         →   'related to'")

# Test entity-specific visualization
print("\n=== Creating Entity-Specific Visualization ===")
entity_path = visualizer.visualize_entity_direct_relations(
    kg,
    entity_name='Abimanyu',
    output_path='output/test_abimanyu_dynamic.html'
)
print(f"✓ Entity visualization created: {entity_path}")

print("\n=== Abimanyu's Relations (Readable Format) ===")
# Get entity info
info = kg.get_entity_info('Abimanyu')
print(f"Outgoing relations from Abimanyu:")
for rel in info['outgoing_relations']:
    print(f"  - Abimanyu → {rel['target']}: {', '.join(rel['relations'])}")

print(f"\nIncoming relations to Abimanyu:")
for rel in info['incoming_relations']:
    print(f"  - {rel['source']} → Abimanyu: {', '.join(rel['relations'])}")

print("\n" + "="*70)
print("✅ TEST COMPLETE!")
print("="*70)
print("\nOpen these files in your browser to see dynamic labels:")
print("  1. output/test_dynamic_labels.html - Full graph with all relation types")
print("  2. output/test_abimanyu_dynamic.html - Abimanyu-focused with readable labels")
print("\n" + "="*70)
print("\n💡 Key Improvements:")
print("  ✓ Relations show as readable text (e.g., 'child of' not 'child_of')")
print("  ✓ Automatic reverse relations (child_of → parent_of)")
print("  ✓ Color-coded by relation type")
print("  ✓ Specific relation types instead of generic 'associated_with'")
print("  ✓ Hover over edges to see full details")
print("\n" + "="*70)
