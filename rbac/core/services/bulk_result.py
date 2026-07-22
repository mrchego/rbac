from dataclasses import dataclass, field


@dataclass
class BulkActionResult:
    succeeded: list[str] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)  # [{"user_id": ..., "reason": ...}]

    def add_success(self, user_id: str) -> None:
        self.succeeded.append(user_id)

    def add_failure(self, user_id: str, reason: str) -> None:
        self.failed.append({"user_id": user_id, "reason": reason})