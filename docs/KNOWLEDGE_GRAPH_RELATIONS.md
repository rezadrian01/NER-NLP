# Knowledge Graph - Ekstraksi Relasi

Dokumen ini menjelaskan bagaimana sistem mengekstrak relasi antar entitas dalam knowledge graph.

## 📊 Hasil

### Peningkatan Signifikan
- **Sebelum**: 12 relasi (density 0.0013)
- **Sesudah**: 94 relasi (density 0.0103)
- **Peningkatan**: 683% lebih banyak relasi terdeteksi!

### Distribusi Relasi Baru
| Relasi | Jumlah | Kategori |
|--------|--------|----------|
| `berinteraksi_dengan` | 54 | Sosial |
| `terkait_dengan_lokasi` | 17 | Lokasi |
| `memerintah_di` | 6 | Lokasi |
| `terlibat_dalam` | 5 | Partisipasi |
| `saudara_dari` | 4 | Keluarga |
| `melawan` | 2 | Konflik |
| `anak_dari` | 2 | Keluarga |
| `membantu` | 1 | Sosial |
| `memimpin` | 1 | Partisipasi |
| `ayah_dari` | 1 | Keluarga |

## 🔍 Tiga Metode Ekstraksi

### 1. Regex Pattern Matching (42 Pola)

**Cara Kerja**: Mencari pola kata kunci dalam teks

**Pola yang Ditambahkan**:

#### Keluarga (11 pola)
- `anak_dari` - "X putra/putri/anak dari Y"
- `orang_tua_dari` - "X melahirkan Y"
- `ayah_dari` - "X adalah ayah/bapak dari Y"
- `ibu_dari` - "X adalah ibu/ibunda dari Y"
- `menikah_dengan` - "X dan Y menikah"
- `pasangan_dari` - "X adalah suami/istri Y"
- `saudara_dari` - "X dan Y adalah saudara"
- `kakak_dari` - "X adalah kakak dari Y"
- `adik_dari` - "X adalah adik dari Y"
- `keturunan_dari` - "X adalah keturunan/cucu Y"

#### Konflik (7 pola)
- `melawan` - "X melawan/memerangi Y"
- `dibunuh_oleh` - "X dibunuh/gugur oleh Y"
- `membunuh` - "X membunuh/mengalahkan Y"
- `menyerang` - "X menyerang Y"
- `dikalahkan_oleh` - "X kalah dari Y"
- `mengalahkan` - "X mengalahkan Y"
- `bermusuhan_dengan` - "X bermusuhan dengan Y"

#### Lokasi (6 pola)
- `memerintah_di` - "X memerintah/memimpin di Y"
- `penguasa_dari` - "X adalah raja/pemimpin dari Y"
- `meninggal_di` - "X gugur/meninggal di Y"
- `berada_di` - "X berada/tinggal di Y"
- `pergi_ke` - "X pergi ke Y"
- `lahir_di` - "X lahir di Y"

#### Partisipasi (4 pola)
- `ikut_dalam` - "X ikut dalam Y"
- `anggota_dari` - "X adalah anggota Y"
- `memimpin` - "X memimpin Y"
- `bergabung_dengan` - "X bergabung dengan Y"

#### Sosial (5 pola - BARU!)
- `bertemu_dengan` - "X bertemu dengan Y"
- `membantu` - "X membantu Y"
- `bersahabat_dengan` - "X bersahabat dengan Y"
- `mengutus` - "X mengutus Y"
- `diutus_oleh` - "X diutus oleh Y"

**Contoh**:
```
Teks: "Nakula dan Sadewa adalah saudara"
Entitas: [Nakula (PERSON), Sadewa (PERSON)]
Pattern: "(.+?) dan (.+?) adalah saudara"
Hasil: Nakula ←→ saudara_dari ←→ Sadewa (bidirectional)
```

### 2. Dependency Parsing (Analisis Sintaksis)

**Cara Kerja**: Menggunakan model spaCy untuk menganalisis struktur kalimat

**Yang Dianalisis**:
- Subject-Object relations (nsubj, obj, iobj)
- Konjungsi (conj) → terkait_dengan
- Preposisi (prep) → berada_di, pergi_ke
- Verb patterns → inferensi relasi

**Verb Inference**:
```python
Verb Konflik: membunuh, mengalahkan, menyerang, melukai, melawan
  → relasi: melawan (kategori: konflik)

Verb Sosial: membantu, menolong, mengutus, mengirim
  → relasi: membantu (kategori: sosial)

Verb Leadership: memimpin, memerintah, menguasai
  → relasi: memimpin (kategori: partisipasi)
```

**Contoh**:
```
Teks: "Prabu Kresna membantu Pandawa"
Parse Tree:
  Prabu Kresna (nsubj) ← membantu (VERB) → Pandawa (obj)
  
Hasil: Prabu Kresna → membantu → Pandawa
```

### 3. Co-occurrence Statistics (Statistik Ko-kemunculan)

**Cara Kerja**: Entitas yang muncul bersama dalam satu kalimat dianggap memiliki relasi lemah

**Aturan**:
- Hanya untuk 2-4 entitas per kalimat (tidak terlalu sedikit/banyak)
- Hanya jika belum ada relasi kuat dari regex/dependency
- Tipe relasi berdasarkan kombinasi tipe entitas

**Relasi Berdasarkan Tipe**:
```
PERSON + PERSON → berinteraksi_dengan (sosial, bidirectional)
PERSON + LOC    → terkait_dengan_lokasi (lokasi)
PERSON + ORG    → terlibat_dalam (partisipasi)
PERSON + EVENT  → terlibat_dalam (partisipasi)
```

**Contoh**:
```
Teks: "Raden Arjuna tiba di Kerajaan Dwarawati"
Entitas: [Raden Arjuna (PERSON), Kerajaan Dwarawati (LOC)]
Co-occurrence: Kedua entitas dalam satu kalimat
Hasil: Raden Arjuna → terkait_dengan_lokasi → Kerajaan Dwarawati
```

## 🎯 Mengapa Relasi Meningkat Drastis?

### Sebelum (12 relasi)
- ❌ Hanya 12 pola regex
- ❌ Tidak ada dependency parsing
- ❌ Tidak ada co-occurrence detection
- ❌ Pattern terlalu ketat

### Sesudah (94 relasi)
- ✅ 42 pola regex (3.5x lebih banyak)
- ✅ Dependency parsing untuk verb relations
- ✅ Co-occurrence statistics (kontribusi terbesar: 54 relasi)
- ✅ Pattern lebih fleksibel

## 📈 Breakdown Kontribusi

| Metode | Relasi Terdeteksi | Persentase |
|--------|-------------------|------------|
| **Co-occurrence** | ~54 | 57% |
| **Regex Patterns** | ~32 | 34% |
| **Dependency Parsing** | ~8 | 9% |

**Insight**: Co-occurrence memberikan kontribusi terbesar karena mendeteksi relasi implisit yang tidak diekspresikan dengan kata kunci eksplisit.

## 🔧 Kustomisasi

### Menambah Pola Regex Baru

Edit `build_knowledge_graph.py`, method `_init_relation_patterns()`:

```python
{'pattern': r'(.+?)\s+KATA_KUNCI\s+(.+)',
 'relation': 'nama_relasi', 
 'category': 'kategori',  # keluarga/konflik/lokasi/partisipasi/sosial
 'bidirectional': True}   # optional: untuk relasi 2 arah
```

### Menyesuaikan Threshold Co-occurrence

Edit method `extract_cooccurrence_relations()`:

```python
# Ubah jumlah entitas minimum/maksimum
if len(entities) < 2 or len(entities) > 4:  # default: 2-4
    return
```

### Menambah Verb Patterns

Edit method `_infer_relation_from_verb()`:

```python
new_verbs = ['kata1', 'kata2', 'kata3']
if any(v in verb_lower for v in new_verbs):
    return {'type': 'relasi_baru', 'category': 'kategori'}
```

## 🌐 Label Bahasa Indonesia

Semua label relasi menggunakan Bahasa Indonesia untuk menjaga konsistensi dengan data asli:

- ✅ `anak_dari` bukan `child_of`
- ✅ `melawan` bukan `fought_with`
- ✅ `memerintah_di` bukan `ruled_in`
- ✅ `berinteraksi_dengan` bukan `interacts_with`

## 📊 Visualisasi

Graph dapat dilihat di `output/knowledge_graph.html`:
- **Node biru** = PERSON (Tokoh)
- **Node teal** = LOC (Lokasi)
- **Node orange** = ORG (Organisasi)
- **Node merah** = EVENT (Peristiwa)

**Edge warna**:
- **Pink** = Keluarga
- **Merah** = Konflik
- **Cyan** = Lokasi
- **Hijau** = Partisipasi
- **Ungu** = Sosial

## 🎓 Referensi Teknis

1. **Regex Pattern Matching**: Rule-based extraction
2. **Dependency Parsing**: spaCy's syntactic analysis
3. **Co-occurrence Statistics**: Statistical NLP technique for implicit relations

---

**Dibuat oleh**: Kelompok 1  
**Tanggal**: November 2025  
**Dataset**: 45 annotated Wayang stories
