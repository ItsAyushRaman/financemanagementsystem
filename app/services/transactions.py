from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.domain import Transaction
from app.schemas.dto import TransactionCreate, TransactionUpdate

class TransactionService:
    @staticmethod
    def get_transaction(db: Session, db_id: int):
        return db.query(Transaction).filter(Transaction.id == db_id).first()

    @staticmethod
    def create_transaction(db: Session, obj_in: TransactionCreate, owner_id: int):
        db_obj = Transaction(
            **obj_in.model_dump(exclude_unset=True),
            owner_id=owner_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_transaction(db: Session, db_obj: Transaction, obj_in: TransactionUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_transaction(db: Session, db_obj: Transaction):
        db.delete(db_obj)
        db.commit()
        return {"detail": "Transaction deleted"}

    @staticmethod
    def get_summary(db: Session, owner_id: int):
        # Admin or specific owner scope? For simplicity let's scope by the user.
        # But if Admin, maybe they can pass different params. Assume scoped to user here.
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.owner_id == owner_id, Transaction.type == "income"
        ).scalar() or 0.0
        
        expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.owner_id == owner_id, Transaction.type == "expense"
        ).scalar() or 0.0

        categories = db.query(Transaction.category, func.sum(Transaction.amount)).filter(
            Transaction.owner_id == owner_id
        ).group_by(Transaction.category).all()
        
        return {
            "total_income": income,
            "total_expense": expense,
            "current_balance": income - expense,
            "category_breakdown": {cat: amt for cat, amt in categories}
        }
