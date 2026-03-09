from sqlmodel import SQLModel, Field, Index
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector

class AudioEmbedding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Do not constrain to be unique
    filename: str = Field(index=True)
    # YAMNet embeddings are 1024 dimensions
    embedding: list[float] = Field(sa_column=Column(Vector(1024)))

    # Index for fast lookup
    __table_args__ = (
        Index(
            "idx_audio_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )