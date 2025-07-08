"""
Comprehensive test suite for Airline Data Insights API
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.main import app
from app.scrapers.flight_scraper import FlightScraper
from app.scrapers.route_scraper import RouteScraper
from app.services.openai_service import OpenAIService

# Initialize test client
client = TestClient(app)

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "app_name" in data
        assert "version" in data
        assert data["app_name"] == "Airline Data Insights"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime" in data
    
    def test_flight_search_endpoint(self):
        """Test flight search endpoint"""
        search_data = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15"
        }
        response = client.post("/flights/search", json=search_data)
        assert response.status_code == 200
        data = response.json()
        assert "flights" in data
        assert "total" in data
        assert isinstance(data["flights"], list)
    
    def test_flight_search_with_filters(self):
        """Test flight search with filters"""
        search_data = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15",
            "min_price": 200,
            "max_price": 800,
            "airline": "American Airlines"
        }
        response = client.post("/flights/search", json=search_data)
        assert response.status_code == 200
        data = response.json()
        assert "flights" in data
        
        # Verify filtering works
        for flight in data["flights"]:
            assert 200 <= flight["price"] <= 800
            assert flight["airline"] == "American Airlines"
    
    def test_popular_routes_endpoint(self):
        """Test popular routes endpoint"""
        response = client.get("/routes/popular")
        assert response.status_code == 200
        data = response.json()
        assert "routes" in data
        assert isinstance(data["routes"], list)
        
        # Verify route structure
        if data["routes"]:
            route = data["routes"][0]
            assert "route" in route
            assert "flights" in route
            assert "avg_price" in route
            assert "popularity" in route
    
    def test_pricing_trends_endpoint(self):
        """Test pricing trends endpoint"""
        response = client.get("/trends/pricing")
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
        assert isinstance(data["trends"], list)
        
        # Verify trend structure
        if data["trends"]:
            trend = data["trends"][0]
            assert "date" in trend
            assert "avg_price" in trend
    
    def test_pricing_analysis_endpoint(self):
        """Test pricing analysis endpoint"""
        response = client.get("/analysis/pricing")
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert "summary" in data
        assert "recommendations" in data
    
    def test_scraping_status_endpoint(self):
        """Test scraping status endpoint"""
        response = client.get("/scraping/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "last_updated" in data
        assert "total_flights" in data
    
    def test_scraping_trigger_endpoint(self):
        """Test scraping trigger endpoint"""
        response = client.post("/scraping/trigger")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "message" in data
    
    def test_insights_generation_endpoint(self):
        """Test insights generation endpoint"""
        response = client.get("/insights/generate")
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert isinstance(data["insights"], list)
        
        # Verify insight structure
        if data["insights"]:
            insight = data["insights"][0]
            assert "title" in insight
            assert "description" in insight
    
    def test_invalid_flight_search(self):
        """Test invalid flight search request"""
        search_data = {
            "origin": "",  # Empty origin
            "destination": "LAX",
            "date": "2024-01-15"
        }
        response = client.post("/flights/search", json=search_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_date_format(self):
        """Test invalid date format in flight search"""
        search_data = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "invalid-date"
        }
        response = client.post("/flights/search", json=search_data)
        assert response.status_code == 422  # Validation error


class TestFlightScraper:
    """Test FlightScraper functionality"""
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        scraper = FlightScraper()
        assert scraper.base_url == "https://example-airline-api.com"
        assert scraper.headers is not None
        assert scraper.session is not None
    
    def test_scrape_flights(self):
        """Test flight scraping"""
        scraper = FlightScraper()
        flights = scraper.scrape_flights("JFK", "LAX", "2024-01-15")
        
        assert isinstance(flights, list)
        assert len(flights) > 0
        
        # Verify flight structure
        flight = flights[0]
        required_fields = ["origin", "destination", "date", "price", "airline", "departure_time", "arrival_time", "duration"]
        for field in required_fields:
            assert field in flight
    
    def test_scrape_popular_routes(self):
        """Test popular routes scraping"""
        scraper = FlightScraper()
        routes = scraper.scrape_popular_routes()
        
        assert isinstance(routes, list)
        assert len(routes) > 0
        
        # Verify route structure
        route = routes[0]
        required_fields = ["route", "flights", "avg_price", "popularity"]
        for field in required_fields:
            assert field in route
    
    def test_scrape_price_trends(self):
        """Test price trends scraping"""
        scraper = FlightScraper()
        trends = scraper.scrape_price_trends()
        
        assert isinstance(trends, list)
        assert len(trends) > 0
        
        # Verify trend structure
        trend = trends[0]
        required_fields = ["date", "avg_price", "route"]
        for field in required_fields:
            assert field in trend


class TestRouteScraper:
    """Test RouteScraper functionality"""
    
    def test_route_scraper_initialization(self):
        """Test route scraper initialization"""
        scraper = RouteScraper()
        assert scraper.graph is not None
        assert scraper.airports is not None
    
    def test_analyze_route_network(self):
        """Test route network analysis"""
        scraper = RouteScraper()
        analysis = scraper.analyze_route_network()
        
        assert isinstance(analysis, dict)
        assert "hub_airports" in analysis
        assert "route_efficiency" in analysis
        assert "network_density" in analysis
    
    def test_get_hub_airports(self):
        """Test hub airport identification"""
        scraper = RouteScraper()
        hubs = scraper.get_hub_airports()
        
        assert isinstance(hubs, list)
        assert len(hubs) > 0
        
        # Verify hub structure
        hub = hubs[0]
        assert "airport" in hub
        assert "centrality" in hub
        assert "connections" in hub


class TestOpenAIService:
    """Test OpenAIService functionality"""
    
    def test_openai_service_initialization(self):
        """Test OpenAI service initialization"""
        service = OpenAIService()
        assert service.client is not None
    
    def test_generate_flight_insights(self):
        """Test flight insights generation"""
        service = OpenAIService()
        sample_flights = [
            {
                "origin": "JFK",
                "destination": "LAX",
                "price": 450,
                "airline": "American Airlines",
                "date": "2024-01-15"
            }
        ]
        
        insights = service.generate_flight_insights(sample_flights)
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        # Verify insight structure
        insight = insights[0]
        assert "title" in insight
        assert "description" in insight
    
    def test_generate_route_analysis(self):
        """Test route analysis generation"""
        service = OpenAIService()
        sample_routes = [
            {
                "route": "JFK-LAX",
                "flights": 45,
                "avg_price": 450,
                "popularity": 85
            }
        ]
        
        analysis = service.generate_route_analysis(sample_routes)
        
        assert isinstance(analysis, dict)
        assert "summary" in analysis
        assert "recommendations" in analysis
    
    @patch('app.services.openai_service.OpenAI')
    def test_openai_api_error_handling(self, mock_openai):
        """Test OpenAI API error handling"""
        # Mock OpenAI client to raise an exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        service = OpenAIService()
        service.client = mock_client
        
        # Should fall back to mock data
        insights = service.generate_flight_insights([])
        assert isinstance(insights, list)
        assert len(insights) > 0


class TestDataValidation:
    """Test data validation and error handling"""
    
    def test_flight_data_validation(self):
        """Test flight data validation"""
        # Test with valid data
        valid_flight = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15",
            "price": 450,
            "airline": "American Airlines",
            "departure_time": "08:00",
            "arrival_time": "11:30",
            "duration": "5h 30m"
        }
        
        # This should not raise any validation errors
        response = client.post("/flights/search", json={
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15"
        })
        assert response.status_code == 200
    
    def test_price_range_validation(self):
        """Test price range validation"""
        search_data = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15",
            "min_price": 1000,
            "max_price": 500  # max_price < min_price
        }
        
        response = client.post("/flights/search", json=search_data)
        # Should handle this gracefully and return empty results
        assert response.status_code == 200
        data = response.json()
        assert len(data["flights"]) == 0


class TestIntegration:
    """Integration tests for the entire system"""
    
    def test_full_flight_search_flow(self):
        """Test complete flight search flow"""
        # 1. Search for flights
        search_data = {
            "origin": "JFK",
            "destination": "LAX",
            "date": "2024-01-15"
        }
        
        response = client.post("/flights/search", json=search_data)
        assert response.status_code == 200
        
        # 2. Get popular routes
        response = client.get("/routes/popular")
        assert response.status_code == 200
        
        # 3. Get pricing trends
        response = client.get("/trends/pricing")
        assert response.status_code == 200
        
        # 4. Generate insights
        response = client.get("/insights/generate")
        assert response.status_code == 200
    
    def test_scraping_and_analysis_flow(self):
        """Test scraping and analysis flow"""
        # 1. Trigger scraping
        response = client.post("/scraping/trigger")
        assert response.status_code == 200
        
        # 2. Check scraping status
        response = client.get("/scraping/status")
        assert response.status_code == 200
        
        # 3. Get pricing analysis
        response = client.get("/analysis/pricing")
        assert response.status_code == 200


# Pytest configuration
@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 