"""
Training Pipeline
Complete end-to-end pipeline for data collection, preprocessing, model training, and evaluation
"""

import os
import sys
import numpy as np
import pandas as pd
import logging
from datetime import datetime
import json

from data_collection import AirQualityDataCollector
from data_preprocessing import DataPreprocessor, prepare_train_test_split
from models import RandomForestModel, LSTMModel, HybridCNNLSTMModel
from evaluation import PerformanceReport, ModelEvaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AirQualityPipeline:
    """Complete pipeline for air quality prediction."""
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize pipeline.
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.collector = AirQualityDataCollector()
        self.preprocessor = DataPreprocessor()
        self.report = PerformanceReport()
        
        self.models = {}
        self.predictions = {}
        self.data = {}
        
        logger.info(f"Pipeline initialized. Output directory: {output_dir}")
    
    def collect_data(self, latitude: float, longitude: float,
                    start_date: str, end_date: str, city_name: str) -> pd.DataFrame:
        """
        Collect air quality and meteorological data.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            city_name: City name
            
        Returns:
            Collected DataFrame
        """
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 1: DATA COLLECTION")
        logger.info(f"{'='*60}")
        
        df = self.collector.collect_data(latitude, longitude, start_date, end_date, city_name)
        
        # Save raw data
        raw_data_path = os.path.join(self.output_dir, f"{city_name}_raw_data.csv")
        df.to_csv(raw_data_path, index=False)
        logger.info(f"Raw data saved to {raw_data_path}")
        
        self.data['raw'] = df
        return df
    
    def preprocess_data(self, df: pd.DataFrame, target_col: str = 'pm25') -> Tuple:
        """
        Preprocess data.
        
        Args:
            df: Raw DataFrame
            target_col: Target column
            
        Returns:
            Tuple of (preprocessed_df, X_train, X_val, X_test, y_train, y_val, y_test)
        """
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 2: DATA PREPROCESSING")
        logger.info(f"{'='*60}")
        
        df_processed, scaler = self.preprocessor.preprocess(df, target_col=target_col)
        
        # Save preprocessed data
        processed_data_path = os.path.join(self.output_dir, "processed_data.csv")
        df_processed.to_csv(processed_data_path, index=False)
        logger.info(f"Processed data saved to {processed_data_path}")
        
        # Train-test split
        X_train, X_val, X_test, y_train, y_val, y_test = prepare_train_test_split(
            df_processed, target_col, test_size=0.2, val_size=0.1
        )
        
        self.data['processed'] = df_processed
        self.data['scaler'] = scaler
        
        return df_processed, X_train, X_val, X_test, y_train, y_val, y_test
    
    def train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray,
                           X_val: np.ndarray, y_val: np.ndarray) -> None:
        """Train Random Forest model."""
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 3: MODEL TRAINING - RANDOM FOREST")
        logger.info(f"{'='*60}")
        
        model = RandomForestModel(n_estimators=100, max_depth=20)
        model.train(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_val = model.predict(X_val)
        
        # Evaluation
        self.report.add_model_results("Random Forest (Train)", y_train, y_pred_train)
        self.report.add_model_results("Random Forest (Validation)", y_val, y_pred_val)
        
        # Save model
        model_path = os.path.join(self.output_dir, "random_forest_model.pkl")
        model.save(model_path)
        
        self.models['random_forest'] = model
        self.predictions['random_forest'] = {'train': y_pred_train, 'val': y_pred_val}
    
    def train_lstm(self, X_train: np.ndarray, y_train: np.ndarray,
                  X_val: np.ndarray, y_val: np.ndarray) -> None:
        """Train LSTM model."""
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 3: MODEL TRAINING - LSTM")
        logger.info(f"{'='*60}")
        
        n_features = X_train.shape[1]
        model = LSTMModel(sequence_length=24, n_features=n_features, 
                         lstm_units=64, dropout_rate=0.2)
        
        history = model.train(X_train, y_train, X_val, y_val, 
                             epochs=50, batch_size=32)
        
        # Predictions
        y_pred_train = model.predict(X_train).flatten()
        y_pred_val = model.predict(X_val).flatten()
        
        # Adjust for sequence length
        y_train_adj = y_train[model.sequence_length - 1:]
        y_val_adj = y_val[model.sequence_length - 1:]
        
        # Evaluation
        self.report.add_model_results("LSTM (Train)", y_train_adj, y_pred_train)
        self.report.add_model_results("LSTM (Validation)", y_val_adj, y_pred_val)
        
        # Save model
        model_path = os.path.join(self.output_dir, "lstm_model.h5")
        model.save(model_path)
        
        self.models['lstm'] = model
        self.predictions['lstm'] = {'train': y_pred_train, 'val': y_pred_val}
    
    def train_hybrid(self, X_train: np.ndarray, y_train: np.ndarray,
                    X_val: np.ndarray, y_val: np.ndarray) -> None:
        """Train Hybrid CNN-LSTM model."""
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 3: MODEL TRAINING - HYBRID CNN-LSTM")
        logger.info(f"{'='*60}")
        
        n_features = X_train.shape[1]
        model = HybridCNNLSTMModel(sequence_length=24, n_features=n_features,
                                  cnn_filters=32, lstm_units=64, dropout_rate=0.2)
        
        history = model.train(X_train, y_train, X_val, y_val,
                             epochs=50, batch_size=32)
        
        # Predictions
        y_pred_train = model.predict(X_train).flatten()
        y_pred_val = model.predict(X_val).flatten()
        
        # Adjust for sequence length
        y_train_adj = y_train[model.sequence_length - 1:]
        y_val_adj = y_val[model.sequence_length - 1:]
        
        # Evaluation
        self.report.add_model_results("Hybrid CNN-LSTM (Train)", y_train_adj, y_pred_train)
        self.report.add_model_results("Hybrid CNN-LSTM (Validation)", y_val_adj, y_pred_val)
        
        # Save model
        model_path = os.path.join(self.output_dir, "hybrid_cnn_lstm_model.h5")
        model.save(model_path)
        
        self.models['hybrid'] = model
        self.predictions['hybrid'] = {'train': y_pred_train, 'val': y_pred_val}
    
    def evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray) -> None:
        """Evaluate all models on test set."""
        logger.info(f"\n{'='*60}")
        logger.info("STAGE 4: MODEL EVALUATION ON TEST SET")
        logger.info(f"{'='*60}")
        
        # Random Forest
        if 'random_forest' in self.models:
            y_pred = self.models['random_forest'].predict(X_test)
            self.report.add_model_results("Random Forest (Test)", y_test, y_pred)
            self.predictions['random_forest']['test'] = y_pred
        
        # LSTM
        if 'lstm' in self.models:
            y_pred = self.models['lstm'].predict(X_test).flatten()
            y_test_adj = y_test[self.models['lstm'].sequence_length - 1:]
            self.report.add_model_results("LSTM (Test)", y_test_adj, y_pred)
            self.predictions['lstm']['test'] = y_pred
        
        # Hybrid
        if 'hybrid' in self.models:
            y_pred = self.models['hybrid'].predict(X_test).flatten()
            y_test_adj = y_test[self.models['hybrid'].sequence_length - 1:]
            self.report.add_model_results("Hybrid CNN-LSTM (Test)", y_test_adj, y_pred)
            self.predictions['hybrid']['test'] = y_pred
    
    def generate_report(self) -> None:
        """Generate final report."""
        logger.info(f"\n{'='*60}")
        logger.info("FINAL REPORT")
        logger.info(f"{'='*60}")
        
        summary = self.report.get_summary()
        print(summary)
        
        # Save report
        report_path = os.path.join(self.output_dir, "evaluation_report.json")
        self.report.save_report(report_path)
        
        # Save summary
        summary_path = os.path.join(self.output_dir, "summary.txt")
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        logger.info(f"Report saved to {report_path}")
        logger.info(f"Summary saved to {summary_path}")
    
    def run_full_pipeline(self, latitude: float, longitude: float,
                         start_date: str, end_date: str, city_name: str) -> None:
        """
        Run complete pipeline.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date
            end_date: End date
            city_name: City name
        """
        try:
            # Stage 1: Data Collection
            df = self.collect_data(latitude, longitude, start_date, end_date, city_name)
            
            # Stage 2: Preprocessing
            df_processed, X_train, X_val, X_test, y_train, y_val, y_test = \
                self.preprocess_data(df, target_col='pm25')
            
            # Stage 3: Model Training
            self.train_random_forest(X_train, y_train, X_val, y_val)
            self.train_lstm(X_train, y_train, X_val, y_val)
            self.train_hybrid(X_train, y_train, X_val, y_val)
            
            # Stage 4: Evaluation
            self.evaluate_models(X_test, y_test)
            
            # Final Report
            self.generate_report()
            
            logger.info("\n" + "="*60)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point."""
    # Initialize pipeline
    pipeline = AirQualityPipeline(output_dir="results")
    
    # Run pipeline for London
    pipeline.run_full_pipeline(
        latitude=51.5074,
        longitude=-0.1278,
        start_date="2023-01-01",
        end_date="2023-12-31",
        city_name="London"
    )


if __name__ == "__main__":
    main()
