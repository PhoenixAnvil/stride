from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Iteration
from app.schemas import IterationCreate, IterationResponse

router = APIRouter()


@router.post("/iterations/", response_model=IterationResponse)
def create_iteration(
    iteration: IterationCreate, db: Session = Depends(get_db)
):
    db_iteration = Iteration(**iteration.model_dump())
    db.add(db_iteration)
    db.commit()
    db.refresh(db_iteration)
    return db_iteration


@router.get("/iterations/", response_model=list[IterationResponse])
def read_iterations(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return db.query(Iteration).offset(skip).limit(limit).all()


@router.get(
    "/iterations/{iteration_id}", response_model=IterationResponse
)
def read_iteration(iteration_id: UUID, db: Session = Depends(get_db)):
    iteration = (
        db.query(Iteration).filter(Iteration.id == iteration_id).first()
    )
    if not iteration:
        raise HTTPException(
            status_code=404, detail="Iteration not found"
        )
    return iteration


@router.delete("/iterations/{iteration_id}", status_code=204)
def delete_iteration(iteration_id: UUID, db: Session = Depends(get_db)):
    iteration = (
        db.query(Iteration).filter(Iteration.id == iteration_id).first()
    )
    if not iteration:
        raise HTTPException(
            status_code=404, detail="Iteration not found"
        )
    db.delete(iteration)
    db.commit()
