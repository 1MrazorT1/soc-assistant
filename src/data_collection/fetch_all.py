import subprocess

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
