"""
Professional PDF Report Generator for AQI Predictor Pro
Generates comprehensive air quality prediction reports with unified theme styling.
Uses theme_config_new.py for consistent colors and styling across Streamlit and PDF.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import pytz
import os
import sys

# Import theme configuration
sys.path.insert(0, os.path.dirname(__file__))
from theme_config_new import THEME, get_pdf_theme_dict, AQI_STATUS_MAP

class ProfessionalReportGenerator:
    """Generate professional PDF reports with unified theme styling."""
    
    def __init__(self, filename: str = None):
        """Initialize report generator."""
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
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor(self.colors_dict['text_primary']),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor(self.colors_dict['text_secondary']),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor(self.colors_dict['primary_dark']),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor(self.colors_dict['text_primary']),
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=12
        ))
        
        # Status label style
        self.styles.add(ParagraphStyle(
            name='StatusLabel',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor(self.colors_dict['text_primary']),
            fontName='Helvetica-Bold',
            spaceAfter=6
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
        """Generate comprehensive PDF report."""
        
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title
        story.append(Paragraph("AQI PREDICTOR PRO", self.styles['CustomTitle']))
        story.append(Paragraph("Air Quality Prediction Report", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # City and timestamp
        city_info = f"<b>City:</b> {city} | <b>Generated:</b> {self._get_uk_time()}"
        story.append(Paragraph(city_info, self.styles['CustomBody']))
        story.append(Spacer(1, 0.15*inch))
        
        # Divider
        divider_data = [['']]
        divider_table = Table(divider_data, colWidths=[7*inch])
        divider_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 2, colors.HexColor(self.colors_dict['accent_primary'])),
        ]))
        story.append(divider_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Current Air Quality Section
        story.append(self._create_current_quality_section(current_data, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Pollutant Values Section
        story.append(self._create_pollutant_section(current_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Health Recommendations Section
        story.append(self._create_health_section(health_recommendations, alert_status))
        story.append(Spacer(1, 0.2*inch))
        
        # Model Predictions Section
        story.append(self._create_predictions_section(predictions))
        story.append(Spacer(1, 0.2*inch))
        
        # Model Performance Section
        story.append(self._create_performance_section(model_performance))
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(self._create_footer())
        
        # Build PDF
        doc.build(story)
        return self.filename
    
    def _create_current_quality_section(self, current_data: dict, alert_status: str) -> Table:
        """Create current air quality section."""
        section_data = [
            [Paragraph("Current Air Quality Status", self.styles['SectionHeading'])]
        ]
        
        # Status box
        status_text = f"""
        <b>Alert Status:</b> {alert_status}<br/>
        <b>PM2.5 Level:</b> {current_data['PM2.5']:.1f} µg/m³<br/>
        <b>Temperature:</b> {current_data['Temperature']:.1f}°C<br/>
        <b>Humidity:</b> {current_data['Humidity']:.0f}%
        """
        
        status_data = [[Paragraph(status_text, self.styles['CustomBody'])]]
        status_table = Table(status_data, colWidths=[6.5*inch])
        status_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['accent_light'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('LINEWIDTH', (0, 0), (-1, -1), 1),
            ('LINESTYLE', (0, 0), (-1, -1), 'solid'),
            ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['accent_primary'])),
        ]))
        
        section_data.append([status_table])
        
        section_table = Table(section_data, colWidths=[6.5*inch])
        section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return section_table
    
    def _create_pollutant_section(self, current_data: dict) -> Table:
        """Create pollutant values section."""
        section_data = [
            [Paragraph("Pollutant Concentrations", self.styles['SectionHeading'])]
        ]
        
        # Pollutant table
        pollutant_table_data = [
            ['Pollutant', 'Concentration', 'Unit'],
            ['PM2.5', f"{current_data['PM2.5']:.1f}", 'µg/m³'],
            ['PM10', f"{current_data['PM10']:.1f}", 'µg/m³'],
            ['NO2', f"{current_data['NO2']:.1f}", 'ppb'],
            ['O3', f"{current_data['O3']:.1f}", 'ppb'],
            ['SO2', f"{current_data.get('SO2', 0):.1f}", 'ppb'],
        ]
        
        pollutant_tbl = Table(pollutant_table_data, colWidths=[2.2*inch, 2.2*inch, 2.1*inch])
        pollutant_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['primary_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['bg_primary'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['border_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor(self.colors_dict['bg_primary']),
                colors.HexColor(self.colors_dict['bg_secondary'])
            ]),
        ]))
        
        section_data.append([pollutant_tbl])
        
        section_table = Table(section_data, colWidths=[6.5*inch])
        section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return section_table
    
    def _create_predictions_section(self, predictions: dict) -> Table:
        """Create model predictions section."""
        section_data = [
            [Paragraph("Model Predictions", self.styles['SectionHeading'])]
        ]
        
        # Predictions table
        pred_table_data = [
            ['Model', 'PM2.5 Prediction', 'Confidence', 'Trend'],
        ]
        
        for model, pred in predictions.items():
            model_name = model.replace('_', ' ').title()
            pred_table_data.append([
                model_name,
                f"{pred['pm25']:.1f} µg/m³",
                f"{pred['confidence']:.0%}",
                pred['trend']
            ])
        
        pred_tbl = Table(pred_table_data, colWidths=[1.6*inch, 1.8*inch, 1.6*inch, 1.5*inch])
        pred_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['primary_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['bg_primary'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['border_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor(self.colors_dict['bg_primary']),
                colors.HexColor(self.colors_dict['bg_secondary'])
            ]),
        ]))
        
        section_data.append([pred_tbl])
        
        section_table = Table(section_data, colWidths=[6.5*inch])
        section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return section_table
    
    def _create_performance_section(self, model_performance: dict) -> Table:
        """Create model performance section."""
        section_data = [
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
        
        perf_tbl = Table(perf_table_data, colWidths=[1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        perf_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors_dict['primary_dark'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(self.colors_dict['bg_primary'])),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.colors_dict['border_light'])),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor(self.colors_dict['bg_primary']),
                colors.HexColor(self.colors_dict['bg_secondary'])
            ]),
        ]))
        
        section_data.append([perf_tbl])
        
        section_table = Table(section_data, colWidths=[6.5*inch])
        section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return section_table
    
    def _create_health_section(self, recommendations: str, alert_status: str) -> Table:
        """Create health recommendations section."""
        section_data = [
            [Paragraph("Health Recommendations", self.styles['SectionHeading'])]
        ]
        
        # Alert box
        alert_text = f"""
        <b>Current Alert Status: {alert_status}</b><br/>
        <br/>
        {recommendations}
        """
        
        alert_data = [[Paragraph(alert_text, self.styles['CustomBody'])]]
        alert_table = Table(alert_data, colWidths=[6.5*inch])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['accent_light'])),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('LINEWIDTH', (0, 0), (-1, -1), 1),
            ('LINESTYLE', (0, 0), (-1, -1), 'solid'),
            ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor(self.colors_dict['accent_primary'])),
        ]))
        
        section_data.append([alert_table])
        
        section_table = Table(section_data, colWidths=[6.5*inch])
        section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        return section_table
    
    def _create_footer(self) -> Table:
        """Create professional footer."""
        footer_text = f"""
        <b>Report Generated:</b> {self._get_uk_time()}<br/>
        <b>System:</b> AQI Predictor Pro v2.0 (Professional Edition)<br/>
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
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor(self.colors_dict['primary_dark'])),
        ]))
        
        return footer_table
