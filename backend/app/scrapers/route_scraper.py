"""
Route Data Scraper
=================

This module contains the RouteScraper class for collecting route and airline network data.
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
import networkx as nx

logger = logging.getLogger(__name__)

@dataclass
class RouteInfo:
    """Data class for route information"""
    origin: str
    destination: str
    airline: str
    frequency: int
    avg_price: float
    peak_season: str
    demand_score: float
    scraped_at: datetime

class RouteScraper:
    """
    Route data scraper for collecting airline route information and network analysis.
    
    This scraper focuses on route connectivity, frequency, and network analysis
    to provide insights into airline route structures.
    """
    
    def __init__(self, delay: float = 2.0, max_retries: int = 3):
        """
        Initialize the route scraper.
        
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
        
        # Sample route data for demonstration
        self.sample_route_data = self._generate_sample_routes()
    
    def _generate_sample_routes(self) -> List[Dict[str, Any]]:
        """Generate sample route data for demonstration purposes"""
        
        # Major airport hubs
        hubs = {
            "ATL": {"city": "Atlanta", "region": "Southeast"},
            "LAX": {"city": "Los Angeles", "region": "West Coast"},
            "ORD": {"city": "Chicago", "region": "Midwest"},
            "DFW": {"city": "Dallas", "region": "Southwest"},
            "DEN": {"city": "Denver", "region": "Mountain"},
            "JFK": {"city": "New York", "region": "Northeast"},
            "SFO": {"city": "San Francisco", "region": "West Coast"},
            "SEA": {"city": "Seattle", "region": "Pacific Northwest"},
            "MIA": {"city": "Miami", "region": "Southeast"},
            "BOS": {"city": "Boston", "region": "Northeast"}
        }
        
        airlines = [
            "American Airlines", "Delta Air Lines", "United Airlines", 
            "Southwest Airlines", "JetBlue Airways", "Alaska Airlines",
            "Spirit Airlines", "Frontier Airlines"
        ]
        
        routes = []
        airports = list(hubs.keys())
        
        # Generate routes between major hubs
        for i, origin in enumerate(airports):
            for destination in airports[i+1:]:
                # Create bidirectional routes
                for direction in [(origin, destination), (destination, origin)]:
                    origin_code, dest_code = direction
                    
                    # Each route may be served by multiple airlines
                    num_airlines = random.randint(1, 4)
                    selected_airlines = random.sample(airlines, num_airlines)
                    
                    for airline in selected_airlines:
                        # Calculate distance-based pricing
                        base_price = random.randint(200, 800)
                        
                        # Adjust for airline type
                        if airline in ["Spirit Airlines", "Frontier Airlines"]:
                            base_price *= 0.7
                        elif airline in ["American Airlines", "Delta Air Lines", "United Airlines"]:
                            base_price *= 1.1
                        
                        # Flight frequency (flights per week)
                        frequency = random.randint(7, 35)
                        
                        # Peak season
                        peak_season = random.choice(["Summer", "Winter", "Spring", "Fall"])
                        
                        # Demand score (0-1)
                        demand_score = random.uniform(0.3, 1.0)
                        
                        route = {
                            "origin": origin_code,
                            "destination": dest_code,
                            "origin_city": hubs[origin_code]["city"],
                            "destination_city": hubs[dest_code]["city"],
                            "airline": airline,
                            "frequency": frequency,
                            "avg_price": round(base_price, 2),
                            "peak_season": peak_season,
                            "demand_score": round(demand_score, 2),
                            "route_type": "domestic",
                            "scraped_at": datetime.now().isoformat()
                        }
                        
                        routes.append(route)
        
        return routes
    
    def scrape_airline_routes(self, airline: str) -> List[RouteInfo]:
        """
        Scrape all routes for a specific airline.
        
        Args:
            airline: Airline name
            
        Returns:
            List of RouteInfo objects for the airline
        """
        logger.info(f"Scraping routes for {airline}")
        
        try:
            airline_routes = []
            
            for route_data in self.sample_route_data:
                if route_data["airline"] == airline:
                    route_info = RouteInfo(
                        origin=route_data["origin"],
                        destination=route_data["destination"],
                        airline=route_data["airline"],
                        frequency=route_data["frequency"],
                        avg_price=route_data["avg_price"],
                        peak_season=route_data["peak_season"],
                        demand_score=route_data["demand_score"],
                        scraped_at=datetime.fromisoformat(route_data["scraped_at"])
                    )
                    airline_routes.append(route_info)
            
            logger.info(f"Found {len(airline_routes)} routes for {airline}")
            return airline_routes
            
        except Exception as e:
            logger.error(f"Error scraping routes for {airline}: {str(e)}")
            return []
    
    def scrape_airport_connections(self, airport: str) -> Dict[str, Any]:
        """
        Scrape connection data for a specific airport.
        
        Args:
            airport: Airport code
            
        Returns:
            Dictionary with connection information
        """
        logger.info(f"Scraping connections for {airport}")
        
        try:
            connections = {
                "airport": airport,
                "destinations": [],
                "airlines": set(),
                "total_routes": 0,
                "avg_frequency": 0,
                "hub_score": 0
            }
            
            for route_data in self.sample_route_data:
                if route_data["origin"] == airport:
                    connections["destinations"].append({
                        "destination": route_data["destination"],
                        "destination_city": route_data["destination_city"],
                        "airline": route_data["airline"],
                        "frequency": route_data["frequency"],
                        "avg_price": route_data["avg_price"]
                    })
                    connections["airlines"].add(route_data["airline"])
                    connections["total_routes"] += 1
            
            if connections["total_routes"] > 0:
                connections["avg_frequency"] = sum(
                    dest["frequency"] for dest in connections["destinations"]
                ) / connections["total_routes"]
                
                # Calculate hub score based on number of destinations and frequency
                connections["hub_score"] = (
                    len(connections["destinations"]) * 0.6 + 
                    connections["avg_frequency"] * 0.4
                ) / 100
            
            connections["airlines"] = list(connections["airlines"])
            connections["hub_score"] = round(connections["hub_score"], 2)
            connections["avg_frequency"] = round(connections["avg_frequency"], 1)
            
            logger.info(f"Found {len(connections['destinations'])} destinations from {airport}")
            return connections
            
        except Exception as e:
            logger.error(f"Error scraping connections for {airport}: {str(e)}")
            return {}
    
    def analyze_route_network(self) -> Dict[str, Any]:
        """
        Analyze the overall route network structure.
        
        Returns:
            Dictionary with network analysis results
        """
        logger.info("Analyzing route network")
        
        try:
            # Create network graph
            G = nx.DiGraph()
            
            # Add edges (routes)
            for route in self.sample_route_data:
                G.add_edge(
                    route["origin"], 
                    route["destination"],
                    airline=route["airline"],
                    frequency=route["frequency"],
                    price=route["avg_price"]
                )
            
            # Calculate network metrics
            centrality = nx.betweenness_centrality(G)
            degree_centrality = nx.degree_centrality(G)
            
            # Find hub airports
            hub_airports = sorted(
                centrality.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            
            # Calculate route efficiency
            path_lengths = dict(nx.all_pairs_shortest_path_length(G))
            avg_path_length = sum(
                length for paths in path_lengths.values() 
                for length in paths.values()
            ) / sum(len(paths) for paths in path_lengths.values())
            
            network_analysis = {
                "total_airports": G.number_of_nodes(),
                "total_routes": G.number_of_edges(),
                "hub_airports": [{"airport": airport, "score": round(score, 3)} 
                               for airport, score in hub_airports],
                "avg_path_length": round(avg_path_length, 2),
                "network_density": round(nx.density(G), 3),
                "strongly_connected": nx.is_strongly_connected(G),
                "airline_coverage": self._calculate_airline_coverage(),
                "route_distribution": self._calculate_route_distribution()
            }
            
            logger.info("Network analysis completed")
            return network_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing route network: {str(e)}")
            return {}
    
    def _calculate_airline_coverage(self) -> Dict[str, Any]:
        """Calculate airline coverage metrics"""
        airline_stats = {}
        
        for route in self.sample_route_data:
            airline = route["airline"]
            if airline not in airline_stats:
                airline_stats[airline] = {
                    "routes": 0,
                    "airports": set(),
                    "total_frequency": 0
                }
            
            airline_stats[airline]["routes"] += 1
            airline_stats[airline]["airports"].add(route["origin"])
            airline_stats[airline]["airports"].add(route["destination"])
            airline_stats[airline]["total_frequency"] += route["frequency"]
        
        # Convert to list format
        coverage = []
        for airline, stats in airline_stats.items():
            coverage.append({
                "airline": airline,
                "routes": stats["routes"],
                "airports": len(stats["airports"]),
                "total_frequency": stats["total_frequency"],
                "avg_frequency": round(stats["total_frequency"] / stats["routes"], 1)
            })
        
        return sorted(coverage, key=lambda x: x["routes"], reverse=True)
    
    def _calculate_route_distribution(self) -> Dict[str, Any]:
        """Calculate route distribution by various metrics"""
        
        # Distribution by frequency
        frequencies = [route["frequency"] for route in self.sample_route_data]
        freq_distribution = {
            "low_frequency": len([f for f in frequencies if f < 14]),
            "medium_frequency": len([f for f in frequencies if 14 <= f < 28]),
            "high_frequency": len([f for f in frequencies if f >= 28])
        }
        
        # Distribution by price
        prices = [route["avg_price"] for route in self.sample_route_data]
        price_distribution = {
            "budget": len([p for p in prices if p < 300]),
            "standard": len([p for p in prices if 300 <= p < 500]),
            "premium": len([p for p in prices if p >= 500])
        }
        
        # Distribution by demand
        demands = [route["demand_score"] for route in self.sample_route_data]
        demand_distribution = {
            "low_demand": len([d for d in demands if d < 0.5]),
            "medium_demand": len([d for d in demands if 0.5 <= d < 0.8]),
            "high_demand": len([d for d in demands if d >= 0.8])
        }
        
        return {
            "frequency": freq_distribution,
            "price": price_distribution,
            "demand": demand_distribution
        }
    
    def get_seasonal_patterns(self) -> Dict[str, Any]:
        """
        Analyze seasonal patterns in route demand.
        
        Returns:
            Dictionary with seasonal analysis
        """
        logger.info("Analyzing seasonal patterns")
        
        try:
            seasonal_data = {}
            
            for route in self.sample_route_data:
                season = route["peak_season"]
                if season not in seasonal_data:
                    seasonal_data[season] = {
                        "routes": 0,
                        "avg_demand": 0,
                        "avg_price": 0,
                        "total_frequency": 0
                    }
                
                seasonal_data[season]["routes"] += 1
                seasonal_data[season]["avg_demand"] += route["demand_score"]
                seasonal_data[season]["avg_price"] += route["avg_price"]
                seasonal_data[season]["total_frequency"] += route["frequency"]
            
            # Calculate averages
            for season, data in seasonal_data.items():
                data["avg_demand"] = round(data["avg_demand"] / data["routes"], 2)
                data["avg_price"] = round(data["avg_price"] / data["routes"], 2)
                data["avg_frequency"] = round(data["total_frequency"] / data["routes"], 1)
            
            logger.info("Seasonal analysis completed")
            return seasonal_data
            
        except Exception as e:
            logger.error(f"Error analyzing seasonal patterns: {str(e)}")
            return {}
    
    def get_all_route_data(self) -> Dict[str, Any]:
        """
        Get all available route data and analysis.
        
        Returns:
            Dictionary containing all route data
        """
        logger.info("Collecting all route data")
        
        return {
            "routes": self.sample_route_data,
            "network_analysis": self.analyze_route_network(),
            "seasonal_patterns": self.get_seasonal_patterns(),
            "last_updated": datetime.now().isoformat()
        } 