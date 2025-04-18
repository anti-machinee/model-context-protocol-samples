from pydantic import BaseModel


class PostgreSQLQuery(BaseModel):
    sql: str