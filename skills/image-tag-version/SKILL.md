---
name: image-tag-version
description: >-
  Manage, generate, validate, calculate, and apply Git tag versions and Docker image tags
  following SemVer, CalVer, and build sequence conventions (<version>-build<seq>, v<semver>,
  exported-*, imported-*). Use when the user asks to tag images, calculate next image version,
  manage GitOps release tags, or automate tag-based CI/CD workflows.
---

# Image Tag Versioning Skill

คู่มือและแบบแผนปฏิบัติการจัดการ Versioning และ Tagging สำหรับ Docker Images, Git Repositories, และ GitOps CI/CD Pipelines

---

## 1. มาตรฐานรูปแบบ Tagging (Tagging Conventions)

### 1.1 Docker Image Tag (Build Sequence Pattern)
รูปแบบ: `<app-version>-build<seq>`
- **โครงสร้าง**:
  - `<app-version>`: เลขเวอร์ชันจาก Application Source Code (เช่น `pom.xml`, `package.json`, `build.gradle`) ตัวอย่าง: `0.0.0-alpha1`, `1.2.0`
  - `build<seq>`: ลำดับการ Build อัตโนมัติ (Build Sequence) โดยตรวจนับจาก Tag ที่มีอยู่แล้วบน Container Registry (Harbor)
- **ตัวอย่าง**:
  - `0.0.0-alpha1-build1`
  - `0.0.0-alpha1-build28`
  - `1.0.0-build5`

### 1.2 GitOps Release Tag (Calendar Versioning Pattern)
รูปแบบ: `{status}-{env}-{domain}-{YYYYMMDD-HHMM}`
- **โครงสร้าง**:
  - `{status}`: สถานะการ Deploy (`exported`, `imported`, `rollback`)
  - `{env}`: Environment เป้าหมาย (`npd`, `prd`, `drp`)
  - `{domain}`: Domain หรือ Subsystem (`DEV-Domain`, `SIT-Domain`, `UAT-Domain`)
  - `{YYYYMMDD-HHMM}`: Timestamp เวลาสร้าง Tag
- **ตัวอย่าง**:
  - `exported-npd-DEV-Domain-20260924-1603`
  - `imported-npd-SIT-Domain-20260924-1615`
  - `rollback-npd-DEV-Domain-20260924-1630`

---

## 2. ขั้นตอนการคำนวณและสร้าง Tag (Step-by-Step Procedures)

### 2.1 ดึง Application Version จาก Source Code
- **Maven (`pom.xml`)**:
  ```bash
  APP_VERSION=$(grep '<version>' pom.xml | head -1 | sed -E 's/.*<version>(.*)<\/version>.*/\1/' | tr -d ' ')
  ```
- **Node.js (`package.json`)**:
  ```bash
  APP_VERSION=$(node -p "require('./package.json').version")
  ```
- **Gradle (`build.gradle`)**:
  ```bash
  APP_VERSION=$(grep 'version' build.gradle | head -1 | awk -F"'" '{print $2}')
  ```

### 2.2 คำนวณ Next Build Sequence จาก Registry (Harbor API)
1. Query รายการ Tag ทั้งหมดของ Repository ใน Harbor
2. Filter หา Tag ที่ขึ้นต้นด้วย `${APP_VERSION}-build`
3. สกัดเลขลำดับ (Build Number) ทั้งหมดแล้วหาค่า `MAX(seq)`
4. กำหนด `NEXT_SEQ = MAX(seq) + 1` (หากยังไม่มี Tag ให้เริ่มที่ 1)
5. สร้าง Full Image Tag: `${APP_VERSION}-build${NEXT_SEQ}`

### 2.3 การสร้างและ Push Git Tag
- **สร้าง Annotated Tag**:
  ```bash
  git tag -a "${TAG_NAME}" -m "Release ${TAG_NAME}" -m "${DETAILS}"
  ```
- **Push Tag ไปยัง Remote**:
  ```bash
  git push origin "${TAG_NAME}"
  ```
- **Checkout Snapshot ด้วย Tag (สำหรับ Rollback / Deploy)**:
  ```bash
  git fetch --tags
  git checkout tags/"${TAG_NAME}"
  ```

---

## 3. อัลกอริทึม Natural Sort สำหรับจัดเรียง Version Tags

เมื่อต้องการนำรายการ Tags มาแสดงผลใน UI / Dropdown ให้เรียงจากใหม่สุดไปเก่าสุด โดยใช้ **Natural Number Sorting**:
```groovy
tags.unique().sort(false) { a, b ->
    def aParts = a.findAll(/[0-9]+|[^0-9]+/)
    def bParts = b.findAll(/[0-9]+|[^0-9]+/)
    for (int i = 0; i < Math.min(aParts.size(), bParts.size()); i++) {
        def aPart = aParts[i]
        def bPart = bParts[i]
        if (aPart != bPart) {
            if (aPart.isInteger() && bPart.isInteger()) {
                return aPart.toInteger() <=> bPart.toInteger()
            }
            return aPart <=> bPart
        }
    }
    return aParts.size() <=> bParts.size()
}.reverse()
```

---

## 4. Runbook: การตั้งชื่อ Tag ใน Jenkins Pipelines

| Pipeline | วัตถุประสงค์ | แหล่งดึง/สร้าง Tag | รูปแบบ Tag |
| :--- | :--- | :--- | :--- |
| **Build Pipeline** | สร้าง Image ใหม่ | อ่าน version จาก `pom.xml` + Query Harbor | `${APP_VERSION}-build${SEQ}` |
| **Export Pipeline** | Export คอนฟิก | สร้าง Calendar Tag หลัง Export สำเร็จ | `exported-${ENV}-${DOMAIN}-${DATE}` |
| **Import Pipeline** | Import คอนฟิก | สร้าง Calendar Tag หลัง Import สำเร็จ | `imported-${ENV}-${DOMAIN}-${DATE}` |
| **Rollback Pipeline** | ย้อนกลับคอนฟิก | Checkout จาก Tag เก่า + สร้าง Tag ใหม่ | `rollback-${ENV}-${DOMAIN}-${DATE}` |
