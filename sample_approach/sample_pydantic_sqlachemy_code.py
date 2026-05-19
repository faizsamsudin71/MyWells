# 1. The SQLModel (The Database Map & Excel Gatekeeper)
# This single class defines both the SQL database table and handles Excel validation.

from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
import pandas as pd

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    # We define the primary key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Alias maps "Excel Header" -> "Python Variable"
    # sa_column_kwargs maps "Python Variable" -> DB Column properties
    name: str = Field(
        alias="Name", 
        sa_column_kwargs={"name": "full_name"}
    )
    
    age: Optional[int] = Field(
        default=None, 
        alias="Age", 
        ge=0, 
        le=120, 
        sa_column_kwargs={"name": "user_age"}
    )
    
    email: Optional[EmailStr] = Field(
        default=None, 
        alias="Email Address", 
        sa_column_kwargs={"name": "email_address", "unique": True}
    )

# 2. The "Relay" Logic
# Load and validate using pandas and SQLModel

# Step A: Load the messy Excel
df = pd.read_excel("data/data.xlsx") 

db_instances = []

# Step B: Iterate and Validate using the faster to_dict('records')
records = df.to_dict(orient='records')

for row in records:
    try:
        # Validates like Pydantic, returns a SQLAlchemy-ready object
        user = User.model_validate(row)
        db_instances.append(user)
        
    except Exception as e:
        print(f"Validation failed for a row: {e}")

# Step C: Load to DB
# session.add_all(db_instances)
# session.commit()