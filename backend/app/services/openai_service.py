"""
OpenAI Service
=============

This module contains the OpenAI service for generating AI-powered insights from airline data.
"""

import openai
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class InsightRequest:
    """Data class for insight generation requests"""
    data_type: str
    data: Dict[str, Any]
    insight_type: str
    parameters: Optional[Dict[str, Any]] = None

class OpenAIService:
    """
    Service for generating AI-powered insights using OpenAI's GPT models.
    
    This service processes airline data and generates meaningful insights,
    predictions, and recommendations using advanced language models.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI service.
        
        Args:
            api_key: OpenAI API key (if None, will use environment variable)
            model: OpenAI model to use for generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            logger.warning("OpenAI API key not provided. AI insights will be simulated.")
            self.use_openai = False
        else:
            openai.api_key = self.api_key
            self.use_openai = True
    
    async def generate_flight_insights(self, flight_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate insights from flight data.
        
        Args:
            flight_data: List of flight information
            
        Returns:
            Dictionary containing generated insights
        """
        logger.info("Generating flight insights")
        
        if not self.use_openai:
            return self._generate_mock_flight_insights(flight_data)
        
        try:
            # Prepare data summary for AI analysis
            data_summary = self._prepare_flight_summary(flight_data)
            
            prompt = f"""
            Analyze the following airline flight data and provide insights:
            
            {data_summary}
            
            Please provide insights in the following format:
            1. Key trends and patterns
            2. Price analysis and predictions
            3. Popular routes and destinations
            4. Recommendations for travelers
            5. Market opportunities
            
            Respond in JSON format with structured insights.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert airline industry analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            insights_text = response.choices[0].message.content
            
            # Parse the response and structure it
            insights = self._parse_insights_response(insights_text, "flight_insights")
            insights["generated_at"] = datetime.now().isoformat()
            insights["data_points"] = len(flight_data)
            
            logger.info("Flight insights generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating flight insights: {str(e)}")
            return self._generate_mock_flight_insights(flight_data)
    
    async def generate_route_analysis(self, route_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate route analysis insights.
        
        Args:
            route_data: List of route information
            
        Returns:
            Dictionary containing route analysis
        """
        logger.info("Generating route analysis")
        
        if not self.use_openai:
            return self._generate_mock_route_analysis(route_data)
        
        try:
            route_summary = self._prepare_route_summary(route_data)
            
            prompt = f"""
            Analyze the following airline route data and provide comprehensive insights:
            
            {route_summary}
            
            Focus on:
            1. Route network efficiency
            2. Hub airport analysis
            3. Seasonal demand patterns
            4. Airline competition analysis
            5. Market opportunities and gaps
            6. Strategic recommendations
            
            Provide detailed analysis in JSON format.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an airline network strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            insights_text = response.choices[0].message.content
            insights = self._parse_insights_response(insights_text, "route_analysis")
            insights["generated_at"] = datetime.now().isoformat()
            insights["routes_analyzed"] = len(route_data)
            
            logger.info("Route analysis generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating route analysis: {str(e)}")
            return self._generate_mock_route_analysis(route_data)
    
    async def generate_price_predictions(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate price predictions and trends.
        
        Args:
            price_data: Historical price data
            
        Returns:
            Dictionary containing price predictions
        """
        logger.info("Generating price predictions")
        
        if not self.use_openai:
            return self._generate_mock_price_predictions(price_data)
        
        try:
            price_summary = json.dumps(price_data, indent=2)
            
            prompt = f"""
            Analyze the following airline pricing data and generate predictions:
            
            {price_summary}
            
            Provide:
            1. Short-term price predictions (1-2 weeks)
            2. Medium-term trends (1-3 months)
            3. Seasonal factors affecting pricing
            4. Best booking timing recommendations
            5. Price volatility analysis
            6. Confidence levels for predictions
            
            Format response as JSON with specific predictions and reasoning.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an airline pricing analyst with expertise in revenue management."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1200
            )
            
            insights_text = response.choices[0].message.content
            insights = self._parse_insights_response(insights_text, "price_predictions")
            insights["generated_at"] = datetime.now().isoformat()
            
            logger.info("Price predictions generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating price predictions: {str(e)}")
            return self._generate_mock_price_predictions(price_data)
    
    async def generate_demand_forecast(self, demand_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate demand forecasting insights.
        
        Args:
            demand_data: Historical demand data
            
        Returns:
            Dictionary containing demand forecasts
        """
        logger.info("Generating demand forecast")
        
        if not self.use_openai:
            return self._generate_mock_demand_forecast(demand_data)
        
        try:
            demand_summary = json.dumps(demand_data, indent=2)
            
            prompt = f"""
            Analyze the following airline demand data and create forecasts:
            
            {demand_summary}
            
            Generate:
            1. Demand forecasts by route and time period
            2. Seasonal demand patterns
            3. Peak travel period predictions
            4. Factors influencing demand changes
            5. Capacity planning recommendations
            6. Market growth opportunities
            
            Provide structured forecasts with confidence intervals.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a demand forecasting specialist for the airline industry."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1200
            )
            
            insights_text = response.choices[0].message.content
            insights = self._parse_insights_response(insights_text, "demand_forecast")
            insights["generated_at"] = datetime.now().isoformat()
            
            logger.info("Demand forecast generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating demand forecast: {str(e)}")
            return self._generate_mock_demand_forecast(demand_data)
    
    def _prepare_flight_summary(self, flight_data: List[Dict[str, Any]]) -> str:
        """Prepare a summary of flight data for AI analysis"""
        if not flight_data:
            return "No flight data available"
        
        total_flights = len(flight_data)
        airlines = list(set(flight["airline"] for flight in flight_data))
        routes = list(set(f"{flight['origin']}-{flight['destination']}" for flight in flight_data))
        avg_price = sum(flight["price"] for flight in flight_data) / total_flights
        
        summary = f"""
        Flight Data Summary:
        - Total flights: {total_flights}
        - Airlines: {', '.join(airlines[:5])} {'and others' if len(airlines) > 5 else ''}
        - Routes: {len(routes)} unique routes
        - Average price: ${avg_price:.2f}
        - Price range: ${min(flight['price'] for flight in flight_data):.2f} - ${max(flight['price'] for flight in flight_data):.2f}
        """
        
        return summary
    
    def _prepare_route_summary(self, route_data: List[Dict[str, Any]]) -> str:
        """Prepare a summary of route data for AI analysis"""
        if not route_data:
            return "No route data available"
        
        total_routes = len(route_data)
        airlines = list(set(route["airline"] for route in route_data))
        airports = list(set(route["origin"] for route in route_data) | set(route["destination"] for route in route_data))
        avg_frequency = sum(route["frequency"] for route in route_data) / total_routes
        
        summary = f"""
        Route Data Summary:
        - Total routes: {total_routes}
        - Airlines: {len(airlines)} airlines
        - Airports: {len(airports)} airports
        - Average frequency: {avg_frequency:.1f} flights per week
        - Seasonal patterns: {', '.join(set(route['peak_season'] for route in route_data))}
        """
        
        return summary
    
    def _parse_insights_response(self, response_text: str, insight_type: str) -> Dict[str, Any]:
        """Parse AI response and structure insights"""
        try:
            # Try to parse as JSON first
            if response_text.strip().startswith('{'):
                return json.loads(response_text)
            
            # If not JSON, structure the text response
            return {
                "insight_type": insight_type,
                "analysis": response_text,
                "structured_insights": self._extract_structured_insights(response_text)
            }
            
        except json.JSONDecodeError:
            return {
                "insight_type": insight_type,
                "analysis": response_text,
                "structured_insights": self._extract_structured_insights(response_text)
            }
    
    def _extract_structured_insights(self, text: str) -> Dict[str, Any]:
        """Extract structured insights from text response"""
        insights = {
            "key_points": [],
            "recommendations": [],
            "trends": [],
            "predictions": []
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Identify sections
            if any(keyword in line.lower() for keyword in ['trend', 'pattern']):
                current_section = 'trends'
            elif any(keyword in line.lower() for keyword in ['recommend', 'suggest']):
                current_section = 'recommendations'
            elif any(keyword in line.lower() for keyword in ['predict', 'forecast']):
                current_section = 'predictions'
            else:
                current_section = 'key_points'
            
            if current_section and line:
                insights[current_section].append(line)
        
        return insights
    
    # Mock generation methods for when OpenAI is not available
    def _generate_mock_flight_insights(self, flight_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate mock flight insights"""
        return {
            "insight_type": "flight_insights",
            "key_trends": [
                "Flight prices show seasonal variation with peaks in summer and holidays",
                "Premium airlines maintain 15-20% price premium over budget carriers",
                "Popular routes show consistent demand with limited price elasticity"
            ],
            "price_analysis": {
                "average_price": 325.50,
                "trend": "increasing",
                "volatility": "moderate"
            },
            "recommendations": [
                "Book flights 6-8 weeks in advance for best prices",
                "Consider flexible dates for 15-30% savings",
                "Tuesday and Wednesday departures typically cheaper"
            ],
            "market_opportunities": [
                "Underserved mid-tier routes with growth potential",
                "Premium economy segment showing strong demand",
                "Regional airports offering lower cost alternatives"
            ],
            "generated_at": datetime.now().isoformat(),
            "confidence": 0.85,
            "data_points": len(flight_data)
        }
    
    def _generate_mock_route_analysis(self, route_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate mock route analysis"""
        return {
            "insight_type": "route_analysis",
            "network_efficiency": {
                "hub_utilization": "high",
                "route_redundancy": "optimal",
                "coverage_gaps": ["Mountain West region", "Secondary cities"]
            },
            "hub_analysis": [
                {"airport": "ATL", "strength": "Southeast connectivity", "opportunity": "International expansion"},
                {"airport": "LAX", "strength": "Pacific gateway", "opportunity": "Asian routes"},
                {"airport": "ORD", "strength": "Midwest hub", "opportunity": "Regional connectivity"}
            ],
            "seasonal_patterns": {
                "summer": "Peak demand for leisure routes",
                "winter": "Business travel concentration",
                "spring_fall": "Balanced demand patterns"
            },
            "recommendations": [
                "Expand secondary hub operations",
                "Optimize frequency on high-demand routes",
                "Consider new international partnerships"
            ],
            "generated_at": datetime.now().isoformat(),
            "routes_analyzed": len(route_data)
        }
    
    def _generate_mock_price_predictions(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock price predictions"""
        return {
            "insight_type": "price_predictions",
            "short_term": {
                "1_week": {"change": "+2.5%", "confidence": 0.82},
                "2_weeks": {"change": "+4.1%", "confidence": 0.75}
            },
            "medium_term": {
                "1_month": {"change": "+8.3%", "confidence": 0.70},
                "3_months": {"change": "+12.7%", "confidence": 0.65}
            },
            "seasonal_factors": {
                "summer_premium": "25-30%",
                "holiday_surge": "40-50%",
                "off_peak_discount": "15-25%"
            },
            "booking_recommendations": {
                "optimal_timing": "6-8 weeks advance",
                "price_drop_probability": 0.25,
                "best_days": ["Tuesday", "Wednesday"]
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_demand_forecast(self, demand_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock demand forecast"""
        return {
            "insight_type": "demand_forecast",
            "overall_trend": "growing",
            "growth_rate": "8.5% annually",
            "peak_periods": [
                {"period": "Summer 2024", "demand_increase": "35%"},
                {"period": "Winter Holidays", "demand_increase": "45%"},
                {"period": "Spring Break", "demand_increase": "25%"}
            ],
            "route_forecasts": [
                {"route": "JFK-LAX", "demand_change": "+12%", "confidence": 0.88},
                {"route": "ORD-LAX", "demand_change": "+8%", "confidence": 0.82},
                {"route": "ATL-MIA", "demand_change": "+15%", "confidence": 0.79}
            ],
            "influencing_factors": [
                "Economic recovery driving leisure travel",
                "Business travel returning to pre-pandemic levels",
                "Fuel price stability supporting route expansion"
            ],
            "capacity_recommendations": [
                "Increase frequency on high-growth routes",
                "Add capacity during peak seasons",
                "Consider larger aircraft on popular routes"
            ],
            "generated_at": datetime.now().isoformat()
        } 