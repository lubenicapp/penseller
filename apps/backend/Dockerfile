# Stage 1: Build frontend
FROM oven/bun:1 AS frontend-builder

WORKDIR /frontend

# Copy frontend files
COPY landing_page/package*.json ./
COPY landing_page/bun.lockb ./

# Install dependencies
RUN bun install

# Copy rest of frontend source
COPY landing_page/ ./

# Build frontend
RUN bun run build

# Stage 2: Build backend with frontend
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app/ ./app/

# Copy built frontend from stage 1
COPY --from=frontend-builder /frontend/dist /app/frontend/dist

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
