# Quy Tắc Dự Án VibeCoding - GOLD STANDARD (29 Skills + Antigravity)

> **"Contract LOCKED = License to Build | 29 Skills Active | Antigravity Integrated"**

---

## Triết Lý Tích Hợp

**Agent-First Philosophy:** Agent là lực lượng thực thi chính, con người đóng vai trò Kiến trúc sư và Điều phối viên.
**Artifact-First Development:** Mọi task phức tạp phải tạo artifact trước khi code.

---

## Các Giai Đoạn (Phases)

| Phase | Tên | Commands |
|-------|-----|----------|
| **A** | Planning | `init`, `start`, `status`, `lock`, `doctor` |
| **B** | Execution | `plan`, `build`, `review`, `snapshot` |
| **C** | Configuration | `config` |
| **E** | Magic Mode | `go` |
| **F** | Agent Mode | `agent` |
| **G** | Debug Mode | `debug`, `assist` |
| **H** | Smart Defaults | `wizard`, `undo`, `learn` |
| **I** | Git Integration | `git`, `watch`, `shell` |
| **K** | Maximize AI | `test`, `docs`, `refactor`, `security`, `ask`, `migrate` |
| **L** | Antigravity | `antigravity-tool`, `antigravity-context`, `antigravity-swarm` |

---

## Máy Trạng Thái (State Machine)

```
STATES = {
  // Phase A: Planning
  INIT                   -> INTAKE_CAPTURED
  INTAKE_CAPTURED        -> BLUEPRINT_DRAFTED
  BLUEPRINT_DRAFTED      -> CONTRACT_DRAFTED | INTAKE_CAPTURED
  CONTRACT_DRAFTED       -> CONTRACT_LOCKED | BLUEPRINT_DRAFTED
  
  // Phase B: Execution
  CONTRACT_LOCKED        -> PLAN_CREATED
  PLAN_CREATED           -> BUILD_IN_PROGRESS
  BUILD_IN_PROGRESS      -> BUILD_DONE
  BUILD_DONE             -> REVIEW_PASSED | REVIEW_FAILED
  REVIEW_PASSED          -> SHIPPED
  REVIEW_FAILED          -> BUILD_IN_PROGRESS | PLAN_CREATED
}
```

---

## ANTIGRAVITY INTEGRATION

> **Tự động áp dụng khi workspace có `.antigravity/` directory**

### Cấu Trúc Thư Mục Antigravity (Extended)

```
project/
 .agent/
    workflows/
    skills/             # <--- Correct Location for Antigravity Skills
 .antigravity/rules.md
 .context/               # Auto-injected knowledge
 .vibecode/
 artifacts/              # Antigravity outputs
    plans/
    logs/
    evidence/
 mission.md
 mcp_servers.json
```

### Artifact Protocol (MUST FOLLOW)

1. **Planning Phase**:
   - Create `artifacts/plan_[task_id].md` TRƯỚC KHI code.
   - Read `mission.md` để hiểu high-level goals.

2. **Execution Phase**:
   - Save test logs to `artifacts/logs/`.

3. **Visual Changes**:
   - Screenshots PHẢI vào `artifacts/`.

---

## Quy Trình Debug 4 Giai Đoạn

1. **EVIDENCE**: Thu thập logs, ảnh chụp, tái hiện lỗi.
2. **ANALYZE (RCA)**: Phân tích nguyên nhân gốc rễ.
3. **FIX**: Triển khai bản sửa lỗi tinh gọn nhất.
4. **VERIFY & PREVENT**: Chạy lại test và viết Rule chống lặp lại.

---

**Version**: 4.0.0 (Gold Standard + Antigravity Full Integration)  
**Last updated**: 2026-01-14
