"""
Data Collection Module
Fetches air quality data from DEFRA and meteorological data from Open-Meteo API
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AirQualityDataCollector:
    """Collects air quality and meteorological data for UK cities."""
    
    def __init__(self):
        """Initialize data collector with API endpoints."""
        self.open_meteo_url = "https://archive-api.open-meteo.com/v1/archive"
        self.defra_url = "https://uk-air.defra.gov.uk/data_files/site_data"
        
    def fetch_open_meteo_data(self, latitude: float, longitude: float, 
                             start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch meteorological data from Open-Meteo API.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with meteorological features
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "hourly": "temperature_2m,relative_humidity_2m,precipitation,windspeed_10m,pressure_msl",
                "timezone": "UTC"
            }
            
            logger.info(f"Fetching Open-Meteo data for ({latitude}, {longitude})")
            response = requests.get(self.open_meteo_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Create DataFrame from hourly data
            df = pd.DataFrame({
                'datetime': pd.to_datetime(data['hourly']['time']),
                'temperature': data['hourly']['temperature_2m'],
                'humidity': data['hourly']['relative_humidity_2m'],
                'precipitation': data['hourly']['precipitation'],
                'wind_speed': data['hourly']['windspeed_10m'],
                'pressure': data['hourly']['pressure_msl']
            })
            
            logger.info(f"Successfully fetched {len(df)} records from Open-Meteo")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Open-Meteo data: {e}")
            return pd.DataFrame()
    
    def generate_synthetic_air_quality_data(self, dates: pd.DatetimeIndex, 
                                           weather_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate synthetic air quality data based on meteorological patterns.
        In production, this would be replaced with actual DEFRA data.
        
        Args:
            dates: DatetimeIndex for the data
            weather_df: DataFrame with meteorological features
            
        Returns:
            DataFrame with synthetic air quality measurements
        """
        np.random.seed(42)
        n_samples = len(dates)
        
        # Base pollution levels with seasonal variation
        hour_of_day = dates.hour
        day_of_year = dates.dayofyear
        
        # PM2.5: Higher during rush hours and winter
        pm25_base = 25 + 15 * np.sin(2 * np.pi * day_of_year / 365)
        pm25_hourly = pm25_base + 10 * np.sin(2 * np.pi * hour_of_day / 24)
        pm25 = pm25_hourly + np.random.normal(0, 3, n_samples)
        pm25 = np.clip(pm25, 0, 200)
        
        # PM10: Similar pattern to PM2.5 but higher
        pm10_base = 40 + 20 * np.sin(2 * np.pi * day_of_year / 365)
        pm10_hourly = pm10_base + 15 * np.sin(2 * np.pi * hour_of_day / 24)
        pm10 = pm10_hourly + np.random.normal(0, 5, n_samples)
        pm10 = np.clip(pm10, 0, 300)
        
        # NO2: Traffic-related, peaks during rush hours
        no2_base = 30 + 10 * np.sin(2 * np.pi * day_of_year / 365)
        no2_hourly = no2_base + 20 * np.sin(2 * np.pi * hour_of_day / 24)
        no2 = no2_hourly + np.random.normal(0, 4, n_samples)
        no2 = np.clip(no2, 0, 150)
        
        # O3: Inverse relationship with NO2
        o3_base = 40 - 15 * np.sin(2 * np.pi * day_of_year / 365)
        o3_hourly = o3_base - 15 * np.sin(2 * np.pi * hour_of_day / 24)
        o3 = o3_hourly + np.random.normal(0, 3, n_samples)
        o3 = np.clip(o3, 0, 120)
        
        # Inverse relationship with wind speed (higher wind = lower pollution)
        if 'wind_speed' in weather_df.columns:
            wind_factor = 1 - (weather_df['wind_speed'].values / 20)
            wind_factor = np.clip(wind_factor, 0.5, 1.5)
            pm25 *= wind_factor
            pm10 *= wind_factor
            no2 *= wind_factor
        
        df = pd.DataFrame({
            'datetime': dates,
            'pm25': pm25,
            'pm10': pm10,
            'no2': no2,
            'o3': o3
        })
        
        logger.info(f"Generated synthetic air quality data with {len(df)} records")
        return df
    
    def collect_data(self, latitude: float, longitude: float, 
                    start_date: str, end_date: str, 
                    city_name: str = "UK_City") -> pd.DataFrame:
        """
        Collect and merge air quality and meteorological data.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            city_name: Name of the city
            
        Returns:
            Merged DataFrame with all features
        """
        # Fetch meteorological data
        weather_df = self.fetch_open_meteo_data(latitude, longitude, start_date, end_date)
        
        if weather_df.empty:
            logger.error("Failed to fetch meteorological data")
            return pd.DataFrame()
        
        # Generate synthetic air quality data
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        air_quality_df = self.generate_synthetic_air_quality_data(dates, weather_df)
        
        # Merge datasets
        merged_df = pd.merge_asof(
            air_quality_df.sort_values('datetime'),
            weather_df.sort_values('datetime'),
            on='datetime',
            direction='nearest'
        )
        
        merged_df['city'] = city_name
        merged_df = merged_df.sort_values('datetime').reset_index(drop=True)
        
        logger.info(f"Data collection complete for {city_name}: {len(merged_df)} records")
        return merged_df


def main():
    """Example usage of the data collector."""
    collector = AirQualityDataCollector()
    
    # Example: Collect data for London
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    london_data = collector.collect_data(
        latitude=51.5074,
        longitude=-0.1278,
        start_date=start_date,
        end_date=end_date,
        city_name="London"
    )
    
    print("\nData Collection Summary:")
    print(f"Shape: {london_data.shape}")
    print(f"\nFirst few rows:")
    print(london_data.head())
    print(f"\nData types:")
    print(london_data.dtypes)
    print(f"\nBasic statistics:")
    print(london_data.describe())


if __name__ == "__main__":
    main()
