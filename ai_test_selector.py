import os
import subprocess
import sys
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression

# Eğitim datası (örnek)
training_data = {
    "tests/test_payment.py": {
        "X": [[5, 10], [3, 8], [1, 6], [0, 3]],
        "y": [1, 1, 1, 0],
    },
    "tests/test_user.py": {
        "X": [[2, 2], [1, 1], [0, 0], [4, 3]],
        "y": [1, 0, 0, 1],
    },
    "tests/test_recommender.py": {
        "X": [[1, 1], [0, 0], [2, 1], [3, 2]],
        "y": [1, 0, 1, 1],
    },
}

# Her test için model eğit
models = {}
for test, data in training_data.items():
    model = LogisticRegression()
    model.fit(data["X"], data["y"])
    models[test] = model

def get_most_recent_test(tests_dir="tests"):
    """tests klasöründe en son değiştirilmiş test dosyasını bul"""
    test_files = list(Path(tests_dir).glob("test_*.py"))
    if not test_files:
        return None
    most_recent = max(test_files, key=os.path.getmtime)
    return str(most_recent)

def select_tests_hybrid(tests_dir="tests", change_count=2, bonus=0.2):
    most_recent = get_most_recent_test(tests_dir)
    ai_scored = []

    for test, model in models.items():
        last_failure_count = training_data[test]["X"][-1][1]
        features = np.array([[change_count, last_failure_count]])
        proba = model.predict_proba(features)[0][1]

        # Eğer en güncel dosya buysa bonus ekle
        if most_recent and test.endswith(os.path.basename(most_recent)):
            proba += bonus
            if proba > 1.0:
                proba = 1.0

        ai_scored.append((test, proba))

    # Skora göre sırala
    ai_scored.sort(key=lambda x: x[1], reverse=True)
    return ai_scored

if __name__ == "__main__":
    tests_with_scores = select_tests_hybrid("tests")

    if not tests_with_scores:
        print("⚠️ Hiç test bulunamadı.")
        sys.exit(1)

    print("▶️ Çalıştırma Sırası (AI + Bonus Skor):")
    for i, (test, score) in enumerate(tests_with_scores, 1):
        print(f"{i}) {test} (score={score:.2f})")

    for test_file, _ in tests_with_scores:
        subprocess.run([sys.executable, "-m", "pytest", "-q", test_file])
