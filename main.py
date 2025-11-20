import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Inquiry
from database import create_document

app = FastAPI(title="Consulting Site API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Consulting website backend is running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


class Service(BaseModel):
    id: str
    title: str
    audience: List[str]
    description: str
    highlights: List[str]


@app.get("/api/services", response_model=List[Service])
def get_services():
    return [
        Service(
            id="architecture",
            title="Solution & Systems Architecture",
            audience=["Technical Architects", "CTOs", "Founders"],
            description="End-to-end architecture for scalable, secure, and cost-efficient systems.",
            highlights=[
                "Cloud-native blueprints (AWS/GCP/Azure)",
                "Event-driven and microservices",
                "Zero-downtime migration strategies",
                "Security, observability, and compliance",
            ],
        ),
        Service(
            id="delivery",
            title="Delivery Acceleration",
            audience=["Developers", "Engineering Managers"],
            description="Unblock teams with hands-on enablement, tooling, and agile delivery.",
            highlights=[
                "CI/CD pipelines and platform engineering",
                "DevEx improvements and code quality",
                "Automated testing and release strategies",
                "Team coaching and playbooks",
            ],
        ),
        Service(
            id="advisory",
            title="Technology Advisory",
            audience=["Business Owners", "Product Leaders"],
            description="Make confident decisions with research, audits, and roadmaps.",
            highlights=[
                "Architecture and cost audits",
                "Build vs buy assessments",
                "Vendor selection and RFP support",
                "Executive-ready recommendations",
            ],
        ),
        Service(
            id="ai",
            title="AI Enablement",
            audience=["Consultants", "Enterprises"],
            description="Identify high-ROI AI use cases and safely integrate LLMs.",
            highlights=[
                "Use-case discovery and prioritization",
                "Prototype -> pilot -> production",
                "Evaluation, guardrails, and governance",
                "Change management and training",
            ],
        ),
    ]


class Highlight(BaseModel):
    label: str
    value: str


@app.get("/api/highlights", response_model=List[Highlight])
def get_highlights():
    return [
        Highlight(label="Average ROI", value="3-10x"),
        Highlight(label="Avg. Time-to-Value", value="< 6 weeks"),
        Highlight(label="Client NPS", value="72"),
        Highlight(label="Engagements Delivered", value="> 120"),
    ]


@app.post("/api/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
