from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define a customer model
class Customer(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

# In-memory customer "database"
customers = []

# Create a customer (POST)
@app.post("/customers/", response_model=Customer)
def create_customer(customer: Customer):
    for existing_customer in customers:
        if existing_customer.id == customer.id:
            raise HTTPException(status_code=400, detail="Customer with this ID already exists.")
    
    customers.append(customer)
    return customer

# Get all customers (GET)
@app.get("/customers/", response_model=List[Customer])
def get_customers():
    return customers

# Get a single customer by ID (GET)
@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    for customer in customers:
        if customer.id == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found.")

# Update a customer (PUT)
@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, updated_customer: Customer):
    for idx, customer in enumerate(customers):
        if customer.id == customer_id:
            customers[idx] = updated_customer
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found.")

# Delete a customer (DELETE)
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    for idx, customer in enumerate(customers):
        if customer.id == customer_id:
            del customers[idx]
            return {"message": "Customer deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found.")
