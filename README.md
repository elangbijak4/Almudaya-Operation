# Almudaya Agentic Operation (`#Operation`) — Dynamic Swarm Manifold Edition (`v0.3`)

> **Status Repositori — Fase A Selesai & Terverifikasi (*Dynamic Swarm Manifold Upgrade + Post-Audit Remediation*)**  
> Repositori ini memuat spesifikasi kanonik **`almudaya.operation/v0.3` (Dynamic Swarm Manifold Edition)**, naskah revisi makalah **`v0.4`**, validator semantik statis & unit test (`0` galat lintas 7 Operation `v0.3` dan 3 Operation `v0.2` yang telah diremediasi), serta tetap menyimpan arsip draf makalah `v0.3` (PDF) dan *scaffold* awal `v0.1` secara utuh sebagai catatan evolusi historis.

---

## 1. Gambaran Umum Gagasan: `#Skill` → `#Operation` sebagai *Dynamic Swarm Manifold*

Dalam sistem agen modern berbasis *Large Language Model* (LLM), **`#Skill`** bertindak sebagai paket kapabilitas prosedural untuk agen tunggal (instruksi domain, prosedur, skrip, serta sumber daya *progressive disclosure*). Namun, ketika misi kompleks menuntut kolaborasi banyak agen, sekadar membagikan `#Skill` yang sama atau berbeda tidak menjawab siapa pemilik berkas, peran mana yang harus dipisahkan secara epistemik untuk mencegah bias konfirmasi, bagaimana penulisan paralel di-*fence*, kapan agen harus lahir atau gugur, serta bagaimana batas pengulangan dan *rollback* ditegakkan.

Untuk menyatukan gagasan `#Operation` dengan filosofi runtime **Almudaya Multi-Agent (`v0.3.6+`)**—di mana agen dibentuk dan dimusnahkan secara *real-time* (*on-the-fly*) tanpa mengasumsikan *predefined pipeline* yang kaku—**`#Operation` (`almudaya.operation/v0.3`)** dirumuskan sebagai **Generator Medan Topologi Dinamis (*Dynamic Swarm Manifold Field*)**:

- **`#Skill`** → **Kapabilitas Prosedural** (*bagaimana satu agen menjalankan kategori tugas*).
- **`#Operation`** → **Spesifikasi Manifold Organisasi Misi** (*bagaimana potensi peran, batas protokol, anti-affinity, kontrak sumber daya, OBS, dan tata kelola menggerakkan topologi swarm yang lahir, menyusut, dan bubar secara dinamis saat runtime*).

### Pilar Utama `almudaya.operation/v0.3`
1. **Peta Realisasi Dinamis $\mu_t : R_{\text{active}}(t) \rightrightarrows B_t$**: `manifold.roles` bukan lagi daftar proses bot statis, melainkan **Role Archetypes** dengan kebijakan siklus hidup *ephemeral* (`spawn_trigger`, `recycle_eligible`, `dissolve_on`, `coalescable`) yang terikat langsung ke `SpawnManager`.
2. **Kontinum Matematis $L=1 \leftrightarrow L>1$ (Proposisi 1)**: Ketika `l1_single_agent_fallback = true` dan kompleksitas tugas rendah ($|B_t|=1$), $\mu_t$ menyusut (*role coalescing*) secara isomorfik menjadi eksekusi satu agen ber-`#Skill` di bawah `PrGate`; ketika kompleksitas meningkat, manifold berekspansi secara elastis melahirkan *worker swarm* tanpa mengganti definisi misi.
3. **Invarian Pemisahan Tugas (`anti_affinity`)**: Menetapkan pasangan peran yang wajib dijalankan oleh proses bot terpisah (`strict_distinct_bot`, mis. `developer` vs `reviewer` atau `manuscript_writer` vs `citation_verifier`/`quality_refiner`), atau diizinkan pada mode $L=1$ hanya melampaui isolasi konteks dan peningkatan `fenceEpoch` (`epoch_reset_required`).
4. **Tiga Rezim Orkestrasi + Kristalisasi *On-the-Fly***:
   - `emergent`: Swarm stigmergik murni (`seed_stages: []`, `allow_dynamic_task_mutation: true`) dengan dukungan sintesis & kristalisasi topologi sukses ke Registry (`crystallization_policy`).
   - `blueprint_seeded`: Menyemai kerangka `GoalLedger` awal yang bebas bermutasi secara adaptif.
   - `stage_gated`: Gerbang fase ketat dengan *worker* *ephemeral* per tahap (mis. *PaperOrchestra Research Pipeline*).
5. **Pemetaan 1-ke-1 ke Primitif Nyata `Almudaya-Multi-Agent`**: Terikat langsung ke `GoalLedger`, 10 protokol atomik `IProtocol` (`PrBot`, `PrBotGlobal`, `PrIterasi`, `PrDE`, `PrMEend`, `PrModerator` *monotonic write-fencing*, `PrTransfer`, `PrMasterFailover`, `PrGate`, `PrReattach`), `ACG`, `DynamicRulesStore`, `SessionSkillBinding`, `PKU` (*PKU-First*), dan `MCP`.

---

## 2. Ringkasan Makalah: Draf `v0.3` (Arsip) & Naskah Revisi `v0.4`

- **Naskah Revisi Terkini (`v0.4` — *Dynamic Swarm Manifold Edition*)**: [paper/From_Agentic_Skills_to_Agentic_Operations_v0_4.md](./paper/From_Agentic_Skills_to_Agentic_Operations_v0_4.md) · [LaTeX (.tex)](./paper/From_Agentic_Skills_to_Agentic_Operations_v0_4.tex) · [BibTeX (.bib)](./paper/references.bib).
- **Arsip Draf Awal (`v0.3` PDF)**: [From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf](./From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf).

### Posisi Konseptual & Model Formal `v0.3`/`v0.4`
Makalah memisahkan secara tegas antara spesifikasi berversi **Operation Definition (`OD`)**—disederhanakan menjadi tupel 10 komponen ortogonal $OD = (I, M, R, T, C, W, B, Q, G, X)$—dan instansiasi dinamis **Operation Instance (`OI(t)`)** $= (OD, \Theta, E(t), \Sigma(t), K(t))$.

| Abstraksi | Fokus Utama | Pertanyaan yang Dijawab |
|---|---|---|
| **Agent / Bot** | Proses eksekusi otonom | Entitas aktif mana yang menjalankan unit tugas saat ini? |
| **Skill (`#Skill`)** | Kapabilitas prosedural | Bagaimana satu agen menjalankan kategori tugas melalui *progressive disclosure*? |
| **Tool / MCP** | Antarmuka kapabilitas eksternal | Alat atau server MCP apa yang boleh dipanggil oleh suatu peran? |
| **Workflow** | Graf ketergantungan tugas | Bagaimana tugas saling bergantung dan memicu kelanjutan? |
| **Memory (Blackboard / PKU)** | *State* transien & pengetahuan persisten | Informasi apa yang dibagi sesaat atau dipertahankan lintas siklus? |
| **Operation (`#Operation`)** | Manifold organisasi swarm dinamis | Bagaimana topologi multi-agen dibentuk, diperlengkapi, di-*fence*, dikoordinasikan, dan dibatasi untuk menuntaskan misi? |

Enam kontribusi utama (`C1`–`C6`) dalam naskah `v0.4`:
- **C1**: Formalisasi pengangkatan komposisional `#Skill → #Operation` beserta **Proposisi 1** (reduksi degeneratif $L=1 \leftrightarrow L>1$).
- **C2**: Tupel ortogonal 10 komponen `OD` dengan *Role Archetypes* *ephemeral*, *role coalescing*, `anti_affinity`, dan 3 rezim orkestrasi.
- **C3**: Formalisasi **OBS** berbasis AST deterministik `PredicateExpr` dan pemisahan `feedback_sources` bertipe `role` vs `resource_evaluator`.
- **C4**: Pengikatan langsung ke 10 protokol atomik (`IProtocol`), *write-fencing* `CapabilityToken`, serta delegasi hierarkis *sub-manifold*.
- **C5**: Kajian posisi komparatif terhadap **MOISE+**, **OperA**, **JaCaMo**, **MetaGPT**, **AutoGen**, **MCP**, dan **A2A**, plus validator statis.
- **C6**: Demonstrasi tersinkronkan atas *PaperOrchestra* (`#Operation-researchPipeline`) serta pola *emergent*, *looping*, dan *multi-hierarchy*.

---

## 3. Struktur Direktori Repositori

```text
.
├── .gitignore
├── LICENSE
├── README.md
├── From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf  # Arsip PDF v0.3
├── paper/                                      # Naskah revisi v0.4 (Dynamic Swarm Manifold Edition)
│   ├── From_Agentic_Skills_to_Agentic_Operations_v0_4.md
│   ├── From_Agentic_Skills_to_Agentic_Operations_v0_4.tex
│   └── references.bib
├── almudaya_operation_v0_3/                    # Spesifikasi kanonik v0.3 (7 Operations valid)
│   ├── OPERATION_SPECIFICATION_v0_3.md
│   ├── manifest.json
│   ├── schemas/operation.schema.json           # JSON Schema Draft 2020-12 ketat + PredicateExpr AST
│   ├── shared/
│   │   ├── manifold-protocol-mapping.md        # Pemetaan 1-ke-1 ke Almudaya-Multi-Agent v0.3.6
│   │   └── runtime-state-machine.md            # Siklus hidup OI & transisi L=1 <-> swarm
│   ├── 01_emergent_bug_hunt/                   # Rezim emergent (seed_stages: [], L=1 fallback, kristalisasi)
│   ├── 02_iterative_quality_loop/              # Rezim blueprint_seeded (loop implement-test-review-evaluate)
│   ├── 03_multi_hierarchy_manifold/            # Parent sub-manifold + 3 child sub_operations konkret
│   │   └── sub_operations/
│   │       ├── research_branch/
│   │       ├── technical_assessment/
│   │       └── integration_quality_gate/
│   └── 04_research_pipeline/                   # Rezim stage_gated (Konversi PaperOrchestra v0.3.0)
├── almudaya_operation_scaffold_v0_2/           # Scaffold v0.2 (telah diremediasi kontradiksi skemanya)
├── almudaya_operation_researchPipeline_v0_1/   # Research Pipeline v0.2 (telah diremediasi parity & skemanya)
├── almudaya_operation_scaffold_v0_1/           # Arsip historis PoC v1alpha1
├── tools/
│   └── validate_operations.py                  # Static Semantic Validator CLI + evaluator PredicateExpr
└── tests/
    └── test_validator.py                       # Suite unit test validator & regresi semantik
```

---

## 4. Validasi Semantik Statis & Pengujian

Jalankan perintah berikut dari akar repositori untuk memverifikasi seluruh skema, konsistensi lintas-berkas, kontrak *parent–child*, deteksi siklus DAG, dan predikat OBS:

```powershell
python tools/validate_operations.py
python -m unittest discover -s tests -v
```

Hasil verifikasi saat ini:
- **`validate_operations.py`**: Lulus penuh (`0` galat) pada **7 Operation `v0.3`** serta **3 Operation `v0.2`** yang diremediasi.
- **`test_validator.py`**: **8 dari 8 pengujian lulus (`OK`)**, mencakup validasi positif seluruh *registry* `v0.3`/`v0.2`, evaluasi AST predikat penerimaan & *rollback* *PaperOrchestra*, serta penolakan otomatis terhadap siklus tahap, siklus referensi *sub-operation*, konflik `l1_single_agent_fallback` vs `strict_distinct_bot`, pencampuran *resource* sebagai *role* pada `feedback_sources`, dan *deliverable* yang hilang dari `output.schema.json`.

---

## Audit menggunakan Model Carbon dari Google

Bagian ini mendokumentasikan hasil audit awal terhadap *baseline* proyek serta status pemenuhan seluruh temuan pada **Fase A**.

### 1. Pernyataan Hasil Audit (*Audit Verdict*)

- **Kekuatan Konseptual**: Gagasan mengangkat `#Skill` menjadi `#Operation` menjawab celah abstraksi nyata pada arsitektur multi-agen—khususnya pemisahan `OD` vs `OI`, kontrol iterasi berbatas pada **OBS** dengan aturan *non-regression rollback*, serta pemisahan peran untuk independensi audit/verifikasi.
- **Keputusan Arah Perbaikan**: Setelah menelaah arsitektur nyata **Almudaya Multi-Agent (`v0.3.6`)**, spesifikasi `#Operation` ditingkatkan menjadi **Dynamic Swarm Manifold (`almudaya.operation/v0.3`)** sehingga tidak terkunci pada bagan tim statis dan langsung selaras dengan siklus *spawn/recycle/apoptosis*, `GoalLedger`, `PrModerator` *write-fencing*, serta 10 protokol atomik `IProtocol`.

### 2. Status Remediasi Fase A atas Temuan Audit

| Kode Temuan | Temuan Audit (*Baseline*) | Status & Penyelesaian di Fase A (`v0.3` / `v0.4`) |
|---|---|---|
| **A1** | Klaim "generalisasi" `#Skill → #Operation` belum dibuktikan secara formal sebagai kasus khusus. | **Selesai.** Dibuktikan lewat peta realisasi dinamis $\mu_t$ & **Proposisi 1** (reduksi degeneratif $L=1 \leftrightarrow L>1$ ke `#Skill`) di [OPERATION_SPECIFICATION_v0_3.md](./almudaya_operation_v0_3/OPERATION_SPECIFICATION_v0_3.md) dan makalah `v0.4`. |
| **A2** | Kesenjangan literatur 2009–2025 (MOISE+, OperA, JaCaMo, MetaGPT, AutoGen, MCP, A2A). | **Selesai.** Seksi 3 dan [references.bib](./paper/references.bib) pada makalah `v0.4` memosisikan AO terhadap ketiga kelompok literatur tersebut. |
| **B1** | Predikat OBS berbasis *string* bebas (*declarative illusion*). | **Selesai.** Digantikan AST ber-tipe `PredicateExpr` (`all`, `any`, `not`, `eq..in`) di [operation.schema.json](./almudaya_operation_v0_3/schemas/operation.schema.json) beserta evaluatornya di [validate_operations.py](./tools/validate_operations.py). |
| **B2** | Non-ortogonalitas tupel 12-elemen `OD` dan duplikasi `guards`/`budgets`/`skills`. | **Selesai.** `OD` dirampingkan menjadi 10 komponen ortogonal tanpa duplikasi file *skill-bindings* atau *guards*; `v0.2` disinkronkan ulang. |
| **B3** | Ketiadaan aturan konkurensi Blackboard/file paralel dan *role coalescing*. | **Selesai.** Ditambahkan `blackboard_acl`, pengikatan ke `PrModerator` `CapabilityToken` (`fenceEpoch` monotonik), kebijakan *role coalescing*, serta invarian `anti_affinity`. |
| **C1** | Salah hitung kontribusi (5 vs 6), duplikasi `Appendix A`, dan *drift* studi kasus *PaperOrchestra* di PDF. | **Selesai.** Makalah `v0.4` memperbaiki hitungan menjadi **six contributions (`C1`–`C6`)**, menata ulang `Appendix A/B/C`, dan menyelaraskan *PaperOrchestra* dengan [04_research_pipeline/operation.yaml](./almudaya_operation_v0_3/04_research_pipeline/operation.yaml). |
| **C2** | *Dual-source-of-truth drift* antara `operation.yaml` dan `skill-bindings.yaml` di `v0.2`. | **Selesai.** Seluruh *role* pada `v0.2` disinkronkan (0 error pada validator) dan di `v0.3` disatukan ke sumber tunggal `manifold.roles[].skills`. |
| **C3** | Ketidakcocokan `output.schema.json` (properti hilang, `*_ref` vs `$.outputs.*`, ketiadaan pengikat `output_schema`). | **Selesai.** `output_schema` wajib di `v0.3` (dan ditambahkan ke `v0.2`), serta seluruh `deliverables` dan `output_mapping` selaras 1-ke-1 dengan `output.schema.json`. |
| **C4** | Sub-skema `operation.schema.json` terlalu longgar (`{"type": "object"}`), `visual_critic` masuk ke `feedback_from` role, *child operations* tanpa *stub*, dan state `paused` hilang di kontrak runtime. | **Selesai.** Skema `v0.3` mengetik ketat seluruh sub-objek (`additionalProperties: false`), memisahkan `feedback_sources` (`role` vs `resource_evaluator`), menyediakan 3 *child operation* lengkap, serta memformalkan `paused_hitl` & `paused_master_unavailable` di [runtime-state-machine.md](./almudaya_operation_v0_3/shared/runtime-state-machine.md) dan [runtime-contract.md](./almudaya_operation_scaffold_v0_2/shared/runtime-contract.md). |

### 3. Langkah Berikutnya (**Fase B — Integrasi ke `Almudaya-Multi-Agent`**)

Setelah Fase A ditinjau dan disetujui, tahap selanjutnya (**Fase B**) adalah mengimplementasikan modul `Operation` secara nyata di proyek utama `D:\almudaya_multiagent_v0.1.0` sesuai disiplin Waterfall dan ADR:
- Membuat `src/operation/` (*OperationLoader*, *StaticValidator*, *OperationRegistry*, *ManifoldCompiler* yang menerjemahkan `#Operation v0.3` menjadi konfigurasi `ProtocolSupervisor`, `SpawnManager`, `DynamicRulesService`, `ACG`, dan `SessionSkillBinding`).
- Menambahkan antarmuka CLI (`almudaya operation list|validate|apply|crystallize`) serta perintah REPL `BOT000` (`/operation <id>`).
- Menjalankan studi evaluasi empiris (`RQ1`–`RQ5`) antara *baseline* agen tunggal ber-`#Skill` vs *Dynamic Swarm Manifold*.
