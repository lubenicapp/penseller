from fastapi import FastAPI, HTTPException, Form, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import redis.asyncio as redis
import json
import os
import logging
import asyncio
from typing import Dict, Set
from app.workflow import workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Landing Page API")

# Mount static files for frontend (if directory exists)
frontend_dist = "/app/frontend/dist"
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=f"{frontend_dist}/assets"), name="assets")

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

# WebSocket connections for log streaming
active_connections: Dict[str, Set[WebSocket]] = {}
log_queues: Dict[str, asyncio.Queue] = {}

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
            .logs-container {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 12px;
                margin-top: 15px;
                display: none;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            .log-line {
                padding: 4px 0;
                color: #495057;
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
            
            <div id="logsContainer" class="logs-container"></div>
            <div id="successMessage" class="success"></div>
        </div>
        
        <script>
            let ws = null;
            
            function connectWebSocket(pageId) {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/logs/${pageId}`;
                
                ws = new WebSocket(wsUrl);
                const logsContainer = document.getElementById('logsContainer');
                
                ws.onopen = () => {
                    console.log('WebSocket connected');
                    logsContainer.style.display = 'block';
                };
                
                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.logs && data.logs.length > 0) {
                        logsContainer.innerHTML = data.logs.map(log => 
                            `<div class="log-line">${log}</div>`
                        ).join('');
                    }
                };
                
                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
                
                ws.onclose = () => {
                    console.log('WebSocket disconnected');
                };
            }
            
            function disconnectWebSocket() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }

            async function checkPageReady(pageId, maxAttempts = 60) {
                for (let i = 0; i < maxAttempts; i++) {
                    try {
                        const response = await fetch('/api/content/' + pageId);
                        if (response.ok) {
                            return true;
                        }
                    } catch (error) {
                        console.log('Checking...', i + 1);
                    }
                    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
                }
                return false;
            }

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
                        // Extract page ID from URL
                        const pageId = data.landing_page_url.split('id=')[1];
                        
                        // Connect to WebSocket for logs
                        connectWebSocket(pageId);
                        
                        // Show loading state
                        successMessage.innerHTML = '⏳ Generating your landing page...<br><small>This may take 1-2 minutes (AI generation in progress)</small>';
                        successMessage.style.display = 'block';
                        
                        // Wait for page to be ready
                        const ready = await checkPageReady(pageId);
                        
                        // Disconnect WebSocket
                        disconnectWebSocket();
                        
                        // Hide logs
                        document.getElementById('logsContainer').style.display = 'none';
                        
                        if (ready) {
                            successMessage.innerHTML = '✓ Landing page generated successfully!<br><br><a href="' + data.landing_page_url + '" target="_blank" style="color: #155724; text-decoration: underline; font-weight: bold;">Click here to view your landing page</a>';
                        } else {
                            successMessage.innerHTML = '⚠️ Generation is taking longer than expected.<br><br><a href="' + data.landing_page_url + '" target="_blank" style="color: #155724; text-decoration: underline; font-weight: bold;">Click here to try viewing your landing page</a>';
                        }
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
    # Extract username from LinkedIn URL - each user has ONE page that gets overwritten
    username = linkedin_url.rstrip('/').split('/')[-1]
    
    # Delete old page data from Redis before starting generation
    # This ensures the frontend polling won't find stale data
    try:
        await redis_client.delete(f"page:{username}")
        logger.info(f"Deleted old page data for: {username}")
    except Exception as e:
        logger.warning(f"Could not delete old page data: {e}")
    
    # Use relative URL so it works regardless of deployment location
    landing_page_url = f"/landing?id={username}"
    
    # Run workflow in background with the username as page_id
    background_tasks.add_task(workflow, product_description, linkedin_url, username)
    
    return {
        "message": "Landing page generation started!",
        "landing_page_url": landing_page_url,
        "page_id": username,
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

@app.websocket("/ws/logs/{page_id}")
async def websocket_logs(websocket: WebSocket, page_id: str):
    """WebSocket endpoint for streaming generation logs"""
    await websocket.accept()
    
    # Add this connection to active connections
    if page_id not in active_connections:
        active_connections[page_id] = set()
    active_connections[page_id].add(websocket)
    
    try:
        # Keep connection alive and send logs from Redis
        while True:
            # Check for logs in Redis
            log_key = f"logs:{page_id}"
            logs = await redis_client.lrange(log_key, -5, -1)  # Get last 5 logs
            
            if logs:
                await websocket.send_json({"logs": logs})
            
            await asyncio.sleep(0.5)  # Check every 500ms
            
    except WebSocketDisconnect:
        active_connections[page_id].discard(websocket)
        if not active_connections[page_id]:
            del active_connections[page_id]

async def emit_log(page_id: str, message: str):
    """Emit a log message to Redis for WebSocket streaming"""
    try:
        log_key = f"logs:{page_id}"
        await redis_client.rpush(log_key, message)
        await redis_client.expire(log_key, 300)  # Expire logs after 5 minutes
        # Keep only last 5 logs
        await redis_client.ltrim(log_key, -5, -1)
    except Exception as e:
        logger.error(f"Failed to emit log: {e}")

@app.get("/landing")
async def serve_landing_page():
    """Serve the React landing page"""
    frontend_index = "/app/frontend/dist/index.html"
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    else:
        raise HTTPException(status_code=404, detail="Landing page not found")
