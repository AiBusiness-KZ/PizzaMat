# Multi-stage build for production frontend
FROM node:20-alpine AS builder

WORKDIR /app

# Declare build arguments
ARG VITE_API_URL=https://api.pizzamat.aibusiness.kz
ARG NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --production=false

# Set environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV NODE_ENV=$NODE_ENV

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Copy built files to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Create nginx configuration
RUN echo 'server { \n\
    listen 80; \n\
    server_name _; \n\
    root /usr/share/nginx/html; \n\
    index index.html; \n\
    \n\
    # Enable access and error logs \n\
    access_log /var/log/nginx/access.log; \n\
    error_log /var/log/nginx/error.log warn; \n\
    \n\
    # Security headers \n\
    add_header X-Frame-Options "SAMEORIGIN" always; \n\
    add_header X-Content-Type-Options "nosniff" always; \n\
    add_header X-XSS-Protection "1; mode=block" always; \n\
    \n\
    # Gzip compression \n\
    gzip on; \n\
    gzip_vary on; \n\
    gzip_min_length 1024; \n\
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/javascript application/xml+rss application/json; \n\
    \n\
    # SPA routing - all routes go to index.html \n\
    location / { \n\
        try_files $uri $uri/ /index.html; \n\
    } \n\
    \n\
    # Cache static assets \n\
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ { \n\
        expires 1y; \n\
        add_header Cache-Control "public, immutable"; \n\
    } \n\
    \n\
    # Health check endpoint \n\
    location /health { \n\
        access_log off; \n\
        return 200 "healthy\n"; \n\
        add_header Content-Type text/plain; \n\
    } \n\
}' > /etc/nginx/conf.d/default.conf

# Redirect logs to stdout/stderr for Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
