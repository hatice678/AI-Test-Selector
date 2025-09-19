import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

REPORTS_DIR = "reports"
OUTPUT_CSV = "training_data.csv"
RESULTS_FILE = os.path.join(REPORTS_DIR, "results.xml")

def parse_junit_xml(file_path):
    """JUnit XML dosyasını parse et, test adı ve sonucunu döndür"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    results = []

    for testsuite in root.iter("testsuite"):
        for testcase in testsuite.iter("testcase"):
            test_name = testcase.get("classname", "") + "." + testcase.get("name", "")
            status = 0

            # Altında failure veya error varsa bu test fail
            for child in testcase:
                if child.tag.lower() in ["failure", "error"]:
                    status = 1
                    break

            results.append((test_name, status))

    return results

def collect_reports():
    """Sadece results.xml dosyasını oku ve CSV’ye yaz"""
    if not os.path.exists(RESULTS_FILE):
        print("[WARN] results.xml bulunamadı, önce testleri çalıştırın.")
        return

    fieldnames = ["timestamp", "report_file", "test_name", "test_fail"]

    with open(OUTPUT_CSV, "w", newline="") as csvfile:  # 'w' → her build baştan yazar
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        test_results = parse_junit_xml(RESULTS_FILE)
        for test_name, status in test_results:
            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "report_file": "results.xml",
                "test_name": test_name,
                "test_fail": status
            })

if __name__ == "__main__":
    os.makedirs(REPORTS_DIR, exist_ok=True)
    collect_reports()
    print(f"✅ Veriler {OUTPUT_CSV} dosyasına eklendi.")
