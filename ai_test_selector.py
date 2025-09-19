import os
import sys
import subprocess
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from pathlib import Path

CSV_FILE = "training_data.csv"
REPORTS_DIR = "reports"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.xml")

def load_training_data(csv_file=CSV_FILE):
    """CSV’den training datasını oku ve feature çıkar"""
    if not os.path.exists(csv_file):
        print("[WARN] Training datası yok, dummy modda çalıştırılıyor...")
        return None, None, None, {}

    df = pd.read_csv(csv_file)

    fail_counts = df.groupby("test_name")["test_fail"].sum().to_dict()
    run_counts = df.groupby("test_name")["test_fail"].count().to_dict()

    X, y, test_names = [], [], []
    for test_name in df["test_name"].unique():
        fails = fail_counts.get(test_name, 0)
        runs = run_counts.get(test_name, 0)
        X.append([runs, fails])  
        y.append(1 if fails > 0 else 0)  
        test_names.append(test_name)

    return np.array(X), np.array(y), test_names, fail_counts

def train_model(X, y):
    """Logistic Regression modeli eğit"""
    if len(set(y)) < 2:
        print("[WARN] Yeterli çeşitlilik yok, model eğitilemedi.")
        return None
    model = LogisticRegression()
    model.fit(X, y)
    return model

def select_tests(tests_dir="tests", change_count=2, bonus=0.2):
    """AI + bonus ile test sıralama"""
    X, y, test_names, fail_counts = load_training_data()
    if X is None:
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
        test_name = test_file.stem.replace("/", ".")
        fails = fail_counts.get(test_name, 0)
        runs = X[:,0].max() if len(X) > 0 else 1  

        features = np.array([[runs, fails]])
        proba = model.predict_proba(features)[0][1]

        if test_file.name == most_recent.name:
            proba = min(proba + bonus, 1.0)

        ranked.append((str(test_file), proba, fails))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked

if __name__ == "__main__":
    tests_with_scores = select_tests("tests")

    if not tests_with_scores:
        print("[WARN] Hiç test bulunamadı veya model eğitilemedi.")
        sys.exit(0)

    print("▶️ Çalıştırma Sırası (Gerçek Data + AI + Bonus Skor):")
    for i, (test, score, fails) in enumerate(tests_with_scores, 1):
        print(f"{i}) {test} (score={score:.2f}, fails={fails})")

    os.makedirs(REPORTS_DIR, exist_ok=True)

    subprocess.run([
        sys.executable, "-m", "pytest", "-q",
        f"--junitxml={RESULTS_FILE}",
        "tests"
    ])
