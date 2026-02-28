"""
Advanced Features Module for AirGuard AI
Implements attention mechanisms, spatiotemporal analysis, and real-time alerts
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

# ATTENTION MECHANISM
class AttentionMechanism:
    """Implements attention-based weighting for time series forecasting."""
    
    def __init__(self, hidden_dim: int = 64):
        """Initialize attention mechanism."""
        self.hidden_dim = hidden_dim
    
    def calculate_attention_weights(self, 
                                   query: np.ndarray,
                                   keys: np.ndarray,
                                   values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate attention weights using scaled dot-product attention.
        
        Args:
            query: Query vector (current state)
            keys: Key vectors (all time steps)
            values: Value vectors (all time steps)
        
        Returns:
            Attention output and attention weights
        """
        # Scaled dot-product attention
        scores = np.dot(query, keys.T) / np.sqrt(self.hidden_dim)
        
        # Softmax normalization
        attention_weights = self._softmax(scores)
        
        # Weighted sum of values
        output = np.dot(attention_weights, values)
        
        return output, attention_weights
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Compute softmax."""
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)
    
    def temporal_attention(self, time_series: np.ndarray) -> np.ndarray:
        """
        Calculate temporal attention weights for time series.
        
        Highlights important time steps based on variance and trends.
        """
        n = len(time_series)
        weights = np.zeros(n)
        
        for i in range(n):
            # Recent data gets higher weight
            recency_weight = 1.0 - (i / n)
            
            # Volatility weight
            if i > 0:
                volatility = np.abs(time_series[i] - time_series[i-1])
            else:
                volatility = 0
            
            # Trend weight
            if i > 5:
                trend = np.mean(np.diff(time_series[max(0, i-5):i]))
            else:
                trend = 0
            
            weights[i] = 0.5 * recency_weight + 0.3 * volatility + 0.2 * np.abs(trend)
        
        # Normalize
        weights = weights / np.sum(weights)
        return weights


# SPATIOTEMPORAL ANALYSIS
class SpatiotemporalAnalyzer:
    """Analyzes spatial and temporal patterns in air quality data."""
    
    def __init__(self, cities_data: Dict[str, pd.DataFrame]):
        """
        Initialize analyzer.
        
        Args:
            cities_data: Dictionary of city names to DataFrames
        """
        self.cities_data = cities_data
        self.city_coords = self._get_city_coordinates()
    
    def _get_city_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """Get approximate coordinates for UK cities."""
        coords = {
            'London': (51.5074, -0.1278),
            'Manchester': (53.4808, -2.2426),
            'Birmingham': (52.5086, -1.8755),
            'Leeds': (53.8008, -1.5491),
            'Glasgow': (55.8642, -4.2518),
            'Liverpool': (53.4084, -2.9916),
            'Edinburgh': (55.9533, -3.1883),
            'Bristol': (51.4545, -2.5879),
            'Cardiff': (51.4816, -3.1791),
            'Belfast': (54.5973, -5.9301)
        }
        return {city: coords.get(city, (0, 0)) for city in self.cities_data.keys()}
    
    def calculate_spatial_correlation(self, pollutant: str = 'PM2.5') -> np.ndarray:
        """
        Calculate spatial correlation between cities.
        
        Args:
            pollutant: Pollutant to analyze
        
        Returns:
            Correlation matrix
        """
        cities = list(self.cities_data.keys())
        n_cities = len(cities)
        correlation_matrix = np.zeros((n_cities, n_cities))
        
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if i == j:
                    correlation_matrix[i, j] = 1.0
                else:
                    data1 = self.cities_data[city1][pollutant].values
                    data2 = self.cities_data[city2][pollutant].values
                    correlation_matrix[i, j] = np.corrcoef(data1, data2)[0, 1]
        
        return correlation_matrix
    
    def calculate_wind_transport(self, source_city: str, target_city: str) -> float:
        """
        Estimate pollution transport between cities based on wind patterns.
        
        Args:
            source_city: Source city
            target_city: Target city
        
        Returns:
            Transport coefficient (0-1)
        """
        source_coords = self.city_coords[source_city]
        target_coords = self.city_coords[target_city]
        
        # Calculate distance
        lat_diff = target_coords[0] - source_coords[0]
        lon_diff = target_coords[1] - source_coords[1]
        distance = np.sqrt(lat_diff**2 + lon_diff**2)
        
        # Get average wind direction
        wind_data = self.cities_data[source_city]['WindSpeed'].mean()
        
        # Transport coefficient (closer + stronger wind = higher transport)
        transport = np.exp(-distance / 5) * (wind_data / 10)
        
        return min(transport, 1.0)
    
    def detect_pollution_events(self, threshold: float = 50.0) -> Dict[str, List]:
        """
        Detect significant pollution events across cities.
        
        Args:
            threshold: PM2.5 threshold for event detection
        
        Returns:
            Dictionary of events by city
        """
        events = {}
        
        for city, df in self.cities_data.items():
            city_events = []
            
            # Find peaks above threshold
            pm25 = df['PM2.5'].values
            for i in range(1, len(pm25) - 1):
                if pm25[i] > threshold and pm25[i] > pm25[i-1] and pm25[i] > pm25[i+1]:
                    city_events.append({
                        'date': df['Date'].iloc[i],
                        'pm25': pm25[i],
                        'severity': 'HIGH' if pm25[i] > 100 else 'MODERATE'
                    })
            
            events[city] = city_events
        
        return events

# REAL-TIME ALERT SYSTEM
@dataclass
class Alert:
    """Alert data class."""
    city: str
    pollutant: str
    level: float
    threshold: float
    status: str
    timestamp: datetime
    health_recommendation: str

class RealTimeAlertSystem:
    """Real-time alert generation system."""
    
    # Alert thresholds (WHO guidelines)
    THRESHOLDS = {
        'PM2.5': {
            'GOOD': 12,
            'MODERATE': 35.4,
            'UNHEALTHY_SENSITIVE': 55.4,
            'UNHEALTHY': 150.4,
            'VERY_UNHEALTHY': 250.4
        },
        'PM10': {
            'GOOD': 50,
            'MODERATE': 100,
            'UNHEALTHY_SENSITIVE': 150,
            'UNHEALTHY': 350,
            'VERY_UNHEALTHY': 500
        },
        'NO2': {
            'GOOD': 40,
            'MODERATE': 100,
            'UNHEALTHY_SENSITIVE': 200,
            'UNHEALTHY': 400,
            'VERY_UNHEALTHY': 1000
        },
        'O3': {
            'GOOD': 50,
            'MODERATE': 100,
            'UNHEALTHY_SENSITIVE': 150,
            'UNHEALTHY': 200,
            'VERY_UNHEALTHY': 300
        }
    }
    
    # Health recommendations
    HEALTH_RECOMMENDATIONS = {
        'GOOD': 'Air quality is satisfactory. Enjoy outdoor activities.',
        'MODERATE': 'Air quality is acceptable. Unusually sensitive people should limit outdoor exertion.',
        'UNHEALTHY_SENSITIVE': 'Sensitive groups should avoid prolonged outdoor exertion. General public unaffected.',
        'UNHEALTHY': 'Some members of the general public may experience health effects. Sensitive groups more serious.',
        'VERY_UNHEALTHY': 'Health alert. Everyone may begin to experience health effects.',
        'HAZARDOUS': 'Health warning. The entire population is more likely to be affected.'
    }
    
    def __init__(self):
        """Initialize alert system."""
        self.active_alerts = []
    
    def generate_alerts(self, cities_data: Dict[str, pd.DataFrame]) -> List[Alert]:
        """
        Generate alerts for all cities and pollutants.
        
        Args:
            cities_data: Dictionary of city DataFrames
        
        Returns:
            List of active alerts
        """
        alerts = []
        
        for city, df in cities_data.items():
            latest = df.iloc[-1]
            
            for pollutant in ['PM2.5', 'PM10', 'NO2', 'O3']:
                if pollutant in df.columns:
                    level = latest[pollutant]
                    status = self._get_status(pollutant, level)
                    
                    # Generate alert if above moderate threshold
                    if status in ['UNHEALTHY_SENSITIVE', 'UNHEALTHY', 'VERY_UNHEALTHY', 'HAZARDOUS']:
                        alert = Alert(
                            city=city,
                            pollutant=pollutant,
                            level=level,
                            threshold=self.THRESHOLDS[pollutant][status],
                            status=status,
                            timestamp=latest['Date'],
                            health_recommendation=self.HEALTH_RECOMMENDATIONS[status]
                        )
                        alerts.append(alert)
        
        self.active_alerts = alerts
        return alerts
    
    def _get_status(self, pollutant: str, level: float) -> str:
        """Get status for a pollutant level."""
        thresholds = self.THRESHOLDS[pollutant]
        
        if level <= thresholds['GOOD']:
            return 'GOOD'
        elif level <= thresholds['MODERATE']:
            return 'MODERATE'
        elif level <= thresholds['UNHEALTHY_SENSITIVE']:
            return 'UNHEALTHY_SENSITIVE'
        elif level <= thresholds['UNHEALTHY']:
            return 'UNHEALTHY'
        elif level <= thresholds['VERY_UNHEALTHY']:
            return 'VERY_UNHEALTHY'
        else:
            return 'HAZARDOUS'
    
    def get_alerts_by_severity(self) -> Dict[str, List[Alert]]:
        """Group alerts by severity."""
        severity_groups = {
            'CRITICAL': [],
            'HIGH': [],
            'MODERATE': []
        }
        
        for alert in self.active_alerts:
            if alert.status in ['VERY_UNHEALTHY', 'HAZARDOUS']:
                severity_groups['CRITICAL'].append(alert)
            elif alert.status == 'UNHEALTHY':
                severity_groups['HIGH'].append(alert)
            else:
                severity_groups['MODERATE'].append(alert)
        
        return severity_groups

# PREDICTIVE ALERT SYSTEM
class PredictiveAlertSystem:
    """Predicts future pollution events and generates proactive alerts."""
    
    def __init__(self, lookback_hours: int = 24, forecast_hours: int = 12):
        """
        Initialize predictive alert system.
        
        Args:
            lookback_hours: Historical data to use
            forecast_hours: Hours to forecast ahead
        """
        self.lookback_hours = lookback_hours
        self.forecast_hours = forecast_hours
    
    def predict_pollution_spike(self, 
                               time_series: np.ndarray,
                               threshold: float = 50.0) -> Tuple[bool, float]:
        """
        Predict if pollution will spike above threshold.
        
        Args:
            time_series: Historical PM2.5 values
            threshold: Alert threshold
        
        Returns:
            (will_spike, confidence)
        """
        if len(time_series) < self.lookback_hours:
            return False, 0.0
        
        recent = time_series[-self.lookback_hours:]
        
        # Calculate trend
        trend = np.polyfit(range(len(recent)), recent, 1)[0]
        
        # Calculate volatility
        volatility = np.std(recent)
        
        # Calculate current level
        current = recent[-1]
        
        # Predict future level
        predicted = current + trend * self.forecast_hours
        
        # Calculate confidence
        confidence = min(abs(trend) / (volatility + 1e-6), 1.0)
        
        will_spike = predicted > threshold
        
        return will_spike, confidence
    
    def detect_anomalies(self, time_series: np.ndarray) -> List[int]:
        """
        Detect anomalies in time series using statistical methods.
        
        Args:
            time_series: PM2.5 values
        
        Returns:
            Indices of anomalous points
        """
        anomalies = []
        
        mean = np.mean(time_series)
        std = np.std(time_series)
        
        for i, val in enumerate(time_series):
            z_score = abs((val - mean) / (std + 1e-6))
            if z_score > 3:  # 3-sigma rule
                anomalies.append(i)
        
        return anomalies

# HEALTH RISK ASSESSMENT
class HealthRiskAssessment:
    """Assesses health risks based on air quality."""
    
    # Health impact thresholds
    HEALTH_IMPACTS = {
        'PM2.5': {
            'respiratory_risk': 35.4,
            'cardiovascular_risk': 55.4,
            'mortality_risk': 150.4
        },
        'NO2': {
            'respiratory_risk': 100,
            'cardiovascular_risk': 200,
            'mortality_risk': 400
        },
        'O3': {
            'respiratory_risk': 100,
            'cardiovascular_risk': 150,
            'mortality_risk': 200
        }
    }
    
    # Vulnerable groups
    VULNERABLE_GROUPS = [
        'Children',
        'Elderly (65+)',
        'People with asthma',
        'People with heart disease',
        'Pregnant women',
        'Athletes/Outdoor workers'
    ]
    
    def assess_health_risk(self, pollutant: str, level: float) -> Dict:
        """
        Assess health risk for a pollutant level.
        
        Args:
            pollutant: Pollutant name
            level: Pollutant level
        
        Returns:
            Risk assessment dictionary
        """
        risk_assessment = {
            'pollutant': pollutant,
            'level': level,
            'respiratory_risk': False,
            'cardiovascular_risk': False,
            'mortality_risk': False,
            'vulnerable_groups': [],
            'recommendations': []
        }
        
        if pollutant not in self.HEALTH_IMPACTS:
            return risk_assessment
        
        thresholds = self.HEALTH_IMPACTS[pollutant]
        
        if level > thresholds['mortality_risk']:
            risk_assessment['mortality_risk'] = True
            risk_assessment['vulnerable_groups'] = self.VULNERABLE_GROUPS
            risk_assessment['recommendations'] = [
                'Avoid all outdoor activities',
                'Use N95/P100 masks if going outside',
                'Keep windows and doors closed',
                'Use air purifiers indoors',
                'Seek medical attention if experiencing symptoms'
            ]
        elif level > thresholds['cardiovascular_risk']:
            risk_assessment['cardiovascular_risk'] = True
            risk_assessment['vulnerable_groups'] = self.VULNERABLE_GROUPS[:-1]
            risk_assessment['recommendations'] = [
                'Limit outdoor activities',
                'Wear masks when outside',
                'Monitor health symptoms',
                'Consult doctor if experiencing chest pain'
            ]
        elif level > thresholds['respiratory_risk']:
            risk_assessment['respiratory_risk'] = True
            risk_assessment['vulnerable_groups'] = self.VULNERABLE_GROUPS[:3]
            risk_assessment['recommendations'] = [
                'Reduce outdoor exertion',
                'Consider wearing masks',
                'Monitor respiratory symptoms'
            ]
        else:
            risk_assessment['recommendations'] = [
                'Air quality is acceptable',
                'Normal outdoor activities are safe'
            ]
        
        return risk_assessment

# ENSEMBLE PREDICTION
class EnsemblePredictor:
    """Ensemble prediction combining multiple models."""
    
    def __init__(self):
        """Initialize ensemble predictor."""
        self.model_weights = {
            'random_forest': 0.3,
            'lstm': 0.4,
            'hybrid': 0.3
        }
    
    def predict_ensemble(self,
                        rf_pred: np.ndarray,
                        lstm_pred: np.ndarray,
                        hybrid_pred: np.ndarray) -> np.ndarray:
        """
        Generate ensemble prediction from multiple models.
        
        Args:
            rf_pred: Random Forest predictions
            lstm_pred: LSTM predictions
            hybrid_pred: Hybrid model predictions
        
        Returns:
            Weighted ensemble prediction
        """
        ensemble = (
            self.model_weights['random_forest'] * rf_pred +
            self.model_weights['lstm'] * lstm_pred +
            self.model_weights['hybrid'] * hybrid_pred
        )
        
        return ensemble
    
    def calculate_prediction_uncertainty(self,
                                        predictions: List[np.ndarray]) -> np.ndarray:
        """
        Calculate uncertainty in predictions.
        
        Args:
            predictions: List of predictions from different models
        
        Returns:
            Uncertainty estimates
        """
        predictions = np.array(predictions)
        uncertainty = np.std(predictions, axis=0)
        
        return uncertainty
