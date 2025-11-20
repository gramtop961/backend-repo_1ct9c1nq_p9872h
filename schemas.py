"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Consulting website specific schema
class Inquiry(BaseModel):
    """
    Inquiries from contact/quote forms
    Collection name: "inquiry"
    """
    name: str = Field(..., min_length=2, description="Contact's full name")
    email: EmailStr
    company: Optional[str] = Field(None, description="Company name")
    role: Optional[str] = Field(None, description="Role or title")
    phone: Optional[str] = Field(None, description="Phone number")
    services: Optional[List[str]] = Field(default=None, description="Requested services")
    budget_range: Optional[str] = Field(None, description="Estimated budget range")
    message: str = Field(..., min_length=10, description="Message or project details")
    source: Optional[str] = Field(None, description="How they heard about us")
