import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

REPORTS_DIR = "reports"
OUTPUT_CSV = "training_data.csv"

def parse_junit_xml(file_path):
    """JUnit XML dosyasını parse et, test adı ve sonucunu döndür"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    results = []

    for testcase in root.iter("testcase"):
        test_name = testcase.get("classname", "") + "." + testcase.get("name", "")

        # Varsayılan passed
        status = 0  

        # Alt elemanları gez
        for child in list(testcase):
            tag = child.tag.lower()
            if "failure" in tag or "error" in tag:
                status = 1
                break

        results.append((test_name, status))

    return results

def collect_reports():
    """reports klasöründeki tüm XML dosyalarını gez, CSV’ye yaz"""
    fieldnames = ["timestamp", "report_file", "test_name", "test_fail"]

    file_exists = os.path.isfile(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for file in os.listdir(REPORTS_DIR):
            if file.endswith(".xml"):
                file_path = os.path.join(REPORTS_DIR, file)
                test_results = parse_junit_xml(file_path)
                for test_name, status in test_results:
                    writer.writerow({
                        "timestamp": datetime.now().isoformat(),
                        "report_file": file,
                        "test_name": test_name,
                        "test_fail": status
                    })

if __name__ == "__main__":
    if not os.path.exists(REPORTS_DIR):
        print("⚠️ reports klasörü bulunamadı, önce testleri çalıştırın.")
    else:
        collect_reports()
        print(f"✅ Veriler {OUTPUT_CSV} dosyasına eklendi.")
