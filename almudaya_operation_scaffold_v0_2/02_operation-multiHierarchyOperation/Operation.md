# Operation: Multi-Hierarchical Research and Delivery

**ID:** `almudaya.operation.multi-hierarchy` · **Version:** `0.2.0` · **Pattern:** parent Operation with nested child Operations.

## Mission
Menghasilkan paket rekomendasi teknis berbasis bukti melalui beberapa sub-Operation spesialis yang dapat berjalan paralel atau berurutan.

## Hierarchy
```text
Parent: Research & Delivery Director
├── Research Branch
│   ├── Literature Search Operation
│   └── Evidence Synthesis Operation
├── Technical Branch
│   ├── Architecture Assessment Operation
│   └── Risk & Security Assessment Operation
└── Integration Branch
    └── Final Integration & Quality Gate Operation
```
File `operation.yaml` mendeklarasikan tiga child pada level pertama. Child dapat memiliki child lain yang diregistrasikan secara terpisah.

## Parent vs child
Parent menetapkan tujuan global, memetakan input, mengelola dependency/concurrency/budget, menyelesaikan konflik lintas cabang, mengintegrasikan hasil, dan menentukan status final. Child menjalankan misi lokal sesuai kontrak input/output, permission, resource, dan OBS miliknya sendiri.

## Behavior
Parent mode `hierarchical`. Research dan Technical Branch dapat paralel. Integration menunggu keduanya. Parent dapat meminta revisi terarah pada child yang gagal quality gate, maksimal 2 putaran. Nesting depth maksimal 3. Aggregate budget dipartisi; child tidak boleh memakai budget child lain.

## Failure/recovery
Child failure dikembalikan melalui error/status contract. Retry hanya bila error retryable. Child timeout ditangani sesuai policy. Cycle/depth violation menolak instansiasi. ACMA memulihkan checkpoint parent/child yang tersedia.

## Invocation
`/operation run almudaya.operation.multi-hierarchy`. Alias `#Operation-multiHierarchyOperation` dipetakan UI ke ID/versi terdaftar.

## Success
Child wajib selesai atau memperoleh waiver resmi; output terintegrasi; evidence traceable; risiko/kontradiksi dicatat; final quality gate disetujui.
