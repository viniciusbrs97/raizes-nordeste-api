from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import TipoMovimentacaoEstoque


class MovimentacaoEstoqueCreate(BaseModel):
    tipo: TipoMovimentacaoEstoque
    quantidade: int = Field(gt=0)

    model_config = ConfigDict(
        json_schema_extra={"example": {"tipo": "entrada", "quantidade": 10}}
    )


class EstoqueRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "produto_id": 1,
                "unidade_id": 1,
                "quantidade_estoque": 60,
                "is_available": True,
            }
        },
    )

    produto_id: int
    unidade_id: int
    quantidade_estoque: int
    is_available: bool
