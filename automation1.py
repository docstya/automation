# made by docstya

import subprocess
import time

print('''
----------------------------------------------

╭━━━┳━━━┳━╮╱╭╮╭━━━━┳━━━┳━━━┳━━━━┳━━━┳━━━╮
┃╭━╮┃╭━━┫┃╰╮┃┃┃╭╮╭╮┃╭━━┫╭━╮┃╭╮╭╮┃╭━━┫╭━╮┃
┃╰━╯┃╰━━┫╭╮╰╯┃╰╯┃┃╰┫╰━━┫╰━━╋╯┃┃╰┫╰━━┫╰━╯┃
┃╭━━┫╭━━┫┃╰╮┃┃╱╱┃┃╱┃╭━━┻━━╮┃╱┃┃╱┃╭━━┫╭╮╭╯
┃┃╱╱┃╰━━┫┃╱┃┃┃╱╱┃┃╱┃╰━━┫╰━╯┃╱┃┃╱┃╰━━┫┃┃╰╮
╰╯╱╱╰━━━┻╯╱╰━╯╱╱╰╯╱╰━━━┻━━━╯╱╰╯╱╰━━━┻╯╰━╯

made by docstya
----------------------------------------------
''')

target_ip = input("Target IP: ")
target_site = input("Target domain: ")
sql_target = input("Target SQL: ")

# -------- NMAP SCAN --------
scan = subprocess.run(
    [
        "nmap",
        "-Pn",
        "-T3",
        "--max-retries", "2",
        "--script", "vuln",
        "--script-timeout", "30s",
        target_ip
    ],
    capture_output=True,
    text=True
)

print(scan.stdout)
time.sleep(0.25)
print("-----------------------------------------")
time.sleep(0.25)

# -------- SUBFINDER --------
scan1 = subprocess.run(
    ["subfinder", "-silent", "-d", target_site],
    capture_output=True,
    text=True
)

print(scan1.stdout)
time.sleep(0.25)
print("-----------------------------------------")
time.sleep(0.25)

# -------- ASSETFINDER + HTTPX --------
scan2 = subprocess.run(
    f"assetfinder --subs-only {target_site} | httpx -silent",
    shell=True,
    capture_output=True,
    text=True
)

print(scan2.stdout)
time.sleep(0.25)
print("-----------------------------------------")
time.sleep(0.25)

# -------- SQLMAP (NON-INTERACTIVE) --------
scan3 = subprocess.run(
    ["sqlmap", "-u", sql_target, "--forms", "--crawl=2", "--batch"],
    capture_output=True,
    text=True
)

print(scan3.stdout)
time.sleep(0.25)
print("-----------------------------------------")
time.sleep(0.25)

# commix scan

scan4 = subprocess.run(
    [
        "commix", "-u", target_site, "--batch", "--level=3", "--risk=2"
    ],
    capture_output=True,
    text=True
)

print(scan3.stdout)
time.sleep(0.25)
print("-----------------------------------------")


# -------- ERROR CHECKS --------
if scan.returncode != 0:
    print("Nmap scan failed!")
    print(scan.stderr)

if scan1.returncode != 0:
    print("Subfinder scan failed!")
    print(scan1.stderr)

if scan2.returncode != 0:
    print("Assetfinder/httpx failed!")
    print(scan2.stderr)

if scan3.returncode != 0:
    print("sqlmap scan failed!")
    print(scan3.stderr)

if scan4.returncode != 0:
    print("Commix scan failed!")
    print(scan4.stderr)
