# คู่มือการย้าย Skills และ Customizations ของ Antigravity ไปยังเครื่องอื่น

เอกสารนี้อธิบายขั้นตอนการคัดลอก Skills, Plugins และ Configurations ของ Antigravity จากเครื่องปัจจุบันไปยังเครื่องปลายทาง

---

## 1. ตำแหน่งไฟล์ที่เกี่ยวข้อง (Paths Overview)

ในเครื่อง Antigravity สกิลและคอนฟิกระดับ Global จะถูกเก็บไว้ที่:

- โฟลเดอร์หลัก: `~/.gemini/config/`
- โฟลเดอร์สกิล: `~/.gemini/config/skills/`
- โฟลเดอร์ปลั๊กอินและ Subagents: `~/.gemini/config/plugins/`
- ไฟล์คอนฟิก Hook และ Lifecycle: `~/.gemini/config/hooks.json`
- ไฟล์คอนฟิก MCP Tools: `~/.gemini/config/mcp_config.json`

---

## 2. วิธีที่ 1: บีบอัดและย้ายผ่าน Archive (แนะนำ - สะดวกและเร็วที่สุด)

### ขั้นตอนที่ 1: ฝั่งเครื่องต้นทาง (เครื่องปัจจุบัน)

รันคำสั่งบีบอัดโฟลเดอร์ config ทั้งหมด (ขนาดประมาณ 27MB):

```bash
tar -czvf ~/Desktop/antigravity-config.tar.gz -C ~/.gemini config
```

*หมายเหตุ: หากต้องการย้ายเฉพาะ Skills และ Plugins ให้รัน:*
```bash
tar -czvf ~/Desktop/antigravity-skills.tar.gz -C ~/.gemini/config skills plugins
```

### ขั้นตอนที่ 2: ถ่ายโอนไฟล์ไปยังเครื่องใหม่

ส่งไฟล์ `antigravity-config.tar.gz` ไปยังเครื่องปลายทางผ่านช่องทางใดช่องทางหนึ่ง:
- AirDrop (กรณี Mac ไป Mac)
- Flash Drive / External SSD
- Cloud Storage (Google Drive, Dropbox, OneDrive)
- คำสั่ง `scp` ผ่านเครือข่ายเดียวกัน:
  ```bash
  scp ~/Desktop/antigravity-config.tar.gz username@remote-ip:~/Downloads/
  ```

### ขั้นตอนที่ 3: ฝั่งเครื่องปลายทาง

1. เปิด Terminal ในเครื่องปลายทาง
2. ตรวจสอบและสร้างโฟลเดอร์ปลายทาง:
   ```bash
   mkdir -p ~/.gemini
   ```
3. แตกไฟล์ทับลงในไดเรกทอรี `~/.gemini/`:
   ```bash
   # กรณีส่งไฟล์ antigravity-config.tar.gz ไปไว้ที่ ~/Downloads
   tar -xzvf ~/Downloads/antigravity-config.tar.gz -C ~/.gemini/
   ```
   *(หากใช้ไฟล์ `antigravity-skills.tar.gz` ให้สร้าง `mkdir -p ~/.gemini/config` แล้วแตกไฟล์ลงใน `~/.gemini/config/`)*

4. ตรวจสอบสิทธิ์การเข้าถึงไฟล์:
   ```bash
   chmod -R u+rw ~/.gemini/config
   ```

---

## 3. วิธีที่ 2: ติดตั้งจากโฟลเดอร์โปรเจกต์ Agent-Learning

หากมีการคัดลอกโปรเจกต์ `Agent-Learning` ไปยังเครื่องใหม่แล้ว สามารถคัดลอกไฟล์เข้าตำแหน่ง Global Config ได้ทันที

รันคำสั่งนี้บนเครื่องปลายทาง (จากโฟลเดอร์โปรเจกต์ `Agent-Learning`):

```bash
# 1. สร้างโฟลเดอร์ปลายทาง
mkdir -p ~/.gemini/config/skills
mkdir -p ~/.gemini/config/plugins

# 2. คัดลอก Skills และ Plugins
cp -R skills/* ~/.gemini/config/skills/
cp -R plugins/* ~/.gemini/config/plugins/

# 3. คัดลอก Subagents เพิ่มเติมเข้า OMA Plugin (ถ้ามี)
if [ -d "antigravity-upgrades/new-agents" ]; then
  mkdir -p ~/.gemini/config/plugins/oh-my-antigravity/agents
  cp -R antigravity-upgrades/new-agents/* ~/.gemini/config/plugins/oh-my-antigravity/agents/
fi
```

---

## 4. วิธีที่ 3: ซิงก์ผ่าน Private Git Repository (ระยะยาว)

เหมาะสำหรับผู้ที่ต้องการอัปเดตสกิลระหว่างหลายเครื่องสม่ำเสมอ:

### ฝั่งเครื่องต้นทาง:
```bash
cd ~/.gemini/config
git init
git add skills plugins hooks.json mcp_config.json
git commit -m "chore: initial antigravity config and skills"
git remote add origin <URL_PRIVATE_REPO>
git push -u origin main
```

### ฝั่งเครื่องปลายทาง:
```bash
mkdir -p ~/.gemini/config
cd ~/.gemini/config
git clone <URL_PRIVATE_REPO> .
```

---

## 5. ตรวจสอบความถูกต้องหลังการย้าย (Verification)

1. **ตรวจสอบจำนวนและโครงสร้างไฟล์:**
   ```bash
   ls ~/.gemini/config/skills | wc -l
   ```
   (ควรแสดงผลจำนวนสกิลใกล้เคียงประมาณ 90-180 โฟลเดอร์)

2. **ตรวจสอบ Dependencies พื้นฐาน:**
   บางสกิลหรือสคริปต์เสริม (เช่น OMA Status Bar) ใช้งาน Node.js หรือ Python ตรวจสอบว่าเครื่องใหม่มีติดตั้งหรือไม่:
   ```bash
   node --version
   python3 --version
   ```

3. **รีสตาร์ท Antigravity:**
   - ปิดและเปิด Antigravity หรือ IDE ใหม่ทั้งหมด
   - เริ่มบทสนทนาใหม่เพื่อทดสอบการเรียกใช้งานสกิล (เช่น ทดสอบพิมพ์ถามเรื่องสกิล หรือให้ลิสต์สกิลที่มี)
