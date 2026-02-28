"""
Model Evaluation Module
Computes performance metrics and generates evaluation reports
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging
from typing import Dict, Tuple
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluates model performance using standard metrics."""
    
    @staticmethod
    def calculate_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Squared Error.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MSE value
        """
        return mean_squared_error(y_true, y_pred)
    
    @staticmethod
    def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Root Mean Squared Error.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            RMSE value
        """
        mse = mean_squared_error(y_true, y_pred)
        return np.sqrt(mse)
    
    @staticmethod
    def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Error.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MAE value
        """
        return mean_absolute_error(y_true, y_pred)
    
    @staticmethod
    def calculate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate R² score.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            R² value
        """
        return r2_score(y_true, y_pred)
    
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MAPE value
        """
        mask = y_true != 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    @staticmethod
    def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, 
                      model_name: str = "Model") -> Dict:
        """
        Comprehensive model evaluation.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            model_name: Name of the model
            
        Returns:
            Dictionary with all metrics
        """
        metrics = {
            'model_name': model_name,
            'mse': ModelEvaluator.calculate_mse(y_true, y_pred),
            'rmse': ModelEvaluator.calculate_rmse(y_true, y_pred),
            'mae': ModelEvaluator.calculate_mae(y_true, y_pred),
            'r2': ModelEvaluator.calculate_r2(y_true, y_pred),
            'mape': ModelEvaluator.calculate_mape(y_true, y_pred)
        }
        
        logger.info(f"\n{model_name} Evaluation Results:")
        logger.info(f"  MSE:  {metrics['mse']:.4f}")
        logger.info(f"  RMSE: {metrics['rmse']:.4f}")
        logger.info(f"  MAE:  {metrics['mae']:.4f}")
        logger.info(f"  R²:   {metrics['r2']:.4f}")
        logger.info(f"  MAPE: {metrics['mape']:.2f}%")
        
        return metrics
    
    @staticmethod
    def compare_models(results: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare multiple models.
        
        Args:
            results: Dictionary with model results
            
        Returns:
            DataFrame with comparison
        """
        comparison_df = pd.DataFrame(results).T
        comparison_df = comparison_df.sort_values('r2', ascending=False)
        
        logger.info("\nModel Comparison:")
        logger.info(comparison_df.to_string())
        
        return comparison_df
    
    @staticmethod
    def calculate_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Calculate prediction residuals.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Residuals
        """
        return y_true - y_pred
    
    @staticmethod
    def get_prediction_intervals(y_true: np.ndarray, y_pred: np.ndarray,
                                confidence: float = 0.95) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate prediction intervals.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            confidence: Confidence level (default 0.95)
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        residuals = y_true - y_pred
        std_residuals = np.std(residuals)
        
        # Z-score for 95% confidence
        z_score = 1.96 if confidence == 0.95 else 1.645
        
        lower_bound = y_pred - z_score * std_residuals
        upper_bound = y_pred + z_score * std_residuals
        
        return lower_bound, upper_bound


class PerformanceReport:
    """Generates comprehensive performance reports."""
    
    def __init__(self):
        """Initialize report generator."""
        self.evaluator = ModelEvaluator()
        self.results = {}
    
    def add_model_results(self, model_name: str, y_true: np.ndarray, 
                         y_pred: np.ndarray) -> None:
        """
        Add model results to report.
        
        Args:
            model_name: Name of the model
            y_true: True values
            y_pred: Predicted values
        """
        metrics = self.evaluator.evaluate_model(y_true, y_pred, model_name)
        self.results[model_name] = metrics
    
    def generate_comparison_table(self) -> pd.DataFrame:
        """
        Generate comparison table of all models.
        
        Returns:
            Comparison DataFrame
        """
        return self.evaluator.compare_models(self.results)
    
    def save_report(self, filepath: str) -> None:
        """
        Save report to JSON file.
        
        Args:
            filepath: Path to save report
        """
        report = {
            'models': self.results,
            'best_model': max(self.results.items(), key=lambda x: x[1]['r2'])[0]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=4)
        
        logger.info(f"Report saved to {filepath}")
    
    def get_summary(self) -> str:
        """
        Get text summary of results.
        
        Returns:
            Summary string
        """
        comparison_df = self.generate_comparison_table()
        best_model = comparison_df.index[0]
        
        summary = f"\n{'='*60}\n"
        summary += "MODEL PERFORMANCE SUMMARY\n"
        summary += f"{'='*60}\n\n"
        summary += comparison_df.to_string()
        summary += f"\n\n{'='*60}\n"
        summary += f"BEST MODEL: {best_model}\n"
        summary += f"R² Score: {self.results[best_model]['r2']:.4f}\n"
        summary += f"RMSE: {self.results[best_model]['rmse']:.4f}\n"
        summary += f"MAE: {self.results[best_model]['mae']:.4f}\n"
        summary += f"{'='*60}\n"
        
        return summary


def main():
    """Example usage of evaluation module."""
    # Simulated predictions
    np.random.seed(42)
    y_true = np.random.uniform(10, 50, 100)
    
    # Model predictions with different accuracy levels
    y_pred_rf = y_true + np.random.normal(0, 2, 100)
    y_pred_lstm = y_true + np.random.normal(0, 1.5, 100)
    y_pred_hybrid = y_true + np.random.normal(0, 1, 100)
    
    # Generate report
    report = PerformanceReport()
    report.add_model_results("Random Forest", y_true, y_pred_rf)
    report.add_model_results("LSTM", y_true, y_pred_lstm)
    report.add_model_results("Hybrid CNN-LSTM", y_true, y_pred_hybrid)
    
    print(report.get_summary())
    report.save_report("evaluation_report.json")


if __name__ == "__main__":
    main()
