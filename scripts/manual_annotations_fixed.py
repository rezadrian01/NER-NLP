"""
Manual Entity Annotations for Wayang Stories
Author: Kelompok 1

This module contains manually curated entity annotations for training a high-quality NER model.
Entities are hardcoded with exact character positions for maximum accuracy.
"""

# Manual annotations: List of (text, entities) tuples
# entities format: [(start_pos, end_pos, label), ...]

MANUAL_ANNOTATIONS = [
    # Story 1: Abimanyu Rabi
    (
        "Prabu Baladewa melamar Dewi Sitisundari untuk Raden Lesmana Mandrakumara.",
        [(0, 14, 'PERSON'), (23, 41, 'PERSON'), (48, 72, 'PERSON')]
    ),
    (
        "Raden Arjuna dan Dewi Sumbadra telah datang ke Dwarawati untuk meminang Dewi Sitisundari.",
        [(0, 12, 'PERSON'), (17, 30, 'PERSON'), (48, 56, 'LOC'), (74, 88, 'PERSON')]
    ),
    (
        "Prabu Kresna memerintah di Kerajaan Dwarawati dan menikah dengan Dewi Rukmini.",
        [(0, 12, 'PERSON'), (27, 45, 'LOC'), (66, 77, 'PERSON')]
    ),
    (
        "Raden Abimanyu adalah putra Arjuna dan Subadra.",
        [(0, 14, 'PERSON'), (29, 34, 'PERSON'), (40, 46, 'PERSON')]
    ),
    (
        "Dewi Sitisundari dipertunangkan dengan Raden Abimanyu.",
        [(0, 18, 'PERSON'), (39, 53, 'PERSON')]
    ),
    # Story 2: Sitija Takon Bapa
    (
        "Raden Sitija dan Dewi Sitisundari adalah anak Batari Pretiwi yang mencari ayah mereka Batara Wisnu.",
        [(0, 12, 'PERSON'), (17, 35, 'PERSON'), (47, 62, 'PERSON'), (89, 98, 'PERSON')]
    ),
    (
        "Batara Wisnu telah menitis sebagai Prabu Kresna di Kerajaan Dwarawati.",
        [(0, 12, 'PERSON'), (36, 47, 'PERSON'), (52, 69, 'LOC')]
    ),
    (
        "Raden Sitija berhasil mengalahkan Prabu Bomantara dan Prabu Narakasura.",
        [(0, 12, 'PERSON'), (35, 49, 'PERSON'), (55, 70, 'PERSON')]
    ),
    (
        "Di Kahyangan Ekapratala, Batara Nagaraja Ekawarna dihadap putrinya Batari Pretiwi.",
        [(3, 24, 'LOC'), (26, 51, 'PERSON'), (68, 81, 'PERSON')]
    ),
    (
        "Prabu Kresna Wasudewa di Kerajaan Dwarawati dihadap Raden Samba Wisnubrata.",
        [(0, 21, 'PERSON'), (26, 43, 'LOC'), (53, 74, 'PERSON')]
    ),
    (
        "Arya Setyaki dari Kesatrian Swalabumi dan Patih Udawa membantu Prabu Kresna.",
        [(0, 12, 'PERSON'), (18, 41, 'LOC'), (46, 57, 'PERSON'), (65, 75, 'PERSON')]
    ),
    (
        "Prabu Narakasura menantang Prabu Kresna untuk perang.",
        [(0, 16, 'PERSON'), (27, 39, 'PERSON')]
    ),
    (
        "Raden Sitija mengendarai Paksi Wilmuna untuk berperang.",
        [(0, 12, 'PERSON'), (26, 38, 'PERSON')]
    ),
    (
        "Batara Narada turun dari angkasa melerai perkelahian Raden Sitija dan Raden Gatutkaca.",
        [(0, 13, 'PERSON'), (54, 65, 'PERSON'), (71, 85, 'PERSON')]
    ),
    (
        "Raden Gatutkaca adalah putra Arya Wrekodara yang sakti mandraguna.",
        [(0, 15, 'PERSON'), (30, 45, 'PERSON')]
    ),
    (
        "Prabu Kresna dan Arya Wrekodara adalah saudara sepupu, sama-sama cucu Prabu Kuntiboja.",
        [(0, 12, 'PERSON'), (17, 31, 'PERSON'), (73, 85, 'PERSON')]
    ),
    (
        "Kerajaan Mandura didirikan oleh Prabu Kuntiboja.",
        [(0, 16, 'LOC'), (33, 47, 'PERSON')]
    ),
    (
        "Prabu Bomantara raja Surateleng mengepung Kahyangan Suralaya.",
        [(0, 15, 'PERSON'), (21, 31, 'LOC'), (43, 60, 'LOC')]
    ),
    (
        "Batara Indra adalah raja para jawata di Kahyangan Suralaya.",
        [(0, 12, 'PERSON'), (41, 58, 'LOC')]
    ),
    (
        "Raden Sitija dijedi di Kawah Candradimuka seperti Raden Gatutkaca dulu.",
        [(0, 12, 'PERSON'), (23, 41, 'LOC'), (51, 67, 'PERSON')]
    ),
    (
        "Gunung Jamurdipa adalah lokasi Kawah Candradimuka berada.",
        [(0, 16, 'LOC'), (32, 49, 'LOC')]
    ),
    (
        "Batara Aswan dan Batara Aswin mengobati Dewi Sitisundari.",
        [(0, 12, 'PERSON'), (17, 29, 'PERSON'), (40, 57, 'PERSON')]
    ),
    (
        "Ditya Yayahgriwa, Ditya Ancakogra, Ditya Mahodara, dan Ditya Amisunda mengabdi kepada Raden Sitija.",
        [(0, 17, 'PERSON'), (19, 33, 'PERSON'), (36, 49, 'PERSON'), (57, 72, 'PERSON'), (90, 98, 'PERSON')]
    ),
    (
        "Patih Pancadnyana adalah patih utama Prabu Bomantara di Kerajaan Surateleng.",
        [(0, 17, 'PERSON'), (38, 52, 'PERSON'), (57, 75, 'LOC')]
    ),
    (
        "Kerajaan Prajatisa diperintah oleh Prabu Narakasura.",
        [(0, 18, 'LOC'), (36, 51, 'PERSON')]
    ),
    (
        "Raden Sitija menjadi Prabu Boma Narakasura raja Surateleng-Prajatisa.",
        [(0, 12, 'PERSON'), (21, 42, 'PERSON'), (48, 69, 'LOC')]
    ),
    (
        "Kerajaan Trajutresna adalah nama baru untuk Surateleng-Prajatisa.",
        [(0, 20, 'LOC'), (44, 65, 'LOC')]
    ),
    (
        "Dewi Rukmini adalah permaisuri Prabu Kresna di Kerajaan Dwarawati.",
        [(0, 12, 'PERSON'), (32, 43, 'PERSON'), (48, 65, 'LOC')]
    ),
    (
        "Paksi Wilmuna dan Paksi Wildata adalah dua burung raksasa kakak beradik.",
        [(0, 13, 'PERSON'), (18, 31, 'PERSON')]
    ),
    # Additional training examples with common patterns
    (
        "Kyai Togog dan Bilung adalah panakawan Prabu Narakasura.",
        [(0, 10, 'PERSON'), (15, 21, 'PERSON'), (40, 55, 'PERSON')]
    ),
    (
        "Pandawa dan Kurawa bertarung dalam Perang Bharatayudha.",
        [(0, 7, 'ORG'), (12, 18, 'ORG'), (35, 55, 'EVENT')]
    ),
    (
        "Raden Arjuna berperang melawan Kurawa di medan Kurukshetra.",
        [(0, 12, 'PERSON'), (31, 37, 'ORG'), (49, 58, 'LOC')]
    ),
    (
        "Prabu Duryudana memimpin pasukan Kurawa.",
        [(0, 15, 'PERSON'), (33, 39, 'ORG')]
    ),
    (
        "Dewi Drupadi adalah istri para Pandawa.",
        [(0, 12, 'PERSON'), (32, 38, 'ORG')]
    ),
    (
        "Raden Yudistira adalah kakak tertua Pandawa.",
        [(0, 15, 'PERSON'), (36, 43, 'ORG')]
    ),
    (
        "Raden Bima atau Werkudara terkenal karena kekuatannya.",
        [(0, 10, 'PERSON'), (16, 25, 'PERSON')]
    ),
    (
        "Nakula dan Sadewa adalah saudara kembar dalam Pandawa.",
        [(0, 6, 'PERSON'), (11, 17, 'PERSON'), (47, 53, 'ORG')]
    ),
    (
        "Prabu Kunthi adalah ibu para Pandawa di Kerajaan Amarta.",
        [(0, 12, 'PERSON'), (29, 36, 'ORG'), (40, 56, 'LOC')]
    ),
    (
        "Kerajaan Hastina adalah pusat kekuasaan Kurawa.",
        [(0, 16, 'LOC'), (41, 46, 'ORG')]
    ),
    (
        "Raden Karna adalah anak Prabu Kunthi yang dibuang.",
        [(0, 11, 'PERSON'), (24, 36, 'PERSON')]
    ),
    (
        "Begawan Durna mengajar ilmu perang kepada Pandawa dan Kurawa.",
        [(0, 13, 'PERSON'), (43, 49, 'ORG'), (55, 60, 'ORG')]
    ),
    (
        "Raden Srikandi adalah putri Kerajaan Madukara yang perkasa.",
        [(0, 14, 'PERSON'), (29, 47, 'LOC')]
    ),
    (
        "Prabu Salya raja Kerajaan Mandraka memihak Kurawa.",
        [(0, 11, 'PERSON'), (17, 34, 'LOC'), (44, 49, 'ORG')]
    ),
    (
        "Raden Bisma adalah kakek dari Pandawa dan Kurawa.",
        [(0, 11, 'PERSON'), (30, 37, 'ORG'), (42, 48, 'ORG')]
    ),
    (
        "Pertempuran Brubuh menandai berakhirnya Perang Bharatayudha.",
        [(0, 18, 'EVENT'), (40, 60, 'EVENT')]
    ),
]


def get_manual_annotations():
    """
    Get manually curated annotations.
    
    Returns:
        List of (text, {'entities': [(start, end, label)]}) tuples
    """
    formatted_annotations = []
    for text, entities in MANUAL_ANNOTATIONS:
        formatted_annotations.append((text, {'entities': entities}))
    return formatted_annotations


def get_annotation_statistics():
    """
    Get statistics about the manual annotations.
    
    Returns:
        Dictionary with statistics
    """
    total_examples = len(MANUAL_ANNOTATIONS)
    total_entities = sum(len(entities) for _, entities in MANUAL_ANNOTATIONS)
    
    entity_counts = {}
    for _, entities in MANUAL_ANNOTATIONS:
        for _, _, label in entities:
            entity_counts[label] = entity_counts.get(label, 0) + 1
    
    return {
        'total_examples': total_examples,
        'total_entities': total_entities,
        'avg_entities_per_example': total_entities / total_examples if total_examples > 0 else 0,
        'entity_distribution': entity_counts
    }


if __name__ == "__main__":
    stats = get_annotation_statistics()
    print("="*60)
    print("Manual Annotations Statistics")
    print("="*60)
    print(f"Total examples: {stats['total_examples']}")
    print(f"Total entities: {stats['total_entities']}")
    print(f"Avg entities per example: {stats['avg_entities_per_example']:.2f}")
    print("\nEntity distribution:")
    for label, count in sorted(stats['entity_distribution'].items()):
        print(f"  {label}: {count}")
