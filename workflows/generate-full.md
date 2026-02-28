---
description: Full pipeline - generate script then auto-convert to JSON (image prompts + voice_over)
---

# /generate-full — Pipeline Hoàn Chỉnh: Script → JSON → Extract

## Khi nào dùng?
User muốn tạo kịch bản VÀ JSON trong một lần gọi. Ví dụ:
- "/generate-full Chapter 1140"
- "Tạo full pipeline cho topic Gear 5"

## Pipeline

### Phase 1: Tạo Kịch Bản
Chạy **toàn bộ** workflow `/generate-script`:
1. Áp dụng System Prompt (rules đã inline trong `/generate-script`)
2. Parse input (TOPIC, TYPE, MODE)
3. Tạo file `.md` trong `outputs/`
4. Viết nội dung kịch bản vào file
5. Thông báo ngắn: `✅ Phase 1 done: [filename].md`

**KHÔNG dừng lại chờ review. Chạy tiếp Phase 2 ngay.**

### Phase 2: Tạo JSON
Chạy **toàn bộ** workflow `/generate-json` trên file `.md` vừa tạo:
1. Áp dụng JSON rules (đã inline trong `/generate-json`)
2. Đọc file `.md` vừa tạo ở Phase 1
3. Tách nội dung, cắt lớp voice_over
4. Tạo JSON với image prompts
5. Ghi vào file `.json` cùng tên

### Phase 3: Trích Xuất (Auto-Extract)
// turbo
Chạy script `extract.py` trên file `.json` vừa tạo:
```
python apps/tools/extract.py apps/script_generator/outputs/[filename].json
```
Script sẽ tự động tạo 2 file cạnh file JSON gốc:
- `[filename]_voice_over.txt` — mỗi dòng = 1 segment voice_over
- `[filename]_prompts.csv` — id, prompt, sample_image

**KHÔNG dừng lại chờ review. Thông báo kết quả cuối cùng.**

### Thông báo cuối cùng:
```
✅ Pipeline hoàn tất!
📝 Script: apps/script_generator/outputs/[filename].md (~X words)
🖼️ JSON: apps/script_generator/outputs/[filename].json (N segments)
📝 Voice Over: apps/script_generator/outputs/[filename]_voice_over.txt
📋 Prompts: apps/script_generator/outputs/[filename]_prompts.csv
Mở files để review nhé!
```

## Lưu ý
- Nếu user chỉ muốn 1 trong 2 bước → dùng `/generate-script` hoặc `/generate-json` riêng lẻ
- Chỉ muốn extract → chạy trực tiếp: `python apps/tools/extract.py <path.json>`
- Pipeline KHÔNG dừng giữa chừng để chờ review — chạy hết cả 3 phase rồi mới thông báo
- Feedback loop: User review files, sửa file nào thì dùng replace_file_content trực tiếp
