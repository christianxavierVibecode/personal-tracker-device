import os
import readline
import glob
import math

# ==============================
# AUTOCOMPLETE (TAB)
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
# READ FILE
# ==============================
with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f if line.strip()]

total_lines = len(lines)

if total_lines == 0:
    print("⚠️ File kosong")
    exit(0)

print(f"\n📄 Jumlah baris di file: {total_lines}")

# ==============================
# LINES PER FILE
# ==============================
try:
    chunk_size = int(input("Masukkan jumlah baris per file: ").strip())
    if chunk_size <= 0:
        raise ValueError
except ValueError:
    print("❌ Harus berupa angka > 0")
    exit(1)

# ==============================
# OUTPUT FILE GENERATION
# ==============================
base_name = os.path.splitext(input_file)[0]
total_parts = math.ceil(total_lines / chunk_size)

print(f"\n✂️  File akan dipecah menjadi {total_parts} bagian\n")

for i in range(total_parts):
    start = i * chunk_size
    end = start + chunk_size
    part_lines = lines[start:end]

    output_file = f"{base_name}_part{i + 1}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for line in part_lines:
            f.write(line + "\n")

    print(f"✅ Dibuat: {output_file} ({len(part_lines)} baris)")

print("\n🎉 Proses selesai")
