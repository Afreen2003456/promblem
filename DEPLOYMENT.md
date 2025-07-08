# Deployment Guide - Airline Data Insights

This guide provides comprehensive instructions for deploying the Airline Data Insights application in various environments.

## 🚀 Quick Start (Recommended)

### Using the Start Script (Linux/macOS)
```bash
./start.sh
```

### Using the Start Script (Windows with Git Bash)
```bash
bash start.sh
```

### Manual Start
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# Terminal 2 - Frontend
cd frontend
python -m http.server 8080
```

## 🐳 Docker Deployment

### Single Container
```bash
# Build the image
docker build -t airline-insights .

# Run the container
docker run -p 8000:8000 airline-insights

# With environment variables
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key airline-insights
```

### Docker Compose (Recommended for Development)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## ☁️ Cloud Deployment

### 1. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps
```bash
# Create Heroku app
heroku create airline-insights-app

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set DEBUG=false

# Deploy
git push heroku main
```

#### Procfile
```
web: python backend/run.py
```

### 2. AWS Deployment

#### Using AWS Elastic Beanstalk
1. **Prepare application**
   ```bash
   # Create application zip
   zip -r airline-insights.zip . -x "*.git*" "*/venv/*" "*/node_modules/*"
   ```

2. **Deploy via AWS Console**
   - Go to Elastic Beanstalk console
   - Create new application
   - Upload zip file
   - Configure environment variables

#### Using AWS ECS
1. **Build and push Docker image**
   ```bash
   # Build image
   docker build -t airline-insights .
   
   # Tag for ECR
   docker tag airline-insights:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/airline-insights:latest
   
   # Push to ECR
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/airline-insights:latest
   ```

2. **Create ECS service**
   - Create task definition
   - Create service
   - Configure load balancer

### 3. Google Cloud Platform

#### Using Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/airline-insights
gcloud run deploy --image gcr.io/PROJECT-ID/airline-insights --platform managed
```

#### Using Google App Engine
Create `app.yaml`:
```yaml
runtime: python39
service: default

env_variables:
  OPENAI_API_KEY: your_key_here

handlers:
  - url: /static
    static_dir: frontend
  - url: /.*
    script: auto
```

### 4. Azure Deployment

#### Using Azure App Service
```bash
# Create resource group
az group create --name airline-insights-rg --location eastus

# Create app service plan
az appservice plan create --name airline-insights-plan --resource-group airline-insights-rg --sku B1

# Create web app
az webapp create --resource-group airline-insights-rg --plan airline-insights-plan --name airline-insights-app

# Deploy code
az webapp deployment source config-zip --resource-group airline-insights-rg --name airline-insights-app --src airline-insights.zip
```

## 🌐 Production Configuration

### Environment Variables
```env
# Required
OPENAI_API_KEY=your_production_key

# Application
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your_secure_secret_key
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Performance
CACHE_TTL=3600
ENABLE_CACHE=true
```

### Reverse Proxy Configuration (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static {
        root /path/to/frontend;
        expires 1y;
    }
}
```

### SSL/TLS Configuration
```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📊 Monitoring and Logging

### Health Checks
The application provides health check endpoints:
- `GET /health` - Application health status
- `GET /health/detailed` - Detailed health information

### Logging Configuration
```python
# Set log level via environment
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json, text
```

### Monitoring Tools
- **Application Performance**: New Relic, Datadog
- **Infrastructure**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **Uptime Monitoring**: Pingdom, UptimeRobot

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Set secure environment variables
- [ ] Configure CORS appropriately
- [ ] Enable rate limiting
- [ ] Use secure headers
- [ ] Implement authentication if needed
- [ ] Regular security updates

### Environment Variables Security
```bash
# Use secrets management
kubectl create secret generic airline-insights-secrets \
  --from-literal=OPENAI_API_KEY=your_key

# Or use cloud-specific solutions
# AWS: AWS Secrets Manager
# Azure: Azure Key Vault
# GCP: Google Secret Manager
```

## 📈 Performance Optimization

### Backend Optimization
- Use gunicorn with multiple workers
- Enable response caching
- Implement connection pooling
- Use async operations where possible

### Frontend Optimization
- Enable gzip compression
- Use CDN for static assets
- Implement browser caching
- Minify CSS/JS files

### Database Optimization (Future)
- Use connection pooling
- Implement read replicas
- Add database indexing
- Use caching layers (Redis)

## 🔧 Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check Python version
python --version

# Check dependencies
pip check

# Check port availability
lsof -i :8000
```

#### Frontend not loading
```bash
# Check backend status
curl http://localhost:8000/health

# Check CORS settings
curl -H "Origin: http://localhost:8080" http://localhost:8000/health
```

#### Docker issues
```bash
# Check container logs
docker logs airline-insights

# Check container health
docker inspect airline-insights

# Rebuild image
docker build --no-cache -t airline-insights .
```

### Performance Issues
- Check memory usage
- Monitor CPU utilization
- Analyze slow queries
- Review error logs

## 📋 Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Security settings reviewed
- [ ] Database migrations applied (if applicable)
- [ ] Dependencies updated

### Post-deployment
- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] SSL certificate valid
- [ ] Backup procedures tested
- [ ] Documentation updated

## 🆘 Support

### Getting Help
- Review application logs
- Check health endpoints
- Verify environment configuration
- Test with minimal setup

### Rollback Procedures
```bash
# Docker rollback
docker run -p 8000:8000 airline-insights:previous-version

# Heroku rollback
heroku rollback v123

# Kubernetes rollback
kubectl rollout undo deployment/airline-insights
```

---

For additional support, please refer to the main README.md or create an issue in the project repository. 