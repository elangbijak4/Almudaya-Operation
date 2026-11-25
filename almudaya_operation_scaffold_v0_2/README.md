# Almudaya Agentic Operation Scaffold v0.2

Scaffold deklaratif untuk dua pola:
1. `01_operation-looping`: siklus kolektif implementasi–test–review–perbaikan.
2. `02_operation-multiHierarchyOperation`: parent Operation yang mengorkestrasi child Operations bertingkat.

Setiap folder memiliki `Operation.md`, `operation.yaml`, `resources/`, `skills/`, `schemas/`, `policies/`, dan `examples/`.

`operation.yaml` adalah deklarasi terstruktur; `Operation.md` dokumentasi manusia. Scaffold ini belum runtime executable.

Integrasi Almudaya: AUCO memilih Operation; Operation Manager memvalidasi dan mengelola lifecycle; Operation Runtime menginterpretasikan definisi; Loop Engine menjalankan OBS; Coordination Engine mengatur delegasi/pesan; Agent Manager mengelola agent; Resource Manager mengatur akses/kuota. Blackboard menangani shared state, ACMA continuity/checkpoint/recovery, dan PKU persistent knowledge. Operation menggunakan adapter ke komponen tersebut.
