"""
Named Entity Recognition (NER) Module for Wayang Stories
Author: Ahmad Reza Adrian

This module implements NER for Indonesian text using spaCy and transformers.
Extracts entities like PERSON, LOCATION, ORGANIZATION, EVENT, and OBJECT.
"""

import re
import logging
from typing import List, Dict, Tuple, Any
import pandas as pd

try:
    import spacy
    from spacy.tokens import Doc
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logging.warning("spaCy not available. Install with: pip install spacy")

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers not available. Install with: pip install transformers")

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WayangNER:
    """
    Named Entity Recognition system for Indonesian wayang texts.
    Supports both spaCy and transformer-based models.
    """
    
    def __init__(self, model_type: str = "spacy", model_name: str = None):
        """
        Initialize NER system.
        
        Args:
            model_type: Type of model ('spacy' or 'transformers')
            model_name: Specific model name (optional)
        """
        self.model_type = model_type
        self.nlp = None
        self.ner_pipeline = None
        
        # Wayang-specific entity patterns
        self.wayang_patterns = self._init_wayang_patterns()
        
        # Initialize model
        self._load_model(model_name)
        
    def _init_wayang_patterns(self) -> Dict[str, List[str]]:
        """
        Initialize regex patterns for wayang-specific entities.
        
        Returns:
            Dictionary of entity type to patterns
        """
        return {
            'PERSON': [
                r'\b(?:Raden|Dewi|Prabu|Arya|Patih|Pandita|Begawan)\s+\w+(?:\s+\w+)*',
                r'\bAbimanyu\b',
                r'\bArjuna\b',
                r'\bSubadra\b',
                r'\bKresna\b',
                r'\bBaladewa\b',
                r'\bDuryudana\b',
                r'\bBima\b',
                r'\bYudistira\b',
                r'\bNakula\b',
                r'\bSadewa\b',
                r'\bKunthi\b',
                r'\bDrupadi\b',
                r'\bSangkuni\b',
                r'\bKarna\b',
                r'\bDurna\b',
                r'\bBisma\b',
                r'\bSalya\b',
                r'\bSrikandi\b'
            ],
            'LOC': [
                r'\bKerajaan\s+\w+',
                r'\bDwarawati\b',
                r'\bHastina\b',
                r'\bMandura\b',
                r'\bAmarta\b',
                r'\bAlengka\b',
                r'\bIndraprasta\b',
                r'\bKahyangan\s+\w+',
                r'\bMadukara\b',
                r'\bNgastina\b'
            ],
            'EVENT': [
                r'\b(?:Perang|Pertempuran)\s+\w+(?:\s+\w+)*',
                r'\bBharatayudha\b',
                r'\bBrubuh\b'
            ],
            'ORG': [
                r'\bPandawa\b',
                r'\bKurawa\b'
            ]
        }
    
    def _load_model(self, model_name: str = None):
        """
        Load the NER model.
        
        Args:
            model_name: Name of the model to load
        """
        if self.model_type == "spacy":
            self._load_spacy_model(model_name or "xx_ent_wiki_sm")
        elif self.model_type == "transformers":
            self._load_transformer_model(model_name or "indobenchmark/indobert-base-p1")
        else:
            logger.warning(f"Unknown model type: {self.model_type}. Using rule-based only.")
    
    def _load_spacy_model(self, model_name: str):
        """Load spaCy model."""
        if not SPACY_AVAILABLE:
            logger.warning("spaCy not available. Using rule-based NER only.")
            return
            
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")
        except OSError:
            logger.warning(f"Model {model_name} not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model_name])
            try:
                self.nlp = spacy.load(model_name)
                logger.info(f"Loaded spaCy model: {model_name}")
            except:
                logger.warning("Could not load spaCy model. Using rule-based NER only.")
    
    def _load_transformer_model(self, model_name: str):
        """Load transformer model."""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available. Using rule-based NER only.")
            return
            
        try:
            self.ner_pipeline = pipeline("ner", 
                                        model=model_name,
                                        aggregation_strategy="simple")
            logger.info(f"Loaded transformer model: {model_name}")
        except Exception as e:
            logger.warning(f"Could not load transformer model: {e}")
    
    def extract_entities_rule_based(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using rule-based patterns.
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        entities = []
        
        for entity_type, patterns in self.wayang_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group(0).strip()
                    entities.append({
                        'text': entity_text,
                        'type': entity_type,
                        'start': match.start(),
                        'end': match.end(),
                        'method': 'rule-based'
                    })
        
        # Remove duplicates (keep first occurrence)
        seen = set()
        unique_entities = []
        for entity in entities:
            key = (entity['text'].lower(), entity['start'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return sorted(unique_entities, key=lambda x: x['start'])
    
    def extract_entities_spacy(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using spaCy.
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entity_type = ent.label_
            # Map spaCy labels to our schema
            if entity_type in ['PERSON', 'PER']:
                entity_type = 'PERSON'
            elif entity_type in ['LOC', 'GPE', 'LOCATION']:
                entity_type = 'LOC'
            elif entity_type in ['ORG', 'ORGANIZATION']:
                entity_type = 'ORG'
            elif entity_type in ['EVENT']:
                entity_type = 'EVENT'
            else:
                entity_type = 'OTHER'
            
            entities.append({
                'text': ent.text,
                'type': entity_type,
                'start': ent.start_char,
                'end': ent.end_char,
                'method': 'spacy'
            })
        
        return entities
    
    def extract_entities_transformer(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using transformer model.
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not self.ner_pipeline:
            return []
        
        try:
            results = self.ner_pipeline(text)
            entities = []
            
            for result in results:
                entity_type = result['entity_group']
                # Map transformer labels to our schema
                if 'PER' in entity_type.upper():
                    entity_type = 'PERSON'
                elif 'LOC' in entity_type.upper() or 'GPE' in entity_type.upper():
                    entity_type = 'LOC'
                elif 'ORG' in entity_type.upper():
                    entity_type = 'ORG'
                else:
                    entity_type = 'OTHER'
                
                entities.append({
                    'text': result['word'],
                    'type': entity_type,
                    'start': result['start'],
                    'end': result['end'],
                    'score': result['score'],
                    'method': 'transformer'
                })
            
            return entities
        except Exception as e:
            logger.error(f"Error in transformer NER: {e}")
            return []
    
    def extract_entities(self, text: str, combine_methods: bool = True) -> List[Dict[str, Any]]:
        """
        Extract entities using all available methods.
        
        Args:
            text: Input text
            combine_methods: Whether to combine results from multiple methods
            
        Returns:
            List of entity dictionaries
        """
        all_entities = []
        
        # Rule-based extraction (always available)
        rule_entities = self.extract_entities_rule_based(text)
        all_entities.extend(rule_entities)
        
        # spaCy extraction
        if self.nlp and combine_methods:
            spacy_entities = self.extract_entities_spacy(text)
            all_entities.extend(spacy_entities)
        
        # Transformer extraction
        if self.ner_pipeline and combine_methods:
            transformer_entities = self.extract_entities_transformer(text)
            all_entities.extend(transformer_entities)
        
        # Merge overlapping entities
        if combine_methods:
            all_entities = self._merge_entities(all_entities)
        
        return all_entities
    
    def _merge_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge overlapping entities, prioritizing longer matches.
        
        Args:
            entities: List of entity dictionaries
            
        Returns:
            Merged list of entities
        """
        if not entities:
            return []
        
        # Sort by start position, then by length (descending)
        sorted_entities = sorted(entities, 
                                key=lambda x: (x['start'], -(x['end'] - x['start'])))
        
        merged = []
        for entity in sorted_entities:
            # Check if overlaps with any existing entity
            overlaps = False
            for existing in merged:
                if not (entity['end'] <= existing['start'] or entity['start'] >= existing['end']):
                    overlaps = True
                    break
            
            if not overlaps:
                merged.append(entity)
        
        return sorted(merged, key=lambda x: x['start'])
    
    def process_dataframe(self, df: pd.DataFrame, text_column: str = 'normalized_text') -> pd.DataFrame:
        """
        Process a DataFrame and extract entities from all texts.
        
        Args:
            df: Input DataFrame
            text_column: Column containing text to process
            
        Returns:
            DataFrame with entities column added
        """
        logger.info(f"Extracting entities from {len(df)} documents...")
        
        entities_list = []
        for idx, row in df.iterrows():
            text = row[text_column]
            if pd.notna(text):
                entities = self.extract_entities(text)
                entities_list.append(entities)
            else:
                entities_list.append([])
            
            if (idx + 1) % 50 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} documents")
        
        df['entities'] = entities_list
        df['entity_count'] = df['entities'].apply(len)
        
        logger.info(f"Extraction complete. Total entities: {df['entity_count'].sum()}")
        
        return df


def main():
    """
    Main function for testing NER module.
    """
    # Test text
    sample_text = """
    Abimanyu adalah putra Arjuna dan Subadra. Ia gugur dalam perang Bharatayudha.
    Prabu Kresna memerintah di Kerajaan Dwarawati. Raden Samba adalah putra mahkota.
    """
    
    # Initialize NER
    ner = WayangNER(model_type="spacy")
    
    # Extract entities
    entities = ner.extract_entities(sample_text)
    
    print("=== NER Results ===")
    print(f"Found {len(entities)} entities:")
    for entity in entities:
        print(f"  - {entity['text']:<30} [{entity['type']}] (method: {entity['method']})")


if __name__ == "__main__":
    main()
