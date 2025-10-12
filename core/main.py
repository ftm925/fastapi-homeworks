from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.responses import JSONResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Started ...")
    yield 
    print("Application Stopped")


app = FastAPI(title="Cost Management Application")
expense_records = [
    {
      "id": 1,
      "description": "coffee",
      "cost": 100000
    },
    {
      "id": 2,
      "description": "pizza",
      "cost": 350000
    },
    {
      "id": 3,
      "description": "shoe",
      "cost": 1500000
    },
    {
        "id": 4,
        "description": "book",
        "cost": 165720
    }
  ]

def generate_record_id(records):

    if len(records):
        return records[-1].get("id")+1
    return 1

@app.post("/expense")
async def add_expense(description: str = Form(title="What was it spent on?"), cost: float = Form(title="The amount money paid.")):
    
    record_id = generate_record_id(expense_records)
    record_description = description
    record_cost = cost

    data = {"id": record_id, "description": record_description, "cost": record_cost}
    expense_records.append(data)

    return JSONResponse(content={"detail": "Cost add successfully."}, status_code=status.HTTP_201_CREATED)

@app.get("/expenses")
async def get_expenses_list():
    if expense_records:
        return JSONResponse(content={"detail": expense_records}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No expense record found.")

@app.get("/expenses/{record_id}")
async def get_unique_expense(record_id: int, ):

    for record in expense_records:
        if record["id"] == record_id:
            return JSONResponse(content={"detail": record}, status_code=status.HTTP_200_OK)
        
    ## when not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

@app.put("/expenses/{record_id}")
async def update_expense_detail(record_id: int, new_cost: float):
    for record in expense_records:
        if record["id"] == record_id:
            record["cost"] = new_cost
            return JSONResponse(content={"detail":record}, status_code=status.HTTP_200_OK)
        
    ## when not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

@app.delete("/expenses/{record_id}")
async def delete_expense(record_id: int):
    for index, record in enumerate(expense_records):
        if record["id"] == record_id:
            del expense_records[index]
            return JSONResponse(content={"detail":f"Expense record with ID {record_id} deleted successfully"}, status_code=status.HTTP_200_OK)
        
    ## when not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")


    
    
    






