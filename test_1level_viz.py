"""
Test script untuk visualisasi 1-level (direct relations only)
Demonstrates optimized visualization for browser performance
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

# 3. Hub visualization (optimized for performance)
print("\n3. Creating HUB visualization (optimized for browser performance)...")
hub_path = visualizer.visualize_hub_network(kg, 'output/test_hub_network.html', top_entities=5)
print(f"   Saved to: {hub_path}")
print(f"   This shows top 5 entities as hubs with their 1-level connections")
print(f"   Perfect for large graphs - much lighter to render in browser!")

print("\n✅ Test complete!")
print("\n" + "="*70)
print("COMPARISON OF VISUALIZATION MODES")
print("="*70)
print("\n📊 Files generated:")
print(f"   1. Full graph: output/test_full_graph.html")
print(f"      - Shows ALL nodes and ALL edges")
print(f"      - Heavy for large graphs (500+ edges)")
print(f"\n   2. 1-level (Endang): output/test_endang_1level.html")
print(f"      - Shows ONE entity + direct neighbors")
print(f"      - Perfect for entity-focused exploration")
print(f"\n   3. Hub network: output/test_hub_network.html")
print(f"      - Shows TOP entities + their 1-level connections")
print(f"      - ⚡ OPTIMIZED for browser performance")
print(f"      - ✅ RECOMMENDED for main visualization")
print("\n" + "="*70)
print("\n💡 The hub network visualization is now used by default in:")
print("   - python pipeline.py (with --light-mode, default)")
print("   - python app.py (at /visualization endpoint)")
print("\nThis makes the browser render MUCH faster! 🚀")
