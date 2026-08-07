import os
import subprocess
import readline
import glob
import sys

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
# HELPER FUNCTIONS
# ==============================
def ensure_txt(name, default):
    if not name:
        return default
    if not name.lower().endswith(".txt"):
        return name + ".txt"
    return name

def run_command(cmd, silent=True):
    if silent:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        subprocess.run(cmd)

# ==============================
# 1. ALERT / INFO
# ==============================
print("\n==================== ALERT ====================")
print("Mohon pastikan komputer anda sudah terinstall program berikut:\n")
print('python 3  => sudo apt install python3')
print('pip       => sudo apt install python3-pip')
print('yt-dlp    => pip install yt-dlp')
print('ffmpeg    => sudo apt install ffmpeg -y')
print('[opsional] nightly yt-dlp => yt-dlp --update-to nightly\n')
print("Direktori saat ini =>", os.getcwd())
print("================================================\n")

# ==============================
# 2. INPUT CHANNEL + LIST FILE
# ==============================
channel_url = input("Masukkan URL Channel: ").strip()

if not channel_url.startswith("http"):
    print("❌ URL channel tidak valid")
    sys.exit(1)

raw_list_name = input(
    "Masukkan nama file txt (default: list.txt): "
).strip()

list_file = ensure_txt(raw_list_name, "list.txt")

print("\n⏳ Mengekstrak daftar video... (harap tunggu)\n")

yt_dlp_cmd = [
    "yt-dlp",
    "--flat-playlist",
    "--print",
    "%(title)s: %(webpage_url)s",
    channel_url
]

with open(list_file, "w", encoding="utf-8") as f:
    subprocess.run(yt_dlp_cmd, stdout=f, stderr=subprocess.DEVNULL)

if not os.path.isfile(list_file) or os.path.getsize(list_file) == 0:
    print("❌ Gagal membuat file list")
    sys.exit(1)

print(f"✅ Daftar video disimpan ke: {list_file}\n")

# ==============================
# 3. CLEAN VERSION CONFIRMATION
# ==============================
choice = input(
    "Apakah anda ingin membuat salinan versi bersih dari file list sebelumnya (Y/N): "
).strip().lower()

clean_file = None

if choice == "y":
    raw_clean_name = input(
        "Masukkan nama file txt hasil bersih (default: Resultlist.txt): "
    ).strip()

    clean_file = ensure_txt(raw_clean_name, "Resultlist.txt")

    cleaned_lines = []

    with open(list_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "http" in line:
                cleaned_lines.append(line[line.find("http"):])

    if not cleaned_lines:
        print("⚠️ Tidak ada URL ditemukan untuk dibersihkan")
        sys.exit(0)

    with open(clean_file, "w", encoding="utf-8") as f:
        for item in cleaned_lines:
            f.write(item + "\n")

    print(f"✅ File bersih dibuat: {clean_file}\n")

# ==============================
# 4. DOWNLOAD CONFIRMATION
# ==============================
if clean_file:
    download_prompt = (
        f"Apakah anda ingin lanjut ke proses download?\n"
        f"Semua file akan di download di direktori saat ini,\n"
        f"nama filenya adalah {clean_file} (Y/N): "
    )

    download_choice = input(download_prompt).strip().lower()

    if download_choice == "y":
        print("\n⬇️  Memulai proses download...\n")
        subprocess.run(["yt-dlp", "-a", clean_file])
        print("\n✅ Proses download selesai")

print("\n🎉 Semua proses selesai. Terima kasih.\n")
