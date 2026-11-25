# Communication Contract — almudaya.operation-message.v1

Setiap pesan membawa `operation_id`, `correlation_id`, `message_id`, `from`, `to`, `kind`, `iteration`, `loop_scope`, `payload_ref`, dan timestamp RFC3339. `kind`: task, result, feedback, status, escalation, cancel. Payload divalidasi schema; artefak besar dirujuk melalui Blackboard/storage. Runtime mengelola correlation, deduplication/idempotency, ordering untuk dependency, dan cancellation propagation.
