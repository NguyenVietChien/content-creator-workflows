---
description: Generate JSON (image prompts + voice_over segments) from a finished script
---

# /generate-json — Tạo JSON Từ Kịch Bản

## Khi nào dùng?
User muốn chuyển kịch bản đã viết sang JSON chứa image prompts + voice_over. Ví dụ:
- "/generate-json" (tự lấy script mới nhất trong outputs/)
- "Tạo JSON cho script Gunko"
- User paste nội dung kịch bản trực tiếp

## Bước 1: Áp Dụng JSON Generation Rules

Tất cả quy tắc JSON generation đã được inline trong workflow này (Bước 4-5). Không cần đọc file bên ngoài.

## Bước 2: Xác Định Script Nguồn

Ưu tiên theo thứ tự:
1. User paste trực tiếp nội dung script → dùng luôn
2. User chỉ file cụ thể (vd: "file Gunko") → đọc file đó trong `apps/script_generator/outputs/`
3. Không chỉ rõ → tìm file `.md` mới nhất trong `apps/script_generator/outputs/` và dùng nó

// turbo
Đọc file script nguồn:
```
view_file apps/script_generator/outputs/[filename].md
```

## Bước 3: Tách Nội Dung Script

**Loại bỏ** các phần KHÔNG phải nội dung đọc:
- Header (`# 🎬 ...`)
- Config line (`**Config:** ...`)
- Stats line (`📊 **Stats:** ...`)
- Separator lines (`---`)
- Headers (`## PHẦN X: ...`, `## KẾT`) → GIỮ LẠI text, bỏ markdown syntax

**Chỉ giữ lại** text thuần — nội dung voice-over thực tế.

## Bước 4: Cắt Lớp Voice Over

Cắt toàn bộ text thành các đoạn nhỏ nối tiếp nhau:
- Ngắt tại dấu câu tự nhiên (. , ! ?)
- Mỗi đoạn tối đa **50-70 từ**
- **NGUYÊN TẮC BẢO TOÀN**: Ghép tất cả đoạn voice_over lại **phải khớp 100%** text gốc. KHÔNG thêm, bớt, sửa bất kỳ từ nào.

## Bước 5: Tạo JSON và Ghi File

**KHÔNG output ra chat. Ghi thẳng vào file JSON.**

File path: `apps/script_generator/outputs/[tên_script_gốc].json`
(Cùng tên với file `.md` nguồn, chỉ đổi extension. Ví dụ: `gunko_shuri_brook_13h20__21_02_2026.json`)

### Cấu trúc JSON — Một file duy nhất, array of parts:

```json
[
  {
    "status": "Part 1/N",
    "metadata": {
      "source_script": "[filename].md",
      "total_segments": 30,
      "generated_at": "YYYY-MM-DD HH:MM"
    },
    "prompts": [
      {
        "id": 1,
        "type": "image",
        "range": "00:00-00:XX",
        "voice_over": "<Đoạn text CẮT CHÍNH XÁC từ script>",
        "visual_description": "<Mô tả tiếng Việt: nhân vật, hành động, bối cảnh>",
        "sample_image": [],
        "prompt": "<STYLE TRIGGER + SCENE DESCRIPTION + TECHNICAL DETAILS>",
        "notes": "<Ghi chú về SFX, biểu cảm, mood>"
      }
    ]
  },
  {
    "status": "Part 2/N",
    "metadata": { "..." : "..." },
    "prompts": [ "...segments tiếp theo..." ]
  }
]
```

**Quy tắc:**
- Luôn xuất **MỘT file JSON duy nhất** — KHÔNG tách thành nhiều file
- Root element là **array `[]`**, mỗi phần tử là một part object
- Mỗi part chứa tối đa **30 segments** trong `prompts`
- Nếu script ≤30 segments → array chỉ có 1 object
- Nếu script >30 segments → array có nhiều objects, id tiếp nối liên tục (part 1: id 1-30, part 2: id 31-60, ...)

### Công thức Prompt hình ảnh (3 phần ghép lại):

**[STYLE TRIGGER]** (cố định):
`Eiichiro Oda art style, authentic One Piece manga page, black and white ink illustration, G-pen texture, traditional screentone shading, dramatic shonen composition,`

**[SCENE DESCRIPTION]** (thay đổi theo đoạn):
Mô tả chi tiết nhân vật, hành động, biểu cảm cường điệu, bối cảnh tương ứng đoạn voice_over.

**[TECHNICAL DETAILS]** (cố định):
`heavy cross-hatching, high contrast monochrome, bold hand-drawn speed lines, large Japanese SFX text integrated into art, gritty texture, extreme perspective.`

### Quy tắc range (timestamp):
- Ước lượng ~150 từ/phút cho voice over tiếng Việt
- Tính duration mỗi đoạn dựa trên word count
- Range nối tiếp nhau: segment 1 kết thúc = segment 2 bắt đầu

## Bước 6: Thông Báo User

Sau khi ghi xong file, thông báo ngắn:

```
✅ Đã tạo JSON: apps/script_generator/outputs/[filename].json
📊 Stats: [N] segments | Source: [script_name].md
Mở file để review nhé!
```

KHÔNG paste JSON vào chat. User review trực tiếp trong editor.

## Bước 7: Feedback Loop

Sau khi user review, chờ feedback:
- **"Sửa prompt segment X"** → dùng replace_file_content sửa trực tiếp trong file JSON
- **"Gộp/tách segment"** → sửa trực tiếp trong file JSON
- **"Đổi style"** → thay STYLE TRIGGER, sửa trực tiếp
- **"Tạo lại"** → overwrite file JSON
