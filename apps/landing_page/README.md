# LambdaPen Landing Page - Dockerized

This is the LambdaPen landing page application, dockerized and ready to deploy.

## Project Structure

```
apps/landing_page/
├── Dockerfile          # Multi-stage Docker build configuration
├── .dockerignore       # Files to exclude from Docker build
├── src/                # React source code
├── public/             # Static assets
└── package.json        # Node.js dependencies
```

## Technology Stack

- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: Radix UI + shadcn/ui
- **Styling**: Tailwind CSS
- **Web Server**: Nginx (in production container)

## Running with Docker Compose

From the root of the project (`/Users/vonguyen/Code/pioneer`):

### Start the application:
```bash
docker-compose up -d
```

### Build and start:
```bash
docker-compose up -d --build
```

### Stop the application:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f landing_page
```

## Accessing the Application

Once running, the landing page will be available at:
- **URL**: http://localhost:3000

## Docker Setup Details

### Multi-Stage Build
The Dockerfile uses a multi-stage build process:
1. **Builder stage**: Installs dependencies and builds the React app
2. **Production stage**: Serves the built static files using Nginx

### Ports
- Container exposes port 80 (Nginx)
- Mapped to host port 3000

### Network
The application runs on a custom bridge network called `pioneer_network`, making it easy to add more services in the future.

## Development

To run the application locally without Docker:

```bash
cd apps/landing_page
npm install
npm run dev
```

The development server will start at http://localhost:5173

## Building for Production

The Docker build process automatically:
1. Installs all dependencies
2. Runs `npm run build` to create optimized production assets
3. Copies the built files to Nginx
4. Configures Nginx to serve the application

## Notes

- The application is a static React site, so no backend is required
- Nginx serves the application efficiently with caching headers
- The Docker image is optimized for production use
