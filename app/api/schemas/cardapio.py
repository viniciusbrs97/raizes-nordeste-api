from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemCardapioRead(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "produto_id": 1,
                "nome": "Cuscuz",
                "descricao": "Cuscuz nordestino com manteiga de garrafa",
                "categoria": "Comida nordestina",
                "preco": "8.00",
                "quantidade_estoque": 50,
            }
        }
    )

    produto_id: int
    nome: str
    descricao: str | None
    categoria: str | None
    preco: Decimal
    quantidade_estoque: int
