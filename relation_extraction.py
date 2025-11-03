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

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RelationExtractor:
    """
    Extracts semantic relations between entities in wayang texts.
    Uses rule-based pattern matching for Indonesian language.
    """
    
    def __init__(self):
        """Initialize relation extractor with pattern rules."""
        self.relation_patterns = self._init_relation_patterns()
    
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
                        relation = {
                            'subject': subject_entity['text'],
                            'subject_type': subject_entity['type'],
                            'relation': relation_type,
                            'object': object_entity['text'],
                            'object_type': object_entity['type'],
                            'context': match.group(0),
                            'confidence': 0.8
                        }
                        relations.append(relation)
        
        # Remove duplicate relations
        relations = self._deduplicate_relations(relations)
        
        return relations
    
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
        
        # Proximity-based relation inference
        proximity_relations = self._extract_proximity_relations(text, entities)
        relations.extend(proximity_relations)
        
        # Deduplicate
        relations = self._deduplicate_relations(relations)
        
        return relations
    
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
                            # Infer generic "associated_with" relation
                            relations.append({
                                'subject': e1['text'],
                                'subject_type': e1['type'],
                                'relation': 'associated_with',
                                'object': e2['text'],
                                'object_type': e2['type'],
                                'context': sentence.strip(),
                                'confidence': 0.5
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
