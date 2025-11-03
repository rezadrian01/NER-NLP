"""
Test script untuk visualisasi 1-level (direct relations only)
"""

from graph_builder import KnowledgeGraph
from visualization import GraphVisualizer

# Create sample graph with many connections
kg = KnowledgeGraph()

# Add entities
entities = [
    ('Endang', 'PERSON'),
    ('Abimanyu', 'PERSON'),
    ('Arjuna', 'PERSON'),
    ('Subadra', 'PERSON'),
    ('Kresna', 'PERSON'),
    ('Baladewa', 'PERSON'),
    ('Bharatayudha', 'EVENT'),
    ('Dwarawati', 'LOC'),
]

for name, etype in entities:
    kg.add_entity(name, etype)

# Add relations
# Endang's direct relations
kg.add_relation('Endang', 'child_of', 'Abimanyu')
kg.add_relation('Endang', 'sibling_of', 'Arjuna')

# Other relations (should NOT appear in Endang's 1-level viz)
kg.add_relation('Abimanyu', 'child_of', 'Arjuna')
kg.add_relation('Abimanyu', 'child_of', 'Subadra')
kg.add_relation('Abimanyu', 'died_in', 'Bharatayudha')
kg.add_relation('Arjuna', 'married_to', 'Subadra')
kg.add_relation('Kresna', 'ruled_in', 'Dwarawati')
kg.add_relation('Kresna', 'sibling_of', 'Baladewa')

print("=== Testing 1-Level Visualization ===")
print(f"Total nodes in graph: {kg.graph.number_of_nodes()}")
print(f"Total edges in graph: {kg.graph.number_of_edges()}")

# Get Endang's direct neighbors
print(f"\nEndang's direct connections:")
print(f"  Outgoing: {list(kg.graph.successors('Endang'))}")
print(f"  Incoming: {list(kg.graph.predecessors('Endang'))}")

# Create visualizations
visualizer = GraphVisualizer()

# 1. Full graph (old behavior - shows everything)
print("\n1. Creating FULL graph visualization...")
full_path = visualizer.visualize_from_knowledge_graph(kg, 'output/test_full_graph.html')
print(f"   Saved to: {full_path}")
print(f"   This will show ALL {kg.graph.number_of_nodes()} nodes and ALL {kg.graph.number_of_edges()} edges")

# 2. 1-level visualization (new behavior - only direct relations)
print("\n2. Creating 1-LEVEL visualization for 'Endang'...")
one_level_path = visualizer.visualize_entity_direct_relations(kg, 'Endang', 'output/test_endang_1level.html')
print(f"   Saved to: {one_level_path}")

# Count what should be shown
endang_neighbors = set(kg.graph.successors('Endang')) | set(kg.graph.predecessors('Endang'))
endang_edges = len(list(kg.graph.successors('Endang'))) + len(list(kg.graph.predecessors('Endang')))
print(f"   Should show: 1 central node (Endang) + {len(endang_neighbors)} neighbors = {1 + len(endang_neighbors)} nodes")
print(f"   Should show: {endang_edges} edges (only connected to Endang)")
print(f"   Should NOT show: Relations between {', '.join(endang_neighbors)}")

print("\n✅ Test complete!")
print("\nOpen these files in browser to compare:")
print(f"   - Full graph: output/test_full_graph.html")
print(f"   - 1-level (Endang only): output/test_endang_1level.html")
print("\nIn the 1-level graph, you should see:")
print("   ✓ Endang (center, large)")
print("   ✓ Abimanyu (neighbor)")
print("   ✓ Arjuna (neighbor)")
print("   ✓ Edge: Endang → Abimanyu (child_of)")
print("   ✓ Edge: Endang → Arjuna (sibling_of)")
print("\nYou should NOT see:")
print("   ✗ Edge: Abimanyu → Arjuna")
print("   ✗ Edge: Abimanyu → Subadra")
print("   ✗ Edge: Abimanyu → Bharatayudha")
print("   ✗ Any other edges not connected to Endang")
