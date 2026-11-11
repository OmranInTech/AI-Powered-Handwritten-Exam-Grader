
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.permissions import require_role
from app.database.session import get_db
from app.models.enums import UserRole
from app.models.examination import Examination
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.user import User
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse
)

router = APIRouter(tags=["Questions"])


@router.post(
    "/api/examinations/{examination_id}/questions/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_question(
    examination_id: uuid.UUID,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    examination = db.query(Examination).filter(
        Examination.id == examination_id,
        Examination.teacher_id == current_user.id
    ).first()

    if examination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examination not found"
        )

    question = Question(
        **question_data.model_dump(exclude={"options"}),
        examination_id=examination.id
    )

    question.options = [
        QuestionOption(**option.model_dump())
        for option in question_data.options
    ]

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get(
    "/api/examinations/{examination_id}/questions/",
    response_model=list[QuestionResponse]
)
def get_questions(
    examination_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    examination = db.query(Examination).filter(
        Examination.id == examination_id,
        Examination.teacher_id == current_user.id
    ).first()

    if examination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examination not found"
        )

    return db.query(Question).options(
        joinedload(Question.options)
    ).filter(
        Question.examination_id == examination_id
    ).order_by(
        Question.position.asc().nullslast()
    ).all()


@router.get(
    "/api/questions/{question_id}",
    response_model=QuestionResponse
)
def get_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    question = db.query(Question).join(
        Examination
    ).options(
        joinedload(Question.options)
    ).filter(
        Question.id == question_id,
        Examination.teacher_id == current_user.id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    return question


@router.patch(
    "/api/questions/{question_id}",
    response_model=QuestionResponse
)
def update_question(
    question_id: uuid.UUID,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    question = db.query(Question).join(Examination).filter(
        Question.id == question_id,
        Examination.teacher_id == current_user.id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    update_data = question_data.model_dump(exclude={"options"})

    for field, value in update_data.items():
        setattr(question, field, value)

    question.options.clear()

    question.options.extend([
        QuestionOption(**option.model_dump())
        for option in question_data.options
    ])

    db.commit()
    db.refresh(question)

    return question


@router.delete(
    "/api/questions/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    question = db.query(Question).join(Examination).filter(
        Question.id == question_id,
        Examination.teacher_id == current_user.id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    db.delete(question)
    db.commit()
