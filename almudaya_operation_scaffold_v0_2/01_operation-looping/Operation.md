# Operation: Iterative Software Quality Loop

**ID:** `almudaya.operation.looping` · **Version:** `0.2.0` · **Pattern:** bounded operation-level loop.

## Mission
Menghasilkan perubahan perangkat lunak yang memenuhi acceptance criteria melalui siklus implementasi, pengujian, review, dan perbaikan. Runtime mengendalikan siklus; setiap bot hanya menjalankan kontrak role-nya.

## Organization
Topologi hybrid:
- `delivery_lead`: dekomposisi tugas, integrasi, keputusan readiness.
- `developer`: implementasi dan perbaikan.
- `test_engineer`: test execution dan temuan terstruktur.
- `reviewer`: review correctness, maintainability, dan security.

## Operational behavior
Loop scope utama adalah `operation`. Satu iterasi: `implement → test → review → evaluate`. Feedback dari tester/reviewer dikembalikan ke developer melalui Coordination Engine. Iterasi berhenti ketika acceptance terpenuhi atau guard tercapai.

Guard: maksimum 5 iterasi Operation, 2 retry per task, no-progress limit 2, deadline 120 menit, budget 100 cost units. Cancellation menghentikan child tasks. Deployment/release memerlukan approval manusia.

## Contracts
Input: requirement, workspace reference, acceptance criteria, constraints. Output: change set, test report, review report, decision record, execution trace.

## Failure/recovery
Retry hanya untuk error retryable dan task idempotent/checkpointed. Agent unavailable dapat diganti jika capability contract terpenuhi. Runtime crash dipulihkan melalui ACMA. Budget/deadline/no-progress guard menyebabkan stop/escalate, bukan loop tak terbatas.

## Invocation
`/operation run almudaya.operation.looping`. Alias `#Operation-looping` dapat dipetakan UI/command parser ke ID dan versi Operation; alias bukan pengganti runtime.

## Success
Acceptance criteria terpenuhi, test wajib lulus, reviewer menyetujui, dan artefak/audit trace tersimpan.
