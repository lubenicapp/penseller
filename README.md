# Pioneer - Dynamic Landing Page Application

A dynamic landing page system with FastAPI backend, Redis key-value database, and React frontend.

## Architecture

```
pioneer/
├── apps/
│   ├── backend/          # FastAPI backend API
│   │   ├── app/
│   │   │   └── main.py   # API endpoints
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── landing_page/     # React frontend
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── docker-compose.yml    # Orchestrates all services
└── init_data.py         # Initialize sample data in Redis
```

## Services

1. **Redis** - Key-value database (port 6379)
2. **Backend API** - FastAPI service (port 8000)
3. **Landing Page** - React/Vite frontend (port 3000)

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for running init_data.py locally)

### 1. Start All Services

```bash
# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 2. Initialize Sample Data

```bash
# Install redis Python package if needed
pip install redis

# Run initialization script
python3 init_data.py
```

This creates sample pages with IDs:
- `default` - Default landing page content
- `123456` - Custom example page
- `promo-2024` - Promotional content
- `education` - Education-focused content

### 3. Access the Application

Open your browser and visit:

- **Default page**: http://localhost:3000
- **Custom page**: http://localhost:3000?id=123456
- **Promo page**: http://localhost:3000?id=promo-2024
- **Education page**: http://localhost:3000?id=education

### 4. Access the API

- **API documentation**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/api/health
- **Get content**: http://localhost:8000/api/content/123456

## Using the Dynamic Content System

### How It Works

1. User visits the landing page with a URL parameter: `?id=YOUR_ID`
2. Frontend fetches content from the backend API
3. Backend retrieves data from Redis using the ID as the key
4. Dynamic content (title, subtitle, description) is displayed

### Creating New Content

#### Option 1: Using the API (POST endpoint)

**Basic content:**
```bash
curl -X POST "http://localhost:8000/api/content/my-new-page?title=My%20Title&subtitle=My%20Subtitle&description=My%20Description"
```

**With custom testimonials:**
```bash
curl -X POST "http://localhost:8000/api/content/my-page" \
  -d "title=My Title" \
  -d "subtitle=My Subtitle" \
  -d "description=My Description" \
  -d "testimonial1_name=John Doe" \
  -d "testimonial1_role=CEO & Founder" \
  -d "testimonial1_avatar_url=https://example.com/avatar.jpg" \
  -d "testimonial2_name=Jane Smith" \
  -d "testimonial2_role=Product Designer"
```

#### Option 2: Using Python with Redis

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

content = {
    "id": "my-new-page",
    "title": "My Custom Title",
    "subtitle": "My custom subtitle text",
    "description": "Optional description"
}

r.set(f"page:my-new-page", json.dumps(content))
```

Then visit: http://localhost:3000?id=my-new-page

#### Option 3: Using Redis CLI

```bash
# Connect to Redis container
docker exec -it redis redis-cli

# Set content
SET page:my-id '{"id":"my-id","title":"My Title","subtitle":"My Subtitle","description":"My Description"}'

# Get content
GET page:my-id

# List all pages
KEYS page:*
```

## Customizable Fields

The landing page supports dynamic customization of the following elements:

### Hero Section
- **title** - Main headline
- **subtitle** - Supporting text
- **description** - Additional descriptive text

### Testimonials Section
You can customize the first two testimonials:

**Testimonial 1:**
- **testimonial1_name** - Customer name (e.g., "Sarah Mitchell")
- **testimonial1_role** - Customer role/title (e.g., "Artist & Illustrator")
- **testimonial1_avatar_url** - Profile picture URL (optional, falls back to initials)

**Testimonial 2:**
- **testimonial2_name** - Customer name
- **testimonial2_role** - Customer role/title
- **testimonial2_avatar_url** - Profile picture URL (optional)

If testimonial fields are not provided, the page displays default testimonials. You can customize just the name and role while keeping the default avatar (initials will be auto-generated from the name).

### Company Logos Section
You can customize up to 4 company logos in the "Trusted by leading companies" section:

- **company_logo1** - First company logo URL
- **company_logo2** - Second company logo URL
- **company_logo3** - Third company logo URL
- **company_logo4** - Fourth company logo URL

If logo URLs are not provided, the page displays default company logos. You can customize individual logos while keeping others as defaults.

**Example with custom testimonials and company logos:**
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

content = {
    "id": "my-campaign",
    "title": "Special Summer Campaign",
    "subtitle": "Limited time offer - 30% off!",
    "description": "Don't miss out on this exclusive deal",
    "testimonial1": {
        "name": "Alex Johnson",
        "role": "Professional Designer",
        "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"
    },
    "testimonial2": {
        "name": "Maria Garcia",
        "role": "Creative Director"
        # avatarUrl is optional - will show initials "MG"
    },
    "companyLogos": {
        "logo1": "https://logo.clearbit.com/google.com",
        "logo2": "https://logo.clearbit.com/microsoft.com",
        "logo3": "https://logo.clearbit.com/apple.com",
        "logo4": "https://logo.clearbit.com/amazon.com"
    }
}

r.set(f"page:my-campaign", json.dumps(content))
```

**Using the API with all custom fields:**
```bash
curl -X POST "http://localhost:8000/api/content/my-page" \
  -d "title=My Custom Page" \
  -d "subtitle=Amazing Products" \
  -d "description=Check out our latest offerings" \
  -d "testimonial1_name=Sarah Mitchell" \
  -d "testimonial1_role=Artist & Illustrator" \
  -d "testimonial1_avatar_url=https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah" \
  -d "testimonial2_name=John Doe" \
  -d "testimonial2_role=Creative Director" \
  -d "company_logo1=https://logo.clearbit.com/netflix.com" \
  -d "company_logo2=https://logo.clearbit.com/spotify.com" \
  -d "company_logo3=https://logo.clearbit.com/adobe.com" \
  -d "company_logo4=https://logo.clearbit.com/figma.com"
```

## API Endpoints

### GET /api/content/{page_id}
Retrieve page content by ID.

**Response:**
```json
{
  "id": "123456",
  "title": "Welcome to Your Custom Landing Page",
  "subtitle": "This content is loaded dynamically...",
  "description": "You can customize this content...",
  "testimonial1": {
    "name": "Alex Johnson",
    "role": "Professional Designer",
    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"
  },
  "testimonial2": {
    "name": "Maria Garcia",
    "role": "Creative Director",
    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Maria"
  }
}
```

### POST /api/content/{page_id}
Create or update page content.

**Parameters:**
- `title` (required) - Page title
- `subtitle` (required) - Page subtitle
- `description` (optional) - Additional description
- `testimonial1_name` (optional) - First testimonial name
- `testimonial1_role` (optional) - First testimonial role
- `testimonial1_avatar_url` (optional) - First testimonial avatar URL
- `testimonial2_name` (optional) - Second testimonial name
- `testimonial2_role` (optional) - Second testimonial role
- `testimonial2_avatar_url` (optional) - Second testimonial avatar URL

### GET /api/health
Health check endpoint for monitoring.

## Development

### Running Services Individually

#### Backend Only
```bash
cd apps/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Only
```bash
cd apps/landing_page
npm install
npm run dev
```

#### Redis Only
```bash
docker-compose up redis
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears Redis data)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f landing_page
docker-compose logs -f redis
```

## Configuration

### Environment Variables

**Backend** (in docker-compose.yml):
- `REDIS_HOST` - Redis hostname (default: redis)
- `REDIS_PORT` - Redis port (default: 6379)

**Frontend** (build argument):
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

### Ports

- `3000` - Frontend (Nginx)
- `8000` - Backend API (FastAPI)
- `6379` - Redis database

To change ports, modify the `ports` section in `docker-compose.yml`.

## Troubleshooting

### Can't connect to Docker daemon
```bash
# Start Docker/Colima
colima start

# Or for Docker Desktop, ensure it's running
```

### Redis connection errors
```bash
# Check if Redis is running
docker-compose ps redis

# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

### Frontend not loading data
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Check browser console for errors
# Verify CORS settings in backend
```

### Port already in use
```bash
# Find what's using the port
lsof -i :3000

# Change port in docker-compose.yml
ports:
  - "3001:80"  # Use 3001 instead of 3000
```

## Production Considerations

1. **Security**:
   - Update CORS settings in `apps/backend/app/main.py`
   - Use environment variables for sensitive data
   - Enable Redis authentication
   - Use HTTPS for production

2. **Performance**:
   - Redis persistence is enabled (appendonly)
   - Consider Redis clustering for scale
   - Use CDN for static assets

3. **Monitoring**:
   - Health check endpoints are configured
   - Add logging and monitoring tools
   - Set up alerts for service failures

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui
- **Backend**: Python 3.11, FastAPI, Redis async client
- **Database**: Redis 7 (key-value store)
- **Web Server**: Nginx (for frontend)
- **Containerization**: Docker, Docker Compose

## License

MIT
