from fastapi import FastAPI, HTTPException, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import redis.asyncio as redis
import json
import os
import logging
from app.workflow import workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with a form to submit product description and LinkedIn URL"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Landing Page Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #333;
                font-weight: bold;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                box-sizing: border-box;
            }
            textarea {
                min-height: 100px;
                resize: vertical;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }
            button:hover {
                background-color: #45a049;
            }
            .success {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 12px;
                border-radius: 4px;
                margin-top: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Landing Page Generator</h1>
            <p class="subtitle">Generate a custom landing page based on a product description and LinkedIn profile</p>
            
            <form id="generateForm">
                <div class="form-group">
                    <label for="product_description">Product Description</label>
                    <textarea 
                        id="product_description" 
                        name="product_description" 
                        required
                    >LambdaPen: Innovative pencil extensions that provide a comfortable, ergonomic grip even when your pencils are sharpened down to a stub. Never waste a pencil again.</textarea>
                </div>
                
                <div class="form-group">
                    <label for="linkedin_url">LinkedIn URL</label>
                    <input 
                        type="url" 
                        id="linkedin_url" 
                        name="linkedin_url" 
                        required
                        value="https://www.linkedin.com/in/roxannevarza/"
                    />
                </div>
                
                <button type="submit">Generate Landing Page</button>
            </form>
            
            <div id="successMessage" class="success"></div>
        </div>
        
        <script>
            document.getElementById('generateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData();
                formData.append('product_description', document.getElementById('product_description').value);
                formData.append('linkedin_url', document.getElementById('linkedin_url').value);
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    const successMessage = document.getElementById('successMessage');
                    if (response.ok) {
                        successMessage.textContent = '✓ ' + data.message;
                        successMessage.style.display = 'block';
                        setTimeout(() => {
                            successMessage.style.display = 'none';
                        }, 5000);
                    } else {
                        successMessage.textContent = '✗ Error: ' + data.detail;
                        successMessage.style.backgroundColor = '#f8d7da';
                        successMessage.style.borderColor = '#f5c6cb';
                        successMessage.style.color = '#721c24';
                        successMessage.style.display = 'block';
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/generate")
async def generate_landing_page(
    background_tasks: BackgroundTasks,
    product_description: str = Form(...),
    linkedin_url: str = Form(...)
):
    """
    Generate a landing page based on product description and LinkedIn URL
    Runs the workflow in the background
    """
    # Extract username from LinkedIn URL for the landing page URL
    username = linkedin_url.rstrip('/').split('/')[-1]
    landing_page_url = f"http://localhost:3000?id={username}"
    
    # Run workflow in background
    background_tasks.add_task(workflow, product_description, linkedin_url)
    
    return {
        "message": "Landing page generation started!",
        "landing_page_url": landing_page_url,
        "status": "processing"
    }

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
