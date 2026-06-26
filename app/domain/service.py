from app.core import security


class SecurityService:

    @classmethod
    def hash_senha(cls, senha: str) -> str:
        return security.hash_senha(senha)

    @classmethod
    def verificar_senha(cls, senha: str, senha_hash: str) -> bool:
        return security.verificar_senha(senha, senha_hash)

    @classmethod
    def criar_access_token(cls, sub: str, perfil: str | None = None) -> str:
        return security.criar_access_token(sub, perfil)

    @classmethod
    def decodificar_token(cls, token: str) -> dict:
        return security.decodificar_token(token)
