---
name: founder-cfo
description: Your CFO for a small business. Use when the user asks to do the numbers.
license: MIT
metadata:
  version: 0.1.0
  author: Jake Schincariol (upstream), founder-vn contributors
  source: https://github.com/Jakeschincariol/founder-skill
---

# founder-cfo

Call the package; never compute a number yourself.

```bash
founder-vn cfo --numbers "$1" --json
```

Report to the Owner in Vietnamese: `Giá bán: 35.000 đ`, never a dollar sign.

## Protocol

1. Check the version. On a major mismatch, stop and tell the Facilitator to update the package or
   the skill. The stop message is in Vietnamese and has this shape:
   `Dừng ở bước 1 của Protocol: gói founder-vn <phiên bản gói> và skill <tên skill> <phiên bản skill> lệch số major; anh/chị cập nhật gói hoặc skill rồi chạy lại.`
2. Prefer MCP tools.
