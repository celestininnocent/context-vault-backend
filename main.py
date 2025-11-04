from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
import os
from datetime import datetime

app = FastAPI(title="Context Vault API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

# Pydantic models
class ContextData(BaseModel):
    user_id: str
    context_type: str
    context_data: dict
    metadata: Optional[dict] = None

class ContextResponse(BaseModel):
    id: str
    user_id: str
    context_type: str
    context_data: dict
    metadata: Optional[dict]
    created_at: str

@app.get("/")
async def root():
    return {
        "message": "Context Vault API",
        "version": "1.0.0",
        "endpoints": ["/vault/save", "/vault/context"]
    }

@app.post("/vault/save", response_model=dict)
async def save_context(context: ContextData):
    """
    Save context data to Supabase.
    
    Args:
        context: Context data containing user_id, context_type, context_data, and optional metadata
    
    Returns:
        Success message with saved context id
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            payload = {
                "user_id": context.user_id,
                "context_type": context.context_type,
                "context_data": context.context_data,
                "metadata": context.metadata or {},
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/context_vault",
                headers=headers,
                json=payload
            )
            
            if response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to save context: {response.text}"
                )
            
            result = response.json()
            return {
                "success": True,
                "message": "Context saved successfully",
                "data": result[0] if isinstance(result, list) else result
            }
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving context: {str(e)}")

@app.get("/vault/context", response_model=dict)
async def get_context(
    user_id: Optional[str] = None,
    context_type: Optional[str] = None,
    limit: int = 10
):
    """
    Retrieve context data from Supabase.
    
    Args:
        user_id: Optional filter by user_id
        context_type: Optional filter by context_type
        limit: Maximum number of records to return (default: 10)
    
    Returns:
        List of context records
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json"
            }
            
            # Build query parameters
            params = {"limit": limit, "order": "created_at.desc"}
            
            # Build filter string
            filters = []
            if user_id:
                filters.append(f"user_id=eq.{user_id}")
            if context_type:
                filters.append(f"context_type=eq.{context_type}")
            
            url = f"{SUPABASE_URL}/rest/v1/context_vault"
            if filters:
                url += "?" + "&".join(filters + [f"limit={limit}", "order=created_at.desc"])
            else:
                url += f"?limit={limit}&order=created_at.desc"
            
            response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to retrieve context: {response.text}"
                )
            
            result = response.json()
            return {
                "success": True,
                "count": len(result),
                "data": result
            }
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
