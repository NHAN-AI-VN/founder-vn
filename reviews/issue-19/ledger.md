# Review closure ledger — #19 vòng 1

S1 FIXED — `docs/hosts/kiro.md` nói `v0.2.0` đã lên PyPI (bỏ "Before the tag", "once the", "After the tag"; đường dẫn wheel chỉ còn là biến thể cục bộ cho phát triển) và `test_kiro_page_has_the_clean_install_walkthrough_for_19` có assertion mới cấm các cụm đó (đỏ trước trên trang cũ, xanh sau): commit `0f422f3`; `uv run pytest tests/test_hosts.py tests/test_front_door.py -q` 22 passed.
