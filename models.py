"""
Machine Learning Models Module
Implements Random Forest, LSTM, and Hybrid CNN-LSTM models for air quality prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
import logging
from typing import Tuple, Dict
import pickle
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RandomForestModel:
    """Random Forest model for air quality prediction."""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 20, 
                 random_state: int = 42):
        """
        Initialize Random Forest model.
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum depth of trees
            random_state: Random seed
        """
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
            verbose=1
        )
        self.name = "Random Forest"
        
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the Random Forest model.
        
        Args:
            X_train: Training features
            y_train: Training target
        """
        logger.info(f"Training {self.name}...")
        self.model.fit(X_train, y_train)
        logger.info(f"{self.name} training complete")
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        return self.model.predict(X)
    
    def get_feature_importance(self, feature_names: list = None) -> Dict:
        """
        Get feature importance scores.
        
        Args:
            feature_names: Names of features
            
        Returns:
            Dictionary of feature importances
        """
        importances = self.model.feature_importances_
        
        if feature_names is None:
            feature_names = [f"Feature_{i}" for i in range(len(importances))]
        
        importance_dict = dict(zip(feature_names, importances))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    def save(self, filepath: str) -> None:
        """Save model to file."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load model from file."""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        logger.info(f"Model loaded from {filepath}")


class LSTMModel:
    """LSTM model for air quality prediction."""
    
    def __init__(self, sequence_length: int = 24, n_features: int = 10,
                 lstm_units: int = 64, dropout_rate: float = 0.2):
        """
        Initialize LSTM model.
        
        Args:
            sequence_length: Length of input sequences
            n_features: Number of features
            lstm_units: Number of LSTM units
            dropout_rate: Dropout rate
        """
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = self._build_model()
        self.name = "LSTM"
        
    def _build_model(self) -> keras.Model:
        """Build LSTM architecture."""
        model = models.Sequential([
            layers.LSTM(self.lstm_units, activation='relu', 
                       return_sequences=True,
                       input_shape=(self.sequence_length, self.n_features)),
            layers.Dropout(self.dropout_rate),
            
            layers.LSTM(self.lstm_units // 2, activation='relu', 
                       return_sequences=False),
            layers.Dropout(self.dropout_rate),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(self.dropout_rate),
            
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_sequences(self, X: np.ndarray) -> np.ndarray:
        """
        Prepare sequences for LSTM.
        
        Args:
            X: Input data
            
        Returns:
            Reshaped sequences
        """
        n_samples = X.shape[0]
        sequences = []
        
        for i in range(n_samples - self.sequence_length + 1):
            sequences.append(X[i:i + self.sequence_length])
        
        return np.array(sequences)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
             X_val: np.ndarray = None, y_val: np.ndarray = None,
             epochs: int = 50, batch_size: int = 32) -> Dict:
        """
        Train the LSTM model.
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            epochs: Number of epochs
            batch_size: Batch size
            
        Returns:
            Training history
        """
        logger.info(f"Training {self.name}...")
        
        # Prepare sequences
        X_train_seq = self.prepare_sequences(X_train)
        y_train_seq = y_train[self.sequence_length - 1:]
        
        validation_data = None
        if X_val is not None and y_val is not None:
            X_val_seq = self.prepare_sequences(X_val)
            y_val_seq = y_val[self.sequence_length - 1:]
            validation_data = (X_val_seq, y_val_seq)
        
        # Early stopping
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss' if validation_data else 'loss',
            patience=10,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_train_seq, y_train_seq,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop],
            verbose=1
        )
        
        logger.info(f"{self.name} training complete")
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        X_seq = self.prepare_sequences(X)
        return self.model.predict(X_seq, verbose=0)
    
    def save(self, filepath: str) -> None:
        """Save model to file."""
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load model from file."""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")


class HybridCNNLSTMModel:
    """Hybrid CNN-LSTM model for air quality prediction."""
    
    def __init__(self, sequence_length: int = 24, n_features: int = 10,
                 cnn_filters: int = 32, lstm_units: int = 64, 
                 dropout_rate: float = 0.2):
        """
        Initialize Hybrid CNN-LSTM model.
        
        Args:
            sequence_length: Length of input sequences
            n_features: Number of features
            cnn_filters: Number of CNN filters
            lstm_units: Number of LSTM units
            dropout_rate: Dropout rate
        """
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.cnn_filters = cnn_filters
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = self._build_model()
        self.name = "Hybrid CNN-LSTM"
        
    def _build_model(self) -> keras.Model:
        """Build Hybrid CNN-LSTM architecture."""
        model = models.Sequential([
            # CNN layers
            layers.Conv1D(self.cnn_filters, kernel_size=3, activation='relu',
                         input_shape=(self.sequence_length, self.n_features)),
            layers.Dropout(self.dropout_rate),
            layers.Conv1D(self.cnn_filters // 2, kernel_size=3, activation='relu'),
            layers.MaxPooling1D(pool_size=2),
            
            # LSTM layers
            layers.LSTM(self.lstm_units, activation='relu', 
                       return_sequences=True),
            layers.Dropout(self.dropout_rate),
            
            layers.LSTM(self.lstm_units // 2, activation='relu',
                       return_sequences=False),
            layers.Dropout(self.dropout_rate),
            
            # Dense layers
            layers.Dense(32, activation='relu'),
            layers.Dropout(self.dropout_rate),
            
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_sequences(self, X: np.ndarray) -> np.ndarray:
        """
        Prepare sequences for model.
        
        Args:
            X: Input data
            
        Returns:
            Reshaped sequences
        """
        n_samples = X.shape[0]
        sequences = []
        
        for i in range(n_samples - self.sequence_length + 1):
            sequences.append(X[i:i + self.sequence_length])
        
        return np.array(sequences)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
             X_val: np.ndarray = None, y_val: np.ndarray = None,
             epochs: int = 50, batch_size: int = 32) -> Dict:
        """
        Train the Hybrid model.
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            epochs: Number of epochs
            batch_size: Batch size
            
        Returns:
            Training history
        """
        logger.info(f"Training {self.name}...")
        
        # Prepare sequences
        X_train_seq = self.prepare_sequences(X_train)
        y_train_seq = y_train[self.sequence_length - 1:]
        
        validation_data = None
        if X_val is not None and y_val is not None:
            X_val_seq = self.prepare_sequences(X_val)
            y_val_seq = y_val[self.sequence_length - 1:]
            validation_data = (X_val_seq, y_val_seq)
        
        # Early stopping
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss' if validation_data else 'loss',
            patience=10,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_train_seq, y_train_seq,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop],
            verbose=1
        )
        
        logger.info(f"{self.name} training complete")
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        X_seq = self.prepare_sequences(X)
        return self.model.predict(X_seq, verbose=0)
    
    def save(self, filepath: str) -> None:
        """Save model to file."""
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load model from file."""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
