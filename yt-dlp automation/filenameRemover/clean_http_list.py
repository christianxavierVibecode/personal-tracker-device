import os
import readline
import glob

# === AUTOCOMPLETE FUNCTION ===
def file_autocomplete(text, state):
    matches = glob.glob(text + "*")
    try:
        return matches[state]
    except IndexError:
        return None

readline.set_completer(file_autocomplete)
readline.parse_and_bind("tab: complete")

# === INPUT FILE ===
input_file = input("Masukkan nama file sumber: ").strip()

if not input_file:
    print("❌ Nama file tidak boleh kosong")
    exit(1)

if not os.path.isfile(input_file):
    print(f"❌ File '{input_file}' tidak ditemukan")
    exit(1)

# === OUTPUT FILE ===
output_file = input(
    "Masukkan nama file output (default: resultlist.txt): "
).strip()

if not output_file:
    output_file = "resultlist.txt"
else:
    if not output_file.lower().endswith(".txt"):
        output_file += ".txt"

cleaned_lines = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if "http" not in line:
            continue

        http_index = line.find("http")
        cleaned_lines.append(line[http_index:])

if not cleaned_lines:
    print("⚠️ Tidak ada data yang mengandung 'http'")
    exit(0)

# === WRITE OUTPUT ===
with open(output_file, "w", encoding="utf-8") as f:
    for item in cleaned_lines:
        f.write(item + "\n")

print(f"✅ Berhasil mengekstrak {len(cleaned_lines)} baris")
print(f"📄 Hasil disimpan di: {output_file}")
