"""
Flight Data Scraper
==================

This module contains the FlightScraper class for collecting flight data from public sources.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
import random
import json
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class FlightInfo:
    """Data class for flight information"""
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
    scraped_at: datetime

class FlightScraper:
    """
    Flight data scraper for collecting airline information from public sources.
    
    This scraper focuses on collecting data from freely available sources
    and flight comparison websites that don't require authentication.
    """
    
    def __init__(self, delay: float = 2.0, max_retries: int = 3):
        """
        Initialize the flight scraper.
        
        Args:
            delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
        """
        self.delay = delay
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Sample data for demonstration (in production, this would come from real scraping)
        self.sample_flight_data = self._generate_sample_data()
    
    def _generate_sample_data(self) -> List[Dict[str, Any]]:
        """Generate sample flight data for demonstration purposes"""
        airlines = [
            "American Airlines", "Delta Air Lines", "United Airlines", 
            "Southwest Airlines", "JetBlue Airways", "Alaska Airlines",
            "Spirit Airlines", "Frontier Airlines"
        ]
        
        routes = [
            ("JFK", "LAX"), ("LAX", "JFK"), ("ORD", "LAX"), ("ATL", "LAX"),
            ("JFK", "SFO"), ("LAX", "SFO"), ("ORD", "ATL"), ("JFK", "MIA"),
            ("LAX", "SEA"), ("DEN", "LAX"), ("JFK", "BOS"), ("LAX", "LAS"),
            ("ORD", "DFW"), ("ATL", "MIA"), ("SFO", "SEA"), ("DEN", "PHX")
        ]
        
        flights = []
        base_date = datetime.now()
        
        for i in range(100):  # Generate 100 sample flights
            airline = random.choice(airlines)
            origin, destination = random.choice(routes)
            
            # Generate flight times
            departure_hour = random.randint(6, 22)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_time = base_date.replace(
                hour=departure_hour, 
                minute=departure_minute, 
                second=0, 
                microsecond=0
            ) + timedelta(days=random.randint(0, 30))
            
            # Calculate arrival time (3-6 hours flight duration)
            flight_duration_hours = random.randint(3, 6)
            arrival_time = departure_time + timedelta(hours=flight_duration_hours)
            
            # Generate price based on route and airline
            base_price = random.randint(200, 800)
            if airline in ["Spirit Airlines", "Frontier Airlines"]:
                base_price *= 0.7  # Budget airlines
            elif airline in ["American Airlines", "Delta Air Lines", "United Airlines"]:
                base_price *= 1.1  # Premium airlines
            
            flight = {
                "flight_id": f"{airline[:2].upper()}{random.randint(100, 999)}",
                "airline": airline,
                "origin": origin,
                "destination": destination,
                "departure_time": departure_time.isoformat(),
                "arrival_time": arrival_time.isoformat(),
                "duration": f"{flight_duration_hours}h {random.randint(0, 59)}m",
                "price": round(base_price, 2),
                "currency": "USD",
                "class_type": random.choice(["economy", "premium_economy", "business"]),
                "stops": random.choice([0, 1, 2]),
                "scraped_at": datetime.now().isoformat()
            }
            
            flights.append(flight)
        
        return flights
    
    def scrape_flights(self, origin: str, destination: str, 
                      departure_date: Optional[str] = None,
                      return_date: Optional[str] = None) -> List[FlightInfo]:
        """
        Scrape flight data for a specific route.
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            departure_date: Departure date (YYYY-MM-DD format)
            return_date: Return date (YYYY-MM-DD format)
            
        Returns:
            List of FlightInfo objects
        """
        logger.info(f"Scraping flights from {origin} to {destination}")
        
        try:
            # In a real implementation, this would scrape actual websites
            # For now, we'll filter our sample data
            filtered_flights = []
            
            for flight_data in self.sample_flight_data:
                if (flight_data["origin"] == origin.upper() and 
                    flight_data["destination"] == destination.upper()):
                    
                    flight_info = FlightInfo(
                        flight_id=flight_data["flight_id"],
                        airline=flight_data["airline"],
                        origin=flight_data["origin"],
                        destination=flight_data["destination"],
                        departure_time=flight_data["departure_time"],
                        arrival_time=flight_data["arrival_time"],
                        duration=flight_data["duration"],
                        price=flight_data["price"],
                        currency=flight_data["currency"],
                        class_type=flight_data["class_type"],
                        stops=flight_data["stops"],
                        scraped_at=datetime.fromisoformat(flight_data["scraped_at"])
                    )
                    filtered_flights.append(flight_info)
            
            logger.info(f"Found {len(filtered_flights)} flights")
            return filtered_flights
            
        except Exception as e:
            logger.error(f"Error scraping flights: {str(e)}")
            return []
    
    def scrape_popular_routes(self) -> List[Dict[str, Any]]:
        """
        Scrape popular flight routes data.
        
        Returns:
            List of popular route information
        """
        logger.info("Scraping popular routes")
        
        try:
            # Analyze sample data to find popular routes
            route_stats = {}
            
            for flight in self.sample_flight_data:
                route_key = f"{flight['origin']} → {flight['destination']}"
                
                if route_key not in route_stats:
                    route_stats[route_key] = {
                        "route": route_key,
                        "flight_count": 0,
                        "total_price": 0,
                        "passengers": 0
                    }
                
                route_stats[route_key]["flight_count"] += 1
                route_stats[route_key]["total_price"] += flight["price"]
                route_stats[route_key]["passengers"] += random.randint(100, 500)
            
            # Calculate averages and sort by popularity
            popular_routes = []
            for route_data in route_stats.values():
                avg_price = route_data["total_price"] / route_data["flight_count"]
                growth = random.uniform(5.0, 20.0)  # Simulated growth
                
                popular_routes.append({
                    "route": route_data["route"],
                    "passengers": route_data["passengers"],
                    "avg_price": round(avg_price, 2),
                    "growth": round(growth, 1)
                })
            
            # Sort by passenger count and return top 10
            popular_routes.sort(key=lambda x: x["passengers"], reverse=True)
            
            logger.info(f"Found {len(popular_routes)} popular routes")
            return popular_routes[:10]
            
        except Exception as e:
            logger.error(f"Error scraping popular routes: {str(e)}")
            return []
    
    def scrape_price_trends(self) -> Dict[str, Any]:
        """
        Scrape price trend data.
        
        Returns:
            Dictionary containing price trend information
        """
        logger.info("Scraping price trends")
        
        try:
            # Analyze sample data for price trends
            prices = [flight["price"] for flight in self.sample_flight_data]
            
            trends = {
                "average_price": round(sum(prices) / len(prices), 2),
                "min_price": min(prices),
                "max_price": max(prices),
                "price_change_24h": f"+{random.uniform(1, 5):.1f}%",
                "price_change_7d": f"+{random.uniform(3, 10):.1f}%",
                "price_change_30d": f"+{random.uniform(5, 15):.1f}%",
                "trend_direction": "increasing",
                "confidence": random.uniform(0.7, 0.95)
            }
            
            logger.info("Price trends analysis completed")
            return trends
            
        except Exception as e:
            logger.error(f"Error scraping price trends: {str(e)}")
            return {}
    
    def scrape_airline_data(self) -> List[Dict[str, Any]]:
        """
        Scrape airline-specific data.
        
        Returns:
            List of airline information
        """
        logger.info("Scraping airline data")
        
        try:
            airline_stats = {}
            
            for flight in self.sample_flight_data:
                airline = flight["airline"]
                
                if airline not in airline_stats:
                    airline_stats[airline] = {
                        "airline": airline,
                        "flight_count": 0,
                        "total_price": 0,
                        "routes": set()
                    }
                
                airline_stats[airline]["flight_count"] += 1
                airline_stats[airline]["total_price"] += flight["price"]
                airline_stats[airline]["routes"].add(f"{flight['origin']}-{flight['destination']}")
            
            # Convert to list format
            airline_data = []
            for stats in airline_stats.values():
                avg_price = stats["total_price"] / stats["flight_count"]
                market_share = (stats["flight_count"] / len(self.sample_flight_data)) * 100
                
                airline_data.append({
                    "airline": stats["airline"],
                    "flight_count": stats["flight_count"],
                    "avg_price": round(avg_price, 2),
                    "route_count": len(stats["routes"]),
                    "market_share": round(market_share, 1)
                })
            
            # Sort by market share
            airline_data.sort(key=lambda x: x["market_share"], reverse=True)
            
            logger.info(f"Found data for {len(airline_data)} airlines")
            return airline_data
            
        except Exception as e:
            logger.error(f"Error scraping airline data: {str(e)}")
            return []
    
    def get_all_data(self) -> Dict[str, Any]:
        """
        Get all available scraped data.
        
        Returns:
            Dictionary containing all scraped data
        """
        logger.info("Collecting all scraped data")
        
        return {
            "flights": self.sample_flight_data,
            "popular_routes": self.scrape_popular_routes(),
            "price_trends": self.scrape_price_trends(),
            "airline_data": self.scrape_airline_data(),
            "last_updated": datetime.now().isoformat()
        }
    
    def _make_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """
        Make a request with retry logic and rate limiting.
        
        Args:
            url: URL to request
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.delay + random.uniform(0, 1))
                response = self.session.get(url, **kwargs)
                response.raise_for_status()
                return response
                
            except requests.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All retry attempts failed for {url}")
                    return None
                
                # Exponential backoff
                time.sleep(2 ** attempt)
        
        return None 