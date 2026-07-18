from dataclasses import dataclass, field


@dataclass
class BulkActionResult:
    succeeded: list[str] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)  # [{"product_id": ..., "reason": ...}]

    def add_success(self, product_id: str) -> None:
        self.succeeded.append(product_id)

    def add_failure(self, product_id: str, reason: str) -> None:
        self.failed.append({"product_id": product_id, "reason": reason})