# Review closure ledger — #9 panel bookkeeping (vòng 1)

S1 FIXED — mặc định `--n 100` lệch thiết kế (Panel mặc định `--n 20`, Q14); cả CLI và MCP dùng `panel.DEFAULT_N = 20`, test đỏ trước rồi xanh, commit 69ebc4d.
SPEC-1 FIXED — cùng nguyên nhân với S1 (mặc định 100 thay vì 20 ở `cli.py` và `server.py`), đóng bằng cùng commit 69ebc4d.
