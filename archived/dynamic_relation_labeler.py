"""
Dynamic Relation Labeling Module
Author: Ahmad Reza Adrian

This module automatically generates meaningful relation labels between entities
using NLP techniques including TF-IDF, dependency parsing, and context analysis.
"""

import re
import logging
from typing import List, Dict, Tuple, Any, Optional
from collections import Counter, defaultdict
import numpy as np

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DynamicRelationLabeler:
    """
    Dynamically generates meaningful relation labels between entities
    based on context analysis, dependency parsing, and TF-IDF.
    """
    
    def __init__(self, spacy_model: str = "xx_ent_wiki_sm"):
        """
        Initialize the dynamic relation labeler.
        
        Args:
            spacy_model: spaCy model to use for dependency parsing
        """
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(spacy_model)
                logger.info(f"Loaded spaCy model: {spacy_model}")
            except:
                logger.warning(f"Could not load spaCy model {spacy_model}")
        
        # Indonesian action verbs commonly found in wayang stories
        self.action_verbs = {
            # Combat/conflict
            'membunuh', 'membantai', 'mengalahkan', 'melawan', 'bertempur', 'bertarung',
            'menyerang', 'menghabisi', 'menewaskan', 'menikam', 'memotong',
            
            # Family/relationships
            'menikah', 'mengawini', 'mempersunting', 'melahirkan', 'membesarkan',
            'mengasuh', 'merawat', 'memelihara',
            
            # Leadership/governance
            'memerintah', 'memimpin', 'menguasai', 'mengatur', 'mengendalikan',
            'mengelola', 'bertahta', 'berkuasa',
            
            # Movement/interaction
            'mengunjungi', 'mendatangi', 'menemui', 'bertemu', 'berjumpa',
            'menghadap', 'datang', 'pergi', 'pulang',
            
            # Communication
            'berkata', 'mengatakan', 'memberitahu', 'menyampaikan', 'berbicara',
            'bercerita', 'memerintahkan', 'meminta', 'memohon',
            
            # Assistance/support
            'membantu', 'menolong', 'mendukung', 'melindungi', 'menyelamatkan',
            'membela', 'menjaga',
            
            # Creation/teaching
            'menciptakan', 'membuat', 'mengajar', 'melatih', 'mendidik',
            'memberi', 'memberikan', 'menyerahkan',
            
            # Events/participation
            'menghadiri', 'mengikuti', 'berpartisipasi', 'ikut', 'hadir',
            'turut', 'serta',
            
            # Emotional/mental
            'mencintai', 'membenci', 'menghormati', 'mengagumi', 'menghargai',
            'memuji', 'menyanjung', 'mengutuk'
        }
        
        # Noun patterns indicating relationships
        self.relationship_nouns = {
            # Family
            'ayah', 'ibu', 'bapak', 'rama', 'ibu', 'induk', 'orang tua',
            'putra', 'putri', 'anak', 'kakak', 'adik', 'saudara',
            'suami', 'istri', 'permaisuri', 'garwa',
            'kakek', 'nenek', 'cucu', 'keponakan', 'paman', 'bibi',
            
            # Social roles
            'raja', 'prabu', 'ratu', 'pangeran', 'putri',
            'patih', 'punggawa', 'penasihat', 'menteri',
            'ksatria', 'pahlawan', 'prajurit', 'panglima',
            'guru', 'murid', 'pandita', 'resi',
            'teman', 'sahabat', 'kawan', 'sekutu',
            'musuh', 'lawan', 'rival',
            
            # Positions/titles
            'pemimpin', 'penguasa', 'komandan', 'kepala',
            'pelindung', 'penjaga', 'pengawal',
            
            # Events/places
            'pertempuran', 'perang', 'perkawinan', 'upacara',
            'kerajaan', 'istana', 'negara', 'desa'
        }
        
        # Prepositions indicating relationships
        self.relationship_prepositions = {
            'dari': 'from',
            'ke': 'to',
            'di': 'in/at',
            'dengan': 'with',
            'oleh': 'by',
            'untuk': 'for',
            'kepada': 'to',
            'pada': 'at/on',
            'dalam': 'in',
            'antara': 'between',
            'bersama': 'together with',
            'melawan': 'against'
        }
        
        # Cache for computed labels
        self.label_cache = {}
        
        # TF-IDF storage for context words
        self.entity_contexts = defaultdict(list)
        self.idf_scores = {}
    
    def extract_relation_label(self, 
                               subject: str, 
                               object_entity: str,
                               context: str,
                               relation_type: Optional[str] = None) -> str:
        """
        Extract a dynamic, meaningful relation label from context.
        
        Args:
            subject: Subject entity
            object_entity: Object entity
            context: Text context where entities co-occur
            relation_type: Optional hint about relation type
            
        Returns:
            Dynamic relation label
        """
        # Check cache
        cache_key = (subject.lower(), object_entity.lower(), context[:50])
        if cache_key in self.label_cache:
            return self.label_cache[cache_key]
        
        # Normalize context
        context_lower = context.lower()
        
        # Strategy 1: Extract verb-based action between entities
        verb_label = self._extract_verb_relation(subject, object_entity, context_lower)
        if verb_label:
            self.label_cache[cache_key] = verb_label
            return verb_label
        
        # Strategy 2: Extract noun-based relationship
        noun_label = self._extract_noun_relation(subject, object_entity, context_lower)
        if noun_label:
            self.label_cache[cache_key] = noun_label
            return noun_label
        
        # Strategy 3: Use dependency parsing if available
        if self.nlp:
            dep_label = self._extract_dependency_relation(subject, object_entity, context)
            if dep_label:
                self.label_cache[cache_key] = dep_label
                return dep_label
        
        # Strategy 4: Use preposition-based relation
        prep_label = self._extract_preposition_relation(subject, object_entity, context_lower)
        if prep_label:
            self.label_cache[cache_key] = prep_label
            return prep_label
        
        # Strategy 5: Use TF-IDF to find most distinctive words
        tfidf_label = self._extract_tfidf_relation(subject, object_entity, context_lower)
        if tfidf_label:
            self.label_cache[cache_key] = tfidf_label
            return tfidf_label
        
        # Fallback: use relation_type if provided
        if relation_type and relation_type != 'associated_with':
            label = relation_type.replace('_', ' ')
            self.label_cache[cache_key] = label
            return label
        
        # Final fallback
        return 'related to'
    
    def _extract_verb_relation(self, subject: str, obj: str, context: str) -> Optional[str]:
        """
        Extract verb-based relation from context.
        
        Args:
            subject: Subject entity
            obj: Object entity
            context: Context text
            
        Returns:
            Verb-based relation label or None
        """
        subject_lower = subject.lower()
        obj_lower = obj.lower()
        
        # Find position of entities
        subj_pos = context.find(subject_lower)
        obj_pos = context.find(obj_lower)
        
        if subj_pos == -1 or obj_pos == -1:
            return None
        
        # Extract text between entities
        if subj_pos < obj_pos:
            between_text = context[subj_pos + len(subject_lower):obj_pos].strip()
        else:
            between_text = context[obj_pos + len(obj_lower):subj_pos].strip()
        
        # Look for action verbs in between text
        words = between_text.split()
        for word in words:
            # Remove common prefixes and check base form
            base_word = re.sub(r'^(me|ber|ter|di|pe)', '', word)
            
            # Check if it's an action verb
            for verb in self.action_verbs:
                if verb in word or base_word in verb or verb in base_word:
                    # Clean up the verb for display
                    if subj_pos < obj_pos:
                        return word
                    else:
                        # Reverse relation
                        return f"{word} (by)"
        
        return None
    
    def _extract_noun_relation(self, subject: str, obj: str, context: str) -> Optional[str]:
        """
        Extract noun-based relationship from context.
        
        Args:
            subject: Subject entity
            obj: Object entity
            context: Context text
            
        Returns:
            Noun-based relation label or None
        """
        # Look for relationship nouns
        for noun in self.relationship_nouns:
            if noun in context:
                # Check proximity to entities
                noun_pos = context.find(noun)
                subj_pos = context.find(subject.lower())
                obj_pos = context.find(obj.lower())
                
                if subj_pos != -1 and obj_pos != -1:
                    # If noun is near one of the entities, it likely describes their relation
                    dist_to_subj = abs(noun_pos - subj_pos)
                    dist_to_obj = abs(noun_pos - obj_pos)
                    
                    if dist_to_subj < 50 or dist_to_obj < 50:
                        # Determine direction
                        if subj_pos < obj_pos:
                            return f"{noun} of"
                        else:
                            return f"is {noun} of"
        
        return None
    
    def _extract_dependency_relation(self, subject: str, obj: str, context: str) -> Optional[str]:
        """
        Use dependency parsing to extract relation.
        
        Args:
            subject: Subject entity
            obj: Object entity
            context: Context text
            
        Returns:
            Dependency-based relation label or None
        """
        if not self.nlp:
            return None
        
        try:
            doc = self.nlp(context)
            
            # Find tokens corresponding to entities
            subj_tokens = []
            obj_tokens = []
            
            for token in doc:
                if subject.lower() in token.text.lower():
                    subj_tokens.append(token)
                if obj.lower() in token.text.lower():
                    obj_tokens.append(token)
            
            if not subj_tokens or not obj_tokens:
                return None
            
            # Find verbs connecting the entities
            for subj_token in subj_tokens:
                for obj_token in obj_tokens:
                    # Find path between tokens
                    if subj_token.head == obj_token.head:
                        verb = subj_token.head
                        if verb.pos_ == 'VERB':
                            return verb.lemma_
                    
                    # Check if one is ancestor of the other
                    ancestors_subj = list(subj_token.ancestors)
                    if obj_token in ancestors_subj:
                        for anc in ancestors_subj:
                            if anc.pos_ == 'VERB':
                                return anc.lemma_
        
        except Exception as e:
            logger.debug(f"Dependency parsing failed: {e}")
        
        return None
    
    def _extract_preposition_relation(self, subject: str, obj: str, context: str) -> Optional[str]:
        """
        Extract preposition-based relation.
        
        Args:
            subject: Subject entity
            obj: Object entity
            context: Context text
            
        Returns:
            Preposition-based relation label or None
        """
        subj_pos = context.find(subject.lower())
        obj_pos = context.find(obj.lower())
        
        if subj_pos == -1 or obj_pos == -1:
            return None
        
        # Extract text between entities
        if subj_pos < obj_pos:
            between_text = context[subj_pos + len(subject):obj_pos].strip()
        else:
            between_text = context[obj_pos + len(obj):subj_pos].strip()
        
        # Look for prepositions
        for prep, eng_prep in self.relationship_prepositions.items():
            if prep in between_text:
                # Get words around the preposition
                words = between_text.split()
                for i, word in enumerate(words):
                    if prep in word:
                        # Get surrounding context
                        context_words = words[max(0, i-1):min(len(words), i+2)]
                        return ' '.join(context_words)
        
        return None
    
    def _extract_tfidf_relation(self, subject: str, obj: str, context: str) -> Optional[str]:
        """
        Use TF-IDF to find most distinctive words as relation label.
        
        Args:
            subject: Subject entity
            obj: Object entity
            context: Context text
            
        Returns:
            TF-IDF based relation label or None
        """
        # Store context for this entity pair
        entity_pair = (subject.lower(), obj.lower())
        
        # Extract words from context (excluding entities)
        words = re.findall(r'\b\w+\b', context)
        words = [w for w in words if len(w) > 3 and 
                 w not in subject.lower() and 
                 w not in obj.lower()]
        
        if not words:
            return None
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Get most common meaningful words (verbs, nouns)
        meaningful_words = []
        for word, freq in word_freq.most_common(5):
            # Check if it's a verb or relationship noun
            if any(v in word for v in self.action_verbs) or \
               any(n in word for n in self.relationship_nouns):
                meaningful_words.append(word)
        
        if meaningful_words:
            # Return most frequent meaningful word
            return meaningful_words[0]
        
        return None
    
    def batch_label_relations(self, relations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate dynamic labels for a batch of relations.
        
        Args:
            relations: List of relation dictionaries with 'subject', 'object', 'context', 'relation'
            
        Returns:
            List of relations with 'dynamic_label' added
        """
        logger.info(f"Generating dynamic labels for {len(relations)} relations...")
        
        labeled_relations = []
        for relation in relations:
            subject = relation.get('subject', '')
            obj = relation.get('object', '')
            context = relation.get('context', '')
            rel_type = relation.get('relation', 'associated_with')
            
            # Generate dynamic label
            dynamic_label = self.extract_relation_label(subject, obj, context, rel_type)
            
            # Add to relation
            relation_copy = relation.copy()
            relation_copy['dynamic_label'] = dynamic_label
            labeled_relations.append(relation_copy)
        
        logger.info("Dynamic labeling complete!")
        return labeled_relations
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about generated labels.
        
        Returns:
            Dictionary with statistics
        """
        label_counts = Counter([label for label in self.label_cache.values()])
        
        return {
            'total_cached_labels': len(self.label_cache),
            'unique_labels': len(label_counts),
            'most_common_labels': label_counts.most_common(10),
            'cache_size': len(self.label_cache)
        }


def main():
    """Test the dynamic relation labeler."""
    # Test data
    test_relations = [
        {
            'subject': 'Abimanyu',
            'object': 'Arjuna',
            'context': 'Abimanyu adalah putra dari Arjuna yang gagah berani',
            'relation': 'child_of'
        },
        {
            'subject': 'Arjuna',
            'object': 'Subadra',
            'context': 'Arjuna menikah dengan Subadra di Dwarawati',
            'relation': 'married_to'
        },
        {
            'subject': 'Gatotkaca',
            'object': 'Abimanyu',
            'context': 'Gatotkaca bertempur melawan Abimanyu di medan perang',
            'relation': 'fought_with'
        },
        {
            'subject': 'Prabu Kresna',
            'object': 'Dwarawati',
            'context': 'Prabu Kresna memerintah di Kerajaan Dwarawati',
            'relation': 'ruled_in'
        },
        {
            'subject': 'Bima',
            'object': 'Pandawa',
            'context': 'Bima adalah salah satu ksatria Pandawa yang terkuat',
            'relation': 'member_of'
        }
    ]
    
    # Initialize labeler
    labeler = DynamicRelationLabeler()
    
    # Generate labels
    labeled = labeler.batch_label_relations(test_relations)
    
    print("\n=== Dynamic Relation Labels ===")
    for rel in labeled:
        print(f"\n{rel['subject']} -> {rel['object']}")
        print(f"  Original: {rel['relation']}")
        print(f"  Dynamic:  {rel['dynamic_label']}")
        print(f"  Context:  {rel['context'][:80]}...")
    
    # Show statistics
    stats = labeler.get_statistics()
    print(f"\n=== Statistics ===")
    print(f"Total labels cached: {stats['total_cached_labels']}")
    print(f"Unique labels: {stats['unique_labels']}")


if __name__ == "__main__":
    main()
