# Phản biện độc lập: đề xuất vòng 5 (Q30–Q36) cho founder-vn

- Ngày: 21/11/2026.
- Người viết: một sub-agent `general-task-execution` với ngữ cảnh mới, được giao toàn bộ trạng thái
  thiết kế đến hết vòng 5 và yêu cầu phản biện, kiểm chứng sự thật, ước lượng công sức. Không sửa file nào.
- Đối tượng: đề xuất Q30–Q36 (package + MCP server, fan-out trong server, trạng thái file, client
  LLM, đóng gói, 14 tuần, kiểm chứng 6 host). Bản thiết kế sau khi tiếp nhận: `docs/founder-vn-design.md`.

## Tiếp nhận

| Mục | Phán quyết của phản biện | Xử lý ở vòng 6–7 |
|---|---|---|
| Q30 | Đồng ý có điều kiện | Chấp nhận: một package xuất cả CLI và MCP, khóa đường dẫn trong `founder/` |
| Q31 | Đồng ý có điều kiện | Chấp nhận: job bất đồng bộ, ghi model + hash prompt, tự parse JSON; đường sub-agent host dời sang v1.1 |
| Q32 | Đồng ý | Chấp nhận; ghi rõ "Grok bot" = Grok Build CLI |
| Q33 | Đồng ý có điều kiện | Chấp nhận: bỏ "sampling để sau", tài liệu hóa khác biệt provider và biến môi trường Gemini CLI |
| Q34 | Đồng ý có điều kiện | Chấp nhận: thêm `founder-vn install --host`, KiroCrew qua dashboard, Gemini/Antigravity cần xác nhận |
| Q35 | Phản đối một phần | Chấp nhận: hỏi toàn/bán thời gian (Q43: toàn thời gian), dời ma trận host sau pilot, hạ mốc tuần 6 |
| Q36 | Phản đối | Chấp nhận: test tương thích tất định trên 6 host, pipeline đầy đủ chỉ Kiro + Claude Code + Codex |
| 7 câu hỏi còn lại | | Thành Q37–Q42 (thuế theo doanh thu, verdict, nguồn pháp lý, baseline/đo lường, đồng thuận, API key/mô hình) và làm rõ Q32 |

Một tiền đề của tôi bị phản biện bác đúng: KiroCrew **có** fan-out (`spawn_run`); vấn đề thật là tên
tool khác nhau giữa host, không phải host thiếu năng lực.

---

## Toàn văn báo cáo

Đã đọc 11 SKILL.md, 4 script, `kirocrew.json`; tra cứu web hôm nay; không sửa file nào.

### 1. Kiểm chứng sự thật

**(a) MCP stdio: cả bốn host đều hỗ trợ.** Codex: `codex mcp add <name> -- <cmd>`, lưu `[mcp_servers.<name>]` trong `~/.codex/config.toml`, `tool_timeout_sec` mặc định 60 s ([docs](https://developers.openai.com/codex/mcp), [60 s](https://zenn.dev/aicoding_guide/articles/acg-codex-mcp-enabled-tools-timeout), [issue #4157](https://github.com/openai/codex/issues/4157)). Gemini CLI: `mcpServers.{command,args,env}` trong settings.json, timeout mặc định 600 s, và **tự xoá biến môi trường khớp `*KEY*`/`*SECRET*` khi spawn server** trừ khi khai báo tường minh trong `env` ([docs](https://geminicli.com/docs/tools/mcp-server/)). Lưu ý: từ 18/6/2026 Gemini CLI ngừng phục vụ tài khoản miễn phí/Pro/Ultra, thay bằng Antigravity CLI `agy` ([thông báo chính thức](https://github.com/google-gemini/gemini-cli/discussions/27274)). Grok Build: `[mcp_servers.<name>]` trong `~/.grok/config.toml`, timeout 6000 s ([docs](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md)); skill ở `.grok/skills/` ([docs](https://docs.x.ai/build/features/skills-plugins-marketplaces)). Cursor: `mcp.json` với `command/args` ([docs](https://cursor.com/docs/mcp)). KiroCrew: `includeMcpJson:false` nên không nạp mcp.json, nhưng thêm được server qua trang MCP Servers của dashboard ([docs](https://github.com/kirodotdev/KiroCrew/blob/main/src/kiro_crew/docs/coming-from-kiro-cli.md)).

**(b) Endpoint tương thích OpenAI: có, nhưng lệch nhau.** Anthropic tự mô tả lớp tương thích là để *test*; `response_format` chỉ nhận `json_schema`+`strict:true` (`json_object` trả 400); `seed` bị bỏ qua; `temperature` < 1 trả 400 trên Claude 4.7+ ([docs](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk)). Gemini dùng được qua thư viện OpenAI, Google khuyên gọi API gốc nếu chưa dùng thư viện đó ([docs](https://ai.google.dev/gemini-api/docs/openai)). xAI chạy `api.x.ai/v1/chat/completions` nhưng xếp nó là *legacy*, tính năng mới vào Responses API trước ([docs](https://docs.x.ai/developers/model-capabilities/legacy/chat-completions)).

**(c) MCP sampling đã bị khai tử** từ phiên bản giao thức 2026-07-28 (SEP-2577); khuyến nghị chính thức là server gọi thẳng API nhà cung cấp ([SEP](https://modelcontextprotocol.io/seps/2577-deprecate-roots-sampling-and-logging), [SDK](https://ruby.sdk.modelcontextprotocol.io/server/sampling/)). Claude Code 2.1.292 không khai báo sampling; chỉ VS Code nêu có ([khảo sát client 26/10/2026](https://modelcontextprotocol.info/docs/clients/)). Tài liệu Kiro chỉ nêu tools/prompts/resources ([docs](https://kiro.dev/docs/mcp/usage/)). "Sampling để sau" nên đổi thành "không bao giờ".

**(d) `npx skills add`** cài theo agent: Kiro CLI `.kiro/skills/`, Grok Build `.grok/skills/`, Codex/Gemini CLI/Cursor `.agents/skills/` ([bảng agent](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)). KiroCrew không có trong danh sách nhưng đọc `<project>/.kiro/skills/` khi dự án được trust; `~/.kiro/skills/` không nằm trong catalog mặc định ([docs](https://github.com/kirodotdev/KiroCrew/blob/main/src/kiro_crew/docs/skills.md)). Agent Skills được trao cho AAIF ngày 22/10/2026 ([Anthropic](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)).

**(e) Tiền lệ:** Claude Code plugin gói skill + MCP server ([ví dụ](https://github.com/jenkinsm13/claude-plugins), [template đa host](https://github.com/DavidEncrypted/portable-agent-plugin-template)); Kiro Powers ([docs](https://kiro.dev/docs/powers/)); plugin Codex/Grok Build kèm stdio MCP + skill ([ví dụ](https://github.com/Reederey87/grok-build-codex-plugin)); `skillz` biến SKILL.md + script thành tool MCP ([PyPI](https://pypi.org/project/skillz/)).

**Một tiền đề sai:** KiroCrew **có** fan-out. Tool `spawn_run` nhận mảng `tasks`, chạy song song, chọn backend kiro/claude/codex ([docs](https://github.com/kirodotdev/KiroCrew/blob/main/src/kiro_crew/docs/subagents.md)). Codex ([docs](https://developers.openai.com/codex/multi-agent)) và Gemini CLI ([docs](https://geminicli.com/docs/core/subagents/)) cũng có sub-agent. Vấn đề thật là tên tool mỗi host khác nhau nên một SKILL.md không điều khiển được hết, không phải host thiếu năng lực.

### 2. Đánh giá kỹ thuật

**MCP có là mẫu số chung?** Cho 4 script tất định: có, nhưng shell cũng là mẫu số chung của cả 6 host (KiroCrew có `shell`). MCP đổi đối số có schema lấy cấu hình riêng từng host, timeout khởi động và lỗi "server disconnected" khó chẩn đoán với người không chuyên. Cách tốt hơn, không hạ cấp: **một package PyPI xuất cả CLI (`founder-vn cfo …`) và MCP server mỏng bọc cùng hàm**; skill ưu tiên MCP, host chưa cấu hình được thì dùng CLI qua shell, đầu ra giống hệt.

**Fan-out trong server (Q31)** đúng hướng theo spec, nhưng:
- *Timeout:* 20–100 lượt gọi LLM vượt 60 s của Codex. MCP Tasks có hai phiên bản không tương thích và Claude Code chưa hỗ trợ ([issue](https://github.com/anthropics/claude-code/issues/102347)). Phải tự thiết kế job: `panel_run` trả job id, `panel_status` để poll, ghi answers tăng dần.
- *Phi xác định:* seed chỉ chi phối thẻ persona, không chi phối câu trả lời; Anthropic bỏ `seed`, cấm hạ `temperature`. Phải ghi model và hash prompt vào `panel.json`.
- *Chất lượng:* một lượt completion ổn định hơn sub-agent có tool (upstream thừa nhận sub-agent hay in JSON ra chat thay vì ghi file). Nhưng model server khác model host, nên bảng "6 host cùng kết quả" vô nghĩa với panel.
- *Provider:* không dựa vào `response_format`/`seed`; tự parse JSON (`panel.py` đã có `_answer_ok`). Biến `FOUNDER_LLM_API_KEY` bị Gemini CLI xoá nếu không khai báo trong `env` của server. Người dùng Kiro/Claude Code trả thêm API key dù thuê bao đã gồm sub-agent.
- *Dữ liệu người pilot:* số liệu tài chính, địa điểm đi qua API bên thứ ba dưới khóa của người điều phối. Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 hiệu lực 1/1/2026 ([nguồn](https://www.aplawjapan.com/application/files/1417/7502/7641/EN_Newsletter_VNM_048.pdf)): cần phiếu đồng thuận và chính sách lưu trữ.

**Tool nhận đường dẫn và ghi file:** rủi ro thật vì server chạy với quyền người dùng. Cần khoá gốc (`FOUNDER_ROOT` hoặc `cwd/founder`), từ chối `..`, đường dẫn tuyệt đối ngoài gốc, symlink; chỉ ghi `.md/.json`; không xoá.

**Lỗi bản địa hoá có sẵn trong code:** `van_westendorp._f` xoá dấu phẩy rồi ép float nên `"35.000"` thành 35.0; `panel.deal` làm tròn thu nhập đến 1.000 (VND/tháng nên là 100.000); `compile.py` nạp `unit_economics.py` qua đường dẫn `../founder-cfo/` nên phải gom package mới chạy. Quan trọng hơn: `price` upstream là *trước thuế*; hộ kinh doanh nộp GTGT/TNCN theo **tỷ lệ % trên doanh thu**, nên "giá gồm VAT" đòi thêm một dòng thuế theo doanh thu vào mô hình, không chỉ đổi ký hiệu tiền.

### 3. Công sức

Cho 1 người có coding agent: gom 4 script thành package + CLI + tham số tiền tệ + test đơn vị (`35.000 đ`, parser `35k`/`1,2 triệu`) 2–3 ngày; MCP server 6 tool + khoá đường dẫn 1–1,5 ngày; client LLM + retry + khác biệt 3 provider 1 ngày; runner panel bất đồng bộ với test LLM giả 2 ngày; PyPI + CI + README 1 ngày. **Tổng 7–9 ngày:** +2 tuần đủ cho phần này, không đủ nếu cộng ma trận 6 host (3–5 ngày cài, debug timeout/env/trust) và viết lại skill song song.

Toàn bộ 14 tuần: 12 skill × 1,5–2 ngày có case thật = 18–24 ngày; server 7–9; 6 host 3–5; pilot 20 × ~4 giờ (intake, chạy, review, PDF, hỏi lại) ≈ 10 ngày chưa kể tuyển người. Tổng 45–55 ngày ≈ 9–11 tuần làm 100%, không dự phòng; buổi pilot cuối phải xong trước tuần 12 để đo sau 2 tuần. Nút thắt là **tuyển 20 người thật sắp mở hộ kinh doanh**, không phải code.

### 4. Sản phẩm và pilot

- "Đổi một quyết định thật" đo bằng tự khai sau 2 tuần, do chính tác giả điều phối: thiên lệch mong muốn xã hội và quy kết nhân quả (ngồi 60 phút với bất kỳ kế hoạch nào cũng đổi quyết định). Khắc phục rẻ: ghi **baseline bằng văn bản** ở intake (giá, địa điểm, vốn, mở/không), đăng ký trước 3 câu hỏi, để người khác gửi khảo sát Zalo. n = 20 với ngưỡng 50% có khoảng tin cậy ±22 điểm; đừng diễn giải như chứng cứ thống kê.
- Panel mô phỏng đang **gác cổng verdict**: `compile.py` ghi "Profitable" khi buy-rate ≥ 25%, trái với cảnh báo upstream "buy rate là cận trên". Bản VN nên tách panel khỏi verdict hoặc đổi tên verdict.
- `founder-permits` "tra tại thời điểm chạy": thử truy cập hôm nay, thuvienphapluat trả 403 cho client không phải trình duyệt; gdt.gov.vn trả 245 byte vỏ JS; dichvucong.gov.vn là portal JS; **vbpl.vn** (CSDL quốc gia về VBQPPL) và chinhphu.vn trả HTML đầy đủ. Tìm web tiếng Việt về pháp lý trả chủ yếu trang dịch vụ SEO. "Cấu trúc tĩnh" cũng sai: Nghị định 168/2025 (hiệu lực 1/7/2025, [VGP](https://en.baochinhphu.vn/govt-promulgates-new-decree-on-business-registration-111250702093740506.htm)) đã bị sửa bởi Nghị định 296/2026 ngày 23/7/2026 ([KPMG](https://kpmg.com/content/dam/kpmgsites/vn/pdf/2026/08/legal-alert-decree-296-ja.pdf.coredownload.inline.pdf)); thuế hộ kinh doanh đổi lớn năm 2026 (bỏ khoán, hoá đơn điện tử theo bậc doanh thu). Skill cần nguồn ưu tiên vbpl.vn, ngày kiểm chứng ghi trong repo, và khi không fetch được thì từ chối thay vì đoán.
- Giả định ngầm: "Grok bot" là Grok Build CLI có filesystem, không phải grok.com; người hỗ trợ cài được cả Node (npx) lẫn uv/Python và có API key; model rẻ viết tiếng Việt giọng người mua đủ tự nhiên.

### 5. Kết luận

| | Phán quyết | Lý do |
|---|---|---|
| Q30 | Đồng ý có điều kiện | Gom package đúng. Xuất **cả CLI và MCP** từ một package; skill gọi MCP trước, CLI sau, cùng đầu ra. Khoá đường dẫn trong gốc `founder/`. |
| Q31 | Đồng ý có điều kiện | Đúng hướng vì sampling đã khai tử. Phải là job bất đồng bộ, ghi model/prompt hash, tự parse JSON. Giữ tuỳ chọn fan-out bằng sub-agent host (Kiro/Claude Code, KiroCrew `spawn_run`) ghi cùng định dạng answers để tally chung: không phải hạ cấp, là tránh trả tiền hai lần. |
| Q32 | Đồng ý | Ghi rõ trong README: chat bot không có filesystem (grok.com, Slack thuần) ngoài v1; "Grok" = Grok Build. |
| Q33 | Đồng ý có điều kiện | Bỏ hẳn "sampling để sau". Không dựa vào `response_format`/`seed`/`temperature`; tài liệu hoá khác biệt Anthropic/Gemini/xAI; Gemini CLI xoá biến `*KEY*`; xAI xem chat completions là legacy. |
| Q34 | Đồng ý có điều kiện | KiroCrew thêm được qua dashboard. Thay Gemini CLI bằng Antigravity CLI. Cân nhắc `founder-vn install-skills` để người hỗ trợ chỉ cần một toolchain. |
| Q35 | Phản đối một phần | +2 tuần đủ cho server nhưng mốc tuần 6 (server + 6 skill có case thật + 5 kế hoạch người thật) quá dày. Dời ma trận 6 host sau pilot; giữ 14 tuần chỉ khi làm toàn thời gian. |
| Q36 | Phản đối | Pipeline đầy đủ trên 6 host tốn 3–5 ngày và kết quả panel không so được vì model khác. Thay bằng test tương thích tất định (mỗi tool gọi 1 lần, CLI + MCP) trên 6 host; pipeline đầy đủ chỉ Kiro + Claude Code + Codex (host khắt khe nhất về timeout). |

**5 rủi ro lớn nhất**
1. Tuyển và đo 20 người thật: tiêu chí thành công nằm ngoài tầm kiểm soát của code và dễ thiên lệch.
2. Pháp lý `founder-permits`: nguồn khó fetch, luật đổi hai lần trong 13 tháng, tìm kiếm tiếng Việt kém, dẫn tới lời khuyên sai cho người sắp bỏ tiền.
3. Quá tải 14 tuần với 1 người: 12 skill + server + pilot + 6 host.
4. Fan-out trong server mong manh giữa host: timeout, khoá API, khác biệt provider, kết quả không so được.
5. Dữ liệu cá nhân người pilot và tool MCP ghi file: thiếu đồng thuận, lưu trữ, khoá đường dẫn.

**7 câu hỏi còn phải hỏi**
1. "Grok bot, KiroCrew bot" là agent chạy trên máy có filesystem hay chat bot thuần? Nếu là chat bot, Q32 mâu thuẫn với yêu cầu "mọi bot".
2. Ai trả và giữ API key của server trong và sau pilot; provider/model nào là tham chiếu cho kết quả panel?
3. Trên Kiro/Claude Code/KiroCrew có được dùng sub-agent host (đã trong thuê bao) thay cho server không, hay bắt buộc một đường mã?
4. Người pilot ký đồng thuận gì (Luật 91/2025) về gửi số liệu lên API bên thứ ba và công bố ẩn danh; ai giữ dữ liệu, bao lâu?
5. Baseline quyết định ghi thế nào ở intake, ai gửi khảo sát Zalo, và "đổi quyết định" định nghĩa cụ thể ra sao?
6. Mô hình CFO có thêm thuế theo doanh thu của hộ kinh doanh và giá gồm VAT không, nghĩa là đổi công thức chứ không chỉ ký hiệu?
7. Nguồn pháp lý nào là chính thức (vbpl.vn, chinhphu.vn, dichvucong, Cục Thuế), và skill làm gì khi không fetch được: từ chối, hay dùng ngày kiểm chứng trong repo?
