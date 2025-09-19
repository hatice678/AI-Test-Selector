import os
import sys
import csv
import subprocess
import numpy as np
from sklearn.linear_model import LogisticRegression
from pathlib import Path

CSV_FILE = "training_data.csv"
REPORTS_DIR = "reports"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.xml")

def load_training_data(csv_file=CSV_FILE):
    """CSV’den training datasını oku"""
    if not os.path.exists(csv_file):
        print("⚠️ Training datası yok, dummy modda çalıştırılıyor...")
        os.makedirs(REPORTS_DIR, exist_ok=True)
        subprocess.run([
            sys.executable, "-m", "pytest", "-q",
            f"--junitxml={RESULTS_FILE}",
            "tests"
        ])
        sys.exit(0)

    X, y, test_names = [], [], []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fail_val = int(row["test_fail"])
            report_idx = 0  # basit feature
            X.append([report_idx, fail_val])
            y.append(fail_val)
            test_names.append(row["test_name"])

    return np.array(X), np.array(y), test_names

def train_model(X, y):
    """Logistic Regression modeli eğit"""
    if len(set(y)) < 2:
        print("⚠️ Yeterli çeşitlilik yok, model eğitilemedi.")
        return None
    model = LogisticRegression()
    model.fit(X, y)
    return model

def select_tests(tests_dir="tests", change_count=2, bonus=0.2):
    """AI + bonus ile test sıralama"""
    X, y, test_names = load_training_data()
    if X is None or y is None or len(y) == 0:
        return []

    model = train_model(X, y)
    if not model:
        return []

    test_files = list(Path(tests_dir).glob("test_*.py"))
    if not test_files:
        return []

    most_recent = max(test_files, key=os.path.getmtime)

    ranked = []
    for test_file in test_files:
        last_failures = y[-5:].tolist().count(1) if len(y) > 5 else sum(y)
        features = np.array([[change_count, last_failures]])
        proba = model.predict_proba(features)[0][1]

        if test_file.name == most_recent.name:
            proba = min(proba + bonus, 1.0)

        ranked.append((str(test_file), proba))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

if __name__ == "__main__":
    tests_with_scores = select_tests("tests")

    if not tests_with_scores:
        print("⚠️ Hiç test bulunamadı veya model eğitilemedi.")
        sys.exit(1)

    print("▶️ Çalıştırma Sırası (Gerçek Data + AI + Bonus Skor):")
    for i, (test, score) in enumerate(tests_with_scores, 1):
        print(f"{i}) {test} (score={score:.2f})")

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Tüm testleri tek XML dosyasına kaydet
    subprocess.run([
        sys.executable, "-m", "pytest", "-q",
        f"--junitxml={RESULTS_FILE}",
        "tests"
    ])
