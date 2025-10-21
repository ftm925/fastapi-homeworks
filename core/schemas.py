from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated

def validate_cost(value: float):
        if value <0:
            raise ValueError("Cost can not be a negative value.")
        return value

def validate_description(value: str):
    if len(value) >50 or len(value) <2:
            raise ValueError("Description must have 2-50 charachters such as: digits, alphabets and . _")
    return value

class ExpenseRecordCreateSchema(BaseModel):
    
    description: Annotated[str,Field(...,description='What was it spent on?'), AfterValidator(validate_description)]
    cost: Annotated[float,Field(..., description='How much do you spent on?'), AfterValidator(validate_cost)]


class ExpenseRecordUpdateSchema(BaseModel):
    
    new_cost: Annotated[float,Field(..., description='What is the updated cost?'), AfterValidator(validate_cost)]
