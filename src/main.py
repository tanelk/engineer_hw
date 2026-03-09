from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, Depends, Form, HTTPException
from sqlmodel import Session, select

from .database import init_db, get_session
from .models import AudioEmbedding
from .yamnet import process_audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Audio Embeddings API", lifespan=lifespan)

@app.post("/embeddings")
async def create_embeddings(files: list[UploadFile], session: Session = Depends(get_session)):
    results = {}

    for file in files:
        if file.filename in results:
            session.rollback()
            # Can't have duplicates here, because we need to use file names as keys on return
            raise HTTPException(status_code=400, detail=f"Duplicate file name '{file.filename}'")

        audio_bytes = await file.read()
        embedding, top_classes = process_audio(audio_bytes)

        # Store in database
        db_embedding = AudioEmbedding(filename=file.filename, embedding=embedding)
        session.add(db_embedding)

        results[file.filename] = top_classes

    session.commit()
    return results

@app.post("/search")
async def search_similar(file: UploadFile, top_k: int = Form(5), session: Session = Depends(get_session)):
    audio_bytes = await file.read()
    query_embedding, _ = process_audio(audio_bytes)

    # Search DB using pgvector's cosine distance
    distance = AudioEmbedding.embedding.cosine_distance(query_embedding).label("distance")

    stmt = (
        select(AudioEmbedding, distance)
        .order_by(distance)
        .limit(top_k)
    )

    similar_records = session.exec(stmt).all()

    results = [
        {
            "filename": record.AudioEmbedding.filename,
            "similarity": round(1.0 - record.distance, 4),
        }
        for record in similar_records
    ]

    return {"results": results}