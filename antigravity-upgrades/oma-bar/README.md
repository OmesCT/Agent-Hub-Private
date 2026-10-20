# OMA Status Bar for Antigravity (AGY)

ระบบแถบสถานะ (Status Bar) สไตล์ OMC สำหรับ Antigravity ที่ผูกเข้ากับ Tmux status bar และ Terminal

## 1. ข้อมูลที่แสดงบน Bar (ตามที่เลือกครบทั้ง 6 รายการ)

ตัวอย่างการแสดงผล:
```text
[OMA:autopilot:team-exec | ralph:PASS | tasks:2/5 | g-3.8-flash | git:dev-ohm* | ctx:42k]
```

1. **OMA Mode & Stage**: โหมดการทำงานและขั้นตอนย่อย เช่น `balanced:idle`, `autopilot:team-exec`, `ralph:verify`
2. **Ralph Status**: ผลการตรวจ Quality Gate เช่น `ralph:PASS` (สีเขียว), `ralph:WARN` (สีส้ม), `ralph:BLOCK` (สีแดง)
3. **Tasks Progress**: จำนวนงานที่เสร็จเทียบกับงานทั้งหมด เช่น `tasks:2/5` (อ่านจาก `.omg/state/taskboard.md`)
4. **Active Model**: โมเดลที่ทำงานอยู่ เช่น `g-3.8-flash`, `g-3.1-pro`
5. **Git Branch & Dirty**: กิ่งปัจจุบันและสถานะการแก้ไข เช่น `git:main*` (มี `*` เมื่อโค้ดยังไม่ commit)
6. **Context Usage & Cost**: การใช้ Context Token เช่น `ctx:42k` หรือ `ctx:1.2M`

---

## 2. วิธีการทำงานร่วมกับ Antigravity

- **สคริปต์หลัก**: `~/.gemini/config/scripts/oma-bar.py`
- **อัตโนมัติผ่าน Hook**: ติดตั้งใน `~/.gemini/config/hooks.json` ภายใต้ชื่อ `oma-status-bar`
  - ทำงานอัตโนมัติในทุกจังหวะ `PreInvocation`, `PostInvocation`, และ `PostToolUse`
  - เมื่อ Antigravity มีการเรียกใช้ Tool หรือตอบกลับ Bar ใน Tmux จะอัปเดตแบบ Real-time ทันที
- **บันทึกสถานะลงไฟล์**:
  - `~/.gemini/oma-status-bar.txt`
  - `.omg/state/status-bar.txt` (ในโปรเจกต์)

---

## 3. คำสั่งและตัวเลือกการใช้งาน

```bash
# พิมพ์สถานะ Bar ออกมาดูทันที
python3 ~/.gemini/config/scripts/oma-bar.py --print

# ส่งคำสั่งอัปเดต tmux status-right โดยตรง
python3 ~/.gemini/config/scripts/oma-bar.py

# พิมพ์พร้อมโค้ดสีสำหรับ tmux
python3 ~/.gemini/config/scripts/oma-bar.py --tmux

# อัปเดต Terminal Window Title
python3 ~/.gemini/config/scripts/oma-bar.py --title
```
