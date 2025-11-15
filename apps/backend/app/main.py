from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import json
import os

app = FastAPI(title="Landing Page API")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_client = await redis.from_url(
        f"redis://{redis_host}:{redis_port}",
        encoding="utf-8",
        decode_responses=True
    )

@app.on_event("shutdown")
async def shutdown_event():
    if redis_client:
        await redis_client.close()

@app.get("/")
async def root():
    return {"message": "Landing Page API", "status": "running"}

@app.get("/api/content/{page_id}")
async def get_content(page_id: str):
    """
    Get page content by ID from Redis
    Returns: {title, subtitle, and any other stored fields}
    """
    try:
        # Get data from Redis
        data = await redis_client.get(f"page:{page_id}")
        
        if data is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Content not found for ID: {page_id}"
            )
        
        # Parse JSON data
        content = json.loads(data)
        return content
        
    except redis.RedisError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}"
        )

@app.post("/api/content/{page_id}")
async def create_content(
    page_id: str, 
    title: str, 
    subtitle: str, 
    description: str = "",
    testimonial1_name: str = None,
    testimonial1_role: str = None,
    testimonial1_avatar_url: str = None,
    testimonial2_name: str = None,
    testimonial2_role: str = None,
    testimonial2_avatar_url: str = None,
    company_logo1: str = None,
    company_logo2: str = None,
    company_logo3: str = None,
    company_logo4: str = None
):
    """
    Create or update page content including testimonials and company logos
    """
    try:
        content = {
            "id": page_id,
            "title": title,
            "subtitle": subtitle,
            "description": description
        }
        
        # Add testimonial1 if any field is provided
        if testimonial1_name or testimonial1_role or testimonial1_avatar_url:
            content["testimonial1"] = {}
            if testimonial1_name:
                content["testimonial1"]["name"] = testimonial1_name
            if testimonial1_role:
                content["testimonial1"]["role"] = testimonial1_role
            if testimonial1_avatar_url:
                content["testimonial1"]["avatarUrl"] = testimonial1_avatar_url
        
        # Add testimonial2 if any field is provided
        if testimonial2_name or testimonial2_role or testimonial2_avatar_url:
            content["testimonial2"] = {}
            if testimonial2_name:
                content["testimonial2"]["name"] = testimonial2_name
            if testimonial2_role:
                content["testimonial2"]["role"] = testimonial2_role
            if testimonial2_avatar_url:
                content["testimonial2"]["avatarUrl"] = testimonial2_avatar_url
        
        # Add company logos if any are provided
        if company_logo1 or company_logo2 or company_logo3 or company_logo4:
            content["companyLogos"] = {}
            if company_logo1:
                content["companyLogos"]["logo1"] = company_logo1
            if company_logo2:
                content["companyLogos"]["logo2"] = company_logo2
            if company_logo3:
                content["companyLogos"]["logo3"] = company_logo3
            if company_logo4:
                content["companyLogos"]["logo4"] = company_logo4
        
        # Store in Redis
        await redis_client.set(
            f"page:{page_id}", 
            json.dumps(content)
        )
        
        return {"message": "Content saved successfully", "data": content}
        
    except redis.RedisError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        await redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
