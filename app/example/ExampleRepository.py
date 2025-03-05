from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from app.shared.config.Database import get_db_connection
from app.Example.ExampleModel import ExampleModel


class ExampleRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, example: ExampleModel) -> ExampleModel:
        self.db.add(example)
        self.db.commit()
        self.db.refresh(example)
        return example

    def get_example_by_id(self, example_id: int) -> Optional[ExampleModel]:
        return self.db.query(ExampleModel).filter(ExampleModel.id == example_id).first()

    def get_example_by_name(self, name: str) -> Optional[ExampleModel]:
        return self.db.query(ExampleModel).filter(ExampleModel.name == name).first()

    def get_example(self) -> Optional[ExampleModel]:
        return self.db.query(ExampleModel).first()

    def update(self, example: ExampleModel) -> ExampleModel:
        self.db.commit()
        self.db.refresh(example)
        return example

    def delete(self, example: ExampleModel) -> None:
        self.db.delete(example)
        self.db.commit()
