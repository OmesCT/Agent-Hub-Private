# ทะเบียนข้อมูลทุกโปรเจคบนเครื่องและรายงานการปฏิบัติงาน (Workspace Portfolio & Activity Log)

เอกสารรวบรวมข้อมูลทุกโปรเจคใน `/Users/chinnawat.t/workspace` บนเครื่องคอมพิวเตอร์ แบ่งตามหมวดหมู่โครงการ พร้อมรายละเอียดสถาปัตยกรรม เทคโนโลยีที่ใช้ พาธไฟล์ Git Repository และสรุปผลการปฏิบัติงานรายสัปดาห์ (29 มิถุนายน - 19 ตุลาคม 2569)

---

## 1. โปรเจคหลักจากการปฏิบัติงานสหกิจศึกษา (Enterprise & Co-op Core Projects)

### 1.1 MFT-Pipeline (MFT Automate Deployment & Jenkins Shared Library)
- **สถานะ**: เสร็จสมบูรณ์ (ใช้งานระดับ Non-Production / เตรียมพร้อม Production)
- **Local Paths**:
  - `/Users/chinnawat.t/workspace/docker-jenkins/MFT-Pipeline-Project`
  - `/Users/chinnawat.t/workspace/docker-jenkins/MFT-Pipeline-Project/mft-shared-library`
  - `/Users/chinnawat.t/workspace/MFT-Automate-Deployment`
  - `/Users/chinnawat.t/workspace/mft`
  - `/Users/chinnawat.t/workspace/tac-source`
- **Git Remotes**:
  - `git@gitlab.tcbank.local:DevOps/Jenkins/MFT-Pipeline.git`
  - `git@gitlab.tcbank.local:DevOps/Jenkins/mft-pipeline-utility.git`
  - `git@gitlab.tcbank.local:wai/tac.git` (Branch: `feature/mft-promote`)
- **Tech Stack**: Jenkins Declarative Pipeline, Groovy Shared Library (`vars/*.groovy`), Docker Engine, Harbor Registry, GitLab REST API v4, Python, Bash, `jq`, Active Choices Reactive Parameter
- **สถาปัตยกรรมและฟีเจอร์สำคัญ**:
  - **4 NPD Pipelines** (แยกโฟลเดอร์ `release/` และ `draft/`):
    1. `Jenkinsfile-build.groovy`: สร้าง Docker Image ของ MFT CLI Utility และแท็กเวอร์ชัน `<version>-build<seq>` อัปโหลดขึ้น Harbor Registry
    2. `Jenkinsfile-list-export.groovy`: ดึงรายการ Flow จาก Git Tag (`export-*`) รันคอนเทนเนอร์ Export ข้อมูลจาก MFT Source และกรองข้อมูลความลับออกก่อน Commit ลง Git
    3. `Jenkinsfile-import-deploy.groovy`: ค้นหา Tag ที่ผ่านการ Export (`exported-*`) นำไฟล์ JSON ไปแทนค่าตัวแปรตาม Environment (`SIT`, `UAT`, `PREPROD`) แล้ว Import เข้า MFT ปลายทาง
    4. `Jenkinsfile-rollback.groovy`: ดึงประวัติ Tag ที่เคย Import สำเร็จ (`imported-*`) เพื่อย้อนคืนค่า Configuration กลับสู่เวอร์ชันเสถียรได้ทันที
  - **10 Groovy Shared Library Modules (`vars/`)**: `dockerUtil.groovy`, `harbor.groovy`, `gitOps.groovy`, `mftBuild.groovy`, `mftExport.groovy`, `mftImport.groovy`, `getImageTags.groovy`, `getExportTriggers.groovy`, `getImportTriggers.groovy`, `getRollbackTags.groovy`
  - **การรักษาความปลอดภัย (Security Hardening)**:
    - ใช้ `jq` ล้างค่า `<password>`, `<hostname>`, `<username>` ใน JSON ทุกครั้งก่อนบันทึกเข้า Git
    - แก้ไขช่องโหว่ `DOP-4966` ด้วยการส่งรหัสผ่านเข้า Docker Container ผ่าน `-e KEY` (ดึงจาก Environment ของ Jenkins Agent โดยไม่พิมพ์ค่าลง Command Line)
- **ผลการปฏิบัติงาน**: ลดเวลาการย้าย MFT Flow จากเดิมทำมือ 30-45 นาที/รายการ เหลือเพียง 3-5 นาทีผ่าน Pipeline อัตโนมัติ ลดความผิดพลาดจากคน (Human Error) เป็น 0% และมีเอกสารรายงานสหกิจศึกษาครบ 6 บทในโฟลเดอร์ `documents/`

---

### 1.2 Kubernetes Lab & Microservices (Restaurant Queue System)
- **สถานะ**: เสร็จสมบูรณ์ (ผ่านการทดสอบบน Kubernetes Cluster และ Jenkins CI/CD)
- **Local Paths**:
  - `/Users/chinnawat.t/workspace/restaurant`
  - `/Users/chinnawat.t/workspace/jenkins-pipeline`
- **Git Remotes**:
  - `git@gitlab.tcbank.local:DevOps/sandbox/ohm/restaurant.git` (Branch: `main`)
  - `git@gitlab.tcbank.local:DevOps/sandbox/ohm/jenkins-pipeline/jenkins-pipeline.git` (Branch: `main`)
- **Tech Stack**: React 19, Vite, Express 5, Node.js, WebSocket (`ws`), OAuth2 Proxy, Kubernetes (`Deployment`, `Service`, `HTTPRoute`, `ConfigMap`, `Secret`, `NetworkPolicy`, `CronJob`), Jenkins
- **สถาปัตยกรรมและฟีเจอร์สำคัญ**:
  - ระบบจองคิวร้านอาหารแบบ Fullstack พร้อมระบบ Admin Authentication (JWT) และ OAuth2 Proxy
  - เชื่อมต่อ Kubernetes API ภายใน Cluster โดยตรง (`PATCH /api/v1/namespaces/.../secrets/...`) เพื่อเปลี่ยนรหัสผ่าน Admin และหมุนเวียน `JWT_SECRET` อัตโนมัติผ่านสิทธิ์ `ServiceAccount` (`Role` และ `RoleBinding`)
  - แยก Microservice สำหรับส่งข้อความแจ้งเตือนคิวแบบ Real-time ผ่าน Pod-to-Pod WebSocket
  - กำหนดค่าความมั่นคงปลอดภัยและเสถียรภาพครบวงจร: `LivenessProbe`, `ReadinessProbe`, `StartupProbe`, `NetworkPolicy` (Zero-Trust), และ `CronJob` ล้างคิวค้างรายวัน
- **ผลการปฏิบัติงาน**: ได้ต้นแบบ Cloud-Native Application ที่ทำงานร่วมกับ Kubernetes RBAC, Gateway API (`HTTPRoute`) และ Jenkins CI/CD Pipeline แบบครบวงจร

---

### 1.3 OpenShift App Onboarding Portal
- **สถานะ**: เสร็จสมบูรณ์ (Fullstack Monorepo + Single-Container Deployment)
- **Local Paths**:
  - `/Users/chinnawat.t/workspace/openshift-onboard`
  - `/Users/chinnawat.t/workspace/openshift-onboarding`
- **Git Remote**:
  - `git@gitlab.tcbank.local:DevOps/sandbox/ohm/openshift-onboard.git` (Branch: `DevOhm`)
- **Tech Stack**: React, TypeScript, Tailwind CSS, NestJS, TypeORM, PostgreSQL, Red Hat Keycloak SSO (OIDC + BFF HttpOnly Cookie), Server-Sent Events (SSE), Docker Multi-stage Build
- **สถาปัตยกรรมและฟีเจอร์สำคัญ**:
  - เปลี่ยนใบคำขอขึ้นระบบ OpenShift จากไฟล์ Excel แบบเดิมเป็น Web Wizard 8 ขั้นตอน (`Project Info`, `Resource Quota`, `GitLab & Jenkins`, `Service Binding`, `Secrets`, `Egress Firewall`, `Review`, `Export Manifests`)
  - รองรับการยืนยันตัวตนด้วย Red Hat Keycloak SSO แบบ BFF (Backend-for-Frontend) เก็บ Token ใน HttpOnly Cookie และแยกสิทธิ์การมองเห็นข้อมูลตามทีม (`WAS1`, `WAS2`)
  - เชื่อมต่อ GitLab API และ Jenkins API แบบ Live Autocomplete ผ่าน Backend Proxy เพื่อป้องกันปัญหา CORS และไม่เปิดเผย Private Token ที่ฝั่ง Browser
  - รองรับการผูกเซอร์วิส (`MongoDB`, `Kafka`, `Kong`) แยกราย Environment (`DEV`, `SIT`, `UAT`) พร้อมสร้างข้อความแจ้งเปิด Firewall สำหรับ Jira และ SDP อัตโนมัติ
  - ส่งออกไฟล์พร้อมใช้งานทันทีในคลิกเดียว: Kustomize YAML (`base/` + `overlays/`), ArgoCD `Application` YAML, `Jenkinsfile` และสคริปต์ `oc apply` ในรูปแบบไฟล์ ZIP
- **ผลการปฏิบัติงาน**: ลดขั้นตอนการกรอกใบคำขอและสร้างไฟล์ Manifest ด้วยมือได้อย่างสมบูรณ์ และปรับปรุงโครงสร้างเป็น Unified Single-Container Dockerfile ลดเวลา Build บน Jenkins จาก 7 นาที เหลือ 1.5 นาที

---

### 1.4 FITs (Financial IT Spend - ระบบบริหารจัดการงบประมาณด้านเทคโนโลยีสารสนเทศ)
- **สถานะ**: เสร็จสมบูรณ์ตามขอบเขตสหกิจศึกษา (พร้อมชุดทดสอบ Playwright E2E และเอกสารส่งมอบ)
- **Local Paths**:
  - `/Users/chinnawat.t/workspace/FITs` (Branch: `dev-ohm`)
  - Git Worktrees แยกตาม Feature Story:
    - `/Users/chinnawat.t/workspace/FITs-story-2.2` (`feat/#15-send-back-mandatory-reason`)
    - `/Users/chinnawat.t/workspace/FITs-story-2.3` (`feat/#16-executive-approval-direct-approved`)
    - `/Users/chinnawat.t/workspace/FITs-story-2.4` (`feat/#17-real-time-signalr-presence`)
    - `/Users/chinnawat.t/workspace/FITs-story-2.5`
    - `/Users/chinnawat.t/workspace/FITs-wt` และ `/Users/chinnawat.t/workspace/FITs-kit`
  - GitOps Manifests: `/Users/chinnawat.t/workspace/fits_manifest` (Branch: `dev`)
  - Dev & Test Packages:
    - `/Users/chinnawat.t/workspace/IT_Budget_Dev/budget-management`
    - `/Users/chinnawat.t/workspace/IT_Budget_Dev/it-budget-aihero`
    - `/Users/chinnawat.t/workspace/IT_Budget_Management_Test_Package_1` (Branch: `ohmdev`)
- **Git Remotes**:
  - `git@gitlab.tcbank.local:cto/it-budget/fits.git`
  - `git@gitlab.tcbank.local:gitops/it-admin/fits_manifest.git`
  - `git@gitlab.tcbank.local:cto/it-budget/budget-management.git`
  - `git@gitlab.tcbank.local:cto/it-budget/it-budget-aihero.git`
- **Tech Stack**: React 19, TypeScript, Tailwind CSS v4, .NET 10 (`Fits.Api`), Entity Framework Core, PostgreSQL 16, SignalR, ClosedXML / ExcelJS, AAA OIDC SSO, OpenShift Helm & Kong Gateway, Playwright E2E
- **สถาปัตยกรรมและฟีเจอร์สำคัญ**:
  - **6-Stage Budget Lifecycle**: `Draft` -> `Submitted` -> `Reviewed` -> `Approved` / `SendBack` (บังคับระบุเหตุผล) / `Cut` พร้อมกฎ **Maker-Checker** บังคับว่าผู้ขอ (`Requester`) ห้ามเป็นคนเดียวกับผู้อนุมัติ (`Reviewer`)
  - **Deterministic BGID Generator**: สร้างรหัสงบประมาณอัตโนมัติตามโครงสร้างมาตรฐานธนาคาร (`YY-RunRate-Type-Category-Department-Seq`) ป้องกันรหัสซ้ำภายใต้การทำงานพร้อมกัน (Concurrency Lock)
  - **Structure A / Structure B & Cross-Fiscal-Year Split**: รองรับการแตกหมวดค่าใช้จ่าย (`Hardware`, `Software`, `Services`, `Cloud`) และการแบ่งงบสัญญาข้ามปีงบประมาณทั้งแบบหารเฉลี่ย 12 เดือน และกำหนดเองรายเดือน
  - **4-Tier Waterfall Cut Simulator**: จำลองการปรับลดงบประมาณอัตโนมัติโดยตัดจาก `Tier 4 (Discretionary)` ไล่ขึ้นไปและล็อกงบ `Tier 1 (Regulatory)` ไม่ให้ถูกตัด
  - **Dual Ledger PO Booking & D365 GL Mapping**: แยกสมุดบัญชี `Approved Plan` ออกจาก `Actual Spent` พร้อมป้องกันการผูกใบสั่งซื้อ (PO) เกินวงเงินคงเหลือ และส่งออกไฟล์ Excel สำหรับ Microsoft Dynamics 365
  - **BOT SHA-256 Hash-Chained Audit Trail**: บันทึกประวัติการแก้ไขและเปลี่ยนสถานะทุกครั้งด้วยโซ่แฮช (`prev_hash` + `payload_hash`) ตามมาตรฐานการตรวจสอบของธนาคารแห่งประเทศไทย (ธปท.)
  - **Real-Time SignalR Presence & Enterprise Integration**: แสดงผู้ใช้งานที่กำลังเปิดดูรายการงบเดียวกันแบบเรียลไทม์ เชื่อมต่อระบบยืนยันตัวตน AAA OIDC SSO และซิงค์โครงสร้างองค์กรจาก HRMS

---

## 2. โปรเจคระบบ AI Agent และเครื่องมือช่วยพัฒนา (AI Agent & Developer Tooling)

| ชื่อโปรเจค | Local Path | Git Remote | รายละเอียดและเทคโนโลยี |
| :--- | :--- | :--- | :--- |
| **Agent-Learning (Agent Hub Private)** | `/Users/chinnawat.t/workspace/Agent-Learning` | `https://github.com/OmesCT/Agent-Hub-Private.git` | คลังรวม AI Agent Skills กว่า 180 รายการ (`BMAD`, `CIS`, `GDS`, `TestArch`, `Ponytail`, `OMC`), ปลั๊กอิน (`oh-my-claudecode`, `claude-code-warp`), `fits-context` (`AGENTS.md`, hooks, memory), `antigravity-upgrades` (8 Subagents + `oma-bar`) และไฟล์รายงาน `activity-log.html` |
| **antigravity-config** | `/Users/chinnawat.t/workspace/antigravity-config` | Local Git (`main`) | โครงสร้างตั้งค่ามาตรฐานของ Antigravity CLI, กฎวิศวกรรมใน `GEMINI.md`, สคริปต์ติดตั้งอัตโนมัติ (`install.sh`) และเทมเพลตการทำงาน |
| **MCP-Chrome** | `/Users/chinnawat.t/workspace/MCP-Chrome` | `https://github.com/ChromeDevTools/chrome-devtools-mcp.git` | เซิร์ฟเวอร์ Model Context Protocol (MCP) สำหรับเชื่อมต่อ Chrome DevTools เพื่อตรวจสอบ DOM, Network Requests, Console Logs และทำ Automated UI Debugging |
| **888router** | `/Users/chinnawat.t/workspace/888router/888router` | `https://github.com/voravitl/888router.git` | ระบบ AI/LLM API Router & Gateway พร้อม CLI, `custom-server.js`, Docker Compose และรองรับการ Deploy บน CapRover (`captain-definition`) |
| **9router** | `/Users/chinnawat.t/workspace/9router/9router` | `https://github.com/voravitl/9router.git` | ระบบ LLM Proxy & Routing Server รุ่นปรับปรุง พร้อมการตั้งค่า `docker-compose.override.yml`, CLI และเอกสารการรันผ่าน Container |
| **Ai-Office** | `/Users/chinnawat.t/workspace/Ai-Office` | Local Project | เว็บแอปพลิเคชันจำลองพื้นที่ทำงาน AI Office พัฒนาด้วย React 19, Vite และ Tailwind CSS v4 |

---

## 3. โปรเจคระบบงานจำลองและบอทอัตโนมัติ (Fullstack Demos & Automation Bots)

| ชื่อโปรเจค | Local Path | Git Remote | รายละเอียดและเทคโนโลยี |
| :--- | :--- | :--- | :--- |
| **bot-vertify-slip** | `/Users/chinnawat.t/workspace/bot-vertify-slip` | `https://github.com/OmesCT/Vertify-Bot-Slip.git` | บอท Discord อัตโนมัติสำหรับตรวจสอบสลิปโอนเงินด้วย OCR (`tesseract.js`), เชื่อมต่อ Google Sheets ผ่าน `google-apps-script.js`, ระบบการ์ดต้อนรับสมาชิกใหม่ และชุดทดสอบ Playwright |
| **loan-system-enterprise** | `/Users/chinnawat.t/workspace/loan-system-enterprise` | Local Project | ระบบสินเชื่อระดับองค์กรแบบครบวงจร ประกอบด้วย `frontend/`, `backend/` (Node.js), `infra/k8s/`, `infra/monitoring/` (Prometheus & Grafana), `infra/terraform/` และไฟล์จำลอง `loan-system-demo.html` |
| **banking-ui** | `/Users/chinnawat.t/workspace/banking-ui` | Local Project | ต้นแบบหน้าจอระบบธรรมาภิบาลข้อมูลธนาคาร (`Bank Data Governance Dashboard.html` และ `TCB Bank - Data Governance v2.html`) |
| **app_demo_dotnet-master** | `/Users/chinnawat.t/workspace/app_demo_dotnet-master` | Local Project | โปรเจคตัวอย่างภาษา C# .NET (`app-demo.sln`) สำหรับทดสอบการสร้าง Container และการรันในไปป์ไลน์ CI/CD |
| **api-demo** | `/Users/chinnawat.t/workspace/api-demo` | Local Project | โปรเจคตัวอย่าง Python Backend API (`main.py`) พร้อมหน้าเว็บทดสอบ (`index.html`) |
| **healthy-food-wheel** | `/Users/chinnawat.t/workspace/healthy-food-wheel` | Local Project | เว็บแอปพลิเคชันวงล้อสุ่มเมนูอาหารเพื่อสุขภาพ (`index.html`) |

---

## 4. โปรเจคศึกษาทดลองด้าน DevOps, Kubernetes และ SRE (DevOps, K8s & SRE Labs)

| ชื่อโปรเจค | Local Path | Git Remote | รายละเอียดและเทคโนโลยี |
| :--- | :--- | :--- | :--- |
| **ci** | `/Users/chinnawat.t/workspace/ci` | `https://github.com/OmesCT/ci-cd-test.git` | คลังทดสอบไปป์ไลน์ CI/CD แบบหลายภาษา ประกอบด้วย `csharp-app`, `python-app`, `html-app`, `Dockerfile` และ `Jenkinsfile` |
| **pipeline** | `/Users/chinnawat.t/workspace/pipeline` | `https://github.com/OmesCT/pipeline-study.git` | โปรเจคศึกษาโครงสร้าง Declarative `Jenkinsfile` และการทำงานของ Stage/Step ใน Jenkins |
| **docker-jenkins** | `/Users/chinnawat.t/workspace/docker-jenkins` | Local Project | สภาพแวดล้อม Docker สำหรับรัน Jenkins Controller และ Agent ในเครื่อง พร้อมเก็บโปรเจค `MFT-Pipeline-Project` และ `Jenkinsfiles` |
| **learning_Kubernate / learning_Kubernates / kubernates_test** | `/Users/chinnawat.t/workspace/learning_Kubernate`<br>`/Users/chinnawat.t/workspace/learning_Kubernates`<br>`/Users/chinnawat.t/workspace/kubernates_test` | Local Project | เอกสารสรุปสถาปัตยกรรม Kubernetes และ OpenShift (`K8S_SUMMARY.md`, `kubernetes-openshift-docs.md`) และไฟล์ YAML ทดสอบ (`hello-nginx.yaml`) |
| **learning_kafka** | `/Users/chinnawat.t/workspace/learning_kafka` | Local Project | เอกสารและคู่มือสถาปัตยกรรม Event Streaming ด้วย Apache Kafka (`KAFKA_GUIDE.md`) |
| **learning_slo** | `/Users/chinnawat.t/workspace/learning_slo` | Local Project | ห้องปฏิบัติการด้านวิศวกรรมความเสถียร (SRE) เรื่อง SLI/SLO และ Error Budget พร้อมเซอร์วิสจำลอง `restaurant-api`, `tshirt-shop` และคู่มือ `slo-guide.md` |

---

## 5. สรุปรายงานการปฏิบัติงานสหกิจศึกษารายสัปดาห์ (17 สัปดาห์: 29 มิ.ย. - 19 ต.ค. 2569)

| สัปดาห์ | ช่วงวันที่ | โปรเจคหลัก | งานที่ได้รับมอบหมายประจำสัปดาห์ | ผลการปฏิบัติงานประจำสัปดาห์ | ปัญหาที่พบ | แนวทางการแก้ไข |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **สัปดาห์ที่ 1** | 29 มิ.ย. - 3 ก.ค. 2569 | **MFT-Pipeline** | ศึกษากระบวนการ Deploy ของระบบ MFT แบบเดิม วิเคราะห์โครงสร้างคำสั่ง CLI และตั้งค่าสภาพแวดล้อม Jenkins, Docker และ Harbor Registry | เข้าใจขั้นตอนการทำงานของ MFT CLI ทั้งหมด ตั้งค่า Jenkins Agent เชื่อมต่อ Docker และ Harbor สำเร็จ พร้อมสร้างโครงสร้างตั้งต้นของ `Jenkinsfile-build.groovy` | การรันคำสั่ง MFT CLI ผ่านเครื่องผู้ใช้งานโดยตรงมีขั้นตอนซับซ้อนและเกิดความคลาดเคลื่อนของพารามิเตอร์บ่อยครั้ง | รวบรวมคำสั่ง CLI ทั้งหมดมาบรรจุลง Docker Image มาตรฐานและเตรียมเปลี่ยนผ่านสู่การรันผ่าน Jenkins Pipeline |
| **สัปดาห์ที่ 2** | 6 - 10 ก.ค. 2569 | **MFT-Pipeline** | พัฒนาไปป์ไลน์สำหรับ Export และ Import ข้อมูล MFT Flow พร้อมออกแบบระบบจัดการเลขเวอร์ชันของอิมเมจบน Harbor | ได้ไปป์ไลน์ Export และ Import ที่ทำงานเชื่อมต่อกับ Harbor Registry ได้จริง พร้อมระบบเรียงลำดับเลขเวอร์ชันอิมเมจที่ถูกต้อง | ไฟล์ JSON ที่ได้จากการ Export มีข้อมูลรหัสผ่านและชื่อเซิร์ฟเวอร์ติดมาด้วย และการใช้คำสั่ง `sort` ปกติทำให้เรียงเลขเวอร์ชันผิด (เช่น `build2` มาก่อน `build10`) | ใช้เครื่องมือ `jq` เขียนสคริปต์แทนที่ข้อมูลความลับด้วย `<password>`, `<hostname>`, `<username>` อัตโนมัติ และเปลี่ยนมาใช้ Natural Sort ในการเรียงลำดับเวอร์ชัน |
| **สัปดาห์ที่ 3** | 13 - 17 ก.ค. 2569 | **MFT-Pipeline** | พัฒนาไปป์ไลน์ Rollback แยกโฟลเดอร์ไปป์ไลน์ระหว่าง `release/` และ `draft/` และย้ายโค้ดที่ใช้ซ้ำเข้าสู่ Jenkins Shared Library | ได้ไปป์ไลน์ครบทั้ง 4 กระบวนการ (`Build`, `Export`, `Import`, `Rollback`) และแยกโค้ดออกเป็นโมดูลใน `mft-shared-library` จำนวน 10 ไฟล์ | โค้ดใน Jenkinsfile ทั้ง 4 ไฟล์มีความซ้ำซ้อนสูง และพบข้อจำกัดด้านความปลอดภัย `DOP-4966` เรื่องการส่งรหัสผ่านเข้า Docker Container | สกัดฟังก์ชันหลักออกเป็น Groovy Shared Library (`vars/*.groovy`) และส่งค่าความลับเข้า Docker ด้วยแฟล็ก `-e KEY` เพื่อไม่ให้รหัสผ่านปรากฏใน Process Log |
| **สัปดาห์ที่ 4** | 20 - 24 ก.ค. 2569 | **MFT-Pipeline** | พัฒนาสคริปต์ดึงตัวเลือกแบบไดนามิก (Active Choices) สำหรับหน้าจอ Jenkins และจัดทำเอกสารรายงานสหกิจศึกษาของโปรเจค MFT | ผู้ใช้งานสามารถเลือก Image Tag และ Flow ที่ต้องการผ่าน Dropdown บน Jenkins ได้ทันที และจัดทำเอกสารคู่มือพร้อมรายงานครบ 6 บท | สคริปต์ Groovy บนหน้า UI ของ Jenkins มีข้อจำกัดในการเรียกใช้ฟังก์ชันซับซ้อนและเกิดข้อผิดพลาดเรื่องตัวแปรบ่อยครั้ง | แยกตรรกะการดึงข้อมูลจาก GitLab API และ Harbor API เข้าสู่ Shared Library (`getImageTags`, `getExportTriggers`, `getImportTriggers`, `getRollbackTags`) เพื่อให้โค้ดฝั่ง UI สั้นและเสถียร |
| **สัปดาห์ที่ 5** | 27 - 31 ก.ค. 2569 | **Kubernetes Lab** | พัฒนาแอปพลิเคชันระบบจองคิวร้านอาหาร (`restaurant`) บรรจุลง Docker Container และเขียนไฟล์ Kubernetes Manifests พื้นฐาน | ได้แอปพลิเคชัน Fullstack ที่รันบน Kubernetes Cluster สำเร็จ พร้อมไฟล์ `Deployment`, `Service`, `HTTPRoute`, `ConfigMap` และ `Secret` | คอนเทนเนอร์เริ่มต้นทำงานช้าในบางจังหวะทำให้ Kubernetes สั่งรีสตาร์ท Pod ก่อนที่ระบบจะพร้อมรับทราฟฟิก | กำหนดค่า `startupProbe`, `readinessProbe` และ `livenessProbe` แยกตามหน้าที่อย่างเหมาะสม ทำให้การสลับเวอร์ชันเป็นแบบ Zero-Downtime |
| **สัปดาห์ที่ 6** | 3 - 7 ส.ค. 2569 | **Kubernetes Lab** | เชื่อมต่อระบบแก้ไขรหัสผ่านจากในแอปเข้ากับ Kubernetes API, แยกเซอร์วิส WebSocket และสร้าง Jenkins CI/CD Pipeline | แอปสามารถอัปเดต `Secret` บน Kubernetes ได้เองอย่างปลอดภัย สื่อสารข้าม Pod ด้วย WebSocket สำเร็จ และมีไปป์ไลน์อัตโนมัติครบวงจร | Pod ของแอปไม่สามารถเรียกใช้งาน Kubernetes API เพื่อแก้ไขข้อมูล `Secret` ได้เนื่องจากติดสิทธิ์การเข้าถึง (403 Forbidden) | สร้าง `ServiceAccount` เฉพาะทางพร้อมกำหนด `Role` และ `RoleBinding` ให้มีสิทธิ์เฉพาะการอ่านและแก้ไข `Secret` ใน Namespace ของตนเองตามหลัก Least Privilege |
| **สัปดาห์ที่ 7** | 10 - 14 ส.ค. 2569 | **OpenShift Onboarding** | วิเคราะห์ปัญหาใบคำขอขึ้นระบบแบบ Excel และออกแบบพัฒนาหน้าเว็บฟอร์ม 8 ขั้นตอนพร้อมฐานข้อมูลหลังบ้าน | ได้โครงสร้างระบบ Monorepo (React + NestJS + PostgreSQL) พร้อมหน้าฟอร์มกรอกข้อมูล 8 แท็บที่มีระบบตรวจสอบความถูกต้องครบถ้วน | ข้อมูลที่ต้องกรอกมีจำนวนมากและมีความสัมพันธ์ซับซ้อน ทำให้ผู้ใช้สับสนหากแสดงทั้งหมดในหน้าเดียว | แบ่งฟอร์มออกเป็น 8 แท็บตามลำดับการทำงานจริง พร้อมระบบตรวจสอบค่าว่างและรูปแบบชื่อทรัพยากรตามมาตรฐาน OpenShift ก่อนอนุญาตให้ข้ามขั้นตอน |
| **สัปดาห์ที่ 8** | 17 - 21 ส.ค. 2569 | **OpenShift Onboarding** | เชื่อมต่อระบบยืนยันตัวตน Red Hat Keycloak SSO และพัฒนาการดึงข้อมูลรายชื่อโปรเจคจาก GitLab และ Jenkins แบบอัตโนมัติ | ระบบล็อกอินด้วย Keycloak SSO แยกสิทธิ์ตามทีม (`WAS1`, `WAS2`) สำเร็จ และมีช่องค้นหา GitLab/Jenkins แบบ Autocomplete ที่ใช้งานได้จริง | การเรียก GitLab API และ Jenkins API จากฝั่งเบราว์เซอร์โดยตรงติดปัญหา CORS และเสี่ยงต่อการรั่วไหลของ Token | สร้าง Backend Proxy ใน NestJS เพื่อเป็นตัวกลางในการแนบ Token และดึงข้อมูลจาก GitLab/Jenkins แทนฝั่ง Frontend |
| **สัปดาห์ที่ 9** | 24 - 28 ส.ค. 2569 | **OpenShift Onboarding** | พัฒนาระบบผูกเซอร์วิส (`MongoDB`, `Kafka`, `Kong`) แยกราย Environment, ระบบแจ้งเตือนสถานะแบบ SSE และตัวสร้างข้อความขอเปิด Firewall | ผู้ใช้ตั้งค่าเซอร์วิสแยกตาม `DEV`/`SIT`/`UAT` ได้ครบถ้วน หน้า Dashboard อัปเดตสถานะแบบเรียลไทม์ผ่าน SSE และสร้างโน้ตขอ Firewall สำหรับ Jira/SDP ได้ทันที | การผูกเซอร์วิสแต่ละตัวใช้พอร์ตและโปรโตคอลต่างกันในแต่ละ Environment ทำให้ผู้ใช้งานกรอกข้อมูลขอเปิด Firewall ผิดพลาดบ่อย | สร้างตาราง Mapping พอร์ตและ IP ปลายทางอัตโนมัติตามชนิดเซอร์วิสและ Environment แล้วแปลงเป็นข้อความสำเร็จรูปสำหรับคัดลอกไปวางใน Jira และ SDP |
| **สัปดาห์ที่ 10** | 31 ส.ค. - 4 ก.ย. 2569 | **OpenShift Onboarding** | พัฒนาระบบส่งออกไฟล์ YAML (`Kustomize`, `ArgoCD`, `Jenkinsfile`) เป็นไฟล์ ZIP และปรับปรุงการ Build Docker Image ให้รวดเร็วขึ้น | ระบบสร้างและดาวน์โหลดไฟล์ ZIP ที่พร้อมนำไปรันบน OpenShift ได้ทันที และลดเวลาการ Build อิมเมจในไปป์ไลน์จาก 7 นาที เหลือ 1.5 นาที | การแยกสร้างและส่งมอบคอนเทนเนอร์ระหว่าง Frontend และ Backend ใช้เวลา Build นานและจัดการไฟล์ตั้งค่ายุ่งยาก | รวมขั้นตอนการ Build ทั้ง Frontend และ Backend เข้าด้วยกันใน Multi-stage Dockerfile เดียว โดยให้ NestJS ทำหน้าที่เสิร์ฟไฟล์ Static ของ React ไปพร้อมกัน |
| **สัปดาห์ที่ 11** | 7 - 11 ก.ย. 2569 | **FITs (IT Budget)** | ศึกษาข้อกำหนดระบบบริหารงบประมาณไอที ออกแบบฐานข้อมูล PostgreSQL 16 และพัฒนาโครงสร้างหลักของ `.NET 10 API` และ `React 19` | ได้โครงสร้างฐานข้อมูลและ API พื้นฐานของระบบ FITs พร้อมตัวสร้างรหัสงบประมาณอัตโนมัติ (`BGID`) ที่ทำงานได้อย่างถูกต้อง | การสร้างรหัส `BGID` พร้อมกันหลายรายการมีความเสี่ยงที่จะได้เลขลำดับซ้ำกันหากไม่มีการจัดการ Concurrency ที่ดี | ออกแบบกลไกการรันเลขลำดับภายใต้ Transaction Lock ของฐานข้อมูล พร้อมตรวจสอบเงื่อนไขปีงบประมาณ ประเภทงบ และรหัสหน่วยงานอย่างรัดกุม |
| **สัปดาห์ที่ 12** | 14 - 18 ก.ย. 2569 | **FITs (IT Budget)** | พัฒนาฟอร์มบันทึกงบประมาณแบบ Structure A และ Structure B พร้อมระบบคำนวณและแบ่งงบประมาณข้ามปีงบประมาณ | ผู้ใช้สามารถกรอกรายละเอียดค่าใช้จ่ายรายหมวดและแบ่งสัดส่วนงบประมาณข้ามปี (ทั้งแบบเฉลี่ย 12 เดือนและกำหนดเอง) ได้อย่างแม่นยำ | การคำนวณตัวเลขทศนิยมในการแบ่งงบข้ามปีอาจเกิดเศษปัดทศนิยมที่ทำให้ผลรวมรายเดือนไม่ตรงกับยอดรวมของสัญญา | ใช้ชนิดข้อมูล `decimal` ความละเอียดสูงในฝั่ง `.NET` และเพิ่มตรรกะปรับเกลี่ยเศษทศนิยมเข้าเดือนสุดท้ายของสัญญาเพื่อให้ยอดรวมตรงกัน 100% |
| **สัปดาห์ที่ 13** | 21 - 25 ก.ย. 2569 | **FITs (IT Budget)** | พัฒนาระบบควบคุมสถานะงบประมาณ 6 ขั้นตอน, กฎ Maker-Checker, การส่งกลับแก้ไขแบบบังคับระบุเหตุผล (`Story 2.2`) และการอนุมัติระดับผู้บริหาร (`Story 2.3`) | ระบบควบคุมการเปลี่ยนสถานะงบประมาณได้ตามสิทธิ์จริง ป้องกันการอนุมัติรายการของตนเอง และรองรับทั้งการส่งกลับแก้ไขและการอนุมัติตรงโดยผู้บริหาร | ผู้ใช้งานบางบทบาทพยายามกดอนุมัติคำของบที่ตนเองเป็นผู้สร้าง หรือส่งกลับคำขอโดยไม่ระบุสาเหตุทำให้ผู้ขอไม่ทราบจุดที่ต้องแก้ไข | บังคับตรวจสอบ `RequesterUserId != ReviewerUserId` ในระดับ API ทุกครั้ง และบังคับให้แนบข้อความเหตุผล (`Reason`) ที่ไม่เป็นค่าว่างเมื่อสั่ง `SendBack` |
| **สัปดาห์ที่ 14** | 28 ก.ย. - 2 ต.ค. 2569 | **FITs (IT Budget)** | พัฒนาเครื่องมือจำลองการปรับลดงบประมาณ 4 ลำดับขั้น (4-Tier Waterfall Cut Simulator) และระบบสมุดบัญชีคู่สำหรับจองวงเงินใบสั่งซื้อ (Dual Ledger PO Booking) | ผู้บริหารสามารถจำลองการตัดลดงบประมาณตามลำดับความสำคัญได้ทันที และระบบป้องกันการออกใบสั่งซื้อ (PO) เกินวงเงินที่ได้รับอนุมัติได้อย่างแม่นยำ | เมื่อมีการปรับลดงบประมาณแล้วยอดตั้งต้นในระบบเดิมถูกเขียนทับ ทำให้ไม่สามารถตรวจสอบย้อนหลังได้ว่ายอดที่ขออนุมัติครั้งแรกเป็นเท่าใด | แยกโครงสร้างข้อมูลเป็นสมุดบัญชีคู่ (`Approved Plan` คู่กับ `Actual Spent`) เพื่อรักษาประวัติวงเงินที่ได้รับอนุมัติแยกจากยอดใช้งานจริง |
| **สัปดาห์ที่ 15** | 5 - 9 ต.ค. 2569 | **FITs (IT Budget)** | พัฒนาระบบนำเข้าและส่งออกไฟล์ Excel สำหรับเชื่อมต่อบัญชีแยกประเภท Dynamics 365 (GL Mapping) และระบบบันทึกประวัติแบบโซ่แฮช (`SHA-256 Hash-Chained Audit Log`) | ระบบส่งออกไฟล์ Excel ตามเทมเพลตบัญชี D365 ได้ถูกต้อง และทุกการเปลี่ยนแปลงข้อมูลถูกบันทึกพร้อมค่าแฮชต่อเนื่องตามมาตรฐาน ธปท. | ข้อมูลประวัติการแก้ไขแบบตารางทั่วไปสามารถถูกแก้ไขย้อนหลังในฐานข้อมูลได้โดยไม่มีร่องรอย หากผู้ดูแลระบบเข้าถึงฐานข้อมูลโดยตรง | นำอัลกอริทึม `SHA-256` มาคำนวณแฮชของข้อมูลปัจจุบันร่วมกับแฮชของรายการก่อนหน้า (`prev_hash`) หากข้อมูลแถวใดถูกแก้ไขจะตรวจพบการขาดของโซ่แฮชทันที |
| **สัปดาห์ที่ 16** | 12 - 16 ต.ค. 2569 | **FITs (IT Budget)** | พัฒนาระบบแสดงผู้ใช้งานออนไลน์แบบเรียลไทม์ด้วย SignalR (`Story 2.4`), เชื่อมต่อระบบล็อกอิน AAA OIDC SSO และซิงค์ข้อมูลหน่วยงานจาก HRMS | ผู้ใช้เห็นรายชื่อเพื่อนร่วมงานที่กำลังเปิดดูงบรายการเดียวกันแบบเรียลไทม์ ล็อกอินผ่าน SSO ได้สมบูรณ์ และข้อมูลแผนกอัปเดตตรงตามฐานข้อมูลบุคคล | เมื่อผู้ใช้หลายคนเปิดแก้ไขงบรายการเดียวกันพร้อมกันโดยไม่ทราบ ทำให้เกิดการบันทึกข้อมูลทับกัน | ใช้ `SignalR Hub` จัดการกลุ่มการเชื่อมต่อตามรหัส `BGID` เพื่อแจ้งเตือนผู้ที่กำลังเปิดดูรายการเดียวกันอยู่บนหน้าจอทันที |
| **สัปดาห์ที่ 17** | 19 ต.ค. 2569 | **FITs (IT Budget) & All Projects** | ตั้งค่าคอนเทนเนอร์แบบ Non-Root สำหรับ OpenShift, รันชุดทดสอบอัตโนมัติ Playwright E2E และรวบรวมเอกสารสรุปผลงานทั้งหมด | คอนเทนเนอร์ทั้งหมดผ่านเกณฑ์ความปลอดภัยของ OpenShift ชุดทดสอบ Playwright E2E ผ่านครบทุกกรณี และจัดทำรายงานสรุปผลการปฏิบัติงานครบทั้ง 4 โปรเจคหลัก | คอนเทนเนอร์มาตรฐานบางตัวพยายามรันด้วยสิทธิ์ `root` (UID 0) ทำให้ไม่สามารถรันภายใต้ Security Context Constraints (SCC) ของ OpenShift ได้ | ปรับปรุง `Dockerfile` และค่าตั้งต้นของพอร์ตให้ทำงานภายใต้ Non-Root User (เช่น พอร์ต 8080 แทนพอร์ต 80) และกำหนดสิทธิ์โฟลเดอร์ให้รองรับ Arbitrary UID ของ OpenShift |
