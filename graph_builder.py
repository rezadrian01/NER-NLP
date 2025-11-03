"""
Knowledge Graph Builder Module
Author: Ahmad Reza Adrian

This module constructs a knowledge graph from extracted entities and relations
using NetworkX. Supports graph analytics and JSON export.
"""

import json
import logging
from typing import List, Dict, Any, Set, Tuple
from collections import Counter
import pandas as pd

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not available. Install with: pip install networkx")

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """
    Knowledge graph for wayang entities and relations.
    Uses NetworkX for graph representation and analytics.
    """
    
    def __init__(self):
        """Initialize empty knowledge graph."""
        if not NETWORKX_AVAILABLE:
            raise ImportError("NetworkX is required. Install with: pip install networkx")
        
        self.graph = nx.DiGraph()
        self.entity_metadata = {}
        self.relation_metadata = {}
        
    def add_entity(self, entity_name: str, entity_type: str, metadata: Dict[str, Any] = None):
        """
        Add an entity node to the graph.
        
        Args:
            entity_name: Name of the entity
            entity_type: Type of entity (PERSON, LOC, etc.)
            metadata: Additional metadata dictionary
        """
        # Normalize entity name
        entity_name = entity_name.strip()
        
        # Add or update node
        if self.graph.has_node(entity_name):
            # Update existing node
            self.graph.nodes[entity_name]['type'] = entity_type
            self.graph.nodes[entity_name]['count'] = self.graph.nodes[entity_name].get('count', 0) + 1
        else:
            # Add new node
            self.graph.add_node(entity_name, 
                              type=entity_type,
                              count=1)
        
        # Store metadata
        if metadata:
            if entity_name not in self.entity_metadata:
                self.entity_metadata[entity_name] = []
            self.entity_metadata[entity_name].append(metadata)
    
    def add_relation(self, subject: str, relation_type: str, obj: str, 
                    confidence: float = 1.0, context: str = None):
        """
        Add a relation edge to the graph.
        
        Args:
            subject: Source entity
            relation_type: Type of relation
            obj: Target entity
            confidence: Confidence score (0-1)
            context: Context sentence where relation was found
        """
        # Normalize entity names
        subject = subject.strip()
        obj = obj.strip()
        
        # Ensure nodes exist
        if not self.graph.has_node(subject):
            self.add_entity(subject, 'UNKNOWN')
        if not self.graph.has_node(obj):
            self.add_entity(obj, 'UNKNOWN')
        
        # Add or update edge
        edge_key = (subject, obj, relation_type)
        
        if self.graph.has_edge(subject, obj):
            # Update existing edge
            existing_relations = self.graph[subject][obj].get('relations', [])
            if relation_type not in existing_relations:
                existing_relations.append(relation_type)
                self.graph[subject][obj]['relations'] = existing_relations
                self.graph[subject][obj]['count'] = self.graph[subject][obj].get('count', 0) + 1
        else:
            # Add new edge
            self.graph.add_edge(subject, obj,
                              relations=[relation_type],
                              count=1,
                              confidence=confidence)
        
        # Store metadata
        if edge_key not in self.relation_metadata:
            self.relation_metadata[edge_key] = []
        self.relation_metadata[edge_key].append({
            'confidence': confidence,
            'context': context
        })
    
    def build_from_dataframe(self, df: pd.DataFrame,
                            entities_column: str = 'entities',
                            relations_column: str = 'relations'):
        """
        Build knowledge graph from a DataFrame with entities and relations.
        
        Args:
            df: Input DataFrame
            entities_column: Column containing entities
            relations_column: Column containing relations
        """
        logger.info(f"Building knowledge graph from {len(df)} documents...")
        
        # Add all entities
        for idx, row in df.iterrows():
            entities = row[entities_column]
            if entities:
                for entity in entities:
                    self.add_entity(
                        entity['text'],
                        entity['type'],
                        metadata={'document_id': idx, 'method': entity.get('method')}
                    )
        
        # Add all relations
        for idx, row in df.iterrows():
            relations = row[relations_column]
            if relations:
                for relation in relations:
                    self.add_relation(
                        relation['subject'],
                        relation['relation'],
                        relation['object'],
                        confidence=relation.get('confidence', 1.0),
                        context=relation.get('context')
                    )
        
        logger.info(f"Graph built: {self.graph.number_of_nodes()} nodes, "
                   f"{self.graph.number_of_edges()} edges")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get graph statistics.
        
        Returns:
            Dictionary of statistics
        """
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'is_connected': nx.is_weakly_connected(self.graph)
        }
        
        # Entity type distribution
        entity_types = Counter(nx.get_node_attributes(self.graph, 'type').values())
        stats['entity_type_distribution'] = dict(entity_types)
        
        # Relation type distribution
        relation_counts = Counter()
        for u, v, data in self.graph.edges(data=True):
            for rel in data.get('relations', []):
                relation_counts[rel] += 1
        stats['relation_type_distribution'] = dict(relation_counts)
        
        # Top entities by degree
        degrees = dict(self.graph.degree())
        top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
        stats['top_entities'] = [{'entity': e, 'degree': d} for e, d in top_entities]
        
        return stats
    
    def get_entity_info(self, entity_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an entity.
        
        Args:
            entity_name: Name of the entity
            
        Returns:
            Dictionary with entity information
        """
        if not self.graph.has_node(entity_name):
            return None
        
        node_data = self.graph.nodes[entity_name]
        
        # Get relations
        outgoing = []
        for target in self.graph.successors(entity_name):
            edge_data = self.graph[entity_name][target]
            outgoing.append({
                'target': target,
                'relations': edge_data['relations']
            })
        
        incoming = []
        for source in self.graph.predecessors(entity_name):
            edge_data = self.graph[source][entity_name]
            incoming.append({
                'source': source,
                'relations': edge_data['relations']
            })
        
        return {
            'name': entity_name,
            'type': node_data.get('type'),
            'mention_count': node_data.get('count', 0),
            'degree': self.graph.degree(entity_name),
            'outgoing_relations': outgoing,
            'incoming_relations': incoming,
            'metadata': self.entity_metadata.get(entity_name, [])
        }
    
    def find_path(self, source: str, target: str, max_length: int = 5) -> List[List[str]]:
        """
        Find paths between two entities.
        
        Args:
            source: Source entity
            target: Target entity
            max_length: Maximum path length
            
        Returns:
            List of paths (each path is a list of entity names)
        """
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            return []
        
        try:
            # Find all simple paths
            paths = nx.all_simple_paths(self.graph, source, target, cutoff=max_length)
            return list(paths)
        except nx.NetworkXNoPath:
            return []
    
    def get_subgraph(self, entity_name: str, depth: int = 1) -> 'KnowledgeGraph':
        """
        Extract subgraph centered on an entity.
        
        Args:
            entity_name: Central entity
            depth: Depth of neighborhood
            
        Returns:
            New KnowledgeGraph with subgraph
        """
        if not self.graph.has_node(entity_name):
            return None
        
        # Get neighbors at specified depth
        nodes = {entity_name}
        current_level = {entity_name}
        
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            current_level = next_level - nodes
            nodes.update(current_level)
        
        # Create subgraph
        subgraph_nx = self.graph.subgraph(nodes).copy()
        
        # Create new KnowledgeGraph
        subgraph_kg = KnowledgeGraph()
        subgraph_kg.graph = subgraph_nx
        subgraph_kg.entity_metadata = {k: v for k, v in self.entity_metadata.items() 
                                       if k in nodes}
        
        return subgraph_kg
    
    def to_json(self, filepath: str = None) -> Dict[str, Any]:
        """
        Export graph to JSON format.
        
        Args:
            filepath: Optional path to save JSON file
            
        Returns:
            Dictionary representing the graph
        """
        # Build nodes list
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                'id': node,
                'label': node,
                'type': data.get('type', 'UNKNOWN'),
                'count': data.get('count', 0)
            })
        
        # Build edges list
        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                'source': source,
                'target': target,
                'relations': data.get('relations', []),
                'count': data.get('count', 0),
                'confidence': data.get('confidence', 1.0)
            })
        
        graph_data = {
            'nodes': nodes,
            'edges': edges,
            'statistics': self.get_statistics()
        }
        
        # Save to file if filepath provided
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Graph exported to {filepath}")
        
        return graph_data
    
    def from_json(self, filepath: str):
        """
        Load graph from JSON file.
        
        Args:
            filepath: Path to JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # Clear existing graph
        self.graph.clear()
        self.entity_metadata.clear()
        self.relation_metadata.clear()
        
        # Add nodes
        for node in graph_data['nodes']:
            self.graph.add_node(node['id'],
                              type=node.get('type', 'UNKNOWN'),
                              count=node.get('count', 0))
        
        # Add edges
        for edge in graph_data['edges']:
            self.graph.add_edge(edge['source'],
                              edge['target'],
                              relations=edge.get('relations', []),
                              count=edge.get('count', 0),
                              confidence=edge.get('confidence', 1.0))
        
        logger.info(f"Graph loaded from {filepath}")


def main():
    """
    Main function for testing graph builder.
    """
    # Create sample graph
    kg = KnowledgeGraph()
    
    # Add entities
    kg.add_entity('Abimanyu', 'PERSON')
    kg.add_entity('Arjuna', 'PERSON')
    kg.add_entity('Subadra', 'PERSON')
    kg.add_entity('Bharatayudha', 'EVENT')
    
    # Add relations
    kg.add_relation('Abimanyu', 'child_of', 'Arjuna', confidence=0.9)
    kg.add_relation('Abimanyu', 'child_of', 'Subadra', confidence=0.9)
    kg.add_relation('Abimanyu', 'died_in', 'Bharatayudha', confidence=0.85)
    
    # Get statistics
    stats = kg.get_statistics()
    
    print("=== Knowledge Graph Statistics ===")
    print(f"Nodes: {stats['total_nodes']}")
    print(f"Edges: {stats['total_edges']}")
    print(f"Entity types: {stats['entity_type_distribution']}")
    print(f"Relation types: {stats['relation_type_distribution']}")
    
    # Get entity info
    info = kg.get_entity_info('Abimanyu')
    print(f"\n=== Entity Info: Abimanyu ===")
    print(f"Type: {info['type']}")
    print(f"Degree: {info['degree']}")
    print(f"Outgoing relations: {info['outgoing_relations']}")
    
    # Export to JSON
    graph_data = kg.to_json('sample_graph.json')
    print(f"\n=== Exported to JSON ===")
    print(f"File: sample_graph.json")


if __name__ == "__main__":
    main()
