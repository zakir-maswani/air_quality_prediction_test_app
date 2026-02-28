"""
Data Preprocessing Module
Handles data cleaning, missing value imputation, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
import logging
from typing import Tuple, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocesses air quality data for machine learning models."""
    
    def __init__(self):
        """Initialize preprocessor with scalers."""
        self.scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        self.imputer = SimpleImputer(strategy='mean')
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values using mean imputation.
        
        Args:
            df: DataFrame with potential missing values
            
        Returns:
            DataFrame with missing values imputed
        """
        logger.info(f"Missing values before imputation:\n{df.isnull().sum()}")
        
        # Identify numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Apply imputation
        df[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])
        
        logger.info(f"Missing values after imputation:\n{df.isnull().sum()}")
        return df
    
    def remove_outliers(self, df: pd.DataFrame, columns: List[str], 
                       method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers using IQR or Z-score method.
        
        Args:
            df: Input DataFrame
            columns: Columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier (default 1.5) or Z-score threshold
            
        Returns:
            DataFrame with outliers removed
        """
        df_clean = df.copy()
        
        for col in columns:
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                removed = len(df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)])
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
                logger.info(f"Removed {removed} outliers from {col} using IQR method")
                
            elif method == 'zscore':
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                removed = len(df_clean[z_scores > threshold])
                df_clean = df_clean[z_scores <= threshold]
                logger.info(f"Removed {removed} outliers from {col} using Z-score method")
        
        return df_clean.reset_index(drop=True)
    
    def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create temporal features from datetime column.
        
        Args:
            df: DataFrame with 'datetime' column
            
        Returns:
            DataFrame with additional temporal features
        """
        df = df.copy()
        
        if 'datetime' not in df.columns:
            logger.warning("'datetime' column not found")
            return df
        
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Temporal features
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['day_of_month'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
        df['day_of_year'] = df['datetime'].dt.dayofyear
        df['week_of_year'] = df['datetime'].dt.isocalendar().week
        
        # Cyclical encoding for hour (24-hour cycle)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # Cyclical encoding for day of week (7-day cycle)
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Cyclical encoding for month (12-month cycle)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Binary features
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
        
        logger.info("Temporal features created successfully")
        return df
    
    def create_lagged_features(self, df: pd.DataFrame, target_col: str, 
                              lags: List[int] = [1, 3, 6, 12, 24]) -> pd.DataFrame:
        """
        Create lagged features for time series prediction.
        
        Args:
            df: Input DataFrame
            target_col: Column to create lags for
            lags: List of lag values
            
        Returns:
            DataFrame with lagged features
        """
        df = df.copy()
        
        for lag in lags:
            df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        
        # Rolling statistics
        for window in [3, 6, 12, 24]:
            df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window=window).mean()
            df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window=window).std()
        
        logger.info(f"Lagged features created for {target_col}")
        return df
    
    def normalize_features(self, df: pd.DataFrame, method: str = 'standard') -> Tuple[pd.DataFrame, object]:
        """
        Normalize numeric features.
        
        Args:
            df: Input DataFrame
            method: 'standard' or 'minmax'
            
        Returns:
            Normalized DataFrame and fitted scaler
        """
        df = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        
        logger.info(f"Features normalized using {method} method")
        return df, scaler
    
    def preprocess(self, df: pd.DataFrame, target_col: str = 'pm25',
                  handle_outliers: bool = True, create_lags: bool = True) -> Tuple[pd.DataFrame, object]:
        """
        Complete preprocessing pipeline.
        
        Args:
            df: Raw input DataFrame
            target_col: Target column for prediction
            handle_outliers: Whether to remove outliers
            create_lags: Whether to create lagged features
            
        Returns:
            Preprocessed DataFrame and fitted scaler
        """
        logger.info("Starting preprocessing pipeline...")
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove outliers
        if handle_outliers:
            pollution_cols = ['pm25', 'pm10', 'no2', 'o3']
            existing_cols = [col for col in pollution_cols if col in df.columns]
            df = self.remove_outliers(df, existing_cols, method='iqr', threshold=1.5)
        
        # Create temporal features
        df = self.create_temporal_features(df)
        
        # Create lagged features
        if create_lags:
            df = self.create_lagged_features(df, target_col, lags=[1, 3, 6, 12, 24])
        
        # Remove rows with NaN values created by lagging
        df = df.dropna()
        
        # Normalize features
        df, scaler = self.normalize_features(df, method='standard')
        
        logger.info(f"Preprocessing complete. Final shape: {df.shape}")
        return df, scaler


def prepare_train_test_split(df: pd.DataFrame, target_col: str, 
                            test_size: float = 0.2, val_size: float = 0.1) -> Tuple:
    """
    Split data into train, validation, and test sets (temporal split).
    
    Args:
        df: Preprocessed DataFrame
        target_col: Target column name
        test_size: Proportion of test set
        val_size: Proportion of validation set
        
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # Temporal split (important for time series)
    n_samples = len(df)
    test_idx = int(n_samples * (1 - test_size))
    val_idx = int(test_idx * (1 - val_size))
    
    # Feature columns (exclude datetime and target)
    feature_cols = [col for col in df.columns if col not in ['datetime', target_col, 'city']]
    
    X_train = df.iloc[:val_idx][feature_cols].values
    y_train = df.iloc[:val_idx][target_col].values
    
    X_val = df.iloc[val_idx:test_idx][feature_cols].values
    y_val = df.iloc[val_idx:test_idx][target_col].values
    
    X_test = df.iloc[test_idx:][feature_cols].values
    y_test = df.iloc[test_idx:][target_col].values
    
    logger.info(f"Train set: {X_train.shape}, Val set: {X_val.shape}, Test set: {X_test.shape}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def main():
    """Example usage of the preprocessor."""
    # This would be used after data collection
    from data_collection import AirQualityDataCollector
    
    collector = AirQualityDataCollector()
    df = collector.collect_data(
        latitude=51.5074,
        longitude=-0.1278,
        start_date="2023-01-01",
        end_date="2023-12-31",
        city_name="London"
    )
    
    preprocessor = DataPreprocessor()
    df_processed, scaler = preprocessor.preprocess(df, target_col='pm25')
    
    print("\nPreprocessing Summary:")
    print(f"Processed shape: {df_processed.shape}")
    print(f"\nProcessed data sample:")
    print(df_processed.head())


if __name__ == "__main__":
    main()
