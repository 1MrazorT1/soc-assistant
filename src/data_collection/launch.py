import subprocess

print("Launching abuseipdb...")
subprocess.run(["python3", "abuseipdb/data_extraction.py"])

print("Launching VirusTotal...")
subprocess.run(["python3", "virus_total/data_extraction.py"])
