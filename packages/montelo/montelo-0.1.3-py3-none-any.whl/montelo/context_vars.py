from contextvars import ContextVar

ctx_datapoint_run_id: ContextVar[str | None] = ContextVar('datapoint_run_id', default=None)
