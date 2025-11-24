"""
Interactive Graph Visualization Module
Author: Ahmad Reza Adrian

This module creates interactive visualizations of the knowledge graph
using PyVis for web-based exploration.
"""

import logging
from typing import Dict, Any, List
from pathlib import Path

try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False
    logging.warning("PyVis not available. Install with: pip install pyvis")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GraphVisualizer:
    """
    Visualizes knowledge graphs using PyVis.
    Creates interactive HTML visualizations.
    """
    
    def __init__(self, 
                 height: str = "800px",
                 width: str = "100%",
                 bgcolor: str = "#222222",
                 font_color: str = "white"):
        """
        Initialize visualizer.
        
        Args:
            height: Height of visualization
            width: Width of visualization
            bgcolor: Background color
            font_color: Font color
        """
        if not PYVIS_AVAILABLE:
            raise ImportError("PyVis is required. Install with: pip install pyvis")
        
        self.height = height
        self.width = width
        self.bgcolor = bgcolor
        self.font_color = font_color
        
        # Color scheme for entity types
        self.entity_colors = {
            'PERSON': '#4a90e2',
            'LOC': '#50e3c2',
            'ORG': '#f5a623',
            'EVENT': '#e94b3c',
            'OBJECT': '#9b59b6',
            'UNKNOWN': '#95a5a6'
        }
        
        # Color scheme for relation types
        self.relation_colors = {
            'child_of': '#e74c3c',
            'parent_of': '#e74c3c',
            'married_to': '#e91e63',
            'sibling_of': '#9c27b0',
            'fought_with': '#f44336',
            'killed_by': '#b71c1c',
            'killed': '#b71c1c',
            'ruled_in': '#ff9800',
            'ruled_by': '#ff9800',
            'died_in': '#607d8b',
            'located_in': '#00bcd4',
            'participated_in': '#4caf50',
            'member_of': '#ff5722',
            'associated_with': '#9e9e9e'
        }
        
        # Human-readable relation labels
        self.relation_labels = {
            'child_of': 'child of',
            'parent_of': 'parent of',
            'married_to': 'married to',
            'sibling_of': 'sibling of',
            'fought_with': 'fought with',
            'killed_by': 'killed by',
            'killed': 'killed',
            'ruled_in': 'ruled in',
            'ruled_by': 'ruled by',
            'died_in': 'died in',
            'located_in': 'located in',
            'participated_in': 'participated in',
            'member_of': 'member of',
            'associated_with': 'related to'
        }
    
    def create_network(self) -> Network:
        """
        Create a new PyVis network.
        
        Returns:
            PyVis Network object
        """
        net = Network(height=self.height,
                     width=self.width,
                     bgcolor=self.bgcolor,
                     font_color=self.font_color,
                     directed=True)
        
        # Configure physics
        net.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {
              "enabled": true,
              "iterations": 200
            },
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 95,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 0.1
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "navigationButtons": true,
            "keyboard": true
          }
        }
        """)
        
        return net
    
    def visualize_from_knowledge_graph(self, kg, output_path: str = "graph.html",
                                      max_nodes: int = None, max_edges: int = None,
                                      one_level_per_node: bool = False) -> str:
        """
        Visualize a KnowledgeGraph object.
        
        Args:
            kg: KnowledgeGraph object
            output_path: Path to save HTML file
            max_nodes: Maximum number of nodes to display (None for all)
            max_edges: Maximum number of edges to display (None for all)
            one_level_per_node: If True, shows only 1-level connections per node (lighter)
            
        Returns:
            Path to generated HTML file
        """
        logger.info("Creating visualization...")
        
        # Create network
        net = self.create_network()
        
        # Get graph statistics for sizing
        degrees = dict(kg.graph.degree())
        max_degree = max(degrees.values()) if degrees else 1
        
        # Filter nodes if needed
        nodes_to_display = list(kg.graph.nodes())
        if max_nodes and len(nodes_to_display) > max_nodes:
            # Keep nodes with highest degree
            sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
            nodes_to_display = [n for n, _ in sorted_nodes[:max_nodes]]
            logger.info(f"Displaying top {max_nodes} nodes by degree")
        
        # Add nodes
        for node in nodes_to_display:
            node_data = kg.graph.nodes[node]
            entity_type = node_data.get('type', 'UNKNOWN')
            mention_count = node_data.get('count', 1)
            degree = degrees.get(node, 0)
            
            # Size based on degree
            size = 10 + (degree / max_degree) * 30
            
            # Color based on entity type
            color = self.entity_colors.get(entity_type, '#95a5a6')
            
            # Create title (tooltip)
            title = f"{node}\nType: {entity_type}\nMentions: {mention_count}\nConnections: {degree}"
            
            net.add_node(node,
                        label=node,
                        title=title,
                        color=color,
                        size=size,
                        font={'size': 12})
        
        # Add edges with optimization
        edges_to_add = []
        
        if one_level_per_node:
            # For each node, only show its direct connections (1-level depth)
            # This creates a "hub" visualization where nodes don't show relations between their neighbors
            added_edges = set()
            for node in nodes_to_display:
                # Get direct connections
                for target in kg.graph.successors(node):
                    if target in nodes_to_display:
                        edge_key = (node, target)
                        if edge_key not in added_edges:
                            edges_to_add.append(edge_key)
                            added_edges.add(edge_key)
                for source in kg.graph.predecessors(node):
                    if source in nodes_to_display:
                        edge_key = (source, node)
                        if edge_key not in added_edges:
                            edges_to_add.append(edge_key)
                            added_edges.add(edge_key)
        else:
            # Normal mode: show all edges
            for source, target in kg.graph.edges():
                if source in nodes_to_display and target in nodes_to_display:
                    edges_to_add.append((source, target))
        
        # Limit edges if specified
        if max_edges and len(edges_to_add) > max_edges:
            # Keep edges with highest count
            edges_with_count = [(s, t, kg.graph[s][t].get('count', 1)) for s, t in edges_to_add]
            edges_with_count.sort(key=lambda x: x[2], reverse=True)
            edges_to_add = [(s, t) for s, t, _ in edges_with_count[:max_edges]]
            logger.info(f"Displaying top {max_edges} edges by count")
        
        # Add edges to visualization
        for source, target in edges_to_add:
            edge_data = kg.graph[source][target]
            relations = edge_data.get('relations', [])
            relation_count = edge_data.get('count', 1)
            
            # Try to get dynamic labels first
            dynamic_labels = edge_data.get('dynamic_labels', [])
            
            # Format relation labels to be more readable
            readable_relations = []
            if dynamic_labels:
                # Use dynamic labels if available
                readable_relations = [str(label) for label in dynamic_labels if label]
            
            # Fallback to static labels if no dynamic labels
            if not readable_relations:
                for rel in relations:
                    readable_label = self.relation_labels.get(rel, rel.replace('_', ' '))
                    readable_relations.append(readable_label)
            
            # Edge label - use readable format
            if len(readable_relations) == 1:
                label = readable_relations[0]
            elif len(readable_relations) == 2:
                label = f"{readable_relations[0]}, {readable_relations[1]}"
            else:
                label = f"{readable_relations[0]}+{len(readable_relations)-1}"
            
            # Edge color based on relation type
            color = self.relation_colors.get(relations[0], '#9e9e9e') if relations else '#9e9e9e'
            
            # Edge width based on count
            width = min(1 + relation_count * 0.5, 5)
            
            # Create detailed title with all relations
            all_relations_text = ', '.join(readable_relations)
            title = f"{source} → {target}\n{all_relations_text}"
            if relation_count > 1:
                title += f" ({relation_count}x)"
            
            net.add_edge(source, target,
                       title=title,
                       label=label,
                       color=color,
                       width=width,
                       arrows='to',
                       font={'size': 10, 'align': 'middle'})
        
        # Save
        net.save_graph(output_path)
        logger.info(f"Visualization saved to {output_path}")
        logger.info(f"Nodes displayed: {len(nodes_to_display)}, Edges displayed: {len(edges_to_add)}")
        
        return output_path
    
    def visualize_hub_network(self, kg, output_path: str = "hub_graph.html",
                             top_entities: int = 20) -> str:
        """
        Create a lighter "hub" visualization showing only top entities and their 1-level connections.
        This is optimized for browser performance with large graphs.
        
        Args:
            kg: KnowledgeGraph object
            output_path: Path to save HTML file
            top_entities: Number of top entities to show as hubs
            
        Returns:
            Path to generated HTML file
        """
        logger.info(f"Creating hub visualization with top {top_entities} entities...")
        
        # Get top entities by degree
        degrees = dict(kg.graph.degree())
        sorted_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        hub_nodes = [entity for entity, _ in sorted_entities[:top_entities]]
        
        # Get all nodes that connect to hub nodes
        all_nodes = set(hub_nodes)
        for hub in hub_nodes:
            all_nodes.update(kg.graph.successors(hub))
            all_nodes.update(kg.graph.predecessors(hub))
        
        # Create subgraph
        subgraph = kg.graph.subgraph(all_nodes).copy()
        
        # Create a temporary KnowledgeGraph object for visualization
        from graph_builder import KnowledgeGraph
        temp_kg = KnowledgeGraph()
        temp_kg.graph = subgraph
        
        logger.info(f"Hub network: {len(all_nodes)} nodes from {kg.graph.number_of_nodes()} total")
        
        # Use standard visualization with the filtered graph
        return self.visualize_from_knowledge_graph(
            temp_kg,
            output_path=output_path,
            one_level_per_node=True
        )
    
    def visualize_from_json(self, json_data: Dict[str, Any], 
                           output_path: str = "graph.html") -> str:
        """
        Visualize from JSON graph data.
        
        Args:
            json_data: Dictionary with 'nodes' and 'edges'
            output_path: Path to save HTML file
            
        Returns:
            Path to generated HTML file
        """
        logger.info("Creating visualization from JSON...")
        
        net = self.create_network()
        
        # Calculate node degrees for sizing
        node_degrees = {}
        for edge in json_data['edges']:
            node_degrees[edge['source']] = node_degrees.get(edge['source'], 0) + 1
            node_degrees[edge['target']] = node_degrees.get(edge['target'], 0) + 1
        
        max_degree = max(node_degrees.values()) if node_degrees else 1
        
        # Add nodes
        for node in json_data['nodes']:
            node_id = node['id']
            entity_type = node.get('type', 'UNKNOWN')
            mention_count = node.get('count', 1)
            degree = node_degrees.get(node_id, 0)
            
            size = 10 + (degree / max_degree) * 30
            color = self.entity_colors.get(entity_type, '#95a5a6')
            
            title = f"{node['label']}\nType: {entity_type}\nMentions: {mention_count}\nConnections: {degree}"
            
            net.add_node(node_id,
                        label=node['label'],
                        title=title,
                        color=color,
                        size=size,
                        font={'size': 12})
        
        # Add edges
        for edge in json_data['edges']:
            relations = edge.get('relations', [])
            
            # Format readable labels
            readable_relations = [self.relation_labels.get(rel, rel.replace('_', ' ')) for rel in relations]
            label = ', '.join(readable_relations) if len(readable_relations) <= 2 else f"{readable_relations[0]}+{len(readable_relations)-1}"
            
            color = self.relation_colors.get(relations[0], '#9e9e9e') if relations else '#9e9e9e'
            width = min(1 + edge.get('count', 1) * 0.5, 5)
            
            title = f"{edge['source']} → {edge['target']}\n{', '.join(readable_relations)}"
            
            net.add_edge(edge['source'], edge['target'],
                        title=title,
                        label=label,
                        color=color,
                        width=width,
                        arrows='to',
                        font={'size': 10, 'align': 'middle'})
        
        # Save
        net.save_graph(output_path)
        logger.info(f"Visualization saved to {output_path}")
        
        return output_path
    
    def visualize_entity_direct_relations(self, kg, entity_name: str,
                                          output_path: str = None) -> str:
        """
        Visualize ONLY direct relationships of an entity (1-level, ego network).
        Shows the entity and its immediate neighbors, but NO edges between neighbors.
        
        Args:
            kg: KnowledgeGraph object
            entity_name: Central entity
            output_path: Path to save HTML file
            
        Returns:
            Path to generated HTML file
        """
        if not kg.graph.has_node(entity_name):
            logger.error(f"Entity '{entity_name}' not found in graph")
            return None
        
        logger.info(f"Creating 1-level visualization for '{entity_name}'...")
        
        # Create network
        net = self.create_network()
        
        # Get central entity data
        central_data = kg.graph.nodes[entity_name]
        central_type = central_data.get('type', 'UNKNOWN')
        central_count = central_data.get('count', 1)
        
        # Add central node (larger size)
        net.add_node(entity_name,
                    label=entity_name,
                    title=f"{entity_name}\nType: {central_type}\nMentions: {central_count}\n(Central Entity)",
                    color=self.entity_colors.get(central_type, '#95a5a6'),
                    size=40,  # Larger for central node
                    font={'size': 14, 'bold': True})
        
        # Get all direct neighbors (incoming and outgoing)
        neighbors = set()
        neighbors.update(kg.graph.successors(entity_name))  # Outgoing
        neighbors.update(kg.graph.predecessors(entity_name))  # Incoming
        
        # Add neighbor nodes
        for neighbor in neighbors:
            neighbor_data = kg.graph.nodes[neighbor]
            neighbor_type = neighbor_data.get('type', 'UNKNOWN')
            neighbor_count = neighbor_data.get('count', 1)
            
            net.add_node(neighbor,
                        label=neighbor,
                        title=f"{neighbor}\nType: {neighbor_type}\nMentions: {neighbor_count}",
                        color=self.entity_colors.get(neighbor_type, '#95a5a6'),
                        size=20,
                        font={'size': 12})
        
        # Add ONLY edges connected to central entity
        # Outgoing edges (central → neighbor)
        for neighbor in kg.graph.successors(entity_name):
            edge_data = kg.graph[entity_name][neighbor]
            relations = edge_data.get('relations', [])
            relation_count = edge_data.get('count', 1)
            
            # Format readable labels
            readable_relations = [self.relation_labels.get(rel, rel.replace('_', ' ')) for rel in relations]
            label = ', '.join(readable_relations) if len(readable_relations) <= 2 else f"{readable_relations[0]}+{len(readable_relations)-1}"
            
            color = self.relation_colors.get(relations[0], '#9e9e9e') if relations else '#9e9e9e'
            width = min(1 + relation_count * 0.5, 5)
            title = f"{entity_name} → {neighbor}\n{', '.join(readable_relations)}"
            
            net.add_edge(entity_name, neighbor,
                        title=title,
                        label=label,
                        color=color,
                        width=width,
                        arrows='to',
                        font={'size': 10, 'align': 'middle'})
        
        # Incoming edges (neighbor → central)
        for neighbor in kg.graph.predecessors(entity_name):
            edge_data = kg.graph[neighbor][entity_name]
            relations = edge_data.get('relations', [])
            relation_count = edge_data.get('count', 1)
            
            # Format readable labels
            readable_relations = [self.relation_labels.get(rel, rel.replace('_', ' ')) for rel in relations]
            label = ', '.join(readable_relations) if len(readable_relations) <= 2 else f"{readable_relations[0]}+{len(readable_relations)-1}"
            
            color = self.relation_colors.get(relations[0], '#9e9e9e') if relations else '#9e9e9e'
            width = min(1 + relation_count * 0.5, 5)
            title = f"{neighbor} → {entity_name}\n{', '.join(readable_relations)}"
            
            net.add_edge(neighbor, entity_name,
                        title=title,
                        label=label,
                        color=color,
                        width=width,
                        arrows='to',
                        font={'size': 10, 'align': 'middle'})
        
        # Generate output path
        if not output_path:
            safe_name = entity_name.replace(' ', '_').lower()
            output_path = f"entity_{safe_name}.html"
        
        # Save
        net.save_graph(output_path)
        logger.info(f"1-level visualization saved to {output_path}")
        logger.info(f"Showing 1 central entity + {len(neighbors)} direct neighbors")
        logger.info(f"Total edges: {len(list(kg.graph.successors(entity_name))) + len(list(kg.graph.predecessors(entity_name)))}")
        
        return output_path
    
    def create_subgraph_visualization(self, kg, entity_name: str,
                                     depth: int = 1,
                                     output_path: str = None) -> str:
        """
        Create visualization of subgraph around an entity.
        
        Args:
            kg: KnowledgeGraph object
            entity_name: Central entity
            depth: Neighborhood depth
            output_path: Path to save HTML file
            
        Returns:
            Path to generated HTML file
        """
        # For depth=1, use the optimized direct relations method
        if depth == 1:
            return self.visualize_entity_direct_relations(kg, entity_name, output_path)
        
        # Get subgraph for depth > 1
        subgraph = kg.get_subgraph(entity_name, depth=depth)
        
        if not subgraph:
            logger.error(f"Entity '{entity_name}' not found in graph")
            return None
        
        # Generate output path
        if not output_path:
            safe_name = entity_name.replace(' ', '_').lower()
            output_path = f"subgraph_{safe_name}.html"
        
        # Visualize
        return self.visualize_from_knowledge_graph(subgraph, output_path)


def main():
    """
    Main function for testing visualization.
    """
    import json
    from graph_builder import KnowledgeGraph
    
    # Create sample graph
    kg = KnowledgeGraph()
    
    # Add sample data
    entities = [
        ('Abimanyu', 'PERSON'),
        ('Arjuna', 'PERSON'),
        ('Subadra', 'PERSON'),
        ('Kresna', 'PERSON'),
        ('Bharatayudha', 'EVENT'),
        ('Dwarawati', 'LOC')
    ]
    
    for name, etype in entities:
        kg.add_entity(name, etype)
    
    relations = [
        ('Abimanyu', 'child_of', 'Arjuna'),
        ('Abimanyu', 'child_of', 'Subadra'),
        ('Abimanyu', 'died_in', 'Bharatayudha'),
        ('Kresna', 'ruled_in', 'Dwarawati')
    ]
    
    for subj, rel, obj in relations:
        kg.add_relation(subj, rel, obj)
    
    # Create visualizer
    visualizer = GraphVisualizer()
    
    # Generate visualization
    output_path = visualizer.visualize_from_knowledge_graph(
        kg, 
        output_path="sample_graph.html"
    )
    
    print(f"=== Visualization Created ===")
    print(f"File: {output_path}")
    print(f"Open this file in a web browser to view the interactive graph")


if __name__ == "__main__":
    main()
