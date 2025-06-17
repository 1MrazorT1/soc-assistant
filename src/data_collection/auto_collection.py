import schedule
import time
import subprocess

def run_fetch_all():
    print("===> Auto-collection started <===")
    print("Fetching AlienVault...")
    subprocess.run(["python3", "alienvault/data_extraction.py"])

    print("Fetching Malshare...")
    subprocess.run(["python3", "src/Malshare/data_extraction.py"])

    print("Fetching MISP...")
    subprocess.run(["python3", "misp/data_extraction.py"])

    print("Fetching NVD...")
    subprocess.run(["python3", "NVD/data_extraction.py"])

    print("Fetching URLhaus...")
    subprocess.run(["python3", "URLhaus/data_extraction.py"])

    print("Building dashboard...")
    subprocess.run(["python3", "dashboard_builder.py"])

schedule.every(30).minutes.do(run_fetch_all)

print("----------- Auto-collection scheduled every 30 minutes.")
while True:
    schedule.run_pending()
    time.sleep(1)
