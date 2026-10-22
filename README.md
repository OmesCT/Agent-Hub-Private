# Agent-Learning: Skills, Plugins, and Context Repository

คลังข้อมูลรวบรวมสกิล (Skills), ปลั๊กอิน (Plugins), บริบทการทำงานของ Agent จากโปรเจกต์ **FITs** และระบบ **Oh-My-ClaudeCode (OMC) / Oh-My-Antigravity (OMA)** เพื่อใช้ในการเรียนรู้และพัฒนาขีดความสามารถของ Antigravity AI Agent

---

## 1. โครงสร้างโฟลเดอร์ (Directory Structure)

```
Agent-Learning/
├── README.md                      # เอกสารคู่มือและการอธิบายระบบทั้งหมด
├── skills/                        # สกิลทั้งหมดจาก FITs, Claude และ Antigravity (200+ สกิล)
│   ├── bmad-*                     # BMAD Framework Core & Extensions (32 สกิล)
│   ├── bmad-cis-*                 # Creative Innovation Suite (8 สกิล)
│   ├── bmad-testarch-*            # Test Architecture Suite (9 สกิล)
│   ├── gds-*                      # Game Design Studio Suite (33 สกิล)
│   ├── ponytail-*                 # Minimalist & YAGNI Engineering Suite (6 สกิล)
│   ├── grill-with-docs/           # Socratic Plan & Architecture Interviewer (1 สกิล)
│   └── omc-skills/                # สกิลเฉพาะทางจาก OMC 5.6.0 (48 สกิล)
├── plugins/                       # ปลั๊กอินการทำงานหลัก
│   ├── oh-my-claudecode/          # OMC v5.6.0 Multi-agent Orchestration Framework
│   └── claude-code-warp/          # Warp Terminal Integration & Shell Hooks v2.2.0
├── fits-context/                  # กฎการทำงานและบันทึกความจำจริงจากโปรเจกต์ FITs
│   ├── AGENTS.md                  # ข้อกำหนด Multi-Agent Protocol & Git Lifecycle 9 ขั้นตอน
│   ├── settings.local.json        # การตั้งค่า Hook triggers ของโปรเจกต์
│   ├── hooks/main-sync.sh         # สคริปต์ Sync และ Guard ป้องกัน Git conflict
│   ├── project-memory.json        # ข้อมูลความจำของโปรเจกต์ (OMC Project Memory)
│   └── memory/                    # บันทึกบทเรียน (Feedback & Rules) ที่ได้จากการพัฒนา FITs
└── antigravity-upgrades/          # ส่วนเสริมที่นำมาพัฒนาตัว Antigravity
    ├── new-agents/                # เอเจนต์เฉพาะทางใหม่ที่ติดตั้งเพิ่มให้ Antigravity
    └── oma-bar/                   # ระบบ Tmux & Terminal Status Bar สำหรับ Antigravity
```

---

## 2. การอัปเกรดขีดความสามารถของ Antigravity (Self-Development)

จากการนำสกิลและปลั๊กอินของ FITs มาประมวลผล Antigravity ได้รับการอัปเกรดโดยตรงในระบบ:

1. **ติดตั้งสกิลระดับ Global ครบ 200+ สกิล** ใน `~/.gemini/config/skills/`:
   - สกิลสาย BMAD CIS (Creative Innovation), TestArch (Test Automation), GDS (Game/App Design) และ OMC Engineering Skills
2. **เพิ่ม 8 Subagents ใหม่** ใน `~/.gemini/config/plugins/oh-my-antigravity/agents/`:
   - `oma-code-simplifier`: ตัดโค้ดซ้ำซ้อน ลดความซับซ้อนโดยคงพฤติกรรมเดิม 100%
   - `oma-critic`: ตรวจสอบ Gap Analysis, ค้นหาจุดบกพร่องที่ซ่อนอยู่ และตรวจสอบสมมติฐาน
   - `oma-git-master`: บริหารจัดการ Git, Conventional Commits แบบ Atomic, Rebase และแก้ Merge Conflict
   - `oma-qa-tester`: ทดสอบ Interactive CLI / E2E และจำลองการรันระบบจริง
   - `oma-security-reviewer`: สแกนช่องโหว่ OWASP Top 10, ตรวจจับ Secret รั่วไหล และตรวจสอบ Auth
   - `oma-test-engineer`: เชี่ยวชาญ TDD, Unit/Integration Test Coverage
   - `oma-tracer`: ตรวจสอบ Call Graph และ Trace หา Root Cause ของบั๊กซับซ้อน
   - `oma-doc-specialist`: สร้างเอกสารสถาปัตยกรรม, PRD และ API Specification
3. **นำหลักการพัฒนาจาก FITs มาปรับใช้**:
   - Git Workflow 9 ขั้นตอน (Branching off main -> Unit/E2E test gate -> Atomic Conventional Commit)
   - ความเข้มงวดในการรักษา Single Source of Truth จาก PRD และ Mockup UI

---

## 3. คู่มือการใช้งาน OMA (Oh-My-Antigravity) และคำอธิบายสกิลทั้งหมด

OMA คือเฟรมเวิร์กจัดการวงจรชีวิตการทำงานของ AI Agent แบบ Multi-Agent Orchestration ที่ช่วยให้เอเจนต์ทำงานอย่างมีขั้นตอน ปลอดภัย มีระบบตรวจสอบย้อนกลับ (Verification Gate) และบริหารจัดการ Context ไม่ให้ล้น

### กลุ่มที่ 1: วงจรชีวิตและการควบคุมการทำงาน (Lifecycle & Orchestration)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `launch` | เริ่มต้นวงจรชีวิตงานใหม่ (Task Lifecycle) พร้อมกำหนดเป้าหมายและขั้นตอน |
| `intent` | วิเคราะห์ Intent ของคำสั่งผู้ใช้ เพื่อส่งต่อให้ Pipeline หรือ Command ที่เหมาะสม |
| `autopilot` | โหมดรันงานอัตโนมัติแบบวนลูปต่อเนื่องจนกว่าจะผ่าน Acceptance Criteria ทั้งหมดหรือเจอบล็อกเกอร์ |
| `ralph` | โหมดตรวจสอบคุณภาพเข้มงวด (Strict Ralph Mode) บังคับผ่าน Verification Gate ทุกขั้นตอน ห้ามข้ามขั้นตอน |
| `ultrawork` | โหมดทำงานแบบ Batch ปริมาณมากสำหรับงานอิสระหลายๆ ชิ้น พร้อมจุดตรวจคุณภาพเป็นระยะ |
| `goal` | รัน Autonomous Delivery Loop โดยโฟกัสที่ผลลัพธ์ของเป้าหมายจนเสร็จสมบูรณ์ |
| `ultragoal` | แตกเป้าหมายขนาดใหญ่ออกเป็นเป้าหมายย่อยตามลำดับ พร้อม Checkpoint บันทึกสถานะ |
| `loop` | บังคับลูป Execute -> Verify -> Fix จนกว่างานจะสมบูรณ์ตามเกณฑ์ |
| `stop` / `cancel` | หยุดการทำงานอย่างปลอดภัย พร้อมสรุปสถานะเพื่อให้นำมารันต่อได้ทันที (Handoff Summary) |
| `approval` | ตรวจสอบหรือตั้งค่าระดับการขออนุญาต (suggest, auto, full-auto) เพื่อควบคุมความปลอดภัย |

### กลุ่มที่ 2: การวางแผนและกำหนดขอบเขต (Planning & Specification)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `plan` / `oma-plan` | วางแผนงานเชิงวิศวกรรม แบ่งเป็น Phase และ Task พร้อมระบุจุดตรวจสอบ (Verification Checkpoint) |
| `prd` | ล็อกขอบเขตงานด้วย Acceptance Criteria รูปแบบ PRD รวมถึงระบุ Non-goals เพื่อป้องกันงานบานปลาย |
| `blueprint` | ออกแบบ Blueprint โครงสร้างระบบ/UI พร้อม State การโต้ตอบ และ Verification Hooks |
| `interview` / `deep-interview` | ใช้บทสนทนาแบบ Socratic เพื่อซักถามและเคลียร์ Requirements ที่ยังคลุมเครือให้ชัดเจน |
| `ralplan` | การวางแผนในโหมด Ralph เน้นความปลอดภัย จุดป้องกันความเสี่ยง และขั้นตอน Fail-safe |
| `consensus` | เปรียบเทียบตัวเลือกทางเทคนิคหลายๆ ทางผ่าน Multi-agent เพื่อหาข้อสรุปที่ดีที่สุด |
| `taskboard` | บริหาร Task Board ขนาดกะทัดรัด ติดตามสถานะ Task ID, ผู้รับผิดชอบ และผลการ Verify |

### กลุ่มที่ 3: การทำงานร่วมกันเป็นทีม (Multi-Agent Team Workflow)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `team` | บริหารวงจรชีวิตทีมเอเจนต์ครบวงจร (5 สเตจ) ตั้งแต่จัดทีมจนถึงส่งมอบงาน |
| `team-assemble` | สเตจ 0: จัดทีมเอเจนต์ที่เหมาะกับเนื้องาน พร้อมกำหนดบทบาทและโมเดลที่เหมาะสม |
| `team-plan` | สเตจ 1: ร่วมกันสร้างแผนงานและลำดับขั้นตอนการส่งต่องานระหว่างเอเจนต์ |
| `team-prd` | สเตจ 2: ล็อกเกณฑ์การยอมรับ (Acceptance Criteria) และขอบเขตงานของทีม |
| `team-exec` | สเตจ 3: เอเจนต์ลงมือเขียนโค้ดและแก้ไขระบบตามขอบเขตที่ได้รับมอบหมาย |
| `team-verify` | สเตจ 4: ตรวจสอบความถูกต้องของโค้ดและการทำงานเทียบกับ Acceptance Criteria |
| `team-fix` | สเตจ 5: แก้ไขเฉพาะจุดที่พบข้อผิดพลาดจากการตรวจสอบ แล้วส่งกลับไป Verify ซ้ำ |

### กลุ่มที่ 4: การลงมือปฏิบัติและการพัฒนาโค้ด (Execution & Engineering)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `execute` | ลงมือเขียนโค้ดและแก้ไขไฟล์อย่างรวดเร็ว ปลอดภัย พร้อมสรุปการเปลี่ยนแปลง |
| `tdd` | บังคับใช้วิถี Test-Driven Development (เขียน Test ให้ Fail -> Implement -> Test Pass -> Refactor) |
| `debug` | ค้นหาและวินิจฉัยบั๊ก สแต็กเทรซ และพฤติกรรมผิดปกติอย่างเป็นระบบ |
| `trace` | ติดตามและวิเคราะห์ Trace ของการทำงาน และ Call Graph เพื่อแยกแยะสาเหตุต้นตอ |
| `review` | รันกระบวนการ Code Review อย่างละเอียด ตรวจสอบความถูกต้อง, Regression, ความปลอดภัย |
| `verify` / `verify-and-stop` | ตรวจสอบหลักฐานการทำงานว่าตรงตามเงื่อนไขการส่งมอบ โดยไม่ขยายขอบเขตงานเกินจำเป็น |
| `pr` | เตรียมข้อมูล ตรวจสอบความพร้อม และสร้าง Pull Request / Merge Request ตามมาตรฐาน |
| `release` | ดำเนินการออก Release, จัดการ Tag เวอร์ชัน และตรวจสอบความพร้อมในการปล่อยระบบ |

### กลุ่มที่ 5: วินัยด้านโค้ดและเอกสาร (Engineering Discipline & Cleanliness)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `minimal-code-discipline` | บังคับใช้ความเรียบง่าย ไม่เขียนโค้ดเกินจำเป็น (YAGNI) และใช้ Native/Standard Library ก่อน |
| `minimal-prose-discipline` | บังคับให้การสื่อสารและการเขียนคำอธิบายกระชับ ตรงประเด็น ตัดคำฟุ่มเฟือย |
| `ai-slop-cleaner` | ตรวจสอบและกำจัดโค้ด/คอมเมนต์ขยะที่มักถูกสร้างขึ้นเกินความจำเป็น |
| `agent-doc-discipline` | ดูแลรักษาเอกสารให้อัปเดตตรงกับโค้ดจริง ไม่ทิ้งเอกสารตกค้าง |
| `diagram` | สร้างไดอะแกรมประกอบสถาปัตยกรรมและการไหลของข้อมูล (Mermaid / PlantUML) |
| `wiki` | บันทึกและจัดระเบียบฐานความรู้ภายในโปรเจกต์ |

### กลุ่มที่ 6: การจัดการ Context, แคช และความจำ (Context & Memory Management)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `memory` | บริหารดัชนีความจำของโปรเจกต์ผ่าน MEMORY.md และ Rule Packs |
| `remember` | บันทึกการตัดสินใจ ข้อตกลง หรือบทเรียนใหม่ลงในระบบความจำของโปรเจกต์ทันที |
| `recall` | ดึงข้อมูลการตัดสินใจเดิมและหลักฐานย้อนหลังมาใช้งานอย่างรวดเร็ว |
| `deep-init` / `deepinit` | วิเคราะห์โครงสร้างโปรเจกต์เชิงลึกเพื่อสร้าง Project Map สำหรับใช้ในเซสชันระยะยาว |
| `cache` / `context-optimize` | ตรวจสอบเสถียรภาพของ Prompt Cache และลดการใช้ Token ที่ไม่จำเป็น |
| `optimize` | ทบทวนการใช้ Context และปรับปรุงประสิทธิภาพของเซสชัน |
| `checkpoint` | บันทึก Snapshot จุดพักของเซสชัน เพื่อให้สามารถย้อนกลับหรือเริ่มต่อได้สะดวก |

### กลุ่มที่ 7: การตรวจสอบและเครื่องมือสนับสนุนระบบ (Diagnostics & System Tools)

| สกิล | หน้าที่และการใช้งาน |
|---|---|
| `doctor` / `omc-doctor` | ตรวจสอบความสมบูรณ์ของระบบ Extension, State ความจำ และความพร้อมของเครื่องมือ |
| `status` | แสดงผลสรุปสถานะปัจจุบันของโปรเจกต์ในรูปแบบ HUD (Head-Up Display) |
| `hud` / `hud-on` / `hud-off` / `hud-compact` | สลับรูปแบบการแสดงผล HUD บนหน้าจอ (ปกติ, กะทัดรัด, ซ่อน) |
| `hooks` / `hooks-init` / `hooks-test` / `hooks-validate` | จัดการ ทดสอบ และตรวจสอบความถูกต้องของสคริปต์ Hook Lifecycle |
| `mode` | ตรวจสอบหรือสลับโหมดการทำงาน (balanced, speed, deep, autopilot, ralph, ultrawork) |
| `model` | กำหนดกลยุทธ์การเลือกโมเดล (balanced, auto, custom) ตามความเหมาะสมของแต่ละงาน |
| `reasoning` | ปรับระดับ Reasoning Effort ของการคิด (Global และราย Teammate) เพื่อคุมประสิทธิภาพและต้นทุน |
| `notify` / `configure-notifications` | กำหนดการแจ้งเตือนเมื่อถึงจุดรอ Approve หรือเมื่องานในเบื้องหลังเสร็จสิ้น |
| `workspace` | จัดการ Workspace และ Worktree สำหรับแยกสภาพแวดล้อมการทำงานของแต่ละ Lane |
