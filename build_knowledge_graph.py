"""
Knowledge Graph Builder using Custom NER Model
Author: Kelompok 1

Builds an interactive knowledge graph from annotated data using the custom NER model.
Optimized for web rendering with intelligent relation extraction.
"""

import json
import logging
import spacy
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from collections import Counter
import re

try:
    import networkx as nx
    from pyvis.network import Network
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False
    print("Missing dependencies. Install with: pip install networkx pyvis")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KnowledgeGraphBuilder:
    """
    Builds knowledge graph from NER annotations and extracts relations.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize graph builder.
        
        Args:
            model_path: Path to custom NER model (optional)
        """
        if not DEPS_AVAILABLE:
            raise ImportError("NetworkX and PyVis required")
        
        self.graph = nx.DiGraph()
        self.entity_mentions = {}  # Track entity occurrences
        self.nlp = None
        
        # Load custom NER model if available
        if model_path and Path(model_path).exists():
            logger.info(f"Loading custom NER model from {model_path}...")
            self.nlp = spacy.load(model_path)
            logger.info("✓ Custom model loaded")
        
        # Relation patterns for extraction
        self.relation_patterns = self._init_relation_patterns()
        
        # Entity type colors
        self.entity_colors = {
            'PERSON': '#4a90e2',  # Blue
            'LOC': '#50e3c2',     # Teal
            'ORG': '#f5a623',     # Orange
            'EVENT': '#e94b3c',   # Red
            'UNKNOWN': '#95a5a6'  # Gray
        }
        
        # Relation colors (Indonesian categories)
        self.relation_colors = {
            'keluarga': '#e91e63',       # Pink (family relations)
            'konflik': '#f44336',        # Red (conflict relations)
            'lokasi': '#00bcd4',         # Cyan (location relations)
            'partisipasi': '#4caf50',    # Green (participation relations)
            'sosial': '#9c27b0',         # Purple (social relations)
            'asosiasi': '#9e9e9e'        # Gray (association)
        }
    
    def _init_relation_patterns(self) -> List[Dict]:
        """Initialize regex patterns for relation extraction."""
        return [
            # Relasi Keluarga (Family Relations) - More patterns
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:putra|putri|anak)\s+(?:dari\s+)?(.+)',
             'relation': 'anak_dari', 'reverse': True, 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+melahirkan\s+(.+)',
             'relation': 'orang_tua_dari', 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:ayah|bapak)\s+(?:dari\s+)?(.+)',
             'relation': 'ayah_dari', 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:ibu|ibunda)\s+(?:dari\s+)?(.+)',
             'relation': 'ibu_dari', 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:dan|dengan|serta)\s+(.+?)\s+(?:menikah|bersuami|beristri|dipersunting)',
             'relation': 'menikah_dengan', 'bidirectional': True, 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:suami|istri|permaisuri)\s+(?:dari\s+)?(.+)',
             'relation': 'pasangan_dari', 'bidirectional': True, 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:dan|dengan|serta)\s+(.+?)\s+(?:adalah\s+)?(?:saudara|kakak|adik|saudari)',
             'relation': 'saudara_dari', 'bidirectional': True, 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?kakak\s+(?:dari\s+)?(.+)',
             'relation': 'kakak_dari', 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?adik\s+(?:dari\s+)?(.+)',
             'relation': 'adik_dari', 'category': 'keluarga'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:keturunan|keponakan|cucu)\s+(?:dari\s+)?(.+)',
             'relation': 'keturunan_dari', 'category': 'keluarga'},
            
            # Relasi Konflik (Conflict Relations) - More patterns
            {'pattern': r'(.+?)\s+(?:melawan|memerangi|berperang\s+dengan|bertempur\s+dengan|bertarung\s+dengan)\s+(.+)',
             'relation': 'melawan', 'bidirectional': True, 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:dibunuh|gugur|tewas|mati|meninggal)\s+(?:oleh|karena|di\s+tangan|akibat)\s+(.+)',
             'relation': 'dibunuh_oleh', 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:membunuh|mengalahkan|menewaskan|menghabisi|melukai)\s+(.+)',
             'relation': 'membunuh', 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:menyerang|menghancurkan|menjarah)\s+(.+)',
             'relation': 'menyerang', 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:kalah|dikalahkan)\s+(?:oleh|dari)\s+(.+)',
             'relation': 'dikalahkan_oleh', 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:mengalahkan|menang\s+(?:atas|melawan))\s+(.+)',
             'relation': 'mengalahkan', 'category': 'konflik'},
            {'pattern': r'(.+?)\s+(?:bermusuhan|berkonflik)\s+dengan\s+(.+)',
             'relation': 'bermusuhan_dengan', 'bidirectional': True, 'category': 'konflik'},
            
            # Relasi Lokasi/Kekuasaan (Location/Rule Relations) - More patterns
            {'pattern': r'(.+?)\s+(?:memerintah|memimpin|menguasai|berkuasa|raja)\s+(?:di|atas|negara|kerajaan)?\s*(.+)',
             'relation': 'memerintah_di', 'category': 'lokasi'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:raja|ratu|pemimpin|penguasa)\s+(?:dari|di)\s+(.+)',
             'relation': 'penguasa_dari', 'category': 'lokasi'},
            {'pattern': r'(.+?)\s+(?:gugur|mati|meninggal|tewas|wafat)\s+(?:di|dalam|pada)\s+(.+)',
             'relation': 'meninggal_di', 'category': 'lokasi'},
            {'pattern': r'(.+?)\s+(?:berada|tinggal|berasal|datang)\s+(?:di|dari)\s+(.+)',
             'relation': 'berada_di', 'category': 'lokasi'},
            {'pattern': r'(.+?)\s+(?:pergi|menuju|berangkat)\s+(?:ke|menuju)\s+(.+)',
             'relation': 'pergi_ke', 'category': 'lokasi'},
            {'pattern': r'(.+?)\s+(?:lahir|dilahirkan)\s+(?:di|dalam)\s+(.+)',
             'relation': 'lahir_di', 'category': 'lokasi'},
            
            # Relasi Partisipasi (Participation Relations) - More patterns
            {'pattern': r'(.+?)\s+(?:ikut|mengikuti|berpartisipasi|terlibat)\s+(?:dalam|di)\s+(.+)',
             'relation': 'ikut_dalam', 'category': 'partisipasi'},
            {'pattern': r'(.+?)\s+(?:adalah\s+)?(?:anggota|bagian|tokoh)\s+(?:dari\s+)?(.+)',
             'relation': 'anggota_dari', 'category': 'partisipasi'},
            {'pattern': r'(.+?)\s+(?:memimpin|mengepalai|mengomandani)\s+(.+)',
             'relation': 'memimpin', 'category': 'partisipasi'},
            {'pattern': r'(.+?)\s+(?:bergabung|masuk)\s+(?:dengan|ke|dalam)\s+(.+)',
             'relation': 'bergabung_dengan', 'category': 'partisipasi'},
            
            # Relasi Sosial (Social Relations) - New patterns
            {'pattern': r'(.+?)\s+(?:bertemu|berjumpa)\s+(?:dengan|sama)\s+(.+)',
             'relation': 'bertemu_dengan', 'bidirectional': True, 'category': 'sosial'},
            {'pattern': r'(.+?)\s+(?:membantu|menolong)\s+(.+)',
             'relation': 'membantu', 'category': 'sosial'},
            {'pattern': r'(.+?)\s+(?:bersahabat|berteman)\s+dengan\s+(.+)',
             'relation': 'bersahabat_dengan', 'bidirectional': True, 'category': 'sosial'},
            {'pattern': r'(.+?)\s+(?:mengutus|mengirim|menyuruh)\s+(.+)',
             'relation': 'mengutus', 'category': 'sosial'},
            {'pattern': r'(.+?)\s+(?:diutus|dikirim)\s+(?:oleh|dari)\s+(.+)',
             'relation': 'diutus_oleh', 'category': 'sosial'},
        ]
    
    def load_from_json(self, json_path: str):
        """
        Load entities from full_data.json.
        
        Args:
            json_path: Path to JSON file with annotations
        """
        logger.info(f"Loading data from {json_path}...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} annotated examples")
        
        # Process each example
        for idx, item in enumerate(data):
            if isinstance(item, (list, tuple)) and len(item) == 2:
                text, entities_dict = item
                entities = entities_dict.get('entities', [])
                
                # Add entities to graph
                for start, end, label in entities:
                    entity_text = text[start:end]
                    self.add_entity(entity_text, label)
                
                # Extract relations from text
                if len(entities) > 1:
                    entity_list = [(text[s:e], l) for s, e, l in entities]
                    # 1. Regex-based extraction
                    self.extract_relations(text, entity_list)
                    # 2. Dependency parsing (if model available)
                    if self.nlp:
                        self.extract_relations_dependency(text, entity_list)
                    # 3. Co-occurrence based (for entities in same sentence)
                    self.extract_cooccurrence_relations(entity_list)
        
        logger.info(f"Graph built: {self.graph.number_of_nodes()} nodes, "
                   f"{self.graph.number_of_edges()} edges")
    
    def add_entity(self, entity_text: str, entity_type: str):
        """
        Add entity to knowledge graph.
        
        Args:
            entity_text: Entity text
            entity_type: Entity type (PERSON, LOC, ORG, EVENT)
        """
        entity_text = entity_text.strip()
        
        if not entity_text:
            return
        
        # Track mentions
        if entity_text not in self.entity_mentions:
            self.entity_mentions[entity_text] = []
        self.entity_mentions[entity_text].append(entity_type)
        
        # Add or update node
        if self.graph.has_node(entity_text):
            self.graph.nodes[entity_text]['count'] += 1
            # Update type if needed (majority vote)
            types = self.entity_mentions[entity_text]
            most_common_type = Counter(types).most_common(1)[0][0]
            self.graph.nodes[entity_text]['type'] = most_common_type
        else:
            self.graph.add_node(
                entity_text,
                type=entity_type,
                count=1
            )
    
    def extract_relations(self, text: str, entities: List[Tuple[str, str]]):
        """
        Extract relations from text using patterns.
        
        Args:
            text: Source text
            entities: List of (entity_text, entity_type) tuples
        """
        # Create entity map
        entity_set = {e[0] for e in entities}
        
        # Try each pattern
        for pattern_info in self.relation_patterns:
            pattern = pattern_info['pattern']
            relation = pattern_info['relation']
            category = pattern_info['category']
            
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                if len(match.groups()) >= 2:
                    subj = match.group(1).strip()
                    obj = match.group(2).strip()
                    
                    # Find matching entities
                    subj_entity = self._find_entity_in_text(subj, entity_set)
                    obj_entity = self._find_entity_in_text(obj, entity_set)
                    
                    if subj_entity and obj_entity and subj_entity != obj_entity:
                        # Add relation
                        if pattern_info.get('reverse'):
                            # Reverse direction (e.g., "A anak dari B" → B parent_of A)
                            self.add_relation(obj_entity, relation, subj_entity, category)
                        elif pattern_info.get('bidirectional'):
                            # Add both directions
                            self.add_relation(subj_entity, relation, obj_entity, category)
                            self.add_relation(obj_entity, relation, subj_entity, category)
                        else:
                            # Normal direction
                            self.add_relation(subj_entity, relation, obj_entity, category)
    
    def _find_entity_in_text(self, text: str, entity_set: Set[str]) -> str:
        """Find which entity from entity_set is mentioned in text."""
        text_lower = text.lower()
        for entity in entity_set:
            if entity.lower() in text_lower or text_lower in entity.lower():
                return entity
        return None
    
    def extract_relations_dependency(self, text: str, entities: List[Tuple[str, str]]):
        """
        Extract relations using spaCy dependency parsing.
        
        Args:
            text: Source text
            entities: List of (entity_text, entity_type) tuples
        """
        if not self.nlp:
            return
        
        entity_set = {e[0] for e in entities}
        entity_map = {e[0]: e[1] for e in entities}
        
        # Parse text
        doc = self.nlp(text)
        
        # Map entities to tokens
        entity_tokens = {}
        for ent_text in entity_set:
            ent_text_lower = ent_text.lower()
            for token in doc:
                if ent_text_lower in token.text.lower():
                    entity_tokens[token.i] = ent_text
        
        # Analyze dependency relations
        for token in doc:
            if token.i in entity_tokens:
                subj_entity = entity_tokens[token.i]
                
                # Check direct dependencies
                for child in token.children:
                    if child.i in entity_tokens:
                        obj_entity = entity_tokens[child.i]
                        
                        # Determine relation type based on dependency label
                        if child.dep_ in ['nsubj', 'obj', 'iobj']:
                            # Subject-Object relation
                            relation = self._infer_relation_from_verb(token.text, token.pos_)
                            if relation:
                                self.add_relation(subj_entity, relation['type'], obj_entity, relation['category'])
                        
                        elif child.dep_ in ['conj']:
                            # Conjunction - possible sibling or association
                            subj_type = entity_map.get(subj_entity)
                            obj_type = entity_map.get(obj_entity)
                            if subj_type == 'PERSON' and obj_type == 'PERSON':
                                self.add_relation(subj_entity, 'terkait_dengan', obj_entity, 'sosial')
                
                # Check if token has prep (preposition) relation
                for child in token.children:
                    if child.dep_ == 'prep':
                        prep_text = child.text.lower()
                        # Look for entity after preposition
                        for grandchild in child.children:
                            if grandchild.i in entity_tokens:
                                obj_entity = entity_tokens[grandchild.i]
                                
                                # Infer relation based on preposition
                                if prep_text in ['di', 'dari', 'ke']:
                                    obj_type = entity_map.get(obj_entity)
                                    if obj_type == 'LOC':
                                        self.add_relation(subj_entity, 'berada_di', obj_entity, 'lokasi')
    
    def _infer_relation_from_verb(self, verb: str, pos: str) -> Dict[str, str]:
        """Infer relation type from verb."""
        if pos != 'VERB':
            return None
        
        verb_lower = verb.lower()
        
        # Conflict verbs
        conflict_verbs = ['membunuh', 'mengalahkan', 'menyerang', 'melukai', 'melawan']
        if any(v in verb_lower for v in conflict_verbs):
            return {'type': 'melawan', 'category': 'konflik'}
        
        # Social verbs
        social_verbs = ['membantu', 'menolong', 'mengutus', 'mengirim']
        if any(v in verb_lower for v in social_verbs):
            return {'type': 'membantu', 'category': 'sosial'}
        
        # Leadership verbs
        leadership_verbs = ['memimpin', 'memerintah', 'menguasai']
        if any(v in verb_lower for v in leadership_verbs):
            return {'type': 'memimpin', 'category': 'partisipasi'}
        
        return None
    
    def extract_cooccurrence_relations(self, entities: List[Tuple[str, str]]):
        """
        Extract relations based on entity co-occurrence in same sentence.
        Uses statistical co-occurrence as weak signal for association.
        
        Args:
            entities: List of (entity_text, entity_type) tuples
        """
        # Only for sentences with 2-4 entities (avoid too sparse or too dense)
        if len(entities) < 2 or len(entities) > 4:
            return
        
        # Build entity type map
        entity_map = {e[0]: e[1] for e in entities}
        
        # Create associations between co-occurring entities
        for i, (ent1, type1) in enumerate(entities):
            for ent2, type2 in entities[i+1:]:
                if ent1 != ent2 and self.graph.has_node(ent1) and self.graph.has_node(ent2):
                    # Only add if no stronger relation exists
                    if not self.graph.has_edge(ent1, ent2) and not self.graph.has_edge(ent2, ent1):
                        # Determine relation type based on entity types
                        if type1 == 'PERSON' and type2 == 'PERSON':
                            # Person-Person co-occurrence
                            self.add_relation(ent1, 'berinteraksi_dengan', ent2, 'sosial')
                            self.add_relation(ent2, 'berinteraksi_dengan', ent1, 'sosial')
                        elif type1 == 'PERSON' and type2 == 'LOC':
                            # Person-Location co-occurrence
                            self.add_relation(ent1, 'terkait_dengan_lokasi', ent2, 'lokasi')
                        elif type1 == 'LOC' and type2 == 'PERSON':
                            self.add_relation(ent2, 'terkait_dengan_lokasi', ent1, 'lokasi')
                        elif type1 == 'PERSON' and type2 in ['ORG', 'EVENT']:
                            # Person-Org/Event co-occurrence
                            self.add_relation(ent1, 'terlibat_dalam', ent2, 'partisipasi')
                        elif type2 == 'PERSON' and type1 in ['ORG', 'EVENT']:
                            self.add_relation(ent2, 'terlibat_dalam', ent1, 'partisipasi')
    
    def add_relation(self, source: str, relation_type: str, target: str, category: str = 'asosiasi'):
        """
        Add relation edge to graph.
        
        Args:
            source: Source entity
            relation_type: Relation type
            target: Target entity
            category: Relation category for coloring
        """
        # Ensure nodes exist
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            return
        
        # Add or update edge
        if self.graph.has_edge(source, target):
            edge_data = self.graph[source][target]
            if relation_type not in edge_data['relations']:
                edge_data['relations'].append(relation_type)
            edge_data['count'] += 1
        else:
            self.graph.add_edge(
                source, target,
                relations=[relation_type],
                category=category,
                count=1
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph) if self.graph.number_of_nodes() > 0 else 0
        }
        
        # Entity type distribution
        entity_types = Counter(
            data['type'] for _, data in self.graph.nodes(data=True)
        )
        stats['entity_distribution'] = dict(entity_types)
        
        # Relation type distribution
        relation_counts = Counter()
        for _, _, data in self.graph.edges(data=True):
            for rel in data.get('relations', []):
                relation_counts[rel] += 1
        stats['relation_distribution'] = dict(relation_counts)
        
        # Top entities by degree
        degrees = dict(self.graph.degree())
        if degrees:
            top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
            stats['top_entities'] = [
                {'entity': e, 'connections': d, 'type': self.graph.nodes[e]['type']}
                for e, d in top_entities
            ]
        else:
            stats['top_entities'] = []
        
        return stats
    
    def create_visualization(self, output_path: str = "output/knowledge_graph.html",
                            max_nodes: int = 100):
        """
        Create interactive HTML visualization.
        
        Args:
            output_path: Output HTML file path
            max_nodes: Maximum nodes to display
        """
        logger.info("Creating interactive visualization...")
        
        # Create PyVis network
        net = Network(
            height="900px",
            width="100%",
            bgcolor="#1a1a1a",
            font_color="white",
            directed=True,
            notebook=False
        )
        
        # Configure physics for better layout
        net.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {
              "enabled": true,
              "iterations": 200
            },
            "barnesHut": {
              "gravitationalConstant": -15000,
              "centralGravity": 0.3,
              "springLength": 120,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 0.2
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "navigationButtons": true,
            "keyboard": true,
            "zoomView": true,
            "dragView": true
          },
          "nodes": {
            "font": {
              "size": 14,
              "face": "Arial"
            },
            "borderWidth": 2,
            "shadow": true
          },
          "edges": {
            "font": {
              "size": 11,
              "align": "middle"
            },
            "smooth": {
              "type": "continuous",
              "roundness": 0.5
            },
            "arrows": {
              "to": {
                "enabled": true,
                "scaleFactor": 0.8
              }
            },
            "shadow": true
          }
        }
        """)
        
        # Get node degrees for sizing
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values()) if degrees else 1
        
        # Select top nodes by degree
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        nodes_to_display = [n for n, _ in sorted_nodes[:max_nodes]]
        
        logger.info(f"Displaying top {len(nodes_to_display)} nodes by connectivity")
        
        # Add nodes
        for node in nodes_to_display:
            node_data = self.graph.nodes[node]
            entity_type = node_data.get('type', 'UNKNOWN')
            count = node_data.get('count', 1)
            degree = degrees[node]
            
            # Size based on degree (10-50 range)
            size = 15 + (degree / max_degree) * 35
            
            # Color based on entity type
            color = self.entity_colors.get(entity_type, '#95a5a6')
            
            # Tooltip
            title = (f"<b>{node}</b><br>"
                    f"Type: {entity_type}<br>"
                    f"Mentions: {count}<br>"
                    f"Connections: {degree}")
            
            net.add_node(
                node,
                label=node,
                title=title,
                color=color,
                size=size
            )
        
        # Add edges
        edge_count = 0
        for source, target in self.graph.edges():
            if source in nodes_to_display and target in nodes_to_display:
                edge_data = self.graph[source][target]
                relations = edge_data.get('relations', [])
                category = edge_data.get('category', 'association')
                count = edge_data.get('count', 1)
                
                # Format label
                if len(relations) == 1:
                    label = relations[0].replace('_', ' ')
                else:
                    label = f"{relations[0].replace('_', ' ')} +{len(relations)-1}"
                
                # Color based on category
                color = self.relation_colors.get(category, '#9e9e9e')
                
                # Width based on frequency
                width = min(1 + count * 0.3, 4)
                
                # Tooltip
                all_relations = ', '.join([r.replace('_', ' ') for r in relations])
                title = f"{source} → {target}<br>{all_relations}"
                if count > 1:
                    title += f"<br>Frequency: {count}x"
                
                net.add_edge(
                    source, target,
                    label=label,
                    title=title,
                    color=color,
                    width=width
                )
                edge_count += 1
        
        # Add legend as HTML overlay (Indonesian labels)
        legend_html = """
        <div style="position: fixed; top: 10px; right: 10px; background: rgba(0,0,0,0.8); 
                    padding: 15px; border-radius: 8px; font-family: Arial; color: white; 
                    font-size: 13px; z-index: 1000;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px;">Legenda Graf Pengetahuan</h3>
            <div style="margin-bottom: 10px;">
                <b>Tipe Entitas:</b><br>
                <span style="color: #4a90e2;">●</span> PERSON (Tokoh)<br>
                <span style="color: #50e3c2;">●</span> LOC (Lokasi)<br>
                <span style="color: #f5a623;">●</span> ORG (Organisasi)<br>
                <span style="color: #e94b3c;">●</span> EVENT (Peristiwa)
            </div>
            <div>
                <b>Kategori Relasi:</b><br>
                <span style="color: #e91e63;">―</span> Keluarga<br>
                <span style="color: #f44336;">―</span> Konflik<br>
                <span style="color: #00bcd4;">―</span> Lokasi<br>
                <span style="color: #4caf50;">―</span> Partisipasi<br>
                <span style="color: #9c27b0;">―</span> Sosial
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #aaa;">
                • Ukuran node = konektivitas<br>
                • Ketebalan edge = frekuensi<br>
                • Hover untuk detail
            </div>
        </div>
        """
        
        # Save visualization
        net.save_graph(output_path)
        
        # Add legend to HTML
        with open(output_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        html = html.replace('</body>', f'{legend_html}</body>')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✓ Visualization saved to {output_path}")
        logger.info(f"  Nodes: {len(nodes_to_display)}, Edges: {edge_count}")
    
    def save_json(self, output_path: str = "output/knowledge_graph.json"):
        """
        Save graph to JSON.
        
        Args:
            output_path: Output JSON file path
        """
        # Build nodes
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                'id': node,
                'label': node,
                'type': data.get('type', 'UNKNOWN'),
                'count': data.get('count', 1)
            })
        
        # Build edges
        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                'source': source,
                'target': target,
                'relations': data.get('relations', []),
                'category': data.get('category', 'association'),
                'count': data.get('count', 1)
            })
        
        graph_data = {
            'nodes': nodes,
            'edges': edges,
            'statistics': self.get_statistics()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ Graph data saved to {output_path}")


def main():
    """Main function to build knowledge graph."""
    print("="*60)
    print("Knowledge Graph Builder - Custom NER Model")
    print("="*60)
    print()
    
    # Paths
    model_path = "models/custom_ner_model"
    data_path = "models/full_data.json"
    html_output = "output/knowledge_graph.html"
    json_output = "output/knowledge_graph.json"
    
    # Build graph
    builder = KnowledgeGraphBuilder(model_path=model_path)
    builder.load_from_json(data_path)
    
    # Get statistics
    stats = builder.get_statistics()
    
    print("\n" + "="*60)
    print("Graph Statistics")
    print("="*60)
    print(f"Total Entities: {stats['total_nodes']}")
    print(f"Total Relations: {stats['total_edges']}")
    print(f"Graph Density: {stats['density']:.4f}")
    
    print(f"\nEntity Distribution:")
    for entity_type, count in stats['entity_distribution'].items():
        print(f"  {entity_type}: {count}")
    
    if stats['relation_distribution']:
        print(f"\nRelation Distribution:")
        for rel_type, count in sorted(stats['relation_distribution'].items(), 
                                      key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {rel_type}: {count}")
    
    if stats['top_entities']:
        print(f"\nTop 10 Most Connected Entities:")
        for entity_info in stats['top_entities']:
            print(f"  {entity_info['entity']} ({entity_info['type']}): "
                  f"{entity_info['connections']} connections")
    
    # Save outputs
    print(f"\n" + "="*60)
    print("Generating Outputs")
    print("="*60)
    builder.save_json(json_output)
    builder.create_visualization(html_output, max_nodes=100)
    
    print(f"\n" + "="*60)
    print("✓ Knowledge Graph Built Successfully!")
    print("="*60)
    print(f"\nView the interactive graph:")
    print(f"  xdg-open {html_output}")
    print(f"\nGraph data saved to:")
    print(f"  {json_output}")


if __name__ == "__main__":
    main()
