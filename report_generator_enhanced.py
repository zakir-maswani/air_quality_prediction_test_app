"""
Enhanced Professional PDF Report Generator for AQI Predictor Pro

Generates comprehensive air quality prediction reports with unified theme styling.
Uses theme_config.py for consistent colors and styling across Streamlit and PDF.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import pytz
import numpy as np
import pandas as pd
from io import BytesIO
import os
import sys

# Import theme configuration
sys.path.insert(0, os.path.dirname(__file__))
from theme_config import THEME, get_pdf_theme_dict, AQI_STATUS_MAP

class EnhancedReportGenerator:
    """Generate professional PDF reports with unified theme styling."""
    
    def __init__(self, filename: str = None):
        """
        Initialize report generator.
        
        Args:
            filename: Output PDF filename
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"AQI_Report_{timestamp}.pdf"
        
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self.theme = get_pdf_theme_dict()
        self.colors_dict = self.theme['colors']
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles using theme colors."""
        # Title style - Light Orange Theme
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor(self.colors_dict['text_header']),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor(self.colors_dict['text_label']),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section heading - Orange theme
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor(self.colors_dict['text_metric']),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor(self.colors_dict['text_dark']),
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
        
        # Status label style
        self.styles.add(ParagraphStyle(
            name='StatusLabel',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor(self.colors_dict['text_metric']),
            fontName='Helvetica-Bold',
            spaceAfter=8
        ))
    
    def _get_uk_time(self) -> str:
        """Get current time in UK timezone."""
        uk_tz = pytz.timezone('Europe/London')
        uk_time = datetime.now(uk_tz)
        return uk_time.strftime("%d %b %Y, %H:%M:%S (UK)")
    
    def _get_aqi_status_color(self, pm25: float) -> tuple:
        """Get AQI status and colors based on PM2.5 level."""
        for status, config in AQI_STATUS_MAP.items():
            if pm25 <= config['pm25_max']:
                return status, config['color'], config['bg_color']
        return 'HAZARDOUS', AQI_STATUS_MAP['HAZARDOUS']['color'], AQI_STATUS_MAP['HAZARDOUS']['bg_color']
    
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
            health_recommendations: Health recommendations text
            alert_status: Current alert status
            
        Returns:
            Path to generated PDF file
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build document content
        story = []
        
        # Header with theme colors
        story.append(self._create_header(city))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(self._create_executive_summary(city, current_data, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Current Air Quality Status
        story.append(self._create_current_status_section(current_data, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Model Predictions
        story.append(self._create_predictions_section(predictions))
        story.append(Spacer(1, 0.2*inch))
        
        # Model Performance
        story.append(self._create_performance_section(model_performance))
        story.append(Spacer(1, 0.2*inch))
        
        # Health Recommendations
        story.append(self._create_health_section(health_recommendations, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Footer
        story.append(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        return self.filename
    
    def _create_header(self, city: str) -> Table:
        """Create professional header with theme colors."""
        header_data = [
            [Paragraph("AQI PREDICTOR PRO", self.styles['CustomTitle'])],
            [Paragraph("Air Quality Prediction Report", self.styles['CustomSubtitle'])],
            [Paragraph(f"<b>{city}</b> | {self._get_uk_time()}", self.styles['CustomSubtitle'])]
        ]
        
        header_table = Table(header_data, colWidths=[7*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['header_light'])),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LINEBELOW', (0, -1), (-1, -1), 3, colors.HexColor(self.colors_dict['header_dark'])),
        ]))
        
        return header_table
    
    def _create_executive_summary(self, city: str, current_data: dict, alert_status: str) -> Table:
        """Create executive summary section."""
        pm25 = current_data['PM2.5']
        status, status_color, status_bg = self._get_aqi_status_color(pm25)
        
        summary_text = f"""
        <b>Executive Summary</b><br/>
        <br/>
        This report provides a comprehensive analysis of air quality conditions in {city} 
        as of {self._get_uk_time()}. Current PM2.5 levels are <b>{pm25:.1f} µg/m³</b>, 
        indicating a <b style="color: {status_color};">{status}</b> air quality status.
        <br/><br/>
        The report includes current measurements, machine learning model predictions, 
        performance metrics, and health recommendations based on WHO guidelines.
        """
        
        summary_data = [[Paragraph(summary_text, self.styles['CustomBody'])]]
        summary_table = Table(summary_data, colWidths=[6.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['page_bg_light'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('LINEWIDTH', (0, 0), (-1, -1), 1),
            ('LINESTYLE', (0, 0), (-1, -1), 'solid'),
            ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['header_dark'])),
        ]))
        
        return summary_table
    
    def _create_current_status_section(self, current_data: dict, alert_status: str) -> Table:
        """Create current air quality status section with color-coded indicators."""
        pm25 = current_data['PM2.5']
        status, status_color, status_bg = self._get_aqi_status_color(pm25)
        
        # Create status cards
        data = [
            [Paragraph("Current Air Quality Status", self.styles['SectionHeading'])]
        ]
        
        # Status indicator
        status_text = f"""
        <font color="{status_color}"><b>Status: {status}</b></font><br/>
        PM2.5: {pm25:.1f} µg/m³
        """
        
        # Measurements
        measurements = [
            ['Parameter', 'Value', 'Unit'],
            ['PM2.5', f"{current_data['PM2.5']:.1f}", 'µg/m³'],
            ['PM10', f"{current_data['PM10']:.1f}", 'µg/m³'],
            ['', f"{current_data['NO2']:.1f}", 'ppb'],
            ['', f"{current_data['O3']:.1f}", 'ppb'],
            ['Temperature', f"{current_data['Temperature']:.1f}", '°C'],
            ['Humidity', f"{current_data['Humidity']:.0f}", '%'],
            ['Wind Speed', f"{current_data['WindSpeed']:.1f}", 'm/s'],
            ['Pressure', f"{current_data['Pressure']:.1f}", 'hPa'],
        ]
        
        meas_table = Table(measurements, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        meas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['header_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['card_bg'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['header_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor(self.colors_dict['card_bg']), 
                                                   colors.HexColor(self.colors_dict['page_bg_light'])]),
        ]))
        
        data.append([meas_table])
        
        status_table = Table(data, colWidths=[6.5*inch])
        status_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return status_table
    
    def _create_predictions_section(self, predictions: dict) -> Table:
        """Create predictions section."""
        pred_data = [
            [Paragraph("Model Predictions", self.styles['SectionHeading'])]
        ]
        
        # Predictions table
        predictions_table_data = [
            ['Model', 'PM2.5 Prediction', 'Confidence', 'Trend'],
        ]
        
        for model, pred in predictions.items():
            model_name = model.replace('_', ' ').title()
            predictions_table_data.append([
                model_name,
                f"{pred['pm25']:.1f} µg/m³",
                f"{pred['confidence']:.0%}",
                pred['trend']
            ])
        
        pred_table = Table(predictions_table_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
        pred_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['header_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['card_bg'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['header_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor(self.colors_dict['card_bg']), 
                                                   colors.HexColor(self.colors_dict['page_bg_light'])]),
        ]))
        
        pred_data.append([pred_table])
        
        predictions_section = Table(pred_data, colWidths=[6.5*inch])
        predictions_section.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return predictions_section
    
    def _create_performance_section(self, model_performance: dict) -> Table:
        """Create model performance section."""
        perf_data = [
            [Paragraph("Model Performance Metrics", self.styles['SectionHeading'])]
        ]
        
        # Performance table
        perf_table_data = [
            ['Model', 'MSE', 'RMSE', 'MAE', 'R² Score'],
        ]
        
        for model, metrics in model_performance.items():
            model_name = model.replace('_', ' ').title()
            perf_table_data.append([
                model_name,
                f"{metrics['mse']:.4f}",
                f"{metrics['rmse']:.4f}",
                f"{metrics['mae']:.4f}",
                f"{metrics['r2']:.4f}"
            ])
        
        perf_table = Table(perf_table_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['header_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['card_bg'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['header_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor(self.colors_dict['card_bg']), 
                                                   colors.HexColor(self.colors_dict['page_bg_light'])]),
        ]))
        
        perf_data.append([perf_table])
        
        perf_section = Table(perf_data, colWidths=[6.5*inch])
        perf_section.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return perf_section
    
    def _create_health_section(self, recommendations: str, alert_status: str) -> Table:
        """Create health recommendations section with color-coded alert."""
        health_data = [
            [Paragraph("Health Recommendations", self.styles['SectionHeading'])]
        ]
        
        # Alert box with theme colors
        alert_text = f"""
        <b>Current Alert Status: {alert_status}</b><br/>
        <br/>
        {recommendations}
        """
        
        alert_data = [[Paragraph(alert_text, self.styles['CustomBody'])]]
        alert_table = Table(alert_data, colWidths=[6.5*inch])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['header_light'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('LINEWIDTH', (0, 0), (-1, -1), 2),
            ('LINESTYLE', (0, 0), (-1, -1), 'solid'),
            ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['header_dark'])),
        ]))
        
        health_data.append([alert_table])
        
        health_section = Table(health_data, colWidths=[6.5*inch])
        health_section.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return health_section
    
    def _create_footer(self) -> Table:
        """Create professional footer."""
        footer_text = f"""
        <b>Report Generated:</b> {self._get_uk_time()}<br/>
        <b>System:</b> AQI Predictor Pro v1.0<br/>
        <b>Data Source:</b> DEFRA UK Air Quality Network + Open-Meteo API<br/>
        <br/>
        <i>This report is generated automatically and contains predictions based on machine learning models.
        For official air quality information, please refer to the UK Air Quality Archive.</i>
        """
        
        footer_data = [[Paragraph(footer_text, self.styles['CustomBody'])]]
        footer_table = Table(footer_data, colWidths=[6.5*inch])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor(self.colors_dict['header_dark'])),
        ]))
        
        return footer_table


# Backward compatibility - use EnhancedReportGenerator
class ProfessionalReportGenerator(EnhancedReportGenerator):
    """Alias for backward compatibility."""
    pass
