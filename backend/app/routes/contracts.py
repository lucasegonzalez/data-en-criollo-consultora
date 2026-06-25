from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate, ContractResponse
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ContractResponse])
def list_contracts(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Contract).all()

@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(contract_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(404, "Contrato no encontrado")
    return contract

@router.post("/", response_model=ContractResponse, status_code=201)
def create_contract(data: ContractCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    contract = Contract(**data.model_dump())
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(contract_id: int, data: ContractCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(404, "Contrato no encontrado")
    for key, val in data.model_dump().items():
        setattr(contract, key, val)
    db.commit()
    db.refresh(contract)
    return contract

@router.delete("/{contract_id}", status_code=204)
def delete_contract(contract_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(404, "Contrato no encontrado")
    db.delete(contract)
    db.commit()
