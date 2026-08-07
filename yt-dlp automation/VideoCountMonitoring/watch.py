import os
import time
import glob
import readline

# ==============================
# AUTOCOMPLETE
# ==============================
def file_autocomplete(text, state):
    matches = glob.glob(text + "*")
    try:
        return matches[state]
    except IndexError:
        return None

readline.set_completer(file_autocomplete)
readline.parse_and_bind("tab: complete")

# ==============================
# INPUT FILE
# ==============================
input_file = input("Masukkan nama file txt: ").strip()

if not input_file:
    print("❌ Nama file tidak boleh kosong")
    exit(1)

if not os.path.isfile(input_file):
    print(f"❌ File '{input_file}' tidak ditemukan")
    exit(1)

# ==============================
# COUNT TOTAL LINES (ONCE)
# ==============================
with open(input_file, "r", encoding="utf-8") as f:
    total_lines = sum(1 for line in f if line.strip())

if total_lines == 0:
    print("⚠️ File input kosong")
    exit(0)

# ==============================
# WATCH LOOP
# ==============================
INTERVAL = 10

try:
    while True:
        mp4_count = len(glob.glob("*.mp4"))

        os.system("clear")  # mirip watch
        print("Monitoring download (Ctrl+C untuk keluar)\n")
        print(f"{mp4_count} / {total_lines}")
        print(f"Update setiap {INTERVAL} detik")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n👋 Monitoring dihentikan oleh user")
