import subprocess

print("Launching abuseipdb...")
subprocess.Popen(["python3", "abuseipdb/data_extraction.py"])

print("Launching VirusTotal...")
subprocess.Popen(["python3", "virus_total/data_extraction.py"])
