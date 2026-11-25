# Almudaya Agentic Operation (`#Operation`)

> **Status Repositori — Snapshot Baseline Pra-Perbaikan (*Pre-Remediation Baseline*)**  
> Commit ini menyimpan arsip versi awal dari makalah konseptual **v0.3** beserta seluruh *scaffold* deklaratif (`v0.1`, `v0.2`, dan `researchPipeline_v0_1`) secara utuh **sebelum** dilakukan perbaikan struktural, penyelarasan skema, maupun revisi pasca-audit.

---

## 1. Gambaran Umum Gagasan: Dari `#Skill` Menuju `#Operation`

Ekosistem pengembangan sistem agenik berbasis *Large Language Model* (LLM) saat ini telah mengadopsi konsep **`#Skill`** secara luas—yakni paket kapabilitas prosedural yang dapat ditemukan (*discoverable*) dan dimuat secara progresif oleh suatu agen tunggal ketika menghadapi kategori tugas tertentu (berisi instruksi domain, prosedur, skrip, templat, serta bahan rujukan).

Namun, ketika suatu misi berskala kompleks membutuhkan keterlibatan **banyak agen** (*multi-agent system*), sekadar membagikan `#Skill` yang sama atau berbeda kepada beberapa agen tidaklah memadai. Paket `#Skill` tidak menetapkan:
- Agen atau peran (*role*) mana saja yang berpartisipasi dan apa batas tanggung jawabnya;
- Bagaimana `#Skill` dan sumber daya (*tools*, model, memori, dataset) didistribusikan secara *least-privilege*;
- Bagaimana topologi organisasi, protokol pertukaran pesan, serta strategi koordinasi dijalankan;
- Bagaimana siklus perbaikan iteratif (*feedback loops*), *rollback*, batasan biaya/waktu, dan tata kelola (*governance* / persetujuan manusia) ditegakkan.

Untuk menutup celah abstraksi tersebut, proyek ini memperkenalkan **`#Operation` (*Agentic Operation / AO*)**: sebuah **spesifikasi organisasi kerja multi-agen yang berorientasi misi (*mission-oriented*), deklaratif, berversi, dan dapat dipakai ulang (*reusable*)**. Gagasan utamanya dapat dirangkum sebagai pergeseran tingkat abstraksi:

- **`#Skill`** → **Kapabilitas Prosedural** (*bagaimana satu agen menjalankan suatu kategori tugas*).
- **`#Operation`** → **Kapabilitas Operasional Kolektif** (*bagaimana banyak agen dirakit, diperlengkapi dengan Skill/sumber daya, dikoordinasikan, dan diawasi tata kelolanya untuk menuntaskan suatu misi*).

---

## 2. Ringkasan Makalah: *From Agentic Skills to Agentic Operations: A Generalized Organizational Abstraction for Multi-Agent Systems*

**Dokumen Sumber:** [From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf](./From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf)  
**Institusi & Versi:** Almudaya Research Institute — *Conceptual Architecture Draft*, Version 0.3 (November 2026).

### 2.1 Motivasi, Posisi Konseptual, dan Kontribusi
Makalah mengakui bahwa penelitian sistem multi-agen (MAS) klasik telah lama mengkaji paradigma organisasi (hierarki, tim, koalisi, federasi, pasar, matriks). Kontribusi yang diusulkan bukanlah penemuan kembali konsep organisasi MAS, melainkan **pengemasan terpadu dan eksplisit** atas aspek organisasi, distribusi `#Skill`, kontrak sumber daya, perilaku eksekusi, dan tata kelola menjadi satu artefak deklaratif yang independen dari *runtime* tertentu.

Tabel berikut merangkum pemosisian konseptual (Tabel 1 dalam makalah):

| Abstraksi | Fokus Utama | Pertanyaan yang Dijawab |
|---|---|---|
| **Agent** | Entitas eksekusi otonom | Siapa yang menjalankan tugas yang diberikan? |
| **Skill** | Kapabilitas prosedural | Bagaimana suatu agen dapat menjalankan suatu kategori tugas? |
| **Tool** | Antarmuka eksekusi atau sumber daya | Apa yang dapat digunakan atau dipanggil oleh agen? |
| **Workflow** | Urutan tugas, graf, dan ketergantungan | Bagaimana pekerjaan bergerak maju antar-tahap? |
| **Memory** | Informasi dan *state* persisten | Informasi apa yang dapat disimpan dan diambil kembali? |
| **Operation** | Organisasi multi-agen dan eksekusi misi | Bagaimana agen-agen diorganisasi dan dikoordinasikan untuk menuntaskan misi? |

Makalah merinci enam kontribusi (tertulis `C1`–`C6` di halaman 2):
- **C1**: Mengartikulasikan transisi konseptual dari *Agentic Skills* menuju *Agentic Operations*.
- **C2**: Mendefinisikan komponen struktural suatu *Agentic Operation*.
- **C3**: Memisahkan *Operation Definition* (`OD`) dari *Operation Instance* (`OI`) saat *runtime*.
- **C4**: Memperkenalkan representasi formal bagi komposisi agen, *role*, *Skill*, komunikasi, topologi, *workflow*, sumber daya, dan *governance*.
- **C5**: Membahas komposisi hierarkis antar-*Operation* serta agenda implementasi dan evaluasi empiris.
- **C6**: Mendemonstrasikan konversi deklaratif *pipeline* penulisan riset multi-agen (*PaperOrchestra*) ke dalam sebuah *Agentic Operation*.

### 2.2 Model Formal (`OD` dan `OI`) serta Komponen Arsitektural
Makalah memisahkan secara tegas antara cetak biru statis (**Operation Definition / `OD`**) dan realisasi eksekusi konkret (**Operation Instance / `OI`**) sehingga satu `OD` dapat diinstansiasi berulang kali untuk misi berbeda dengan parameter dan agen berbeda:

```text
OD = (I, M, A, R, S, T, C, W, B, Q, G, X)
```

Keterangan komponen `OD`:
- `I`: Identitas, versi, dan metadata deskriptif *Operation*.
- `M`: Spesifikasi misi (tujuan, ruang lingkup, asumsi, input/output, kriteria penerimaan, batas anggaran/tenggat, kondisi penghentian).
- `A`: Himpunan *agent slots* atau agen yang berpartisipasi.
- `R`: Penugasan *role*, tanggung jawab, dan otoritas (terpisah dari identitas model/agen fisik).
- `S`: Distribusi `#Skill` (*many-to-many* melalui matriks biner $X \in \{0,1\}^{n \times m}$ yang dapat diperluas dengan versi, izin, dan kondisi pemanggilan).
- `T`: Topologi organisasi (*hierarchical, decentralized, peer-to-peer, pipeline, mesh, hybrid*).
- `C`: Protokol komunikasi (skema pesan, korelasi, pola *direct/broadcast/pub-sub/request-response*, *acknowledgement*, *timeout*, *retry*, *deduplication*, eskalasi).
- `W`: *Workflow* dan strategi koordinasi (graf tahapan serta ketergantungan tugas).
- `B`: *Operational Behavior Specification* (OBS).
- `Q`: Kontrak alokasi dan kuota sumber daya (terpisah dari implementasi vendor/runtime).
- `G`: Tata kelola (*least privilege*, *approval gates*, batasan alat/data, jejak audit).
- `X`: Kontrak integrasi *runtime* eksternal dan *adapter*.

Saat dieksekusi, `OI` dinyatakan sebagai:

```text
OI = (OD, Θ, E, Σ, K)
```

dengan `Θ` parameter khusus misi, `E` lingkungan eksekusi yang telah di-*resolve* (agen konkret & sumber daya teralokasi), `Σ` *state* mutabel saat *runtime* (`{created, validated, provisioning, ready, running, paused, failed, completed, terminated}`), serta `K` metadata *checkpoint* dan pemulihan.

### 2.3 *Operational Behavior Specification* (OBS) & Siklus Hidup
Salah satu komponen kunci makalah adalah **OBS**, yang mendeklarasikan perilaku eksekusi spesifik misi secara terpisah dari mesin *runtime* generik (`Loop Engine`, penjadwal, *state machine*). OBS membedakan minimal **empat cakupan *bounded loop***:
1. **Task retry**: pengulangan tugas tunggal yang gagal karena galat *retryable*.
2. **Agent iteration**: penyempurnaan berulang oleh satu agen berdasarkan umpan balik evaluator.
3. **Operation iteration**: siklus perbaikan kolektif lintas beberapa *role* (misalnya siklus implementasi–uji–*review*–evaluasi).
4. **Nested-Operation iteration**: pengulangan atau revisi *sub-Operation* oleh *parent Operation*.

Setiap *loop* wajib bersifat terbatas (*bounded*) dengan batas iterasi, waktu, anggaran, deteksi *no-progress*, serta kebijakan pembatalan dan pemulihan.

Secara operasional, siklus hidup sebuah *Operation* menempuh **9 tahap**: *Definition → Validation → Instantiation → Provisioning → Agent Initialization → Execution → Monitoring & Adaptation → Completion/Failure Handling → Archival*.

### 2.4 Komposisi Hierarkis, Prinsip Desain, Layanan Manajemen, & Agenda Riset
- **Komposisi Hierarkis**: Suatu *parent Operation* $O_p$ dapat mendelegasikan sub-misi terbatas ke himpunan *child Operations* $D(O_p) = \{O_1, \dots, O_k\}$ melalui kontrak input/output tervalidasi, isolasi batas izin/anggaran, propagasi pembatalan, pembatasan kedalaman (*max nesting depth*), dan deteksi siklus referensi.
- **6 Prinsip Arsitektural**: (1) *Organizational explicitness*, (2) *Capability modularity*, (3) *Runtime independence*, (4) *Contract-based interaction*, (5) *Governed adaptability*, dan (6) *Reproducibility and traceability*.
- **Operation Management Layer**: Mengusulkan 8 layanan inti (*Operation Registry, Operation Validator, Instantiation Engine, Agent Manager, Skill and Resource Resolver, Communication Layer, Execution and Coordination Manager, Monitor and Audit Service*) yang terintegrasi lewat *adapter* ke layanan platform seperti *Shared Blackboard*, memori proyek persisten (**PKU**), serta kontinuitas/*checkpoint* (**ACMA**).
- **Agenda Riset (`RQ1`–`RQ5`)**: Menguji independensi *runtime*, peningkatan *reuse*, dampak topologi terhadap latensi/biaya/pemulihan, skalabilitas komposisi hierarkis, serta mekanisme *governance* untuk adaptasi dinamis; dibandingkan terhadap *baseline* agen tunggal ber-Skill dan *workflow* multi-agen non-deklaratif.
- **Demonstrasi & Studi Kasus**: Lampiran makalah menyajikan konversi deklaratif *PaperOrchestra* (`#Operation-pipelineResearch` pada lampiran pertama di halaman 18–23) serta tiga dokumen operasi demonstratif (*Scientific Literature Review*, *Software Feature Delivery*, dan *Reproducible Dataset Analysis* pada halaman 24–28).

---

## 3. Struktur Direktori Repositori

```text
.
├── From_Agentic_Skills_to_Agentic_Operations__A_Generalized_Organizational_Abstraction_for_Multi_Agent_Systems.pdf
├── LICENSE
├── README.md
├── almudaya_operation_scaffold_v0_1/           # PoC awal (api_version: almudaya.operation/v1alpha1)
│   ├── manifest.json
│   ├── README.md
│   ├── 01_scientific_literature_review/        # Topologi hierarkis (6 role, 6 stage)
│   ├── 02_software_feature_delivery/           # Topologi hybrid (6 role, 6 stage)
│   └── 03_dataset_analysis/                    # Topologi pipeline + validasi independen (6 role, 6 stage)
├── almudaya_operation_scaffold_v0_2/           # Spesifikasi & scaffold v0.2 (apiVersion: almudaya.operation/v0.2)
│   ├── OPERATION_SPECIFICATION.md              # Ringkasan spesifikasi formal v0.2 & OBS
│   ├── manifest.json
│   ├── README.md
│   ├── schemas/
│   │   ├── operation.schema.json               # Skema utama definisi Operation
│   │   └── resource.schema.json                # Skema manifest resource
│   ├── shared/
│   │   ├── communication-contract.md           # Kontrak pesan almudaya.operation-message.v1
│   │   ├── governance-policy.yaml              # Kebijakan default least-privilege & bounded loops
│   │   └── runtime-contract.md                 # Kontrak lifecycle & adapter runtime
│   ├── 01_operation-looping/                   # Pola bounded operation-level feedback loop
│   └── 02_operation-multiHierarchyOperation/   # Pola parent Operation dengan nested child Operations
└── almudaya_operation_researchPipeline_v0_1/   # Konversi deklaratif PaperOrchestra (almudaya.operation/v0.2)
    ├── Operation.md
    ├── README.md
    ├── manifest.json
    ├── operation.json & operation.yaml
    ├── docs/paperorchestra-mapping.md          # Pemetaan komponen PaperOrchestra ke Almudaya AO
    ├── examples/sample-input.json
    ├── policies/                               # execution-policy.yaml & academic-integrity.yaml
    ├── resources/                              # resource-manifest.yaml & resource-budgets.yaml
    ├── schemas/                                # input.schema.json & output.schema.json
    └── skills/skill-bindings.yaml
```

Tautan cepat ke berkas kunci:
- Spesifikasi v0.2: [OPERATION_SPECIFICATION.md](./almudaya_operation_scaffold_v0_2/OPERATION_SPECIFICATION.md)
- Skema Utama v0.2: [operation.schema.json](./almudaya_operation_scaffold_v0_2/schemas/operation.schema.json) & [resource.schema.json](./almudaya_operation_scaffold_v0_2/schemas/resource.schema.json)
- Kontrak Bersama v0.2: [communication-contract.md](./almudaya_operation_scaffold_v0_2/shared/communication-contract.md), [runtime-contract.md](./almudaya_operation_scaffold_v0_2/shared/runtime-contract.md), [governance-policy.yaml](./almudaya_operation_scaffold_v0_2/shared/governance-policy.yaml)
- Contoh Pola *Looping*: [01_operation-looping/operation.yaml](./almudaya_operation_scaffold_v0_2/01_operation-looping/operation.yaml)
- Contoh Pola *Multi-Hierarchy*: [02_operation-multiHierarchyOperation/operation.yaml](./almudaya_operation_scaffold_v0_2/02_operation-multiHierarchyOperation/operation.yaml)
- Studi Kasus *Research Pipeline*: [almudaya_operation_researchPipeline_v0_1/operation.yaml](./almudaya_operation_researchPipeline_v0_1/operation.yaml) & [paperorchestra-mapping.md](./almudaya_operation_researchPipeline_v0_1/docs/paperorchestra-mapping.md)

---

## Audit menggunakan Model Carbon dari Google

Bagian ini mendokumentasikan hasil audit menyeluruh (dimensi konseptual-teoretis, arsitektural-formal, dan konsistensi teknis lintas berkas) terhadap makalah `v0.3` beserta seluruh direktori *scaffold* pada kondisi *baseline* pra-perbaikan.

### 1. Pernyataan Hasil Audit (*Audit Verdict*)

- **Kekuatan & Nilai Orisinal**: Gagasan mengangkat `#Skill` menjadi `#Operation` memiliki **diagnosis masalah yang tepat dan relevan** terhadap arsitektur agen modern. Pemisahan `OD` (*Operation Definition*) dari `OI` (*Operation Instance*), pengenalan **OBS** (*Operational Behavior Specification* dengan 4 cakupan *bounded loop*, predikat non-regresi, dan *versioned rollback*), serta pemanfaatan batas *role* untuk **isolasi konteks verifikasi independen** (memisahkan pembuat artefak dari penilai/verifikator agar terhindar dari bias konfirmasi) merupakan kontribusi desain yang solid.
- **Status Kesiapan Saat Ini**: Secara keseluruhan, artefak pada repositori ini **masih berada pada tahap draf konseptual dan *scaffold* awal yang belum siap dieksekusi (*non-executable*)**. Ditemukan sejumlah celah teoretis-literatur pada makalah, ambiguitas semantik eksekusi pada spesifikasi OBS/Blackboard, serta ketidaksinkronan kontrak teknis antar-berkas yang akan menyebabkan kegagalan validasi maupun *runtime* apabila tidak diperbaiki terlebih dahulu.

### 2. Kekurangan & Temuan Audit yang Ditemukan

#### A. Kekurangan Konseptual & Celah Literatur
1. **Ketidaktepatan Klaim "Generalisasi" Secara Formal**:  
   Secara matematis/ontologis, `B` merupakan *generalisasi* dari `A` jika `A` adalah kasus khusus (*degenerate case*) dari `B`. Dalam formulasi makalah, `S` (*Skills*) justru menjadi elemen komposisi di dalam tupel `OD`, sekaligus dinyatakan bahwa *Operation* bukan sekadar "*Skill* berukuran besar". Tanpa mendefinisikan reduksi kasus degeneratif secara eksplisit (mis. saat jumlah agen $|A| = 1$, topologi trivial, dan tanpa protokol komunikasi antar-agen, sebuah `OD` tereduksi secara isomorfik menjadi eksekusi satu agen dengan himpunan `#Skill`), relasi `#Skill → #Operation` lebih akurat dirumuskan sebagai **pengangkatan komposisional (*compositional/organizational lifting*)**, bukan generalisasi murni.
2. **Kekosongan Literatur Antara Tahun 2009 dan 2025**:  
   Makalah hanya menyertakan 5 rujukan (`[1]`–`[5]`) dan melewatkan dua pilar literatur penting:
   - *MAS Organisasional Deklaratif Klasik*: **MOISE / MOISE+** (spesifikasi *Structural, Functional, Deontic* untuk organisasi agen) dan **OperA**, yang sejak lama memformalkan pemisahan spesifikasi organisasi dari instansiasi agen. Makalah perlu memperjelas kebaruan **Agentic Operation** dibanding MOISE+ (yakni integrasi dengan paket prosedural *progressive disclosure* `#Skill`, manajemen anggaran token/model, serta mekanisme *evaluator-driven refinement* OBS untuk agen LLM stokastik).
   - *Standar & Orkestrator Agen LLM Modern*: Belum ada posisi komparatif terhadap **MetaGPT**, **CrewAI**, **LangGraph**, **MCP (*Model Context Protocol*)** untuk kontrak sumber daya `Q`, serta **A2A (*Agent2Agent Protocol*)** untuk protokol komunikasi `C`.

#### B. Kekurangan Arsitektural & Formalisasi
3. **Ilusi Deklaratif pada Predikat OBS (*Free-Text Predicates*)**:  
   Pada [01_operation-looping/operation.yaml](./almudaya_operation_scaffold_v0_2/01_operation-looping/operation.yaml) dan [almudaya_operation_researchPipeline_v0_1/operation.yaml](./almudaya_operation_researchPipeline_v0_1/operation.yaml), predikat `continuation`, `acceptance`, dan `termination` masih ditulis sebagai teks bebas (contoh: `"overall_score_improved OR overall_score_tied_with_no_required_subscore_regression"`). Tanpa bahasa ekspresi formal yang deterministik dan terikat ke skema keluaran evaluator (seperti **CEL** atau **JSONLogic**), klaim bahwa fungsi transisi *runtime* $\Sigma(t+1) = F(OD, \Theta, E, \Sigma(t), \text{events}(t))$ sepenuhnya generik tidak terpenuhi karena pengembang tetap harus menulis kode evaluator predikat khusus untuk setiap misi.
4. **Non-Ortogonalitas Model Formal 12-Elemen `OD`**:  
   - Tupel formal makalah memisahkan `A` (*agent slots*) dan `R` (*roles*), namun skema JSON `v0.2` ([operation.schema.json](./almudaya_operation_scaffold_v0_2/schemas/operation.schema.json)) menghapus `A` dan meleburnya ke `organization.roles[].cardinality`.
   - Aturan batas eksekusi (*budget*, batas iterasi, *human approval*) dideklarasikan secara duplikat di tiga berkas/bagian berbeda (`behavior.guards`, `resources/resource-budgets.yaml`, dan `policies/execution-policy.yaml`) tanpa aturan presedensi apabila terjadi perbedaan angka.
5. **Ketiadaan Semantik Konkurensi Blackboard & Mekanisme *Role Coalescing***:  
   - [communication-contract.md](./almudaya_operation_scaffold_v0_2/shared/communication-contract.md) mengatur *envelope* pesan, tetapi belum mendefinisikan **isolasi *namespace* serta *access control* baca/tulis Blackboard per *role*** maupun resolusi konflik penulisan ketika beberapa agen paralel (`cardinality.max: 2` pada `developer`, `visualization_specialist`, atau `manuscript_writer`) bekerja serentak pada artefak yang sama.
   - Belum tersedia kebijakan *role coalescing* (penggabungan beberapa *role* ke satu agen fisik saat *provisioning* `E` untuk misi berisiko rendah) maupun kriteria ambang kompleksitas untuk menghindari *coordination overhead* (biaya token dan latensi *handoff*) pada tugas yang cukup diselesaikan oleh satu agen ber-Skill.

#### C. Kekurangan Teknis & Inkonsistensi Lintas Artefak Repositori
6. **Inkonsistensi Editorial & *Spec Drift* pada Makalah PDF**:  
   - Pada halaman 2 PDF tertulis *"The paper makes **five** contributions:"*, padahal daftar di bawahnya memuat **enam** butir (`C1`–`C6`).
   - Terdapat duplikasi label bab **`Appendix A`** pada dua bagian berbeda: halaman 18 (`A Declarative Conversion of PaperOrchestra into an Agentic Operation`) dan halaman 24 (`A APPENDIX: Demonstrative Operation Documents`), yang kemudian diikuti `B` di halaman 27.
   - Terjadi *drift* definisi *PaperOrchestra* antara teks PDF (`almudaya.operation.pipeline-research`, alias `#Operation-pipelineResearch`, 5 *role*, dan `manuscript_refinement` ber-`scope: agent`) dengan berkas di direktori [almudaya_operation_researchPipeline_v0_1/operation.yaml](./almudaya_operation_researchPipeline_v0_1/operation.yaml) (`almudaya.operation.research-pipeline`, alias `#Operation-researchPipeline`, 8 *role* termasuk `operation_coordinator`, `citation_verifier`, `human_researcher`, dan `manuscript_refinement_loop` ber-`scope: operation`).
7. ***Dual-Source-of-Truth Drift* antara `operation.yaml` dan `skill-bindings.yaml`**:  
   Penugasan `#Skill` diduplikasi di `organization.roles[].skills` dan `skills/skill-bindings.yaml`, sehingga menimbulkan perbedaan nyata:
   - Pada `almudaya_operation_researchPipeline_v0_1`, **ketujuh *role* agen memiliki daftar Skill yang tidak identik** antara [operation.yaml](./almudaya_operation_researchPipeline_v0_1/operation.yaml) dan [skill-bindings.yaml](./almudaya_operation_researchPipeline_v0_1/skills/skill-bindings.yaml) (misalnya `artifact-integration`, `visualization-planning`, `figure-captioning`, `citation-management`, `reference-deduplication`, `table-generation`, dan `revision-planning` hanya muncul di `skill-bindings.yaml`, sementara `human_researcher` absen di `skill-bindings.yaml`).
   - Pada `02_operation-multiHierarchyOperation`, *role* `operation_director` memiliki `decision-integration` di [skill-bindings.yaml](./almudaya_operation_scaffold_v0_2/02_operation-multiHierarchyOperation/skills/skill-bindings.yaml), tetapi tidak tercantum di [operation.yaml](./almudaya_operation_scaffold_v0_2/02_operation-multiHierarchyOperation/operation.yaml).
8. **Ketidakcocokan Kontrak `output.schema.json` yang Menggagalkan Validasi**:  
   - Pada [02_operation-multiHierarchyOperation/operation.yaml](./almudaya_operation_scaffold_v0_2/02_operation-multiHierarchyOperation/operation.yaml), `mission.deliverables` dan `sub_operations[].output_mapping` merujuk ke `architecture_options`, `research_synthesis`, `quality_decision`, serta keluaran `$.outputs.evidence_register` dan `$.outputs.risk_register`. Namun [schemas/output.schema.json](./almudaya_operation_scaffold_v0_2/02_operation-multiHierarchyOperation/schemas/output.schema.json) memberlakukan `"additionalProperties": false`, menggunakan nama properti ber-sufiks `*_ref`, dan **tidak memiliki properti untuk `architecture_options`, `research_synthesis`, maupun `quality_decision`**.
   - Pada `almudaya_operation_researchPipeline_v0_1`, `mission.deliverables` mewajibkan `research_plan.json` dan `citation_registry.json`, namun keduanya tidak terdefinisi dalam `artifacts.properties` pada [schemas/output.schema.json](./almudaya_operation_researchPipeline_v0_1/schemas/output.schema.json).
   - Skema `v0.2` hanya menyediakan `mission.parameters_schema` (untuk input) dan **kehilangan properti pengikat `output_schema`** yang sebelumnya ada pada kontrak `v0.1`.
9. **Kelemahan Validasi Skema Utama, Pencampuran Entitas, *Missing Child Stubs*, dan State `Σ`**:  
   - Pada [schemas/operation.schema.json](./almudaya_operation_scaffold_v0_2/schemas/operation.schema.json), sub-komponen kritis (`roles.items`, `sub_operations.items`, `stages.items`, `communication`, `resources`, `governance`, `guards`) hanya diketik sebagai `{"type": "object"}` kosong tanpa kontrak *field* internal.
   - Pada `almudaya_operation_researchPipeline_v0_1/operation.yaml`, `visual_critique_loop` mengisi `feedback_from` dengan `["visual_critic"]`, padahal `visual_critic` dideklarasikan sebagai **resource** (`type: model`) di [resource-manifest.yaml](./almudaya_operation_researchPipeline_v0_1/resources/resource-manifest.yaml), bukan sebagai **role**.
   - Ketiga *child operation* yang dirujuk oleh `02_operation-multiHierarchyOperation` (`almudaya.operation.research-branch`, `almudaya.operation.technical-assessment`, dan `almudaya.operation.integration-quality-gate`) belum memiliki *stub* definisi di repositori sehingga skenario *multi-hierarchy* belum dapat divalidasi secara *end-to-end*.
   - Himpunan *state* pada [runtime-contract.md](./almudaya_operation_scaffold_v0_2/shared/runtime-contract.md) belum mencantumkan status `paused` / `awaiting_human_approval` yang dibutuhkan oleh mekanisme *human approval gates* dan tercantum pada Bagian 5.2 makalah.

---

### 3. Rencana Perbaikan (*Remediation Roadmap*)

Setelah *snapshot baseline* ini diarsipkan, perbaikan akan dijalankan dalam empat tahap terstruktur:

1. **Tahap 1 — Revisi Makalah & Penguatan Fondasi Teoretis**
   - Memperbaiki cacat editorial pada PDF (hitungan kontribusi menjadi enam `C1`–`C6`, penomoran ulang menjadi `Appendix A`, `Appendix B`, `Appendix C`, serta menyelaraskan studi kasus *PaperOrchestra* antara makalah dan direktori `almudaya_operation_researchPipeline_v0_1`).
   - Merumuskan proposisi reduksi formal kasus degeneratif ($|A|=1$) menuju `#Skill` sekaligus memperjelas posisi ontologis sebagai *compositional/organizational lifting*.
   - Menambahkan kajian komparatif terhadap **MOISE+**, **OperA**, **MetaGPT**, **CrewAI**, **LangGraph**, **MCP**, dan **A2A**.

2. **Tahap 2 — Konsolidasi *Single Source of Truth* & Pengetatan Skema (`v0.3`)**
   - Menghapus duplikasi penugasan `#Skill` antara `operation.yaml` dan `skill-bindings.yaml` serta menetapkan aturan presedensi tunggal untuk `guards`, `resource-budgets.yaml`, dan `execution-policy.yaml`.
   - Menambahkan pengikat `output_schema` pada `mission` di `operation.schema.json`, mengetik penuh sub-skema `roles`, `sub_operations`, `stages`, `communication`, `resources`, `governance`, dan `guards`.
   - Menyelaraskan seluruh `schemas/output.schema.json` agar 100% konsisten dengan `mission.deliverables` dan `output_mapping`.
   - Memisahkan referensi `role_ref` vs `evaluator_resource_ref` pada `feedback_from` di OBS, menyinkronkan *state* `paused` / `awaiting_approval` di `runtime-contract.md`, serta menyediakan *stub* definisi untuk ketiga *child Operation* di `02_operation-multiHierarchyOperation`.

3. **Tahap 3 — Formalisasi DSL Predikat OBS & Protokol Konkurensi Blackboard**
   - Mengganti predikat *string* bebas pada `behavior.loops` dan `behavior.termination` dengan bahasa ekspresi formal yang dapat dievaluasi secara deterministik (misalnya **CEL** atau **JSONLogic**) di atas skema metrik/keluaran evaluator yang tervalidasi.
   - Menambahkan spesifikasi kontrol akses baca/tulis Blackboard per *role* (*scoped namespace* & *versioned optimistic locking*) serta kebijakan opsional *role coalescing*.

4. **Tahap 4 — Implementasi *Static Semantic Validator CLI* & *Minimal Reference Runtime***
   - Membangun validator statis lintas-berkas (*schema check*, resolusi *role–skill–resource*, deteksi siklus DAG *workflow* & *sub-operation*, verifikasi pemetaan kontrak *parent–child*, dan validasi konsistensi anggaran).
   - Membangun *minimal reference runtime* untuk menguji `RQ1`–`RQ5` secara empiris dan membandingkan `#Operation` terhadap *baseline* agen tunggal ber-Skill dari sisi kualitas keluaran, tingkat halusinasi/regresi, latensi, dan konsumsi token.
