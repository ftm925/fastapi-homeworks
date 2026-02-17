from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from logging import Logger

from database import Base, engine, get_db, Expense
import schemas
import json

logger = Logger(name="app log")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("Application Started!")
    Base.metadata.create_all(engine)
    yield 
    print("Application Stopped")

app = FastAPI(title="Cost Management Application", lifespan=app_lifespan)

@app.post("/expenses")
async def add_expense(expense_record: schemas.ExpenseRecordCreateSchema, db: Session = Depends(get_db) ):
    
    new_record = Expense(cost=expense_record.cost, description=expense_record.description)

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(content={"detail": "Cost add successfully."}, status_code=status.HTTP_201_CREATED)

@app.get("/expenses")
async def get_expenses_list(db: Session = Depends(get_db)):
    
    all_expenses = db.query(Expense).all()
    
    if all_expenses:
        all_expenses = [expense.as_dict() for expense in all_expenses]
        print(all_expenses)
        return JSONResponse(content={"detail": all_expenses}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No expense record found.")

@app.get("/expenses/{record_id}")
async def get_unique_expense(record_id: int, db:Session = Depends(get_db)):

    expense_record = db.query(Expense).filter_by(id= record_id).one_or_none()
    if expense_record:
        return JSONResponse(content={"detail": expense_record.as_dict()}, status_code=status.HTTP_200_OK)
    else:
        ## when not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

@app.put("/expenses/{record_id}")
async def update_expense_detail(record_id: int, expense: schemas.ExpenseRecordUpdateSchema, db:Session = Depends(get_db)):
    
    expense_record = db.query(Expense).filter_by(id= record_id).one_or_none()
    
    if expense_record:
        expense_record.cost = expense.new_cost
        db.commit()
        db.refresh(expense_record)
        return JSONResponse(content={"detail":expense_record.as_dict()}, status_code=status.HTTP_200_OK)

    else:                
        ## when not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

@app.delete("/expenses/{record_id}")
async def delete_expense(record_id: int, db:Session = Depends(get_db)):
    
    expense_record = db.query(Expense).filter_by(id= record_id).one_or_none()
    if expense_record:
        db.delete(expense_record)
        db.commit()
        return JSONResponse(content={"detail":f"Expense record with ID {record_id} deleted successfully"}, status_code=status.HTTP_200_OK)
    
    else:        
        ## when not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")


    

