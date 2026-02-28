"""
Professional PDF Report Generator for AQI Predictor Pro
Generates comprehensive air quality prediction reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import numpy as np
import pandas as pd
from io import BytesIO
import os

class ProfessionalReportGenerator:
    """Generate professional PDF reports for air quality predictions."""
    
    def __init__(self, filename: str = None):
        """
        Initialize report generator.
        
        Args:
            filename: Output PDF filename
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"AQI_Predictor_Pro_{timestamp}.pdf"
        
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#FFD580'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2a5298'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e3c72'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            borderPadding=10,
            borderColor=colors.HexColor('#2a5298'),
            borderWidth=2,
            borderRadius=5
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=14
        ))
        
        # Alert style
        self.styles.add(ParagraphStyle(
            name='AlertText',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#ffffff'),
            alignment=TA_LEFT,
            spaceAfter=5
        ))
    
    def generate_report(self, 
                       city: str,
                       current_data: dict,
                       predictions: dict,
                       model_performance: dict,
                       health_recommendations: str,
                       alert_status: str) -> str:
        """
        Generate comprehensive PDF report.
        
        Args:
            city: City name
            current_data: Current air quality measurements
            predictions: Model predictions
            model_performance: Model performance metrics
            health_recommendations: Health advisory text
            alert_status: Current alert status
        
        Returns:
            Path to generated PDF
        """
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build story
        story = []
        
        # Header
        story.extend(self._build_header(city))
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.extend(self._build_executive_summary(current_data, alert_status))
        story.append(PageBreak())
        
        # Current Conditions
        story.extend(self._build_current_conditions(city, current_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Predictions
        story.extend(self._build_predictions(predictions))
        story.append(Spacer(1, 0.2*inch))
        
        # Model Performance
        story.extend(self._build_model_performance(model_performance))
        story.append(PageBreak())
        
        # Health Advisory
        story.extend(self._build_health_advisory(health_recommendations, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Detailed Analysis
        story.extend(self._build_detailed_analysis(current_data, predictions))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.extend(self._build_recommendations(alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Footer
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        
        return self.filename
    
    def _build_header(self, city: str) -> list:
        """Build report header."""
        elements = []
        
        # Title
        title = Paragraph("🌬️ AirGuard AI", self.styles['CustomTitle'])
        elements.append(title)
        
        # Subtitle
        subtitle = Paragraph(
            f"Air Quality Prediction Report - {city}",
            self.styles['CustomSubtitle']
        )
        elements.append(subtitle)
        
        # Date
        date_text = Paragraph(
            f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
            self.styles['CustomBody']
        )
        elements.append(date_text)
        
        return elements
    
    def _build_executive_summary(self, current_data: dict, alert_status: str) -> list:
        """Build executive summary section."""
        elements = []
        
        heading = Paragraph("Executive Summary", self.styles['SectionHeading'])
        elements.append(heading)
        
        pm25 = current_data.get('PM2.5', 0)
        
        # Determine alert color and message
        if alert_status == 'HAZARDOUS':
            alert_color = colors.HexColor('#7f1d1d')
            alert_bg = colors.HexColor('#fee2e2')
            message = "CRITICAL: Air quality is at hazardous levels. Immediate action recommended."
        elif alert_status == 'VERY_UNHEALTHY':
            alert_color = colors.HexColor('#991b1b')
            alert_bg = colors.HexColor('#fecaca')
            message = "WARNING: Air quality is very unhealthy. Sensitive groups should stay indoors."
        elif alert_status == 'UNHEALTHY':
            alert_color = colors.HexColor('#dc2626')
            alert_bg = colors.HexColor('#fca5a5')
            message = "ALERT: Air quality is unhealthy. Sensitive groups should limit outdoor activities."
        elif alert_status == 'UNHEALTHY_SENSITIVE':
            alert_color = colors.HexColor('#ea580c')
            alert_bg = colors.HexColor('#ffedd5')
            message = "CAUTION: Air quality is unhealthy for sensitive groups."
        else:
            alert_color = colors.HexColor('#10b981')
            alert_bg = colors.HexColor('#d1fae5')
            message = "Good air quality. Normal outdoor activities are safe."
        
        # Alert box
        alert_data = [[Paragraph(message, self.styles['AlertText'])]]
        alert_table = Table(alert_data, colWidths=[6.5*inch])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), alert_bg),
            ('TEXTCOLOR', (0, 0), (-1, -1), alert_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BORDER', (0, 0), (-1, -1), 1),
            ('BORDERCOLOR', (0, 0), (-1, -1), alert_color),
            ('BORDERRADIUS', (0, 0), (-1, -1), 5),
        ]))
        elements.append(alert_table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Summary text
        summary_text = f"""
        This report provides a comprehensive analysis of air quality conditions in the monitored region.
        Current PM2.5 levels are at {pm25:.1f} µg/m³, indicating {alert_status.lower().replace('_', ' ')} air quality.
        The report includes current measurements, model predictions, health recommendations, and detailed analysis.
        """
        
        summary = Paragraph(summary_text, self.styles['CustomBody'])
        elements.append(summary)
        
        return elements
    
    def _build_current_conditions(self, city: str, current_data: dict) -> list:
        """Build current conditions section."""
        elements = []
        
        heading = Paragraph("Current Air Quality Conditions", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Data table
        data = [
            ['Pollutant', 'Level (µg/m³)', 'Status'],
            ['PM2.5', f"{current_data.get('PM2.5', 0):.1f}", self._get_status_text(current_data.get('PM2.5', 0))],
            ['PM10', f"{current_data.get('PM10', 0):.1f}", self._get_status_text(current_data.get('PM10', 0), 'PM10')],
            ['NO₂', f"{current_data.get('NO2', 0):.1f}", self._get_status_text(current_data.get('NO2', 0), 'NO2')],
            ['O₃', f"{current_data.get('O3', 0):.1f}", self._get_status_text(current_data.get('O3', 0), 'O3')],
        ]
        
        table = Table(data, colWidths=[2*inch, 2*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Meteorological data
        met_text = f"""
        <b>Meteorological Conditions:</b><br/>
        Temperature: {current_data.get('Temperature', 0):.1f}°C | 
        Humidity: {current_data.get('Humidity', 0):.0f}% | 
        Wind Speed: {current_data.get('WindSpeed', 0):.1f} m/s | 
        Pressure: {current_data.get('Pressure', 0):.0f} hPa
        """
        
        met = Paragraph(met_text, self.styles['CustomBody'])
        elements.append(met)
        
        return elements
    
    def _build_predictions(self, predictions: dict) -> list:
        """Build predictions section."""
        elements = []
        
        heading = Paragraph("Model Predictions (Next 24 Hours)", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Predictions table
        data = [
            ['Model', 'PM2.5 Prediction (µg/m³)', 'Confidence', 'Trend'],
            [
                'Random Forest',
                f"{predictions.get('random_forest', {}).get('pm25', 0):.1f}",
                f"{predictions.get('random_forest', {}).get('confidence', 0):.1f}%",
                predictions.get('random_forest', {}).get('trend', 'Stable')
            ],
            [
                'LSTM Network',
                f"{predictions.get('lstm', {}).get('pm25', 0):.1f}",
                f"{predictions.get('lstm', {}).get('confidence', 0):.1f}%",
                predictions.get('lstm', {}).get('trend', 'Stable')
            ],
            [
                'Hybrid CNN-LSTM',
                f"{predictions.get('hybrid', {}).get('pm25', 0):.1f}",
                f"{predictions.get('hybrid', {}).get('confidence', 0):.1f}%",
                predictions.get('hybrid', {}).get('trend', 'Stable')
            ],
        ]
        
        table = Table(data, colWidths=[1.8*inch, 2*inch, 1.5*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7fa')]),
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Ensemble prediction
        ensemble_pm25 = (
            predictions.get('random_forest', {}).get('pm25', 0) * 0.3 +
            predictions.get('lstm', {}).get('pm25', 0) * 0.4 +
            predictions.get('hybrid', {}).get('pm25', 0) * 0.3
        )
        
        ensemble_text = f"""
        <b>Ensemble Prediction (Weighted Average):</b> {ensemble_pm25:.1f} µg/m³<br/>
        The ensemble model combines predictions from all three models using optimized weights 
        (Random Forest: 30%, LSTM: 40%, Hybrid: 30%) to provide the most accurate forecast.
        """
        
        ensemble = Paragraph(ensemble_text, self.styles['CustomBody'])
        elements.append(ensemble)
        
        return elements
    
    def _build_model_performance(self, model_performance: dict) -> list:
        """Build model performance section."""
        elements = []
        
        heading = Paragraph("Model Performance Metrics", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Performance table
        data = [
            ['Model', 'MSE', 'RMSE', 'MAE', 'R² Score'],
            [
                'Random Forest',
                f"{model_performance.get('random_forest', {}).get('mse', 0):.4f}",
                f"{model_performance.get('random_forest', {}).get('rmse', 0):.4f}",
                f"{model_performance.get('random_forest', {}).get('mae', 0):.4f}",
                f"{model_performance.get('random_forest', {}).get('r2', 0):.4f}"
            ],
            [
                'LSTM Network',
                f"{model_performance.get('lstm', {}).get('mse', 0):.4f}",
                f"{model_performance.get('lstm', {}).get('rmse', 0):.4f}",
                f"{model_performance.get('lstm', {}).get('mae', 0):.4f}",
                f"{model_performance.get('lstm', {}).get('r2', 0):.4f}"
            ],
            [
                'Hybrid CNN-LSTM',
                f"{model_performance.get('hybrid', {}).get('mse', 0):.4f}",
                f"{model_performance.get('hybrid', {}).get('rmse', 0):.4f}",
                f"{model_performance.get('hybrid', {}).get('mae', 0):.4f}",
                f"{model_performance.get('hybrid', {}).get('r2', 0):.4f}"
            ],
        ]
        
        table = Table(data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f4f8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7fa')]),
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Metrics explanation
        metrics_text = """
        <b>Metric Definitions:</b><br/>
        • <b>MSE:</b> Mean Squared Error - Average of squared differences between predicted and actual values<br/>
        • <b>RMSE:</b> Root Mean Squared Error - Square root of MSE, in same units as target variable<br/>
        • <b>MAE:</b> Mean Absolute Error - Average of absolute differences between predicted and actual values<br/>
        • <b>R² Score:</b> Coefficient of Determination - Proportion of variance explained by the model (0-1)
        """
        
        metrics = Paragraph(metrics_text, self.styles['CustomBody'])
        elements.append(metrics)
        
        return elements
    
    def _build_health_advisory(self, health_recommendations: str, alert_status: str) -> list:
        """Build health advisory section."""
        elements = []
        
        heading = Paragraph("Health Advisory & Recommendations", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Health recommendations
        health_text = f"""
        <b>Current Status: {alert_status.replace('_', ' ').upper()}</b><br/><br/>
        {health_recommendations}
        """
        
        health = Paragraph(health_text, self.styles['CustomBody'])
        elements.append(health)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Vulnerable groups
        vulnerable_text = """
        <b>Vulnerable Groups:</b><br/>
        • Children and elderly persons<br/>
        • People with respiratory conditions (asthma, COPD)<br/>
        • People with cardiovascular disease<br/>
        • Pregnant women<br/>
        • Outdoor workers and athletes
        """
        
        vulnerable = Paragraph(vulnerable_text, self.styles['CustomBody'])
        elements.append(vulnerable)
        
        return elements
    
    def _build_detailed_analysis(self, current_data: dict, predictions: dict) -> list:
        """Build detailed analysis section."""
        elements = []
        
        heading = Paragraph("Detailed Analysis", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        analysis_text = f"""
        <b>Current Conditions Analysis:</b><br/>
        The current PM2.5 level of {current_data.get('PM2.5', 0):.1f} µg/m³ indicates the air quality status 
        in the monitored region. Temperature is {current_data.get('Temperature', 0):.1f}°C with humidity at 
        {current_data.get('Humidity', 0):.0f}%. Wind speed of {current_data.get('WindSpeed', 0):.1f} m/s may affect 
        pollutant dispersion patterns.<br/><br/>
        
        <b>Prediction Analysis:</b><br/>
        The ensemble of machine learning models predicts PM2.5 levels for the next 24 hours. 
        The Random Forest model provides a baseline prediction based on historical patterns, 
        while the LSTM network captures temporal dependencies. The Hybrid CNN-LSTM model combines 
        spatial and temporal features for enhanced accuracy. The weighted ensemble combines all three 
        models to provide the most robust forecast.<br/><br/>
        
        <b>Model Confidence:</b><br/>
        The confidence scores reflect the agreement between models and the consistency of predictions. 
        Higher confidence indicates more reliable forecasts. When confidence is low, predictions should 
        be interpreted with caution and monitored closely.
        """
        
        analysis = Paragraph(analysis_text, self.styles['CustomBody'])
        elements.append(analysis)
        
        return elements
    
    def _build_recommendations(self, alert_status: str) -> list:
        """Build recommendations section."""
        elements = []
        
        heading = Paragraph("Recommendations", self.styles['SectionHeading'])
        elements.append(heading)
        
        elements.append(Spacer(1, 0.1*inch))
        
        if alert_status == 'HAZARDOUS':
            recommendations = """
            <b>Immediate Actions Required:</b><br/>
            1. Avoid all outdoor activities<br/>
            2. Use N95/P100 respirator masks if going outside<br/>
            3. Keep windows and doors closed<br/>
            4. Use HEPA air purifiers indoors<br/>
            5. Seek medical attention if experiencing respiratory distress<br/>
            6. Monitor air quality updates regularly
            """
        elif alert_status == 'VERY_UNHEALTHY':
            recommendations = """
            <b>Urgent Precautions:</b><br/>
            1. Limit outdoor activities to essential only<br/>
            2. Wear N95 masks when going outside<br/>
            3. Keep indoor air clean with air purifiers<br/>
            4. Increase water intake<br/>
            5. Monitor health symptoms closely<br/>
            6. Consult healthcare provider if needed
            """
        elif alert_status == 'UNHEALTHY':
            recommendations = """
            <b>Recommended Actions:</b><br/>
            1. Reduce outdoor exertion and activities<br/>
            2. Consider wearing masks outdoors<br/>
            3. Keep windows closed during peak hours<br/>
            4. Use air purifiers in living spaces<br/>
            5. Monitor air quality forecasts<br/>
            6. Vulnerable groups should stay indoors
            """
        else:
            recommendations = """
            <b>General Guidance:</b><br/>
            1. Normal outdoor activities are safe<br/>
            2. No special precautions needed<br/>
            3. Continue regular outdoor exercise<br/>
            4. Maintain good indoor air quality<br/>
            5. Stay informed about air quality changes
            """
        
        rec = Paragraph(recommendations, self.styles['CustomBody'])
        elements.append(rec)
        
        return elements
    
    def _build_footer(self) -> list:
        """Build report footer."""
        elements = []
        
        elements.append(Spacer(1, 0.2*inch))
        
        footer_text = """
        <b>Report Information:</b><br/>
        This report was generated by AirGuard AI - Research-Grade Air Quality Prediction System.<br/>
        For more information, visit the dashboard or contact the system administrator.<br/><br/>
        <i>Disclaimer: This report is for informational purposes only. For health-related concerns, 
        please consult with healthcare professionals. Air quality predictions are based on machine learning 
        models and may not be 100% accurate.</i>
        """
        
        footer = Paragraph(footer_text, self.styles['CustomBody'])
        elements.append(footer)
        
        return elements
    
    def _get_status_text(self, level: float, pollutant: str = 'PM2.5') -> str:
        """Get status text for pollutant level."""
        if pollutant == 'PM2.5':
            if level <= 12:
                return 'Good'
            elif level <= 35.4:
                return 'Moderate'
            elif level <= 55.4:
                return 'Unhealthy (Sensitive)'
            elif level <= 150.4:
                return 'Unhealthy'
            elif level <= 250.4:
                return 'Very Unhealthy'
            else:
                return 'Hazardous'
        elif pollutant == 'PM10':
            if level <= 50:
                return 'Good'
            elif level <= 100:
                return 'Moderate'
            elif level <= 150:
                return 'Unhealthy (Sensitive)'
            else:
                return 'Unhealthy'
        elif pollutant == 'NO2':
            if level <= 40:
                return 'Good'
            elif level <= 100:
                return 'Moderate'
            elif level <= 200:
                return 'Unhealthy (Sensitive)'
            else:
                return 'Unhealthy'
        elif pollutant == 'O3':
            if level <= 50:
                return 'Good'
            elif level <= 100:
                return 'Moderate'
            elif level <= 150:
                return 'Unhealthy (Sensitive)'
            else:
                return 'Unhealthy'
        
        return 'Unknown'
