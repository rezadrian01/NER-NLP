"""
Relation Extraction Module for Wayang Knowledge Graph
Author: Ahmad Reza Adrian

This module extracts semantic relations between entities using
rule-based pattern matching and dependency parsing.
"""

import re
import logging
from typing import List, Dict, Tuple, Any
import pandas as pd

# Import dynamic relation labeler
try:
    from dynamic_relation_labeler import DynamicRelationLabeler
    DYNAMIC_LABELER_AVAILABLE = True
except ImportError:
    DYNAMIC_LABELER_AVAILABLE = False
    logging.warning("Dynamic relation labeler not available")

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RelationExtractor:
    """
    Extracts semantic relations between entities in wayang texts.
    Uses rule-based pattern matching for Indonesian language.
    """
    
    def __init__(self, use_dynamic_labels: bool = True):
        """
        Initialize relation extractor with pattern rules.
        
        Args:
            use_dynamic_labels: Whether to use dynamic relation labeling
        """
        self.relation_patterns = self._init_relation_patterns()
        
        # Reverse relation mappings for bidirectional inference
        self.reverse_relations = {
            'child_of': 'parent_of',
            'parent_of': 'child_of',
            'married_to': 'married_to',  # symmetric
            'sibling_of': 'sibling_of',  # symmetric
            'fought_with': 'fought_with',  # symmetric
            'killed_by': 'killed',
            'killed': 'killed_by',
            'ruled_in': 'ruled_by',
            'ruled_by': 'ruled_in'
        }
        
        # Initialize dynamic relation labeler
        self.use_dynamic_labels = use_dynamic_labels and DYNAMIC_LABELER_AVAILABLE
        self.dynamic_labeler = None
        if self.use_dynamic_labels:
            try:
                self.dynamic_labeler = DynamicRelationLabeler()
                logger.info("Dynamic relation labeling enabled")
            except Exception as e:
                logger.warning(f"Could not initialize dynamic labeler: {e}")
                self.use_dynamic_labels = False
    
    def _init_relation_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Initialize relation extraction patterns.
        
        Returns:
            Dictionary of relation types to pattern configurations
        """
        return {
            'child_of': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?putra\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?putri\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?anak\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'putra\s+(\w+(?:\s+\w+)*)\s+(?:yang\s+)?(?:bernama|adalah)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 2,
                    'object_group': 1
                }
            ],
            'married_to': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+menikah\s+dengan\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?istri\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?suami\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'perkawinan\s+(?:antara\s+)?(\w+(?:\s+\w+)*)\s+(?:dengan|dan)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+rabi\s+(?:dengan\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ],
            'fought_with': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+bertempur\s+(?:dengan|melawan)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+bertarung\s+(?:dengan|melawan)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+melawan\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'pertempuran\s+(?:antara\s+)?(\w+(?:\s+\w+)*)\s+(?:dengan|dan|melawan)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ],
            'killed_by': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+tewas\s+(?:di\s+tangan|oleh)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+gugur\s+(?:di\s+tangan|oleh)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+dibunuh\s+(?:oleh\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+mati\s+(?:di\s+tangan|oleh)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ],
            'sibling_of': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?(?:kakak|adik|saudara)\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+dan\s+(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?(?:kakak\s+beradik|bersaudara)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ],
            'ruled_in': [
                {
                    'pattern': r'(?:Prabu|Raja)\s+(\w+(?:\s+\w+)*)\s+(?:memerintah\s+)?(?:di|dari)\s+(Kerajaan\s+\w+)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?raja\s+(?:di|dari)\s+(Kerajaan\s+\w+)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(Kerajaan\s+\w+)\s+(?:dipimpin|diperintah)\s+(?:oleh\s+)?(?:Prabu|Raja)?\s*(\w+(?:\s+\w+)*)',
                    'subject_group': 2,
                    'object_group': 1
                }
            ],
            'died_in': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+gugur\s+(?:dalam|di)\s+(?:perang|pertempuran)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+tewas\s+(?:dalam|di)\s+(?:perang|pertempuran)?\s*(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+mati\s+(?:dalam|di)\s+(?:perang|pertempuran)\s+(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ],
            'parent_of': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:adalah\s+)?(?:ayah|ibu|orang\s+tua)\s+(?:dari\s+)?(\w+(?:\s+\w+)*)',
                    'subject_group': 1,
                    'object_group': 2
                }
            ]
        }
    
    def extract_relations_from_text(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract relations from text using pattern matching.
        
        Args:
            text: Input text
            entities: List of extracted entities
            
        Returns:
            List of relation dictionaries
        """
        relations = []
        
        # Create entity lookup by text
        entity_texts = {e['text'].lower(): e for e in entities}
        
        # Apply each relation pattern
        for relation_type, patterns in self.relation_patterns.items():
            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                subj_group = pattern_config['subject_group']
                obj_group = pattern_config['object_group']
                
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    subject_text = match.group(subj_group).strip()
                    object_text = match.group(obj_group).strip()
                    
                    # Check if subject and object are recognized entities
                    subject_entity = self._find_entity(subject_text, entities)
                    object_entity = self._find_entity(object_text, entities)
                    
                    if subject_entity and object_entity:
                        context_text = match.group(0)
                        
                        # Generate dynamic label if enabled
                        dynamic_label = None
                        if self.use_dynamic_labels and self.dynamic_labeler:
                            dynamic_label = self.dynamic_labeler.extract_relation_label(
                                subject_entity['text'],
                                object_entity['text'],
                                context_text,
                                relation_type
                            )
                        
                        relation = {
                            'subject': subject_entity['text'],
                            'subject_type': subject_entity['type'],
                            'relation': relation_type,
                            'object': object_entity['text'],
                            'object_type': object_entity['type'],
                            'context': context_text,
                            'confidence': 0.8,
                            'dynamic_label': dynamic_label
                        }
                        relations.append(relation)
        
        # Remove duplicate relations
        relations = self._deduplicate_relations(relations)
        
        return relations
    
    def extract_relations_from_entities(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract relations considering entity proximity and co-occurrence.
        
        Args:
            text: Input text
            entities: List of entities
            
        Returns:
            List of relations
        """
        # Pattern-based extraction
        relations = self.extract_relations_from_text(text, entities)
        
        # Add reverse relations (e.g., if A child_of B, then B parent_of A)
        relations = self._add_reverse_relations(relations)
        
        # Proximity-based relation inference (only if no other relations found)
        if len(relations) < len(entities) * 0.3:  # Less than 30% coverage
            proximity_relations = self._extract_proximity_relations(text, entities)
            relations.extend(proximity_relations)
        
        # Deduplicate
        relations = self._deduplicate_relations(relations)
        
        return relations
    
    def _add_reverse_relations(self, relations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add reverse relations for bidirectional relationships.
        
        Args:
            relations: Original relations
            
        Returns:
            Relations with reverse relations added
        """
        reverse_relations = []
        
        for relation in relations:
            rel_type = relation['relation']
            
            # Check if this relation has a reverse
            if rel_type in self.reverse_relations:
                reverse_rel_type = self.reverse_relations[rel_type]
                
                # Don't create reverse for symmetric relations (would be duplicate)
                if rel_type != reverse_rel_type:
                    # Generate dynamic label for reverse relation if enabled
                    dynamic_label = None
                    if self.use_dynamic_labels and self.dynamic_labeler and relation.get('context'):
                        dynamic_label = self.dynamic_labeler.extract_relation_label(
                            relation['object'],
                            relation['subject'],
                            relation['context'],
                            reverse_rel_type
                        )
                    
                    reverse_relation = {
                        'subject': relation['object'],
                        'subject_type': relation['object_type'],
                        'relation': reverse_rel_type,
                        'object': relation['subject'],
                        'object_type': relation['subject_type'],
                        'context': relation['context'],
                        'confidence': relation['confidence'],
                        'dynamic_label': dynamic_label
                    }
                    reverse_relations.append(reverse_relation)
        
        return relations + reverse_relations
    
    def _find_entity(self, text: str, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Find entity that matches the given text.
        
        Args:
            text: Text to match
            entities: List of entities
            
        Returns:
            Matching entity or None
        """
        text_lower = text.lower()
        
        # Exact match
        for entity in entities:
            if entity['text'].lower() == text_lower:
                return entity
        
        # Partial match (entity contains text or vice versa)
        for entity in entities:
            entity_lower = entity['text'].lower()
            if text_lower in entity_lower or entity_lower in text_lower:
                # Prefer longer match
                if len(entity_lower) >= len(text_lower) * 0.7:
                    return entity
        
        return None
    
    def _deduplicate_relations(self, relations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate relations.
        
        Args:
            relations: List of relations
            
        Returns:
            Deduplicated list
        """
        seen = set()
        unique_relations = []
        
        for relation in relations:
            # Create a key for deduplication
            key = (
                relation['subject'].lower(),
                relation['relation'],
                relation['object'].lower()
            )
            
            if key not in seen:
                seen.add(key)
                unique_relations.append(relation)
        
        return unique_relations
    
    def _extract_proximity_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Infer relations based on entity proximity in text.
        
        Args:
            text: Input text
            entities: List of entities
            
        Returns:
            List of inferred relations
        """
        relations = []
        person_entities = [e for e in entities if e['type'] == 'PERSON']
        
        # Check for entities appearing in same sentence
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence_entities = [e for e in person_entities 
                               if e['text'].lower() in sentence.lower()]
            
            # If multiple persons in same sentence, they might be related
            if len(sentence_entities) >= 2:
                # Look for connecting words
                if any(word in sentence.lower() for word in ['dan', 'dengan', 'bersama']):
                    for i, e1 in enumerate(sentence_entities[:-1]):
                        for e2 in sentence_entities[i+1:]:
                            # Infer specific relation type based on entity types and context
                            relation_type = 'associated_with'
                            
                            # Try to infer more specific relation
                            if e1['type'] == 'PERSON' and e2['type'] == 'PERSON':
                                if any(word in sentence.lower() for word in ['bersama', 'dengan', 'dan']):
                                    relation_type = 'associated_with'
                            elif e1['type'] == 'PERSON' and e2['type'] == 'LOC':
                                if any(word in sentence.lower() for word in ['di', 'ke', 'dari']):
                                    relation_type = 'located_in'
                            elif e1['type'] == 'PERSON' and e2['type'] == 'EVENT':
                                if any(word in sentence.lower() for word in ['dalam', 'saat', 'ketika']):
                                    relation_type = 'participated_in'
                            elif e1['type'] == 'PERSON' and e2['type'] == 'ORG':
                                relation_type = 'member_of'
                            
                            # Generate dynamic label if enabled
                            dynamic_label = None
                            if self.use_dynamic_labels and self.dynamic_labeler:
                                dynamic_label = self.dynamic_labeler.extract_relation_label(
                                    e1['text'],
                                    e2['text'],
                                    sentence.strip(),
                                    relation_type
                                )
                            
                            relations.append({
                                'subject': e1['text'],
                                'subject_type': e1['type'],
                                'relation': relation_type,
                                'object': e2['text'],
                                'object_type': e2['type'],
                                'context': sentence.strip(),
                                'confidence': 0.5,
                                'dynamic_label': dynamic_label
                            })
        
        return relations
    
    def process_dataframe(self, df: pd.DataFrame, 
                         text_column: str = 'normalized_text',
                         entities_column: str = 'entities') -> pd.DataFrame:
        """
        Extract relations from all documents in DataFrame.
        
        Args:
            df: Input DataFrame
            text_column: Column containing text
            entities_column: Column containing entities
            
        Returns:
            DataFrame with relations column added
        """
        logger.info(f"Extracting relations from {len(df)} documents...")
        
        relations_list = []
        for idx, row in df.iterrows():
            text = row[text_column]
            entities = row[entities_column]
            
            if pd.notna(text) and entities:
                relations = self.extract_relations_from_entities(text, entities)
                relations_list.append(relations)
            else:
                relations_list.append([])
            
            if (idx + 1) % 50 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} documents")
        
        df['relations'] = relations_list
        df['relation_count'] = df['relations'].apply(len)
        
        logger.info(f"Extraction complete. Total relations: {df['relation_count'].sum()}")
        
        return df


def main():
    """
    Main function for testing relation extraction.
    """
    # Test data
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra. Ia gugur dalam perang Bharatayudha.
    Prabu Kresna memerintah di Kerajaan Dwarawati. Arjuna menikah dengan Subadra.
    """
    
    # Sample entities
    entities = [
        {'text': 'Abimanyu', 'type': 'PERSON', 'start': 0, 'end': 8},
        {'text': 'Arjuna', 'type': 'PERSON', 'start': 24, 'end': 30},
        {'text': 'Subadra', 'type': 'PERSON', 'start': 35, 'end': 42},
        {'text': 'perang Bharatayudha', 'type': 'EVENT', 'start': 60, 'end': 79},
        {'text': 'Prabu Kresna', 'type': 'PERSON', 'start': 81, 'end': 93},
        {'text': 'Kerajaan Dwarawati', 'type': 'LOC', 'start': 110, 'end': 128}
    ]
    
    # Extract relations
    extractor = RelationExtractor()
    relations = extractor.extract_relations_from_entities(sample_text, entities)
    
    print("=== Relation Extraction Results ===")
    print(f"Found {len(relations)} relations:")
    for relation in relations:
        print(f"  ({relation['subject']}) -[{relation['relation']}]-> ({relation['object']})")
        print(f"    Context: {relation['context'][:80]}...")


if __name__ == "__main__":
    main()
