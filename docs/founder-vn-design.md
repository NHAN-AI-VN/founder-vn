# founder-vn: bản thiết kế (hiểu biết chung)

Kết quả phiên grill ngày 21/11/2026, 7 vòng, 49 câu hỏi, một lượt phản biện độc lập
(xem `docs/review-round5.md`). Tài liệu này ghi lại những gì đã được chủ dự án xác nhận;
chưa có dòng mã nào được viết. Bước tiếp theo dự kiến: `/to-spec`, rồi `/to-tickets` cho đợt A.

## 0. Bối cảnh thực tế đã khảo sát

Workspace `Research/HDDH` chứa ba nhóm skill:

- **27 skill engineering/productivity của mattpocock** (symlink từ `.agents/skills`, khóa trong
  `skills-lock.json`): công cụ để *phát triển* phần mềm (grill, tdd, to-spec, implement...).
  Không đưa vào sản phẩm.
- **11 skill `founder-*`** (Jake Schincariol, MIT, nguồn `github.com/Jakeschincariol/founder-skill`,
  ~2.400 dòng, 4 script Python chuẩn-thư-viện): tài sản cốt lõi. Pipeline cố định
  `board → competitors → consumer → pricing → offer → cfo → marketing → brand → ops → launch → plan`,
  trạng thái trong thư mục `founder/`, không có orchestrator. Toàn bộ tiếng Anh, `$` hardcode trong
  4 script, ví dụ ở Toronto, mô hình "thuế bán hàng cộng thêm", đăng ký nhãn hiệu chỉ liệt kê
  USPTO/CIPO/EUIPO/UKIPO. `founder-consumer` gọi 100 sub-agent/lần; `founder-board` gọi 3.
- **11 skill analyst của ID8Labs** (~5.200 dòng, nguồn `jmsktm/claude-settings`): thuần phương pháp,
  không script, không ghi file, nguồn dữ liệu Mỹ (SEC EDGAR, Census Bureau), tham chiếu Firecrawl MCP
  chưa cài. **Không có trường license và không có file LICENSE** → không tái phân phối.

Không có một dòng nào về Việt Nam, VND, Zalo, hộ kinh doanh hay thuế. Chưa có `founder/` nào được
sinh ra, chưa có docs, chưa có git.

Lỗi bản địa hóa có sẵn trong code (phản biện phát hiện): `van_westendorp._f` xóa dấu phẩy rồi ép
float nên `"35.000"` → `35.0`; `panel.deal` làm tròn thu nhập đến 1.000; `compile.py` nạp
`unit_economics.py` qua đường dẫn tương đối `../founder-cfo/`; `price` upstream là *trước thuế*
trong khi hộ kinh doanh nộp GTGT + TNCN theo tỷ lệ % trên doanh thu; `compile.py` cho panel mô
phỏng gác cổng verdict (buy-rate ≥ 25%).

Sự thật về host (có nguồn trong `docs/review-round5.md`):

- Agent Skills là chuẩn trung lập dưới Agentic AI Foundation / Linux Foundation từ 22/10/2026;
  Kiro, Claude Code, Codex, Cursor, Gemini CLI, Grok Build, KiroCrew đều đọc SKILL.md và đều có
  `mcpServers` (stdio).
- Codex timeout tool mặc định 60 giây; Gemini CLI xóa biến môi trường tên có `KEY`/`SECRET` khi
  khởi chạy MCP server trừ khi khai báo tường minh trong `env`; KiroCrew không đọc `mcp.json` của
  workspace (thêm server qua dashboard) nhưng **có** fan-out qua tool `spawn_run`.
- MCP sampling đã bị khai tử trong giao thức bản 2026-07-28 (SEP-2577).
- Endpoint OpenAI-compatible: Anthropic coi là lớp thử nghiệm (bỏ `seed`, chặn `temperature` < 1
  trên Claude 4.7+); xAI xếp chat completions là legacy; Gemini dùng được.
- `npx skills add` cài theo agent: Kiro `.kiro/skills/`, Grok `.grok/skills/`, Codex/Gemini/Cursor
  `.agents/skills/`. KiroCrew đọc `<project>/.kiro/skills/` khi dự án được trust.
- Nguồn pháp lý VN: thuvienphapluat trả 403 cho client không phải trình duyệt; gdt.gov.vn và
  dichvucong.gov.vn là vỏ JS; **vbpl.vn** và chinhphu.vn trả HTML đầy đủ. Nghị định 168/2025 về
  đăng ký kinh doanh (hiệu lực 1/7/2025) đã bị sửa bởi Nghị định 296/2026 (23/7/2026).

## 1. Mục tiêu và tiêu chí thành công

- Dự án **mã nguồn mở**, giấy phép MIT, repo GitHub `founder-vn`, public từ ngày đầu, công bố sau pilot.
- Người dùng v1: người sắp mở hoặc mở dưới 6 tháng một **hộ kinh doanh** ở Việt Nam (F&B, bán lẻ,
  dịch vụ nhỏ). Startup là track sau.
- Phạm vi v1: giai đoạn khởi sự (ý tưởng → kế hoạch có số → khai trương → 30 ngày đầu). Vận hành
  chỉ ở mức checklist kèm link nguồn chính thức, không tư vấn thuế chi tiết.
- Thành công = **20 người thật** (không phải bạn bè) đi hết luồng, **≥ 50% đổi một quyết định**
  (giá, địa điểm, vốn, mở/không mở) so với **baseline viết tay ở buổi intake**. 3 câu hỏi theo dõi
  đăng ký trước trong repo, do **một người khác** gửi qua Zalo sau 2 tuần. Báo cáo dạng mô tả,
  không diễn giải thống kê (n = 20 ở ngưỡng 50% có khoảng tin cậy ±22 điểm).
- Không đạt → sửa luồng, không thêm skill.

## 2. Kiến trúc

- **Đơn vị kiến thức**: SKILL.md theo chuẩn Agent Skills. 11 skill founder viết lại +
  `founder-permits` mới. Bỏ 11 skill ID8Labs; không đưa skill dev của mattpocock vào sản phẩm.
- **Package Python `founder_vn`**: toàn bộ phép tính (unit economics có thuế theo doanh thu,
  Van Westendorp, panel, compile) trong một package; xuất **cả CLI `founder-vn` và MCP server stdio
  `founder-vn-mcp`** bọc *cùng* hàm, đầu ra giống hệt từng byte. Skill gọi MCP nếu host đã cấu hình,
  không thì chạy CLI qua shell. Hai đường vận chuyển, một kết quả: không có hạ cấp.
- **Fan-out trong server**: `panel_run` và `board_run` là job bất đồng bộ (`job_id` + `job_status`,
  một tool poll chung cho mọi loại job, Q50; answers ghi dần; chia lại khi `answers/` còn câu trả lời của
  một lần chia khác thì bị từ chối, chia lại y hệt thì qua, Q58) để vượt timeout 60 giây của Codex.
  Server gọi mô hình cấu hình qua env
  `FOUNDER_LLM_BASE_URL` / `FOUNDER_LLM_API_KEY` / `FOUNDER_LLM_MODEL`, một client OpenAI-compatible,
  tự parse JSON (không dựa vào `response_format`/`seed`/`temperature`), ghi `model` và hash prompt
  vào `panel.json`. Chưa cấu hình thì tool báo lỗi kèm hướng dẫn, không âm thầm dùng mặc định.
  Không dùng MCP sampling. Đường "dùng sub-agent của host" là v1.1.
- **Trạng thái**: file `founder/` trong workspace (server cùng máy). Tool nhận đường dẫn phải khóa
  trong gốc `founder/`: từ chối `..`, đường dẫn tuyệt đối ngoài gốc, symlink; chỉ ghi `.md`/`.json`;
  không xóa. Chat bot không có filesystem (grok.com, Slack thuần) nằm ngoài v1; "Grok bot" nghĩa là
  Grok Build CLI.
- Skill và package **cùng số phiên bản** (`metadata.version` = phiên bản package); skill gọi
  `founder-vn --version` hoặc tool `server_info` và dừng cảnh báo nếu lệch major.
- Không UI, không dịch vụ hosted trong v1.

## 3. Bản địa hóa: viết lại, không dịch

Mỗi skill được viết lại theo bối cảnh Việt Nam và kiểm chứng trên một case thật trước khi coi là xong.

- VND định dạng Việt (`35.000 đ`), parser số kiểu Việt (`35k`, `35 nghìn`, `1,2 triệu`), thu nhập
  **theo tháng**, `price` là giá khách trả. `numbers.json` thêm `tax_rate_on_revenue` (tỷ lệ % GTGT +
  TNCN theo ngành) và `tax_free_threshold` (ngưỡng doanh thu miễn thuế năm). Lợi nhuận = doanh thu −
  chi phí biến đổi − chi phí cố định − thuế theo doanh thu. Tỷ lệ và ngưỡng **không hardcode**; skill
  tra theo luật hiện hành và ghi link.
- Verdict `Profitable / Not yet / Incomplete` tính từ số CFO thôi; panel in dòng riêng
  "tín hiệu cầu (mô phỏng, cận trên)", không tham gia verdict.
- Panel mặc định `--n 20` (100 là tùy chọn), tên Việt, hành vi mua kiểu Việt (quen quán, mua theo
  hội nhóm, săn voucher app), **BRIEF cho người mua mô phỏng viết thẳng tiếng Việt**.
- `founder-competitors`: phiếu khảo sát thực địa (5–10 đối thủ trong bán kính, giá, lượng khách giờ
  cao điểm, ảnh menu) là đầu vào bắt buộc; web search chỉ bổ trợ. Skill in mẫu phiếu để chủ hộ mang đi.
- `founder-board`: lens Offers ($100M Offers) + Product (Isaacson) + **Systems (The E-Myth Revisited)**
  thay lens Monopoly (Thiel). Giữ quy tắc upstream: chỉ áp dụng framework đã xuất bản, không nói thay tác giả.
- `founder-permits` (mới): sở hữu đăng ký hộ kinh doanh, giấy phép ATTP, nghĩa vụ thuế và hóa đơn
  sau khai trương. F&B viết đầy đủ; bán lẻ và dịch vụ nhỏ dùng đường chung kèm dòng "ngành có điều
  kiện: tra tại đây". Cấu trúc checklist tĩnh (bước, cơ quan, hồ sơ); mọi con số và mốc thời gian
  phải có link và ngày kiểm chứng. Nguồn ưu tiên **vbpl.vn** và chinhphu.vn. Repo kèm
  `permits/sources.md` lưu trích đoạn đã kiểm chứng + ngày + link. Khi chạy, skill fetch lại để xác
  nhận; fetch hỏng → dùng bản lưu và ghi rõ "kiểm chứng ngày X, chưa xác nhận lại hôm nay";
  **không bao giờ đoán con số**. `founder-ops` giữ nhà cung cấp, nhân sự, quy trình, rủi ro và trỏ sang permits.
- Kênh: Zalo OA, Facebook, ShopeeFood/GrabFood thay Instagram/Yelp; Cục Sở hữu trí tuệ thay USPTO;
  đăng ký tại UBND cấp xã; ví dụ Việt Nam.
- Kiến thức thị trường **viết thẳng vào từng skill**; không tách "gói thị trường". Thị trường khác thì fork.
- Giữ mọi câu miễn trừ trách nhiệm và cảnh báo "panel là mô phỏng, không phải khách hàng" của upstream.

## 4. Ngôn ngữ

| Lớp | Ngôn ngữ |
|---|---|
| Định danh: tên skill `founder-*`, lệnh `/founder-cfo`, tên file `founder/cfo.md`, khóa JSON | Tiếng Anh |
| Hướng dẫn mô hình trong SKILL.md | Tiếng Anh; `description` kèm cụm kích hoạt tiếng Việt ("có nên mở quán", "cần bao nhiêu vốn") |
| README, CONTRIBUTING, docs | Tiếng Anh, có một mục tiếng Việt |
| Đầu ra cho chủ hộ, `examples/`, BRIEF người mua | Theo ngôn ngữ người dùng, mặc định tiếng Việt, xưng "anh/chị" |

README nhắm **người hỗ trợ** (tư vấn viên, nhân viên vườn ươm, người thân biết công nghệ) vận hành
cho chủ hộ; chủ hộ tự chạy CLI không phải đối tượng v1.

## 5. Phân phối, repo, kiểm chứng, quản trị

- Cài skill: `npx skills add <owner>/founder-vn` (dev) hoặc `founder-vn install --host
  kiro|claude|codex|grok|kirocrew` (người hỗ trợ chỉ cần Python/uv): sao chép skill vào đúng thư mục,
  ghi sổ nguồn `permits/sources.md` của gói vào dự án (Q57) và đăng ký MCP (Q54): host có file đăng ký trong dự án (Kiro `.kiro/settings/mcp.json`, Claude Code
  `.mcp.json`, Codex `.codex/config.toml`, Grok `.grok/config.toml`) thì ghi file đó khi chưa có và chỉ in đoạn
  cấu hình khi đã có; KiroCrew chỉ in. Server trên PyPI, chạy `uvx --from founder-vn founder-vn-mcp` (`uvx <lệnh>` cài gói tên `<lệnh>`
  nếu không có `--from`, Q53). `docs/hosts/<host>.md` có
  đoạn cấu hình cho từng host; KiroCrew thêm qua dashboard; "Gemini CLI / Antigravity CLI" cần xác
  nhận khi cài. Kiro Power / Claude Code plugin để sau pilot.
- Bố cục repo: `skills/founder-*/SKILL.md`, `src/founder_vn/`, `permits/sources.md`,
  `examples/<case-mẫu>/founder/`, `pilot/` (phiếu đồng thuận, mẫu baseline, 3 câu hỏi đăng ký trước,
  bảng kết quả ẩn danh), `docs/hosts/`. CI: pytest + ruff + build mỗi push; PyPI trusted publishing
  khi gắn tag. Phụ thuộc tối thiểu `mcp`, `httpx`; Python ≥ 3.11.
- Định nghĩa "xong" một skill: (1) chạy trọn trên case mẫu, sinh đúng file đầu ra; (2) test đơn vị
  cho package (định dạng VND, parser số Việt, thu nhập theo tháng, Van Westendorp ở độ lớn VND, thuế
  theo doanh thu); (3) checklist rà soát: không còn `$`, không lọt tiếng Anh trong đầu ra, mọi khẳng
  định pháp lý/số liệu có link, có miễn trừ trách nhiệm, có cảnh báo panel mô phỏng.
- Kiểm chứng host hai mức: **test tương thích tất định** (mỗi tool gọi một lần qua MCP và CLI, so
  golden file, ~1 giờ/host) trên 6 host (Kiro CLI, Claude Code, Codex, Gemini/Antigravity CLI,
  Grok Build, KiroCrew); **pipeline đầy đủ** trên case mẫu chỉ ở Kiro CLI, Claude Code, Codex.
  Bảng kết quả trong README. Làm sau pilot; kiểm chứng liên tục khi đổi mã chỉ trên Kiro + Claude Code.
- Upstream: ghi công đầy đủ trong README và frontmatter; mở một issue giới thiệu founder-vn và báo
  các lỗi i18n đã gặp. Không PR lớn.
- Quản trị tối thiểu: CONTRIBUTING với quy tắc cứng "mọi khẳng định pháp lý cần link chính thức +
  ngày kiểm chứng"; mẫu issue "luật đã đổi".
- Công cụ phát triển: bộ skill mattpocock trong workspace (`tdd`, `code-review`, `to-spec`,
  `to-tickets`...).

## 6. Pilot

- Tuyển từ mạng quan hệ + 1–2 nhóm Facebook chủ quán/chủ shop, miễn phí, điều kiện: đang định mở
  hoặc mở dưới 6 tháng. **Bắt đầu tuyển từ tuần 1** (nút thắt lớn nhất, không phụ thuộc code).
  Địa bàn không ràng buộc; buổi gặp trực tiếp hoặc qua Zalo.
- Hai lần gặp: **Lần 1** (30 phút) lấy ý tưởng, số liệu, ghi **baseline bằng văn bản** (giá dự định,
  địa điểm, vốn, mở/không mở), ký phiếu đồng thuận, giao phiếu khảo sát thực địa. **Ở giữa**: người
  hỗ trợ chạy 6 skill đợt A, mỗi người một thư mục riêng ngoài git. **Lần 2** (45–60 phút) đi qua
  `business-plan.md`, ghi phản ứng và quyết định dự định; gửi PDF qua Zalo. **+2 tuần**: 3 câu hỏi
  đăng ký trước, người khác gửi.
- "Đổi quyết định" = một trong bốn mục baseline khác đi so với văn bản intake.
- Dữ liệu (Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15): phiếu đồng thuận nêu rõ dữ liệu đi qua API bên
  thứ ba và công bố ẩn danh; thư mục từng người xóa sau 90 ngày trừ khi họ đồng ý giữ; chỉ công bố
  số liệu tổng hợp trong `pilot/`.
- API key của chủ dự án trong pilot; sau đó mỗi người hỗ trợ mang key riêng. Tuần 2 bake-off 3 mô
  hình rẻ trên 5 persona, chọn mô hình có giọng người mua Việt tự nhiên nhất làm tham chiếu, ghi tên
  vào mọi `results.json`.

## 7. Thứ tự và lộ trình: 14 tuần, một người toàn thời gian

Đợt A: `board, competitors, consumer, pricing, cfo, plan`. Đợt B: `permits, ops, marketing, launch`.
Sau pilot: `offer, brand`.

| Tuần | Việc |
|---|---|
| 1 | Repo public, chốt case mẫu (barbershop của chủ dự án, Q51; trước đó dự định F&B của một người quen sắp mở quán), phiếu đồng thuận + mẫu baseline + 3 câu hỏi đăng ký trước, bắt đầu tuyển pilot |
| 2 | Package `founder_vn`: gom 4 script, CLI, thuế theo doanh thu, định dạng/parser VND, test đơn vị; bake-off mô hình |
| 3 | MCP server, job panel bất đồng bộ, khóa đường dẫn, test, bản PyPI đầu |
| 4–6 | Đợt A trên case mẫu; `install --host`. **Mốc tuần 6: server chạy + 6 skill + 2 bản kế hoạch của người thật** |
| 7–9 | Đợt B; pilot người 3–12 |
| 10–11 | Pilot người 13–20 (buổi cuối trước hết tuần 11 để đo sau 2 tuần) |
| 12–13 | Theo dõi +2 tuần, bảng kết quả, test tương thích 6 host, pipeline đầy đủ 3 host |
| 14 | Công bố, issue upstream, dự phòng |

Ước lượng 45–55 ngày công (phản biện): 12 skill × 1,5–2 ngày có case thật = 18–24; package + server
+ client + test + PyPI 7–9; 6 host 3–5; 20 pilot × ~4 giờ ≈ 10 chưa kể tuyển. 14 tuần cho ~3 tuần
dự phòng.

## 8. Rủi ro hàng đầu và cách đã chốt

1. **Tuyển và đo 20 người thật**: tuyển từ tuần 1; baseline viết tay; câu hỏi đăng ký trước; người khác gửi.
2. **Pháp lý sai cho người sắp bỏ tiền**: vbpl.vn/chinhphu.vn, `permits/sources.md` có ngày, không đoán, miễn trừ trách nhiệm, mẫu issue "luật đã đổi".
3. **Quá tải một người**: đợt A trước; offer/brand và ma trận host sau pilot; mốc tuần 6 chỉ 2 kế hoạch người thật.
4. **Fan-out mong manh giữa host**: job bất đồng bộ; một mô hình cho panel trên mọi host; ghi model + hash prompt.
5. **Dữ liệu người pilot và tool ghi file**: phiếu đồng thuận; 90 ngày; khóa đường dẫn trong `founder/`.

## 9. Để sau (đã nêu tên, chưa làm)

UI/runtime tự xây; bot không filesystem (server sở hữu trạng thái theo `project_id`); đường fan-out
bằng sub-agent của host (v1.1); `founder-offer`, `founder-brand`; đường F&B đầy đủ của `founder-permits` (Q56); track startup và lens Monopoly;
Kiro Power / Claude Code plugin; máy tính web tĩnh dùng chung công thức; mô hình tài chính bền vững
cho dự án OSS (chưa bàn, không cần cho v1).

## Phụ lục: nhật ký quyết định (Q1–Q59)

Vòng 1

- Q1 Bản chất dự án → (d) mã nguồn mở.
- Q2 Phân khúc v1 → hộ kinh doanh (F&B, bán lẻ, dịch vụ nhỏ); startup là track sau.
- Q3 Giai đoạn → khởi sự; vận hành chỉ checklist + link.
- Q4 Nguồn lực → 1 người có coding agent, API vài triệu đồng/tháng, 8–12 tuần (sửa thành 14 ở Q35/Q43).
- Q5 Tiêu chí → 20 người thật, 50% đổi một quyết định.
- Q6 Đơn vị kiến thức SKILL.md + runtime mỏng (sửa ở Q8, rồi Q30).
- Q7 Bản địa hóa = viết lại, kiểm chứng bằng case thật.

Vòng 2

- Q8 Không runtime/UI; pilot có người điều phối trên Kiro CLI (sửa ở Q30: có tool server local).
- Q9 Repo mới MIT, 11 founder + 1 permits; bỏ ID8Labs và mattpocock khỏi sản phẩm; PR upstream nhỏ (sửa ở Q46).
- Q10 Phân phối qua `npx skills add`.
- Q11 SKILL.md tiếng Việt (đảo ở Q24).
- Q12 Đợt A/B; offer, brand sau pilot.
- Q13 Tuyển qua mạng quan hệ + nhóm Facebook; đo sau 2 tuần qua Zalo; bảng kết quả ẩn danh (bổ sung ở Q40, Q41).
- Q14 Panel mặc định 20; thu nhập theo tháng bằng VND; tên Việt.
- Q15 Khảo sát thực địa là đầu vào bắt buộc.

Vòng 3

- Q16 Tương thích host → yêu cầu tổng quát cho mọi agent phổ biến và bot (Grok, KiroCrew) → dẫn tới Q25–Q36.
- Q17 Định danh tiếng Anh, nội dung tiếng Anh (làm rõ ở Q24).
- Q18 Chính sách tươi mới pháp lý: lai (cấu trúc tĩnh, số liệu tra khi chạy, link bắt buộc) (chi tiết ở Q39).
- Q19 Tên `founder-vn`.
- Q20 Định nghĩa "xong": case mẫu + test script + checklist rà soát.
- Q21 Một case mẫu F&B dùng chung, ẩn danh vào `examples/` (ngành đổi sang barbershop ở Q51).
- Q22 Pilot hai lần gặp.
- Q23 Public từ ngày đầu; README nhắm người hỗ trợ; xưng anh/chị; CONTRIBUTING + mẫu issue.

Vòng 4

- Q24 Bốn lớp ngôn ngữ: định danh, hướng dẫn, README tiếng Anh; đầu ra và examples theo người dùng, mặc định tiếng Việt.
- Q25–Q28 Từ chối hạ cấp có kiểm soát: "cover đầy đủ, không hạ cấp".
- Q29 Kiến thức thị trường viết thẳng vào skill.

Vòng 5 → phản biện độc lập → Vòng 6 (sửa theo phản biện)

- Q30 Một package xuất cả CLI và MCP; khóa đường dẫn.
- Q31 Fan-out trong server dạng job bất đồng bộ; ghi model + hash prompt; sub-agent host là v1.1 (tên tool poll sửa ở Q50).
- Q32 File trong workspace; "Grok bot" = Grok Build CLI; chat bot không file ngoài v1.
- Q33 Client OpenAI-compatible qua env; tài liệu hóa khác biệt provider; không sampling.
- Q34 `founder-vn install --host`; PyPI/uvx; KiroCrew qua dashboard; Gemini/Antigravity cần xác nhận.
- Q35 14 tuần; ma trận host sau pilot; mốc tuần 6 hạ còn 2 kế hoạch người thật (nhánh toàn/bán thời gian → Q43).
- Q36 Test tương thích tất định trên 6 host; pipeline đầy đủ trên 3 host.
- Q37 Mô hình CFO thêm thuế theo doanh thu và ngưỡng miễn thuế; giá là giá khách trả.
- Q38 Panel không gác cổng verdict.
- Q39 Nguồn vbpl.vn/chinhphu.vn; `permits/sources.md`; fetch hỏng dùng bản lưu có ngày; không đoán.
- Q40 Baseline viết tay; câu hỏi đăng ký trước; người khác gửi; báo cáo mô tả.
- Q41 Phiếu đồng thuận; xóa sau 90 ngày; chỉ công bố tổng hợp.
- Q42 API key của chủ dự án trong pilot; bake-off 3 mô hình tuần 2.

Vòng 7

- Q43 Toàn thời gian → 14 tuần.
- Q44 Một repo; bố cục; CI pytest + ruff + build; PyPI trusted publishing; deps `mcp`, `httpx`; Python ≥ 3.11.
- Q45 Skill và package cùng phiên bản; cảnh báo khi lệch major.
- Q46 Upstream: ghi công + issue, không PR lớn.
- Q47 `founder-permits`: F&B đầy đủ, ngành khác đường chung.
- Q48 Lens Systems (E-Myth) thay Monopoly.
- Q49 BRIEF người mua mô phỏng bằng tiếng Việt.

Vòng 8 (sau spec và mã; từng mục ghi ngày và chỗ phát sinh)

- Q50 (2026-11-23, review Standards của lane #11, S1) Tool poll của job là `job_status`, dùng chung cho
  `panel_run` và `board_run`; không có `panel_status`. Spec #1 (bảng CLI↔MCP: `panel status` /
  `job_status`; mục job; mục test LLM boundary) và ticket T08, T12, T15 đều đặt tên này vì hai loại
  job chạy trên cùng một runner (T08) và một tool poll chung đơn giản hơn hai tool theo loại. §2 sửa
  theo; `docs/review-round5.md` giữ nguyên vì là biên bản phản biện có ngày, không phải nguồn luật.
- Q51 (2026-11-23, lane #5 T04, quyết định của chủ dự án) Case mẫu đổi từ F&B sang **tiệm cắt tóc nam
  kiểu barbershop** (sửa Q21 và dòng tuần 1 của §7): tiệm đầu tiên 4 ghế cắt + 2 giường gội, 55–60 m²,
  tại Quận 7 cũ, TP.HCM, đăng ký hộ kinh doanh, lấy từ nghiên cứu thị trường riêng
  của chủ dự án (concept chưa quyết mở: đúng tình huống "có nên mở, cần bao nhiêu vốn" của người dùng
  v1). Lý do: chưa chốt được quán F&B thật nào trong khi T11–T17 đứng chờ ticket này (H-7 trong
  `docs/agents/kiro-harness.md`); chủ case là chính chủ dự án nên đồng thuận công bố ẩn danh không
  phụ thuộc người thứ ba; dữ liệu đủ cho đợt A. Hệ quả: (1) mục sổ nguồn đầu tiên của T11 là thuế
  suất theo doanh thu của ngành dịch vụ, không phải ăn uống; (2) đường F&B đầy đủ của `founder-permits`
  (Q47) không được case mẫu chạy qua, đợt B cần một case F&B phụ hoặc đổi ưu tiên, và Q56 chọn đổi ưu tiên;
  (3) ticket T13 nói "ảnh menu", với barbershop đọc là ảnh bảng giá; (4) tên gọi của case là tên tạm
  mô tả, không phải thương hiệu thật nào, kể cả thương hiệu tham chiếu của nghiên cứu; vị trí ghi tới
  cấp quận cũ. Spec #1 (user story 48) và ticket #5 sửa cùng ngày; ví dụ ở `examples/barbershop/`.
- Q52 (2026-11-23, lane #12 T11, quyết định của operator) Giữ mô hình thuế gộp của Q37: một
  `tax_rate_on_revenue` (GTGT cộng TNCN, giá trị 7 cho "cắt tóc, làm đầu, gội đầu") áp lên toàn bộ
  doanh thu năm khi doanh thu năm vượt `tax_free_threshold` (1.000.000.000 đ mỗi năm; nguồn trong
  `permits/sources.md`). Luật tính GTGT 5% trên toàn bộ doanh thu nhưng TNCN 2% chỉ trên phần vượt
  ngưỡng, nên mô hình tính thừa tối đa 20 triệu đồng mỗi năm, theo hướng an toàn. Giới hạn thứ hai:
  trên 3 tỷ đồng doanh thu năm TNCN tính trên thu nhập với thuế suất 17%, chưa có cờ máy. Hệ quả:
  (1) `cfo.md` của skill `founder-cfo` nêu cả hai giới hạn bằng chữ, kèm một dòng "có ưu đãi tạm
  thời, chưa tính" không có con số, vì `src/founder_vn/cfo.py` (T05) không đổi trong T11 nên phần
  này do skill nối vào cuối `cfo.md`; (2) tách `tax_rate_on_revenue` thành hai tỷ lệ với hai căn cứ
  tính, thêm cờ mốc 3 tỷ đồng và đưa phần giới hạn vào báo cáo của công cụ là một ticket mới sau T11.
- Q53 (2026-11-24, quyết định của operator, sau khi #19 BLOCKED) Server MCP khởi động bằng
  `uvx --from founder-vn founder-vn-mcp`, không phải `uvx founder-vn-mcp`. Lý do: `uvx` suy gói từ tên
  lệnh nếu `--from` không nêu gói, mà console script `founder-vn-mcp` nằm trong gói `founder-vn`. Đã đo
  2026-11-24 với uv 0.11.24: `uvx founder-vn-mcp` báo "founder-vn-mcp was not found in the package
  registry" (và sẽ báo y như vậy sau khi phát hành, vì không có gói tên đó);
  `uvx --from ./dist/founder_vn-0.1.0-py3-none-any.whl founder-vn --version` in `founder-vn 0.1.0`.
  Bản 0.1.0 chưa bao giờ lên PyPI; 0.2.0 là bản PyPI đầu tiên. Sửa §5, `src/founder_vn/install.py`,
  `docs/hosts/` và README cùng thay đổi.
- Q54 (2026-11-25, quyết định của operator, từ #94) Với host Kiro, `founder-vn install` ghi
  `.kiro/settings/mcp.json` kèm mục server `founder-vn` khi file chưa tồn tại; khi file đã có, chỉ in đoạn
  cấu hình và không ghi (không bao giờ gộp vào file có sẵn, không bao giờ xoá). Cùng quy tắc cho các host có
  file đăng ký nằm trong dự án: Claude Code `.mcp.json`, Codex `.codex/config.toml`, Grok `.grok/config.toml`
  (đối chiếu tài liệu chính thức 2026-11-25: Codex đọc `.codex/config.toml` của dự án tin cậy; Grok Build đọc
  `[mcp_servers]` từ `.grok/config.toml` của repo). KiroCrew giữ chế độ chỉ in (đăng ký qua dashboard).
  `--print-only` vẫn không ghi gì. File ghi ra bị khoá trong gốc dự án như mọi lần ghi khác (§2): đích
  thoát khỏi dự án qua `..` hay symlink thì từ chối trước khi chép bất cứ gì. Lý do: trên máy sạch, đây là
  bước duy nhất của cài đặt không phải dán một lệnh (#19). Sửa §5, `src/founder_vn/install.py`,
  `tests/golden/install_*.json` (kế hoạch nay liệt kê file đăng ký) và `docs/hosts/` cùng thay đổi; trang
  Codex và Grok trước đó ghi file ở thư mục home, nay ghi file của dự án.
- Q55 (2026-11-25, quyết định của operator, sau hai lượt review độc lập bản chia đợt B, từ #111) Kế hoạch
  kinh doanh có mục `Giấy phép và thuế`, lấy từ `founder/permits.md`, đặt ngay sau `Kinh tế đơn vị` (cfo)
  và trước `Tiếp thị`, theo câu pipeline của spec #1 ("… unit economics → business plan (đợt A), rồi
  permits, ops, marketing, launch") và §7 ("Đợt B: permits, ops, marketing, launch"). Phương án đặt sau
  `Vận hành` như danh sách artefact của spec #1 (`ops.md, permits.md, launch.md`) đã được cân nhắc và
  không chọn: Owner nên đọc luật yêu cầu gì trước khi đọc tiệm vận hành ra sao. Khoá `permits`, file
  `permits.md` (hợp đồng trạng thái của spec #1: artefact giữ tên của upstream). `offer` và `brand` vẫn
  nằm trong `plan.SECTIONS` (sau pilot, Q12), nên kế hoạch biên dịch khi chưa có hai skill ấy luôn còn hai
  dòng "Chưa làm". Kế hoạch gọi skill của một mục là "chưa có trong bản này" khi gói không đem skill ấy (Q59), và đánh
  dấu mục Owner tự đưa vào là chưa qua rà soát. Sửa `src/founder_vn/plan.py` (và chú thích trên `SECTIONS`, trước đó ghi sai "design §2"),
  `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/business-plan.md` và `tests/golden/plan_*.json`
  cùng thay đổi.
- Q56 (2026-11-25, quyết định của operator, từ #111) Đường F&B đầy đủ của `founder-permits` (chứng nhận an
  toàn thực phẩm, thuế suất F&B; Q47) hoãn tới khi có người pilot F&B đã đồng thuận. Không thêm case mẫu F&B
  phụ tổng hợp: user story 48 của spec #1 và §5 giữ một case mẫu ẩn danh duy nhất, và Q7 đòi kiểm chứng trên
  một case thật. Việc này chốt mục còn mở ở hệ quả (2) của Q51 theo hướng "đổi ưu tiên": đường chung ra
  trước. Sửa câu hệ quả của Q51 và danh sách "Để sau" ở §9 cùng thay đổi.
- Q57 (2026-11-27, quyết định của operator, từ #142) Gói phân phối sổ nguồn: wheel mang `permits/sources.md`
  (hatch force-include vào `founder_vn/permits/sources.md`, cùng cơ chế với `skills/`), và bộ cài tìm nó theo hai
  đường như skill (bản trong gói khi cài từ wheel, nếu không thì `permits/` của repo). `founder-vn install --host
  <host>` ghi `<dự án>/permits/sources.md` cho mọi host của `install.SKILL_FOLDERS`, KiroCrew gồm cả (sổ nguồn là
  file của dự án, không phải file đăng ký), theo quy tắc của file skill chứ không theo quy tắc của file đăng ký:
  `create` khi chưa có, `update` khi file trong dự án khác bản trong gói (nội dung của gói thắng và kế hoạch nói
  rõ), `unchanged` khi giống hệt; không bao giờ xoá; `--print-only` không ghi gì; đích thoát khỏi dự án qua `..`
  hay symlink thì bị từ chối bằng `InstallRefused` và mã thoát 2 trước khi ghi bất cứ gì. Lý do: sổ nguồn là nội
  dung gói đã được review, thay đổi của nó (luật đổi, thêm mục đã kiểm chứng) phải tới dự án khi nâng cấp; một
  sổ chỉ ghi khi chưa có sẽ giữ im lặng số pháp lý cũ, tức rủi ro 2. Sửa tay trong sổ không phải mục đã kiểm
  chứng (đầu sổ; luật không đoán số của `founder-permits`), nên bộ cài ghi đè và báo `update`. Ba skill đọc sổ
  (`founder-permits` bước 2, `founder-cfo` bước 3, `founder-plan` bước tóm tắt) thêm một câu tiếng Anh hướng
  dẫn người hỗ trợ: sổ vắng thì chạy `founder-vn install --host <host>`, không điền số từ trí nhớ hay từ website;
  hành vi khi sổ vẫn vắng giữ nguyên. Sửa §5, `src/founder_vn/install.py`, `pyproject.toml`,
  `tests/golden/install_*.json` (kế hoạch nay liệt kê `permits/sources.md`), ba skill, `docs/agents/standards.md`,
  `docs/hosts/kiro.md`, `docs/hosts/README.md` và README cùng thay đổi. Bản 0.3.0 trên PyPI chưa có thay đổi này.
- Q58 (2026-11-27, quyết định của operator, từ #143) `panel init` từ chối chia lại không nhất quán: khi
  `founder/panel/answers/` có ít nhất một file, `init` so hash prompt của panel đang có trên đĩa (các thẻ trong
  `personas.json` và lời chào hàng trong `panel.json`) với hash prompt của lần chia sắp làm (thẻ từ hồ sơ khách,
  `n` và seed đã cho, cùng lời chào hàng đã cho). Hash bằng nhau là cùng một panel: `init` chạy như cũ (cùng
  file, cùng stdout). Hash khác, hoặc panel trên đĩa không đọc được (`panel.json` hay `personas.json` thiếu hoặc
  hỏng trong khi còn câu trả lời): `init` từ chối trước khi ghi bất cứ gì, bằng `PanelError` tiếng Việt nêu
  `founder/panel/answers/`, số câu trả lời, rằng công cụ không bao giờ xoá, và việc cần làm: cất panel cũ sang thư
  mục khác (ví dụ `founder/panel-lan-1/`) rồi chia lại. Hai đường vận chuyển cùng một văn bản: CLI in ra stderr với
  mã thoát 2, MCP `panel_init` trả lỗi tool. Skill `founder-consumer` bước 3 thêm một câu hướng dẫn xử lý lời từ
  chối này. Lý do: công cụ không bao giờ được đếm một câu trả lời dưới thẻ hay lời chào hàng mà nó không được hỏi
  (§2, Q31: hash prompt là nguồn gốc của một kết quả); điểm dừng giữ panel đầu của Owner để so sánh, với giá là
  một lần chuyển thư mục do con người làm. Phương án đóng dấu `prompt_hash` vào từng file trả lời đã cân nhắc và
  không chọn cho 0.3.1. Sửa §2, `src/founder_vn/panel.py`, `src/founder_vn/server.py` và
  `skills/founder-consumer/SKILL.md` cùng thay đổi.
- Q59 (2026-11-27, quyết định của operator, từ #144) Kế hoạch không bao giờ bảo Owner chạy một skill mà bản này
  không đem: "bản này có skill `founder-<skill>`" được suy ra, không ghi cứng, từ việc gói có thư mục skill ấy với
  `SKILL.md` (`install.packaged_skills_dir()`: `founder_vn/skills/` trong wheel, nếu không thì `skills/` của repo).
  `plan.SECTIONS` giữ thứ tự pipeline và hai hàng `offer`, `brand` (Q55). Mục thiếu mà bản này không đem skill thì
  dòng `Chưa làm` đọc ``- Đề xuất giá trị: để sau pilot, chưa có trong bản này (skill `founder-offer` sẽ tạo
  founder/offer.md).`` (cùng dạng cho `Thương hiệu` và `founder-brand`); mục thiếu mà skill có trong gói giữ dòng
  `chạy skill`. Mục có file mà bản này không đem skill thì vẫn được biên dịch, và dòng đầu dưới `## <tiêu đề>` là
  ``_Mục này lấy từ file founder/offer.md anh/chị cung cấp; bản này chưa có skill `founder-offer`, nên nội dung
  chưa qua rà soát của founder-vn._``; mục có skill trong gói biên dịch như cũ. Khi `founder-offer` và
  `founder-brand` được đem vào gói, văn bản kế hoạch tự đổi. `skills/founder-plan/SKILL.md` bước 1 đổi hai hàng
  bảng thành "để sau pilot, chưa có trong bản này" và thêm một câu: Owner hỏi mục đề xuất giá trị hay thương hiệu
  thì nói bằng tiếng Việt rằng hai skill ấy đến sau pilot và chưa có trong bản này, không tải, dịch hay tự dựng
  skill từ nơi khác (phiên #118 đã tải skill upstream tiếng Anh). Lý do: Owner không được bị bảo chạy một skill
  không tồn tại, và một kế hoạch phải nói mục nào đến từ skill founder-vn đã rà soát (§3) và mục nào không.
  Ngoài phạm vi: viết hay đem `founder-offer`, `founder-brand` (Q12), bỏ hay đổi thứ tự hai hàng trong
  `SECTIONS` (Q55), phát hiện ai viết một file mà skill của nó có trong gói. Sửa `src/founder_vn/plan.py`,
  `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/business-plan.md` (biên dịch lại bằng công cụ) và
  `tests/golden/plan_*.json` (hai dòng) cùng thay đổi. Dự án có sẵn `business-plan.md` sẽ cũ một lần:
  `founder-vn plan --check` thoát 1 tới khi biên dịch lại.
