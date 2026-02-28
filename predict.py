"""
Prediction Script
Make predictions using trained models
"""

import numpy as np
import pandas as pd
import logging
import os
from datetime import datetime, timedelta
from typing import Dict

from models import RandomForestModel, LSTMModel, HybridCNNLSTMModel
from data_collection import AirQualityDataCollector
from data_preprocessing import DataPreprocessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AirQualityPredictor:
    """Makes predictions using trained models."""
    
    def __init__(self, models_dir: str = "results"):
        """
        Initialize predictor.
        
        Args:
            models_dir: Directory containing trained models
        """
        self.models_dir = models_dir
        self.models = {}
        self.preprocessor = DataPreprocessor()
        self.collector = AirQualityDataCollector()
        
    def load_models(self) -> None:
        """Load all trained models."""
        logger.info("Loading trained models...")
        
        # Load Random Forest
        rf_path = os.path.join(self.models_dir, "random_forest_model.pkl")
        if os.path.exists(rf_path):
            rf_model = RandomForestModel()
            rf_model.load(rf_path)
            self.models['random_forest'] = rf_model
            logger.info("Random Forest model loaded")
        
        # Load LSTM
        lstm_path = os.path.join(self.models_dir, "lstm_model.h5")
        if os.path.exists(lstm_path):
            lstm_model = LSTMModel()
            lstm_model.load(lstm_path)
            self.models['lstm'] = lstm_model
            logger.info("LSTM model loaded")
        
        # Load Hybrid
        hybrid_path = os.path.join(self.models_dir, "hybrid_cnn_lstm_model.h5")
        if os.path.exists(hybrid_path):
            hybrid_model = HybridCNNLSTMModel()
            hybrid_model.load(hybrid_path)
            self.models['hybrid'] = hybrid_model
            logger.info("Hybrid CNN-LSTM model loaded")
    
    def prepare_prediction_data(self, latitude: float, longitude: float,
                               days_ahead: int = 7) -> np.ndarray:
        """
        Prepare data for prediction.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days_ahead: Number of days to predict ahead
            
        Returns:
            Preprocessed features for prediction
        """
        # Collect recent data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        df = self.collector.collect_data(latitude, longitude, start_date, end_date)
        
        if df.empty:
            logger.error("Failed to collect data for prediction")
            return None
        
        # Preprocess
        df_processed, _ = self.preprocessor.preprocess(df, target_col='pm25')
        
        # Get features (exclude target and datetime)
        feature_cols = [col for col in df_processed.columns 
                       if col not in ['datetime', 'pm25', 'city']]
        
        return df_processed[feature_cols].values
    
    def predict_pm25(self, X: np.ndarray) -> Dict:
        """
        Predict PM2.5 levels using all models.
        
        Args:
            X: Input features
            
        Returns:
            Dictionary with predictions from all models
        """
        predictions = {}
        
        if 'random_forest' in self.models:
            pred = self.models['random_forest'].predict(X)
            predictions['random_forest'] = pred[-1]  # Latest prediction
            logger.info(f"Random Forest prediction: {pred[-1]:.2f} µg/m³")
        
        if 'lstm' in self.models:
            pred = self.models['lstm'].predict(X).flatten()
            predictions['lstm'] = pred[-1]
            logger.info(f"LSTM prediction: {pred[-1]:.2f} µg/m³")
        
        if 'hybrid' in self.models:
            pred = self.models['hybrid'].predict(X).flatten()
            predictions['hybrid'] = pred[-1]
            logger.info(f"Hybrid CNN-LSTM prediction: {pred[-1]:.2f} µg/m³")
        
        # Ensemble prediction (average)
        if predictions:
            ensemble_pred = np.mean(list(predictions.values()))
            predictions['ensemble'] = ensemble_pred
            logger.info(f"Ensemble prediction: {ensemble_pred:.2f} µg/m³")
        
        return predictions
    
    def get_air_quality_level(self, pm25: float) -> str:
        """
        Classify air quality level based on PM2.5.
        
        Args:
            pm25: PM2.5 concentration
            
        Returns:
            Air quality level
        """
        if pm25 <= 12:
            return "Good"
        elif pm25 <= 35.4:
            return "Moderate"
        elif pm25 <= 55.4:
            return "Unhealthy for Sensitive Groups"
        elif pm25 <= 150.4:
            return "Unhealthy"
        elif pm25 <= 250.4:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def generate_alert(self, predictions: Dict) -> str:
        """
        Generate alert based on predictions.
        
        Args:
            predictions: Dictionary with model predictions
            
        Returns:
            Alert message
        """
        ensemble_pred = predictions.get('ensemble', np.mean(list(predictions.values())))
        level = self.get_air_quality_level(ensemble_pred)
        
        alert = f"\n{'='*60}\n"
        alert += "AIR QUALITY PREDICTION ALERT\n"
        alert += f"{'='*60}\n"
        alert += f"Predicted PM2.5: {ensemble_pred:.2f} µg/m³\n"
        alert += f"Air Quality Level: {level}\n"
        
        if level in ["Unhealthy", "Very Unhealthy", "Hazardous"]:
            alert += "\n⚠️  WARNING: Air quality is poor\n"
            alert += "Recommendations:\n"
            alert += "- Limit outdoor activities\n"
            alert += "- Use air purifiers indoors\n"
            alert += "- Wear N95 masks if going outside\n"
        
        alert += f"{'='*60}\n"
        
        return alert
    
    def make_prediction(self, latitude: float, longitude: float) -> None:
        """
        Make and display prediction.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        """
        logger.info(f"Making prediction for ({latitude}, {longitude})...")
        
        # Prepare data
        X = self.prepare_prediction_data(latitude, longitude)
        
        if X is None:
            logger.error("Failed to prepare prediction data")
            return
        
        # Make predictions
        predictions = self.predict_pm25(X)
        
        # Generate alert
        alert = self.generate_alert(predictions)
        print(alert)
        
        return predictions


def main():
    """Main entry point."""
    # Initialize predictor
    predictor = AirQualityPredictor(models_dir="results")
    
    # Load trained models
    predictor.load_models()
    
    # Make prediction for London
    predictions = predictor.make_prediction(
        latitude=51.5074,
        longitude=-0.1278
    )


if __name__ == "__main__":
    main()
