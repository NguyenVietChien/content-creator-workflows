"""JSON Extractor CLI — Extract voice_over & prompts from script JSON files.

Usage:
    python extract.py <path_to_json>
    python extract.py               (tự tìm file .json mới nhất trong outputs/)

Output: tạo 2 file cạnh file JSON gốc:
    - *_voice_over.txt   (mỗi dòng = 1 segment voice_over)
    - *_prompts.csv      (id, prompt, sample_image)

Zero dependencies — chỉ dùng Python stdlib.
"""
import sys
import os
import json
import csv
import glob

# Fix Windows console encoding
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_latest_json():
    """Tìm file .json mới nhất trong outputs/."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(script_dir, "..", "script_generator", "outputs")
    outputs_dir = os.path.normpath(outputs_dir)

    if not os.path.isdir(outputs_dir):
        return None

    json_files = glob.glob(os.path.join(outputs_dir, "*.json"))
    if not json_files:
        return None

    return max(json_files, key=os.path.getmtime)


def extract(json_path):
    """Đọc JSON và tạo voice_over.txt + prompts.csv."""
    print(f"📂 File: {os.path.basename(json_path)}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Collect all prompts
    all_prompts = []
    if isinstance(data, list):
        for part in data:
            all_prompts.extend(part.get("prompts", []))
    elif isinstance(data, dict):
        all_prompts = data.get("prompts", [])

    if not all_prompts:
        print("❌ Không tìm thấy prompts trong JSON!")
        return False

    print(f"📊 Tìm thấy {len(all_prompts)} segments")

    base = os.path.splitext(json_path)[0]
    txt_path = base + "_voice_over.txt"
    csv_path = base + "_prompts.csv"

    # 1. voice_over.txt
    with open(txt_path, "w", encoding="utf-8") as f:
        for p in all_prompts:
            f.write(p.get("voice_over", "").strip() + "\n")
    print(f"📝 → {os.path.basename(txt_path)}")

    # 2. prompts.csv (no header: id, prompt, sample_image)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for p in all_prompts:
            pid = p.get("id", "")
            prompt = p.get("prompt", "")
            samples = p.get("sample_image", [])
            sample_str = ",".join(samples) if samples else ""
            writer.writerow([pid, prompt, sample_str])
    print(f"📋 → {os.path.basename(csv_path)}")

    print(f"\n✅ Hoàn tất! Files đã lưu cạnh file JSON gốc.")
    return True


def main():
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = find_latest_json()
        if not json_path:
            print("❌ Không tìm thấy file JSON. Dùng: python extract.py <path>")
            sys.exit(1)
        print(f"🔍 Tự động chọn file mới nhất:")

    if not os.path.isfile(json_path):
        print(f"❌ File không tồn tại: {json_path}")
        sys.exit(1)

    try:
        extract(json_path)
    except json.JSONDecodeError as e:
        print(f"❌ JSON không hợp lệ: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
