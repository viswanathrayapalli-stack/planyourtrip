from sqlalchemy import text

from app.shared.database.engine import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT version()"))
    print(result.scalar())