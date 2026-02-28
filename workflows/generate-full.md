---
description: Full pipeline - generate script then auto-convert to JSON (image prompts + voice_over)
---

# /generate-full — Pipeline Hoàn Chỉnh: Script → JSON

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

### Thông báo cuối cùng:
```
✅ Pipeline hoàn tất!
📝 Script: apps/script_generator/outputs/[filename].md (~X words)
🖼️ JSON: apps/script_generator/outputs/[filename].json (N segments)
Mở 2 file để review nhé!
```

## Lưu ý
- Nếu user chỉ muốn 1 trong 2 bước → dùng `/generate-script` hoặc `/generate-json` riêng lẻ
- Pipeline KHÔNG dừng giữa chừng để chờ review — chạy hết cả 2 phase rồi mới thông báo
- Feedback loop: User review cả 2 file, sửa file nào thì dùng replace_file_content trực tiếp
