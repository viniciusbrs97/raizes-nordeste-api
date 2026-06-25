import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://raizes:senha@localhost:5432/raizes_nordeste",
)
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("SUPER_ADMIN_EMAIL", "admin@raizes.com")
os.environ.setdefault("SUPER_ADMIN_PASSWORD", "troque-essa-senha")
