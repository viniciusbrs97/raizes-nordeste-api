from sqlalchemy import BigInteger, DateTime

from app.models.base import Base, BaseModel, TimestampMixin


class _EditableModel(TimestampMixin, BaseModel):
    __tablename__ = "_editable_model_test"


class _ImmutableModel(BaseModel):
    __tablename__ = "_immutable_model_test"


def test_base_is_declarative_with_metadata():
    assert hasattr(Base, "metadata")


def test_base_model_is_abstract():
    assert BaseModel.__abstract__ is True


def test_editable_model_has_id_created_and_updated():
    columns = _EditableModel.__table__.columns

    assert "id" in columns
    assert "created_at" in columns
    assert "updated_at" in columns


def test_immutable_model_has_no_updated_at():
    columns = _ImmutableModel.__table__.columns

    assert "id" in columns
    assert "created_at" in columns
    assert "updated_at" not in columns


def test_id_is_bigint_primary_key():
    id_column = _EditableModel.__table__.columns["id"]

    assert id_column.primary_key is True
    assert isinstance(id_column.type, BigInteger)


def test_created_at_is_timezone_aware():
    created_at = _EditableModel.__table__.columns["created_at"]

    assert isinstance(created_at.type, DateTime)
    assert created_at.type.timezone is True
