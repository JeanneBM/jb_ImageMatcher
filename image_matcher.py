import cv2
import numpy as np
import os
import shutil
from pathlib import Path
from typing import List, Tuple

class ImageMatcher:
    def __init__(self, patterns_folder: str, search_folder: str, output_folder: str = "matched_images", min_matches: int = 15):
        """
        Args:
            patterns_folder: Folder ze zdjęciami wzorcowymi (10 zdjęć)
            search_folder: Folder do przeszukania
            output_folder: Folder do zapisania wyników
            min_matches: Minimalna liczba dopasowanych cech
        """
        self.patterns_folder = patterns_folder
        self.search_folder = search_folder
        self.output_folder = output_folder
        self.min_matches = min_matches
        self.patterns = []
        self.sift = cv2.SIFT_create()

        Path(output_folder).mkdir(exist_ok=True)

    def load_patterns(self) -> List[Tuple[str, cv2.Mat, list, list]]:
        """Wczytuje zdjęcia wzorcowe i wyznacza ich cechy"""
        print(f"📷 Wczytywanie wzorców z: {self.patterns_folder}")

        for filename in os.listdir(self.patterns_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                path = os.path.join(self.patterns_folder, filename)
                img = cv2.imread(path)

                if img is None:
                    print(f"⚠️  Nie mogę wczytać: {filename}")
                    continue

                # Konwersja do skali szarości
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Wyszukiwanie cech SIFT
                kp, des = self.sift.detectAndCompute(gray, None)

                if des is not None:
                    self.patterns.append((filename, img, kp, des))
                    print(f"✓ Załadowany wzorzec: {filename} ({len(kp)} cech)")

        if not self.patterns:
            print("❌ Brak wzorców do załadowania!")
            return False

        print(f"✓ Załadowano {len(self.patterns)} wzorców\n")
        return True

    def count_matches(self, image_path: str) -> int:
        """Liczy dopasowania między wzorcami a zdjęciem"""
        img = cv2.imread(image_path)

        if img is None:
            return 0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, des = self.sift.detectAndCompute(gray, None)

        if des is None:
            return 0

        # FLANN matcher
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        total_matches = 0

        # Porównanie ze wszystkimi wzorcami
        for pattern_name, _, _, pattern_des in self.patterns:
            matches = flann.knnMatch(pattern_des, des, k=2)

            if not matches:
                continue

            # Lowe's ratio test
            good_matches = 0
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches += 1

            total_matches += good_matches

        return total_matches

    def search_and_match(self) -> None:
        """Przeszukuje folder i przenosi pasujące zdjęcia"""
        print(f"🔍 Przeszukiwanie folderu: {self.search_folder}")

        matched_images = []
        image_files = [f for f in os.listdir(self.search_folder)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

        print(f"Znaleziono {len(image_files)} zdjęć do przeszukania\n")

        for idx, filename in enumerate(image_files, 1):
            image_path = os.path.join(self.search_folder, filename)
            matches = self.count_matches(image_path)

            status = "✓ PASUJE" if matches >= self.min_matches else "✗"
            print(f"[{idx}/{len(image_files)}] {filename}: {matches} dopasowań {status}")

            if matches >= self.min_matches:
                matched_images.append((filename, matches))

        # Przenoszenie pasujących zdjęć
        print(f"\n📁 Przenoszenie {len(matched_images)} pasujących zdjęć do: {self.output_folder}")

        for filename, matches in matched_images:
            src = os.path.join(self.search_folder, filename)
            dst = os.path.join(self.output_folder, filename)

            shutil.copy2(src, dst)
            print(f"✓ {filename} (dopasowania: {matches})")

        print(f"\n✅ Gotowe! Znaleziono i przeniesiono {len(matched_images)} zdjęć")

if __name__ == "__main__":
    # Konfiguracja
    PATTERNS_FOLDER = "patterns"  # Folder z 10 wzorcowymi zdjęciami
    SEARCH_FOLDER = "images"      # Folder do przeszukania
    OUTPUT_FOLDER = "matched_images"  # Folder z wynikami
    MIN_MATCHES = 15  # Minimalna liczba dopasowań

    # Sprawdzenie folderów
    if not os.path.exists(PATTERNS_FOLDER):
        print(f"❌ Folder {PATTERNS_FOLDER} nie istnieje!")
        exit(1)

    if not os.path.exists(SEARCH_FOLDER):
        print(f"❌ Folder {SEARCH_FOLDER} nie istnieje!")
        exit(1)

    # Uruchomienie
    matcher = ImageMatcher(PATTERNS_FOLDER, SEARCH_FOLDER, OUTPUT_FOLDER, MIN_MATCHES)

    if matcher.load_patterns():
        matcher.search_and_match()
