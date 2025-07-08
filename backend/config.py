"""
Configuration module for Airline Data Insights backend
"""
import os
from typing import List
from functools import lru_cache

class Settings:
    """Application settings with environment variable support"""
    
    # Application Configuration
    APP_NAME: str = "Airline Data Insights"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500"
    ).split(",")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./airline_data.db")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    
    # External API Configuration
    SCRAPER_USER_AGENT: str = os.getenv(
        "SCRAPER_USER_AGENT", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Cache Configuration
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Sample Data Configuration
    SAMPLE_DATA_SIZE: int = int(os.getenv("SAMPLE_DATA_SIZE", "100"))
    
    # API Response Configuration
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()


# Default settings instance
settings = get_settings()

# Environment-specific configurations
ENVIRONMENT_CONFIGS = {
    "development": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "CORS_ORIGINS": ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:5500"],
    },
    "production": {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "CORS_ORIGINS": ["https://yourdomain.com"],
    },
    "testing": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "DATABASE_URL": "sqlite:///./test_airline_data.db",
    }
}

def get_environment_config(env: str = "development") -> dict:
    """Get environment-specific configuration"""
    return ENVIRONMENT_CONFIGS.get(env, ENVIRONMENT_CONFIGS["development"])

# API Response Messages
API_MESSAGES = {
    "FLIGHT_SEARCH_SUCCESS": "Flights retrieved successfully",
    "FLIGHT_SEARCH_ERROR": "Failed to search for flights",
    "ROUTES_SUCCESS": "Popular routes retrieved successfully",
    "ROUTES_ERROR": "Failed to retrieve popular routes",
    "INSIGHTS_SUCCESS": "AI insights generated successfully",
    "INSIGHTS_ERROR": "Failed to generate AI insights",
    "SCRAPING_SUCCESS": "Data scraping completed successfully",
    "SCRAPING_ERROR": "Failed to scrape data",
    "INVALID_REQUEST": "Invalid request parameters",
    "INTERNAL_ERROR": "Internal server error",
    "SERVICE_UNAVAILABLE": "Service temporarily unavailable"
}

# Default airline data for fallback
DEFAULT_AIRLINES = [
    "American Airlines",
    "Delta Air Lines", 
    "United Airlines",
    "Southwest Airlines",
    "JetBlue Airways",
    "Alaska Airlines",
    "Spirit Airlines",
    "Frontier Airlines"
]

# Default airport codes
DEFAULT_AIRPORTS = {
    "JFK": "John F. Kennedy International Airport",
    "LAX": "Los Angeles International Airport",
    "ORD": "Chicago O'Hare International Airport",
    "DFW": "Dallas/Fort Worth International Airport",
    "DEN": "Denver International Airport",
    "SFO": "San Francisco International Airport",
    "LAS": "McCarran International Airport",
    "MIA": "Miami International Airport",
    "BOS": "Boston Logan International Airport",
    "SEA": "Seattle-Tacoma International Airport",
    "ATL": "Hartsfield-Jackson Atlanta International Airport",
    "PHX": "Phoenix Sky Harbor International Airport",
    "LGA": "LaGuardia Airport",
    "EWR": "Newark Liberty International Airport",
    "IAD": "Washington Dulles International Airport",
    "DCA": "Ronald Reagan Washington National Airport"
}

# Route patterns for sample data generation
POPULAR_ROUTES = [
    ("JFK", "LAX"), ("LAX", "JFK"),
    ("ORD", "LAS"), ("LAS", "ORD"),
    ("DFW", "DEN"), ("DEN", "DFW"),
    ("BOS", "SFO"), ("SFO", "BOS"),
    ("MIA", "LGA"), ("LGA", "MIA"),
    ("ATL", "PHX"), ("PHX", "ATL"),
    ("SEA", "IAD"), ("IAD", "SEA"),
    ("EWR", "DCA"), ("DCA", "EWR")
] 