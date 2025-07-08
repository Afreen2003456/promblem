"""
Main FastAPI Application
========================

This module contains the main FastAPI application for the airline data insights platform.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Airline Data Insights API",
    description="API for airline data scraping, processing, and insights generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class FlightSearchRequest(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    passengers: Optional[int] = 1
    class_type: Optional[str] = "economy"

class FlightData(BaseModel):
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    currency: str
    class_type: str
    stops: int

class InsightData(BaseModel):
    insight_type: str
    title: str
    description: str
    data: Dict[str, Any]
    generated_at: datetime

class ScrapingStatus(BaseModel):
    status: str
    message: str
    progress: float
    last_updated: datetime

# Global variables for demo data
sample_flights = [
    {
        "flight_id": "AA101",
        "airline": "American Airlines",
        "origin": "JFK",
        "destination": "LAX",
        "departure_time": "2024-07-15T08:00:00Z",
        "arrival_time": "2024-07-15T11:30:00Z",
        "duration": "5h 30m",
        "price": 299.99,
        "currency": "USD",
        "class_type": "economy",
        "stops": 0
    },
    {
        "flight_id": "DL205",
        "airline": "Delta Air Lines",
        "origin": "JFK",
        "destination": "LAX",
        "departure_time": "2024-07-15T14:00:00Z",
        "arrival_time": "2024-07-15T17:45:00Z",
        "duration": "5h 45m",
        "price": 279.99,
        "currency": "USD",
        "class_type": "economy",
        "stops": 0
    },
    {
        "flight_id": "UA307",
        "airline": "United Airlines",
        "origin": "JFK",
        "destination": "LAX",
        "departure_time": "2024-07-15T18:30:00Z",
        "arrival_time": "2024-07-15T22:15:00Z",
        "duration": "5h 45m",
        "price": 319.99,
        "currency": "USD",
        "class_type": "economy",
        "stops": 0
    }
]

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Airline Data Insights API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "airline-insights-api"
    }

# Flight search endpoint
@app.post("/api/flights/search")
async def search_flights(request: FlightSearchRequest):
    """Search for flights based on criteria"""
    try:
        # Filter sample flights based on request
        filtered_flights = sample_flights.copy()
        
        # Apply filters if provided
        if request.origin:
            filtered_flights = [f for f in filtered_flights if f["origin"] == request.origin.upper()]
        if request.destination:
            filtered_flights = [f for f in filtered_flights if f["destination"] == request.destination.upper()]
        if request.class_type:
            filtered_flights = [f for f in filtered_flights if f["class_type"] == request.class_type.lower()]
        
        logger.info(f"Flight search request: {request}")
        logger.info(f"Found {len(filtered_flights)} flights")
        
        return {
            "flights": filtered_flights,
            "count": len(filtered_flights),
            "search_criteria": request.dict(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error searching flights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching flights: {str(e)}")

# Popular routes endpoint
@app.get("/api/routes/popular")
async def get_popular_routes():
    """Get popular flight routes"""
    try:
        popular_routes = [
            {"route": "JFK → LAX", "passengers": 15420, "avg_price": 299.99, "growth": 12.5},
            {"route": "LAX → JFK", "passengers": 14890, "avg_price": 289.99, "growth": 8.3},
            {"route": "ORD → LAX", "passengers": 13210, "avg_price": 279.99, "growth": 15.2},
            {"route": "ATL → LAX", "passengers": 12850, "avg_price": 259.99, "growth": 6.8},
            {"route": "JFK → SFO", "passengers": 11940, "avg_price": 319.99, "growth": 9.7}
        ]
        
        return {
            "popular_routes": popular_routes,
            "count": len(popular_routes),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting popular routes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting popular routes: {str(e)}")

# Trends endpoint
@app.get("/api/insights/trends")
async def get_trends():
    """Get airline industry trends"""
    try:
        trends = {
            "price_trends": {
                "overall_change": "+8.5%",
                "domestic_change": "+5.2%",
                "international_change": "+12.3%",
                "trend_period": "last_30_days"
            },
            "demand_patterns": {
                "peak_days": ["Friday", "Sunday"],
                "peak_months": ["July", "December"],
                "seasonal_factor": 1.15
            },
            "popular_destinations": [
                {"destination": "LAX", "growth": 15.2},
                {"destination": "JFK", "growth": 12.1},
                {"destination": "ORD", "growth": 9.8},
                {"destination": "ATL", "growth": 8.5}
            ]
        }
        
        return {
            "trends": trends,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting trends: {str(e)}")

# Pricing analysis endpoint
@app.get("/api/insights/pricing")
async def get_pricing_analysis():
    """Get pricing analysis and predictions"""
    try:
        pricing_analysis = {
            "current_avg_price": 289.99,
            "price_change_24h": "+2.5%",
            "price_change_7d": "+5.8%",
            "price_change_30d": "+8.5%",
            "price_prediction": {
                "next_week": 295.50,
                "next_month": 305.75,
                "confidence": 0.85
            },
            "price_ranges": {
                "budget": {"min": 199, "max": 249},
                "standard": {"min": 250, "max": 399},
                "premium": {"min": 400, "max": 699}
            }
        }
        
        return {
            "pricing_analysis": pricing_analysis,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting pricing analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting pricing analysis: {str(e)}")

# Scraping status endpoint
@app.get("/api/scrape/status")
async def get_scraping_status():
    """Get current scraping status"""
    return {
        "status": "idle",
        "message": "Scraping service is ready",
        "progress": 0.0,
        "last_updated": datetime.now().isoformat()
    }

# Trigger scraping endpoint
@app.post("/api/scrape/trigger")
async def trigger_scraping(background_tasks: BackgroundTasks):
    """Trigger data scraping process"""
    try:
        # Add background task for scraping
        background_tasks.add_task(run_scraping_task)
        
        return {
            "status": "started",
            "message": "Scraping process has been triggered",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error triggering scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error triggering scraping: {str(e)}")

# Background task for scraping
async def run_scraping_task():
    """Background task to run scraping process"""
    try:
        logger.info("Starting scraping task...")
        # Simulate scraping process
        import asyncio
        await asyncio.sleep(5)  # Simulate work
        logger.info("Scraping task completed")
    except Exception as e:
        logger.error(f"Error in scraping task: {str(e)}")

# Generate insights endpoint
@app.post("/api/insights/generate")
async def generate_insights(background_tasks: BackgroundTasks):
    """Generate AI insights from data"""
    try:
        background_tasks.add_task(generate_ai_insights)
        
        return {
            "status": "started",
            "message": "AI insights generation has been triggered",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

async def generate_ai_insights():
    """Background task to generate AI insights"""
    try:
        logger.info("Starting AI insights generation...")
        # Simulate AI processing
        import asyncio
        await asyncio.sleep(3)
        logger.info("AI insights generation completed")
    except Exception as e:
        logger.error(f"Error in AI insights generation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 