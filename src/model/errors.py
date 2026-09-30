"""Domain-level failures independent of presentation and storage."""


class PIMError(Exception):
    """Base class for expected model failures."""


class ValidationError(PIMError):
    """An ID, field, type, or value is invalid."""


class RecordNotFoundError(PIMError):
    """A well-formed ID is absent from the current collection."""


class SearchSyntaxError(ValidationError):
    """The complete search expression cannot be parsed."""
