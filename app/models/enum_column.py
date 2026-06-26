from enum import StrEnum

from sqlalchemy import Enum


def enum_column(enum_cls: type[StrEnum]) -> Enum:
    """Coluna de enum como VARCHAR que persiste o value (não o name do membro)."""
    return Enum(
        enum_cls,
        native_enum=False,
        length=50,
        values_callable=lambda enum: [member.value for member in enum],
    )
