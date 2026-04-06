from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.domain import User, Transaction
from app.schemas.dto import TransactionCreate, TransactionUpdate, TransactionResponse, FinancialSummary
from app.api.deps import require_role, get_current_user
from app.services.transactions import TransactionService

router = APIRouter()

# CREATE: Everyone except Viewers. ("Viewer" = read-only roughly)
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Analyst"]))
):
    return TransactionService.create_transaction(db, transaction_in, current_user.id)

# READ: Viewers, Analysts, Admins
@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    type_: Optional[str] = Query(None, alias="type"),
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Viewer", "Analyst", "Admin"]))
):
    query = db.query(Transaction).filter(Transaction.owner_id == current_user.id)
    if type_: query = query.filter(Transaction.type == type_)
    if category: query = query.filter(Transaction.category == category)
    if start_date: query = query.filter(Transaction.date >= start_date)
    if end_date: query = query.filter(Transaction.date <= end_date)
    
    return query.offset(skip).limit(limit).all()

# UPDATE: Analysts and Admins
@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    transaction_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Analyst"]))
):
    db_obj = TransactionService.get_transaction(db, id)
    if not db_obj or db_obj.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found or forbidden")
    return TransactionService.update_transaction(db, db_obj, transaction_in)

# DELETE: Admins only
@router.delete("/{id}")
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin"]))
):
    db_obj = TransactionService.get_transaction(db, id)
    if not db_obj or db_obj.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found or forbidden")
    return TransactionService.delete_transaction(db, db_obj)

# SUMMARY: Analysts and Admins (maybe view too, but let's give viewers less access for demo purposes, or grant all)
@router.get("/summary", response_model=FinancialSummary)
def get_financial_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Viewer", "Analyst", "Admin"]))
):
    return TransactionService.get_summary(db, current_user.id)
