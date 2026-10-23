"""Expected failures independent of presentation and storage I/O."""

from model.diagnostics import MAX_ERROR_DETAIL, bounded_detail


class PIMError(Exception):
    """Base class for expected application failures, with bounded diagnostics."""

    category = "APPLICATION"

    def __init__(self, detail: str) -> None:
        super().__init__(bounded_detail(detail))


class ValidationError(PIMError):
    """An ID, field, type, or value is invalid."""

    category = "VALIDATION"


class RecordNotFoundError(PIMError):
    """A well-formed ID is absent from the current collection."""

    category = "NOT_FOUND"


class SearchSyntaxError(ValidationError):
    """The complete search expression cannot be parsed."""

    category = "SEARCH"

    def __init__(self, detail: str, position: int | None = None) -> None:
        self.position = position
        suffix = f" at character {position}" if position is not None else ""
        super().__init__(bounded_detail(detail, MAX_ERROR_DETAIL - len(suffix)) + suffix)
