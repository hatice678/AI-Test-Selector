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

    for testcase in root.iter("testcase"):
        test_name = testcase.get("classname", "") + "." + testcase.get("name", "")
        status = 0  # passed by default

        # Alt tag’lerde failure veya error var mı kontrol et
        for child in testcase:
            if "failure" in child.tag.lower() or "error" in child.tag.lower():
                status = 1
                break

        results.append((test_name, status))

    return results

def collect_reports():
    """Tek results.xml dosyasını oku ve CSV’ye ekle"""
    if not os.path.exists(RESULTS_FILE):
        print("⚠️ results.xml bulunamadı, önce testleri çalıştırın.")
        return

    fieldnames = ["timestamp", "report_file", "test_name", "test_fail"]
    file_exists = os.path.isfile(OUTPUT_CSV)

    with open(OUTPUT_CSV, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
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
