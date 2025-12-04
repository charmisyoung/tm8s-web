
# =======================================
# Stage 1: Build the React Frontend
# =======================================
FROM node:18-alpine as frontend-builder

# Set working directory for the build
WORKDIR /app-frontend

# Copy frontend dependency files first (better caching)
COPY tm8s-frontend/package*.json ./

# Install Node dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY tm8s-frontend/ ./

# Build the React app (creates the /dist folder)
RUN npm run build

# =======================================
# Stage 2: Run the Python Backend
# =======================================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend requirements first
COPY tm8s-web/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Backend Source Code
COPY tm8s-web/ .

# Copy the Built Frontend from Stage 1
# We place it in a specific folder so FastAPI can serve it
COPY --from=frontend-builder /app-frontend/dist /app/static_ui

# Expose the port Fly.io expects
ENV PORT=8080

# Command to start the server
# We bind to 0.0.0.0 so external traffic can reach it
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

