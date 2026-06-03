# Image Matcher - Rozpoznawanie tego samego obiektu

Program do wyszukiwania zdjęć tego samego obiektu w dużym folderze zdjęć.

## Jak uruchomić

### 1. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 2. Przygotowanie folderów

Utwórz następującą strukturę:
```
projekt-py/
├── image_matcher.py
├── requirements.txt
├── patterns/           ← Wrzuć tu 10 zdjęć wzorcowych
│   ├── object_1.jpg
│   ├── object_2.jpg
│   └── ...
└── images/            ← Folder ze zdjęciami do przeszukania
    ├── photo1.jpg
    ├── photo2.jpg
    └── ...
```

### 3. Uruchomienie
```bash
python image_matcher.py
```

## Jak to działa

1. **Załadowanie wzorców** - Program analizuje 10 zdjęć z folderu `patterns`
2. **Ekstrakcja cech** - Używa algorytmu SIFT do wyznaczenia unikalnych punktów charakterystycznych
3. **Przeszukiwanie** - Porównuje każde zdjęcie z folderu `images` z wzorcami
4. **Dopasowanie** - Liczy liczbę pasujących cech (domyślnie: minimum 15)
5. **Przenoszenie** - Pasujące zdjęcia trafiają do folderu `matched_images`

## Konfiguracja

Edytuj parametry w `image_matcher.py`:

```python
MIN_MATCHES = 15  # Zwiększ dla bardziej restrykcyjnego wyszukiwania
```

## Parametry

| Parametr | Znaczenie |
|----------|-----------|
| `PATTERNS_FOLDER` | Folder z wzorcami (10 zdjęć) |
| `SEARCH_FOLDER` | Folder do przeszukania |
| `OUTPUT_FOLDER` | Folder z wynikami |
| `MIN_MATCHES` | Minimalna liczba dopasowań (wyższa = bardziej restrykcyjne) |

## Porady

- **Zbyt mało wyników?** - Zmniejsz `MIN_MATCHES` na 10-12
- **Zbyt wiele fałszywych pozytywów?** - Zwiększ `MIN_MATCHES` na 20-25
- **Lepsze wyniki** - Wrzuć wzorce z różnych kątów tego samego obiektu

## Format zdjęć

Obsługiwane: JPG, JPEG, PNG, BMP

## Przykład wyjścia

```
Wczytywanie wzorców z: patterns
✓ Załadowany wzorzec: object_1.jpg (245 cech)
✓ Załadowany wzorzec: object_2.jpg (189 cech)
...
✓ Załadowano 10 wzorców

Przeszukiwanie folderu: images
Znaleziono 50 zdjęć do przeszukania

[1/50] photo1.jpg: 3 dopasowań ✗
[2/50] photo2.jpg: 42 dopasowań ✓ PASUJE
[3/50] photo3.jpg: 18 dopasowań ✓ PASUJE
...

Przenoszenie 15 pasujących zdjęć do: matched_images
✓ photo2.jpg (dopasowania: 42)
✓ photo3.jpg (dopasowania: 18)
...

✅ Gotowe! Znaleziono i przeniesiono 15 zdjęć
```

Oryginał porównuje detale lokalne (cechy, kształty, punkty charakterystyczne).

PyTorch porównuje ogólną reprezentację obrazu (cechy semantyczne / wizualne na poziomie całego obrazu).
