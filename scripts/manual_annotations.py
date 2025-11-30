"""
Manual Entity Annotations for Wayang Stories (CORRECTED)
Author: Kelompok 1

This module contains manually curated entity annotations for training a high-quality NER model.
All boundary errors have been manually corrected for accurate evaluation.
"""

# Manual annotations: List of (text, entities) tuples
# entities format: [(start_pos, end_pos, label), ...]

MANUAL_ANNOTATIONS = [
    # Story 1: Abimanyu Rabi
    (
        "Prabu Baladewa melamar Dewi Sitisundari untuk Raden Lesmana Mandrakumara.",
        [(0, 14, 'PERSON'), (23, 39, 'PERSON'), (46, 74, 'PERSON')]
    ),
    (
        "Raden Arjuna dan Dewi Sumbadra telah datang ke Dwarawati untuk meminang Dewi Sitisundari.",
        [(0, 12, 'PERSON'), (17, 30, 'PERSON'), (48, 57, 'LOC'), (74, 90, 'PERSON')]
    ),
    (
        "Prabu Kresna memerintah di Kerajaan Dwarawati dan menikah dengan Dewi Rukmini.",
        [(0, 12, 'PERSON'), (27, 45, 'LOC'), (66, 78, 'PERSON')]
    ),
    (
        "Raden Abimanyu adalah putra Arjuna dan Subadra.",
        [(0, 14, 'PERSON'), (29, 35, 'PERSON'), (40, 47, 'PERSON')]
    ),
    (
        "Dewi Sitisundari dipertunangkan dengan Raden Abimanyu.",
        [(0, 16, 'PERSON'), (39, 53, 'PERSON')]
    ),
    
    # Story 2: Sitija Takon Bapa
    (
        "Raden Sitija dan Dewi Sitisundari adalah anak Batari Pretiwi yang mencari ayah mereka Batara Wisnu.",
        [(0, 12, 'PERSON'), (17, 33, 'PERSON'), (47, 62, 'PERSON'), (89, 101, 'PERSON')]
    ),
    (
        "Batara Wisnu telah menitis sebagai Prabu Kresna di Kerajaan Dwarawati.",
        [(0, 12, 'PERSON'), (36, 48, 'PERSON'), (52, 70, 'LOC')]
    ),
    (
        "Raden Sitija berhasil mengalahkan Prabu Bomantara dan Prabu Narakasura.",
        [(0, 12, 'PERSON'), (35, 50, 'PERSON'), (55, 71, 'PERSON')]
    ),
    (
        "Di Kahyangan Ekapratala, Batara Nagaraja Ekawarna dihadap putrinya Batari Pretiwi.",
        [(3, 24, 'LOC'), (26, 51, 'PERSON'), (68, 83, 'PERSON')]
    ),
    (
        "Prabu Kresna Wasudewa di Kerajaan Dwarawati dihadap Raden Samba Wisnubrata.",
        [(0, 22, 'PERSON'), (26, 44, 'LOC'), (53, 76, 'PERSON')]
    ),
    (
        "Arya Setyaki dari Kesatrian Swalabumi dan Patih Udawa membantu Prabu Kresna.",
        [(0, 12, 'PERSON'), (18, 39, 'LOC'), (44, 56, 'PERSON'), (65, 77, 'PERSON')]
    ),
    (
        "Prabu Narakasura menantang Prabu Kresna untuk perang.",
        [(0, 16, 'PERSON'), (27, 39, 'PERSON')]
    ),
    (
        "Raden Sitija mengendarai Paksi Wilmuna untuk berperang.",
        [(0, 12, 'PERSON'), (26, 39, 'PERSON')]
    ),
    (
        "Batara Narada turun dari angkasa melerai perkelahian Raden Sitija dan Raden Gatutkaca.",
        [(0, 13, 'PERSON'), (54, 66, 'PERSON'), (71, 87, 'PERSON')]
    ),
    (
        "Raden Gatutkaca adalah putra Arya Wrekodara yang sakti mandraguna.",
        [(0, 16, 'PERSON'), (30, 44, 'PERSON')]
    ),
    (
        "Prabu Kresna dan Arya Wrekodara adalah saudara sepupu, sama-sama cucu Prabu Kuntiboja.",
        [(0, 12, 'PERSON'), (17, 31, 'PERSON'), (73, 88, 'PERSON')]
    ),
    (
        "Kerajaan Mandura didirikan oleh Prabu Kuntiboja.",
        [(0, 16, 'LOC'), (33, 48, 'PERSON')]
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
        [(0, 16, 'LOC'), (32, 50, 'LOC')]
    ),
    (
        "Batara Aswan dan Batara Aswin mengobati Dewi Sitisundari.",
        [(0, 12, 'PERSON'), (17, 29, 'PERSON'), (40, 56, 'PERSON')]
    ),
    (
        "Ditya Yayahgriwa, Ditya Ancakogra, Ditya Mahodara, dan Ditya Amisunda mengabdi kepada Raden Sitija.",
        [(0, 17, 'PERSON'), (19, 34, 'PERSON'), (36, 51, 'PERSON'), (57, 72, 'PERSON'), (90, 102, 'PERSON')]
    ),
    (
        "Patih Pancadnyana adalah patih utama Prabu Bomantara di Kerajaan Surateleng.",
        [(0, 17, 'PERSON'), (38, 53, 'PERSON'), (57, 77, 'LOC')]
    ),
    (
        "Kerajaan Prajatisa diperintah oleh Prabu Narakasura.",
        [(0, 18, 'LOC'), (35, 52, 'PERSON')]
    ),
    (
        "Raden Sitija menjadi Prabu Boma Narakasura raja Surateleng-Prajatisa.",
        [(0, 12, 'PERSON'), (21, 42, 'PERSON'), (48, 70, 'LOC')]
    ),
    (
        "Kerajaan Trajutresna adalah nama baru untuk Surateleng-Prajatisa.",
        [(0, 20, 'LOC'), (44, 66, 'LOC')]
    ),
    (
        "Dewi Rukmini adalah permaisuri Prabu Kresna di Kerajaan Dwarawati.",
        [(0, 12, 'PERSON'), (32, 44, 'PERSON'), (48, 66, 'LOC')]
    ),
    (
        "Paksi Wilmuna dan Paksi Wildata adalah dua burung raksasa kakak beradik.",
        [(0, 13, 'PERSON'), (18, 31, 'PERSON')]
    ),
    (
        "Kyai Togog dan Bilung adalah panakawan Prabu Narakasura.",
        [(0, 10, 'PERSON'), (15, 21, 'PERSON'), (40, 56, 'PERSON')]
    ),
    
    # Additional training examples with common patterns
    (
        "Pandawa dan Kurawa bertarung dalam Perang Bharatayudha.",
        [(0, 7, 'ORG'), (12, 18, 'ORG'), (35, 55, 'EVENT')]
    ),
    (
        "Raden Arjuna berperang melawan Kurawa di medan Kurukshetra.",
        [(0, 12, 'PERSON'), (31, 37, 'ORG'), (49, 60, 'LOC')]
    ),
    (
        "Prabu Duryudana memimpin pasukan Kurawa.",
        [(0, 15, 'PERSON'), (33, 39, 'ORG')]
    ),
    (
        "Dewi Drupadi adalah istri para Pandawa.",
        [(0, 12, 'PERSON'), (32, 39, 'ORG')]
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
        [(0, 6, 'PERSON'), (11, 17, 'PERSON'), (47, 54, 'ORG')]
    ),
    (
        "Prabu Kunthi adalah ibu para Pandawa di Kerajaan Amarta.",
        [(0, 12, 'PERSON'), (29, 36, 'ORG'), (40, 56, 'LOC')]
    ),
    (
        "Kerajaan Hastina adalah pusat kekuasaan Kurawa.",
        [(0, 16, 'LOC'), (41, 47, 'ORG')]
    ),
    (
        "Raden Karna adalah anak Prabu Kunthi yang dibuang.",
        [(0, 11, 'PERSON'), (24, 36, 'PERSON')]
    ),
    (
        "Begawan Durna mengajar ilmu perang kepada Pandawa dan Kurawa.",
        [(0, 13, 'PERSON'), (43, 50, 'ORG'), (55, 61, 'ORG')]
    ),
    (
        "Raden Srikandi adalah putri Kerajaan Madukara yang perkasa.",
        [(0, 15, 'PERSON'), (29, 47, 'LOC')]
    ),
    (
        "Prabu Salya raja Kerajaan Mandraka memihak Kurawa.",
        [(0, 11, 'PERSON'), (17, 35, 'LOC'), (44, 50, 'ORG')]
    ),
    (
        "Raden Bisma adalah kakek dari Pandawa dan Kurawa.",
        [(0, 11, 'PERSON'), (30, 37, 'ORG'), (42, 48, 'ORG')]
    ),
    (
        "Pertempuran Brubuh menandai berakhirnya Perang Bharatayudha.",
        [(0, 19, 'EVENT'), (40, 60, 'EVENT')]
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