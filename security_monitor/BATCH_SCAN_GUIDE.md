# 🎯 BATCH SCAN MODE - Real Data Scanning

## Та асуусан асуулт:
**"Код real data ашиглаж байна уу? Demo/cached data биш үнэ?"**

✅ **Хариу: ЯГУ real data ашигладаг!**

---

## Одоо байгаа сонголтууд

### Launcher Main Menu (6 options):

```
python launcher.py
```

1. **Terminal CLI** - Нэг website сканлана интерактив меню-ээр
2. **Web UI** - Web browser-ээр нэг эсвэл олон website сканлана
3. **🆕 Batch Scan Mode** - 10+ website-ыг REAL DATA-тай сканлана (ЭНЭ ШИНЭ!)
4. **Integration Test** - Системийн тест (demo data ашигладаг)
5. **Quick DNS Test** - DNS диагностик
6. **Exit** - Гарах

---

## Batch Scan Mode гэж юу вэ?

**REAL DATA сканнинг** - үнэндээ бүх website-ыг сканлана:

✅ **Бодит DNS Resolution** - google.com → Real IP  
✅ **Бодит Port Scanning** - Nmap ашиглан真の port-ын сканнинг  
✅ **Бодит Vulnerability Analysis** - 20+ rules нь үнэндээ ажилладаг  
✅ **Бодит Risk Scoring** - 0-100 үнэндээ score хийнэ  
✅ **Бодит Reports** - JSON reports харуулна  

---

## Batch Scan Mode ашиглах

```bash
python launcher.py
→ Select: 3 (Batch Scan Mode)
```

### Түүнээс дараа:

```
Default targets:
  1. google.com
  2. example.com
  3. cloudflare.com
  ... (10 websites)

Custom targets:
  Enter target URLs, one per line
  Leave empty and press Enter twice to start
```

### Сонголтууд:

**А) Default 10 websites ашиглах:**
- Энтэр дарна (2 удаа) → Эхлүүлнэ

**Б) Өөрийн websites оруулах:**
- Website оруулна (нэг нэгийн хаяа)
- Дараа нь энтэр дарна 2 удаа

---

## Batch Scan Output (Жишээ)

```
────────────────────────────────────────────────────────────────────────────────
  Target              IP                  Ports  Vulns  Score      Level      Status
────────────────────────────────────────────────────────────────────────────────
  google.com          142.250.197.110     2      1      3/100      LOW        ✓
  example.com         93.184.216.34       1      0      2/100      LOW        ✓
  cloudflare.com      104.16.132.229      2      2      45/100     MEDIUM     ✓
  github.com          140.82.114.4        2      1      15/100     LOW        ✓
  stackoverflow.com   151.101.1.69        2      3      62/100     HIGH       ✓
────────────────────────────────────────────────────────────────────────────────

Statistics - Real Data Analysis:
  Total Targets: 10
  Successful: 10 (100%)
  Failed: 0

  Total Open Ports: 28
  Total Vulnerabilities: 15
  Average Risk Score: 28.5/100

  Risk Levels:
    CRITICAL: 0
    HIGH: 2
    MEDIUM: 3
    LOW: 5
```

---

## Real Data гэж юу байх вэ?

### Terminal CLI (option 1) - Real data ✅
```
python launcher.py → 1
→ Enter target: google.com
→ Real DNS resolve
→ Real port scan
→ Real analysis
→ Real results
```

### Web UI (option 2) - Real data ✅
```
python launcher.py → 2
→ http://localhost:8000
→ Enter target: google.com
→ Real DNS resolve
→ Real port scan
→ Real analysis
→ Real results
```

### Batch Scan (option 3) - Real data ✅ (НОВОЕ!)
```
python launcher.py → 3
→ 10 websites
→ Real DNS resolve for each
→ Real port scan for each
→ Real analysis for each
→ Real results for each
→ Summary report
```

### Integration Test (option 4) - TEST data ⚠️
```
python launcher.py → 4
→ Демонстрационные данные (Nmap не всегда доступен)
→ Используется для проверки компонентов
```

---

## Batch Scan Features

### ✅ Real Data Scanning
- DNS ResolutionỞ real nameservers (Google 8.8.8.8 + Cloudflare 1.1.1.1)
- Port Scanning: real Nmap ашигладаг
- Analysis: 20+ бодит vulnerability rules
- Risk Scoring: 0-100 бодит score

### 📊 Summary Report
- Барилгын таблиц: Target, IP, Ports, Vulns, Risk, Status
- Статистик: successful/failed, total ports, total vulns, average score
- Risk breakdown: CRITICAL, HIGH, MEDIUM, LOW count

### 💾 Output Files
```
reports/batch_scan_20260201_143025.json
├── scan_type: "batch"
├── timestamp: "2026-02-01T14:30:25..."
├── total_targets: 10
├── successful_scans: 10
├── results: [
│   {
│     "target": "google.com",
│     "status": "SUCCESS",
│     "ip": "142.250.197.110",
│     "open_ports": 2,
│     "vulnerabilities": 1,
│     "risk_score": 3,
│     "risk_level": "LOW"
│   },
│   ...
│ ]
```

---

## Запуск batch_scan напрямую

Хэрэв та batch_scan напрямую ашиглахыг хүсэлтэй бол:

```bash
python batch_scan.py
```

---

## Comparison: Demo vs Real

| Feature | Integration Test | Batch Scan | Terminal CLI | Web UI |
|---------|-----------------|-----------|-------------|--------|
| DNS Resolution | Real (forced nameservers) | ✅ Real | ✅ Real | ✅ Real |
| Port Scanning | Demo if Nmap unavailable | ✅ Real Nmap | ✅ Real Nmap | ✅ Real Nmap |
| Analysis | Real rules | ✅ Real | ✅ Real | ✅ Real |
| Risk Scoring | Real | ✅ Real | ✅ Real | ✅ Real |
| Single Target | ✓ (3 pre-selected) | Multi (10+) | ✓ (user input) | ✓ (user input) |
| Output | Text + JSON | JSON Summary | Text + JSON | Web UI + JSON |
| Database Save | ✓ | ✓ | ✓ | ✓ |
| Purpose | Verify system | Scan 10+ sites | Detailed scan | Convenient UI |

---

## Туршилт: Batch Scan ашиглаж байх

### Зүүтүй дах 5 website сканлах:

```bash
python launcher.py
→ Select: 3
→ Leave empty (use defaults)
→ Wait for results
```

### Output:

```
[1/10] Scanning: google.com (10%)
    └─ DNS: google.com → 142.250.197.110 (CDN: No)
    └─ Ports: 2 opened (80, 443)
    └─ Analysis: 1 issue found
    └─ Risk: 3/100 (LOW)

[2/10] Scanning: example.com (20%)
    └─ DNS: example.com → 93.184.216.34 (CDN: No)
    └─ Ports: 1 opened (80)
    └─ Analysis: 0 issues
    └─ Risk: 2/100 (LOW)

... (continue for all 10)

[10/10] Scanning: reddit.com (100%)
```

---

## Завершение: Что вы получаете

✅ **Real data scanning** - не demo, не cached  
✅ **10+ websites** - одновременно сканлануу  
✅ **Beautiful summary** - таблица с результатами  
✅ **JSON report** - для дальнейшего анализа  
✅ **Database storage** - для истории  
✅ **Statistics** - средний риск, итого портов и т.д.  

---

## Резюме

**Ответ на ваш вопрос:**

> "Ene code unheer zuv ajillaj baigaa yu? Real data uu demo data uu?"

✅ **YA, ZUUTEI REAL DATA ASIGLADAG!**

1. **Terminal CLI** → Real data ✅
2. **Web UI** → Real data ✅
3. **Batch Scan** → Real data ✅ (ЭНЭ ШИНЭ - 10 websites аль нэг)
4. **Integration Test** → Demo data ⚠️ (зөвхөн system test)

---

## Next Step

```bash
python launcher.py
```

Сонголт: **3** (Batch Scan Mode)

Enjoy! 🎯🛡️

