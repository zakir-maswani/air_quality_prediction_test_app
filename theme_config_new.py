"""
Professional Theme Configuration for AQI Predictor Pro
Environmental Analytics Design - Clean, Minimal, Corporate

Color Palette:
- Primary: Dark professional tone (#1a1a1a, #2d3436)
- Secondary: Soft neutral shade (#f5f5f5, #e8e8e8)
- Accent: Environmental green (#10b981, #059669)
- Background: Light and clean (#ffffff, #fafafa)
"""

from dataclasses import dataclass
from typing import Tuple

# ==========================================
# COLOR PALETTE - ENVIRONMENTAL ANALYTICS
# ==========================================

@dataclass
class ThemeColors:
    """Professional environmental analytics color scheme."""
    
    # Primary Colors - Dark Professional
    primary_dark: str = "#1a1a1a"          # Deep charcoal
    primary_medium: str = "#2d3436"        # Dark gray
    primary_light: str = "#636e72"         # Medium gray
    
    # Secondary Colors - Neutral
    secondary_light: str = "#f5f5f5"       # Off-white
    secondary_medium: str = "#e8e8e8"      # Light gray
    secondary_dark: str = "#d0d0d0"        # Medium gray
    
    # Accent - Environmental Green
    accent_primary: str = "#10b981"        # Vibrant green
    accent_dark: str = "#059669"           # Deep green
    accent_light: str = "#d1fae5"          # Pale green
    
    # Background Colors
    bg_primary: str = "#ffffff"            # Pure white
    bg_secondary: str = "#fafafa"          # Off-white
    bg_tertiary: str = "#f5f5f5"           # Light gray
    
    # Text Colors
    text_primary: str = "#1a1a1a"          # Dark charcoal
    text_secondary: str = "#4b5563"        # Medium gray
    text_tertiary: str = "#8b95a5"         # Light gray
    text_light: str = "#ffffff"            # White
    
    # AQI Status Colors
    aqi_good: str = "#10b981"              # Green
    aqi_moderate: str = "#f59e0b"          # Amber
    aqi_sensitive: str = "#ef4444"         # Red
    aqi_unhealthy: str = "#dc2626"         # Dark red
    aqi_very_unhealthy: str = "#991b1b"    # Very dark red
    aqi_hazardous: str = "#7f1d1d"         # Maroon
    
    # AQI Background Colors
    aqi_good_bg: str = "#ecfdf5"           # Very light green
    aqi_moderate_bg: str = "#fffbeb"       # Very light amber
    aqi_sensitive_bg: str = "#fef2f2"      # Very light red
    aqi_unhealthy_bg: str = "#fef2f2"      # Very light dark red
    aqi_very_unhealthy_bg: str = "#fef2f2" # Very light very dark red
    aqi_hazardous_bg: str = "#fef2f2"      # Very light maroon
    
    # Alert Colors
    alert_success: str = "#ecfdf5"         # Light green
    alert_warning: str = "#fffbeb"         # Light amber
    alert_danger: str = "#fef2f2"          # Light red
    alert_info: str = "#eff6ff"            # Light blue
    
    # Border Colors
    border_light: str = "#e5e7eb"          # Light border
    border_medium: str = "#d1d5db"         # Medium border
    border_dark: str = "#9ca3af"           # Dark border
    
    # Card & Component
    card_bg: str = "#ffffff"               # White cards
    card_border: str = "#e5e7eb"           # Light card border
    card_shadow: str = "rgba(0, 0, 0, 0.08)"  # Subtle shadow

# ==========================================
# TYPOGRAPHY CONFIGURATION
# ==========================================

@dataclass
class ThemeTypography:
    """Professional typography settings."""
    
    # Font Families - Modern professional
    font_sans: str = "Inter, Segoe UI, -apple-system, sans-serif"
    font_mono: str = "Menlo, Monaco, Courier New, monospace"
    
    # Font Sizes
    size_xs: str = "0.75rem"       # 12px
    size_sm: str = "0.875rem"      # 14px
    size_base: str = "1rem"        # 16px
    size_lg: str = "1.125rem"      # 18px
    size_xl: str = "1.25rem"       # 20px
    size_2xl: str = "1.5rem"       # 24px
    size_3xl: str = "1.875rem"     # 30px
    size_4xl: str = "2.25rem"      # 36px
    
    # Font Weights
    weight_normal: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700
    weight_extrabold: int = 800
    
    # Line Heights
    line_tight: str = "1.25"
    line_normal: str = "1.5"
    line_relaxed: str = "1.75"
    line_loose: str = "2"

# ==========================================
# SPACING CONFIGURATION
# ==========================================

@dataclass
class ThemeSpacing:
    """Consistent spacing values."""
    
    xs: str = "0.25rem"    # 4px
    sm: str = "0.5rem"     # 8px
    md: str = "1rem"       # 16px
    lg: str = "1.5rem"     # 24px
    xl: str = "2rem"       # 32px
    xxl: str = "3rem"      # 48px

# ==========================================
# BORDER RADIUS CONFIGURATION
# ==========================================

@dataclass
class ThemeBorderRadius:
    """Consistent border radius values."""
    
    sm: str = "4px"
    md: str = "6px"
    lg: str = "8px"
    xl: str = "12px"
    full: str = "9999px"

# ==========================================
# SHADOW CONFIGURATION
# ==========================================

@dataclass
class ThemeShadows:
    """Professional shadow definitions."""
    
    # Subtle shadows
    sm: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    xl: str = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    
    # Component shadows
    card: str = "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)"
    button_hover: str = "0 4px 12px rgba(0, 0, 0, 0.15)"

# ==========================================
# ANIMATION CONFIGURATION
# ==========================================

@dataclass
class ThemeAnimations:
    """Animation timing and easing."""
    
    duration_fast: str = "150ms"
    duration_base: str = "300ms"
    duration_slow: str = "500ms"
    
    easing_ease_in: str = "ease-in"
    easing_ease_out: str = "ease-out"
    easing_ease_in_out: str = "ease-in-out"
    easing_linear: str = "linear"

# ==========================================
# COMPLETE THEME OBJECT
# ==========================================

THEME = {
    'colors': ThemeColors(),
    'typography': ThemeTypography(),
    'spacing': ThemeSpacing(),
    'border_radius': ThemeBorderRadius(),
    'shadows': ThemeShadows(),
    'animations': ThemeAnimations(),
}

# ==========================================
# AQI STATUS MAPPING
# ==========================================

AQI_STATUS_MAP = {
    'GOOD': {
        'pm25_max': 12,
        'color': THEME['colors'].aqi_good,
        'bg_color': THEME['colors'].aqi_good_bg,
        'text_color': '#047857',
        'recommendation': 'Air quality is satisfactory. Enjoy outdoor activities without restrictions.'
    },
    'MODERATE': {
        'pm25_max': 35.4,
        'color': THEME['colors'].aqi_moderate,
        'bg_color': THEME['colors'].aqi_moderate_bg,
        'text_color': '#92400e',
        'recommendation': 'Air quality is acceptable. Unusually sensitive people should consider limiting prolonged outdoor exertion.'
    },
    'UNHEALTHY_FOR_SENSITIVE': {
        'pm25_max': 55.4,
        'color': THEME['colors'].aqi_sensitive,
        'bg_color': THEME['colors'].aqi_sensitive_bg,
        'text_color': '#7f1d1d',
        'recommendation': 'Members of sensitive groups should limit prolonged outdoor exertion.'
    },
    'UNHEALTHY': {
        'pm25_max': 150.4,
        'color': THEME['colors'].aqi_unhealthy,
        'bg_color': THEME['colors'].aqi_unhealthy_bg,
        'text_color': '#7f1d1d',
        'recommendation': 'Some members of the general public may experience health effects.'
    },
    'VERY_UNHEALTHY': {
        'pm25_max': 250.4,
        'color': THEME['colors'].aqi_very_unhealthy,
        'bg_color': THEME['colors'].aqi_very_unhealthy_bg,
        'text_color': '#7f1d1d',
        'recommendation': 'Health alert. Everyone may experience health effects.'
    },
    'HAZARDOUS': {
        'pm25_max': float('inf'),
        'color': THEME['colors'].aqi_hazardous,
        'bg_color': THEME['colors'].aqi_hazardous_bg,
        'text_color': '#7f1d1d',
        'recommendation': 'Health warning. Avoid all outdoor activities.'
    }
}

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def get_aqi_status(pm25: float) -> Tuple[str, str, str]:
    """Get AQI status based on PM2.5 level."""
    for status, config in AQI_STATUS_MAP.items():
        if pm25 <= config['pm25_max']:
            return status, config['color'], config['bg_color']
    return 'HAZARDOUS', AQI_STATUS_MAP['HAZARDOUS']['color'], AQI_STATUS_MAP['HAZARDOUS']['bg_color']

def get_aqi_recommendation(pm25: float) -> str:
    """Get health recommendation based on PM2.5 level."""
    status, _, _ = get_aqi_status(pm25)
    return AQI_STATUS_MAP[status]['recommendation']

def get_aqi_color(pm25: float) -> str:
    """Get AQI color for a given PM2.5 level."""
    _, color, _ = get_aqi_status(pm25)
    return color

def get_aqi_bg_color(pm25: float) -> str:
    """Get AQI background color for a given PM2.5 level."""
    _, _, bg_color = get_aqi_status(pm25)
    return bg_color

# ==========================================
# STREAMLIT CSS STYLES
# ==========================================

def get_streamlit_css() -> str:
    """Get complete CSS styling for Streamlit application."""
    colors = THEME['colors']
    shadows = THEME['shadows']
    animations = THEME['animations']
    typography = THEME['typography']
    
    return f"""
    <style>
        /* ==========================================
           ROOT & GLOBAL STYLES
           ========================================== */
        
        :root {{
            --primary-dark: {colors.primary_dark};
            --primary-medium: {colors.primary_medium};
            --primary-light: {colors.primary_light};
            --accent-primary: {colors.accent_primary};
            --accent-dark: {colors.accent_dark};
            --accent-light: {colors.accent_light};
            --bg-primary: {colors.bg_primary};
            --text-primary: {colors.text_primary};
            --text-secondary: {colors.text_secondary};
            --border-light: {colors.border_light};
        }}
        
        * {{
            font-family: {typography.font_sans};
        }}
        
        body {{
            background-color: {colors.bg_secondary};
            color: {colors.text_primary};
        }}
        
        /* ==========================================
           MAIN CONTAINER
           ========================================== */
        
        [data-testid="stAppViewContainer"] {{
            background-color: {colors.bg_secondary};
        }}
        
        [data-testid="stMainBlockContainer"] {{
            background-color: {colors.bg_secondary};
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* ==========================================
           HEADER & TITLE
           ========================================== */
        
        h1, h2, h3, h4, h5, h6 {{
            color: {colors.text_primary};
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: 1.875rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid {colors.accent_primary};
            padding-bottom: 0.75rem;
        }}
        
        h3 {{
            font-size: 1.25rem;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
        }}
        
        /* ==========================================
           TEXT & PARAGRAPHS
           ========================================== */
        
        p {{
            color: {colors.text_secondary};
            line-height: 1.6;
            font-size: 0.95rem;
        }}
        
        label {{
            color: {colors.text_primary};
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        /* ==========================================
           BUTTONS
           ========================================== */
        
        .stButton > button {{
            background-color: {colors.accent_primary};
            color: {colors.text_light};
            border: none;
            border-radius: {THEME['border_radius'].md};
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            transition: all {animations.duration_base} {animations.easing_ease_in_out};
            box-shadow: {shadows.sm};
        }}
        
        .stButton > button:hover {{
            background-color: {colors.accent_dark};
            box-shadow: {shadows.button_hover};
            transform: translateY(-2px);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* ==========================================
           INPUT FIELDS
           ========================================== */
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div > select {{
            background-color: {colors.bg_primary};
            color: {colors.text_primary};
            border: 1px solid {colors.border_light};
            border-radius: {THEME['border_radius'].md};
            padding: 0.75rem;
            transition: all {animations.duration_base} {animations.easing_ease_in_out};
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stMultiSelect > div > div > select:focus {{
            border-color: {colors.accent_primary};
            box-shadow: 0 0 0 3px {colors.accent_light};
        }}
        
        /* ==========================================
           METRICS
           ========================================== */
        
        [data-testid="stMetricValue"] {{
            font-size: 2.5rem;
            font-weight: 800;
            color: {colors.accent_primary};
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 0.9rem;
            color: {colors.text_secondary};
            font-weight: 600;
        }}
        
        [data-testid="stMetricDelta"] {{
            color: {colors.accent_primary};
        }}
        
        /* ==========================================
           CARDS & CONTAINERS
           ========================================== */
        
        [data-testid="stVerticalBlock"] {{
            background-color: transparent;
        }}
        
        .stCard {{
            background-color: {colors.card_bg};
            border: 1px solid {colors.card_border};
            border-radius: {THEME['border_radius'].lg};
            padding: 1.5rem;
            box-shadow: {shadows.card};
        }}
        
        /* ==========================================
           ALERTS
           ========================================== */
        
        .stAlert {{
            border-radius: {THEME['border_radius'].lg};
            padding: 1rem;
        }}
        
        .stSuccess {{
            background-color: {colors.alert_success};
            border-left: 4px solid {colors.aqi_good};
        }}
        
        .stWarning {{
            background-color: {colors.alert_warning};
            border-left: 4px solid {colors.aqi_moderate};
        }}
        
        .stError {{
            background-color: {colors.alert_danger};
            border-left: 4px solid {colors.aqi_sensitive};
        }}
        
        .stInfo {{
            background-color: {colors.alert_info};
            border-left: 4px solid {colors.accent_primary};
        }}
        
        /* ==========================================
           SIDEBAR
           ========================================== */
        
        [data-testid="stSidebar"] {{
            background-color: {colors.bg_primary};
            border-right: 1px solid {colors.border_light};
        }}
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {colors.text_primary};
        }}
        
        /* ==========================================
           TABS
           ========================================== */
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 2px solid {colors.border_light};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 0;
            padding: 1rem 1.5rem;
            background-color: transparent;
            border: none;
            color: {colors.text_secondary};
            font-weight: 600;
            transition: all {animations.duration_base} {animations.easing_ease_in_out};
            border-bottom: 3px solid transparent;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: transparent;
            color: {colors.accent_primary};
            border-bottom-color: {colors.accent_primary};
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            color: {colors.text_primary};
        }}
        
        /* ==========================================
           EXPANDER
           ========================================== */
        
        .streamlit-expanderHeader {{
            background-color: {colors.bg_tertiary};
            border-radius: {THEME['border_radius'].md};
            padding: 1rem;
            color: {colors.text_primary};
            font-weight: 600;
            transition: all {animations.duration_base} {animations.easing_ease_in_out};
            border: 1px solid {colors.border_light};
        }}
        
        .streamlit-expanderHeader:hover {{
            background-color: {colors.secondary_light};
            border-color: {colors.accent_primary};
        }}
        
        /* ==========================================
           DATAFRAME
           ========================================== */
        
        [data-testid="stDataFrame"] {{
            background-color: {colors.bg_primary};
            border-radius: {THEME['border_radius'].lg};
            overflow: hidden;
        }}
        
        /* ==========================================
           FOOTER
           ========================================== */
        
        footer {{
            visibility: hidden;
        }}
        
        /* ==========================================
           CUSTOM ALERT BOXES
           ========================================== */
        
        .alert-box {{
            padding: 1rem;
            border-radius: {THEME['border_radius'].lg};
            border-left: 4px solid;
            margin: 1rem 0;
        }}
        
        .alert-success {{
            background-color: {colors.alert_success};
            border-left-color: {colors.aqi_good};
            color: {colors.text_primary};
        }}
        
        .alert-warning {{
            background-color: {colors.alert_warning};
            border-left-color: {colors.aqi_moderate};
            color: {colors.text_primary};
        }}
        
        .alert-danger {{
            background-color: {colors.alert_danger};
            border-left-color: {colors.aqi_sensitive};
            color: {colors.text_primary};
        }}
        
        .alert-info {{
            background-color: {colors.alert_info};
            border-left-color: {colors.accent_primary};
            color: {colors.text_primary};
        }}
    </style>
    """

def get_pdf_theme_dict() -> dict:
    """Get theme values formatted for PDF generation."""
    colors = THEME['colors']
    return {
        'colors': {
            'primary_dark': colors.primary_dark,
            'primary_medium': colors.primary_medium,
            'primary_light': colors.primary_light,
            'accent_primary': colors.accent_primary,
            'accent_dark': colors.accent_dark,
            'accent_light': colors.accent_light,
            'bg_primary': colors.bg_primary,
            'text_primary': colors.text_primary,
            'text_secondary': colors.text_secondary,
            'aqi_good': colors.aqi_good,
            'aqi_moderate': colors.aqi_moderate,
            'aqi_sensitive': colors.aqi_sensitive,
            'aqi_unhealthy': colors.aqi_unhealthy,
            'aqi_very_unhealthy': colors.aqi_very_unhealthy,
            'aqi_hazardous': colors.aqi_hazardous,
        },
        'aqi_status_map': AQI_STATUS_MAP,
    }
