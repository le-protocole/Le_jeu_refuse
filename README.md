## 项目简介
本系统用于在**不入侵、不利用漏洞、不访问数据**的前提下，
评估网络与网站的安全态势（Security Posture）。
仅适用于测试、教学和演示，并且只能在获得授权的环境中使用。

---

##  免责声明
本系统：
- 仅用于测试和演示
- 不针对任何官方机构或个人
- 不执行入侵、登录、漏洞利用或数据提取行为
- 对任何未经授权的使用不承担责任

---

## 🛠 核心技术

### 1. 扫描技术
- **Nmap（主要）**
  - TCP SYN 扫描
  - 服务与版本识别
  - 操作系统识别
- **Python Socket（备用）**
  - ThreadPoolExecutor（10–15 线程）
- **自动回退**
  - Nmap 失败时自动使用 Python

---

### 2. DNS 技术
- `dnspython` 库
- 支持记录类型：
  - A, AAAA, MX, TXT, CNAME
- 实时 DNS 验证（无缓存）

---

### 3. 漏洞识别
- 基于规则的模式匹配
- 服务与端口关联分析
- 加权风险评分算法

---

### 4. 并行处理
- ThreadPoolExecutor（10–15 线程）
- 并发扫描
- 批量处理

---

### 5. 数据库
- SQLite
- 六表结构
- 参数化查询（防 SQL 注入）
- 索引优化提升性能

---

### 6. Web 架构
- FastAPI – REST API
- WebSocket – 实时更新
- JSON 轮询（每 10 秒）

---

### 7. 安全标准
- CIS Benchmarks
- OWASP Top 10
- PCI-DSS
- 自定义规则

---

### 8. 错误处理
- 自动重试（指数退避）
- 回退机制
- 扫描状态保持

---

##  项目目标
- 安全态势评估
- 非侵入式侦察
- 蓝队、安全研究、演示用途

---



## Présentation du projet
Ce système est conçu pour évaluer la **posture de sécurité réseau et web**
sans intrusion, exploitation ou accès aux données.
Il est destiné uniquement à des fins de test, d’éducation et de démonstration,
et doit être utilisé dans des environnements autorisés.

---

##  Avertissement
Ce système :
- Est destiné uniquement aux tests et démonstrations
- Ne constitue aucune menace envers une organisation ou un individu
- N’effectue aucune intrusion, authentification, exploitation ou extraction de données
- L’auteur décline toute responsabilité en cas d’utilisation non autorisée

---

## 🛠 Techniques principales

### 1. Techniques de scan
- **Nmap (principal)**
  - TCP SYN Scan
  - Détection de services et versions
  - Détection du système d’exploitation
- **Sockets Python (secours)**
  - ThreadPoolExecutor (10–15 workers)
- **Fallback automatique**
  - Utilisation de Python en cas d’échec de Nmap

---

### 2. Techniques DNS
- Bibliothèque `dnspython`
- Enregistrements supportés :
  - A, AAAA, MX, TXT, CNAME
- Vérification DNS en temps réel (sans cache)

---

### 3. Détection des vulnérabilités
- Règles basées sur des patterns
- Détection des services par port
- Scoring des risques (algorithme pondéré)

---

### 4. Traitement parallèle
- ThreadPoolExecutor (10–15 threads)
- Scan concurrent
- Traitement par lots

---

### 5. Base de données
- SQLite
- Structure à 6 tables
- Requêtes paramétrées (protection SQL injection)
- Optimisation des index

---

### 6. Architecture Web
- FastAPI – API REST
- WebSocket – mises à jour en temps réel
- JSON polling toutes les 10 secondes

---

### 7. Référentiels de sécurité
- CIS Benchmarks
- OWASP Top 10
- PCI-DSS
- Règles personnalisées

---

### 8. Gestion des erreurs
- Reprise automatique (exponential backoff)
- Mécanismes de secours
- Conservation de l’état des scans

---

##  Objectif
- Évaluation de la posture de sécurité
- Reconnaissance non intrusive
- Usage Blue-team, bug bounty et démonstration

---




## Төслийн танилцуулга
Энэхүү систем нь сүлжээ болон веб орчны **аюулгүй байдлын байршил (security posture)**-ыг
нэвтрэх, эвдэх, exploit хийхгүйгээр үнэлэхэд зориулагдсан.
Зөвхөн туршилт, боловсрол, танилцуулга (demo) болон зөвшөөрөлтэй орчинд ашиглагдана.

---

##  Анхааруулга (Disclaimer)
Энэхүү систем нь:
- Зөвхөн тест болон demo зорилготой
- Ямар нэгэн албан ёсны байгууллага эсвэл хувь хүнд заналхийлэхгүй
- Нэвтрэх оролдлого, login, exploit, өгөгдөл татах (data dump) үйлдэл хийхгүй
- Зөвшөөрөлгүй ашиглалтад зохиогч хариуцлага хүлээхгүй

---

## 🛠 Үндсэн Техникүүд

### 1. Сканнинг Техник
- **Nmap (Үндсэн)**
  - TCP SYN Scan
  - Service / Version Detection
  - OS Detection
- **Python Socket (Fallback)**
  - ThreadPoolExecutor (10–15 worker)
- **Automatic Fallback**
  - Nmap алдаа өгвөл Python socket-д шилжинэ

---

### 2. DNS Техник
- `dnspython`
- Дэмжих рекордууд:
  - A, AAAA, MX, TXT, CNAME
- Real-time DNS шалгалт (cache ашиглахгүй)

---

### 3. Эмзэг Байдлын Илрүүлэлт
- Pattern-based rules (сүлжээний дүрмүүд)
- Service detection (порт ↔ үйлчилгээ)
- Risk scoring (жинлэсэн алгоритм)

---

### 4. Параллель Боловсруулалт
- ThreadPoolExecutor (10–15 thread)
- Concurrent scanning
- Batch processing

---

### 5. Мэдээллийн Сан
- SQLite
- 6 хүснэгттэй бүтэц
- Parameterized queries (SQL injection-оос хамгаалсан)
- Index optimization (query хурд)

---

### 6. Вэб Архитектур
- **FastAPI** – REST API
- **WebSocket** – Real-time update
- JSON polling – 10 секунд тутам

---

### 7. Баталгаажуулалт (Standards)
- CIS Benchmarks
- OWASP Top 10
- PCI-DSS
- Сонгомол (custom) дүрмүүд

---

### 8. Алдаа Нөхөлт
- Automatic retry (Exponential backoff)
- Fallback механизм
- State preservation (скан төлөв хадгална)

---

##  Зорилго
- Security posture үнэлгээ
- Non-intrusive reconnaissance
- Blue-team, bug bounty, demo зориулалт

---
