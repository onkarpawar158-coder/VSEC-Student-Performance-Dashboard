import os
import textwrap
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Student Performance Analysis | VSEC",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Theme (Default Dark)
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"


# Strict Monochrome Base Palette with Coordinated Chart Colors
def get_theme_colors(theme):
    if theme == "Light":
        return {
            # Strict Pure White Canvas
            "bg_page": "#FFFFFF",
            "bg_sidebar": "#FFFFFF",
            "bg_card": "#FFFFFF",
            "bg_surface": "#F8FAFC",
            "border": "#D1D5DB",
            "border_subtle": "#E5E7EB",
            
            # High-Contrast Light Mode Typography (Pure dark for clarity)
            "text_primary": "#111827",
            "text_secondary": "#374151",
            "text_muted": "#4B5563",
            
            # Visualizations (Pure White Backgrounds)
            "plot_bg": "#FFFFFF",
            "plot_text": "#111827",
            "plot_grid": "#E5E7EB",
            "plot_spine": "#CBD5E1",
            
            # Coordinated Subject Colors (Professional palette)
            "math_color": "#4E79A7",       # Steel Blue
            "reading_color": "#2A9D8F",    # Teal
            "writing_color": "#E76F51",    # Muted Red / Coral
            "overall_color": "#8172B3",    # Purple
            "amber_color": "#E9C46A",      # Amber
            "slate_color": "#8A94A6",      # Slate Grey
            
            # Grade Palette
            "grade_colors": ["#2A9D8F", "#4E79A7", "#8172B3", "#E9C46A", "#E76F51", "#8A94A6"]
        }
    else:  # Dark
        return {
            # Strict Pure Black Canvas
            "bg_page": "#000000",
            "bg_sidebar": "#000000",
            "bg_card": "#111111",
            "bg_surface": "#18181B",
            "border": "#27272A",
            "border_subtle": "#1F1F23",
            
            # High-Contrast Dark Mode Typography
            "text_primary": "#FFFFFF",
            "text_secondary": "#D1D5DB",
            "text_muted": "#9CA3AF",
            
            # Visualizations (Near-Black Backgrounds)
            "plot_bg": "#111111",
            "plot_text": "#FFFFFF",
            "plot_grid": "#222222",
            "plot_spine": "#333333",
            
            # Coordinated Subject Colors
            "math_color": "#4E79A7",       # Steel Blue
            "reading_color": "#2A9D8F",    # Teal
            "writing_color": "#E76F51",    # Muted Red / Coral
            "overall_color": "#8172B3",    # Purple
            "amber_color": "#E9C46A",      # Amber
            "slate_color": "#8A94A6",      # Slate Grey
            
            # Grade Palette
            "grade_colors": ["#2A9D8F", "#4E79A7", "#8172B3", "#E9C46A", "#E76F51", "#8A94A6"]
        }

current_theme = st.session_state["theme"]
palette = get_theme_colors(current_theme)


# Global Theme CSS: Stationary Fixed Sidebar, Move Content to Top, High-Contrast Typography
base_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Strict Monochrome Canvas */
    [data-testid="stAppViewContainer"] {{
        background-color: {palette["bg_page"]} !important;
        color: {palette["text_primary"]} !important;
    }}
    
    /* Move Main Content Directly to Top with proper breathing room */
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        padding-top: 0.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 1400px !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: {palette["bg_page"]} !important;
        left: 250px !important;
        width: calc(100% - 250px) !important;
        height: 2.0rem !important;
    }}

    /* Stationary Fixed Sidebar (250px wide) - Stays Anchored On Screen During Scrolling */
    section[data-testid="stSidebar"] {{
        background-color: {palette["bg_sidebar"]} !important;
        border-right: 1px solid {palette["border"]} !important;
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        height: 100vh !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        z-index: 999 !important;
        width: 250px !important;
        min-width: 250px !important;
        max-width: 250px !important;
    }}
    
    section[data-testid="stSidebar"] > div:first-child {{
        width: 250px !important;
        padding: 12px 10px 24px 10px !important;
    }}
    
    /* Main Content Area Offset to match Fixed Sidebar - Crucial fix: targets [data-testid="stMain"] and main.stMain */
    [data-testid="stMain"],
    main.stMain,
    #stMain {{
        margin-left: 250px !important;
        width: calc(100% - 250px) !important;
        max-width: calc(100% - 250px) !important;
        display: block !important;
    }}
    
    @media (max-width: 900px) {{
        section[data-testid="stSidebar"] {{
            position: relative !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
        }}
        [data-testid="stMain"],
        main.stMain,
        #stMain {{
            margin-left: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
        }}
        [data-testid="stHeader"] {{
            left: 0 !important;
            width: 100% !important;
        }}
    }}
    
    /* Sidebar Brand Header */
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 2px 2px 8px 2px;
    }}
    .brand-icon {{
        font-size: 1.45rem;
        line-height: 1;
    }}
    .brand-text-box {{
        display: flex;
        flex-direction: column;
    }}
    .brand-title {{
        font-size: 0.98rem;
        font-weight: 700;
        color: {palette["text_primary"]};
        line-height: 1.15;
    }}
    .brand-subtitle {{
        font-size: 0.68rem;
        color: {palette["text_muted"]};
        line-height: 1.15;
        margin-top: 2px;
    }}
    
    /* Thin Subtle Divider */
    .sidebar-divider {{
        height: 1px;
        background-color: {palette["border"]};
        margin: 6px 0 8px 0;
    }}
    
    /* Hide ugly default radio circle dots in Sidebar */
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child:not(:only-child) {{
        display: none !important;
    }}
    
    /* Theme Toggle Segmented Control */
    [data-testid="stSidebar"] div[role="radiogroup"]:first-of-type {{
        background-color: {palette["bg_surface"]} !important;
        border: 1px solid {palette["border"]} !important;
        border-radius: 6px !important;
        padding: 2px !important;
        display: flex !important;
        justify-content: space-between !important;
        gap: 3px !important;
        margin-bottom: 4px !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:first-of-type > label {{
        padding: 4px 10px !important;
        border-radius: 4px !important;
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        margin: 0 !important;
        border: none !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:first-of-type > label:has(input:checked) {{
        background-color: {palette["bg_card"]} !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.15) !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:first-of-type > label p {{
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        color: {palette["text_primary"]} !important;
        margin: 0 !important;
    }}
    
    /* Navigation Menu Items */
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type {{
        gap: 2px !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type > label {{
        padding: 7px 10px !important;
        border-radius: 6px !important;
        margin: 0 !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease, border-color 0.15s ease;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type > label p {{
        font-size: 0.84rem !important;
        color: {palette["text_secondary"]} !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type > label:hover {{
        background-color: {palette["bg_surface"]} !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type > label:has(input:checked) {{
        background-color: {palette["bg_surface"]} !important;
        border-left: 3px solid #4E79A7 !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"]:last-of-type > label:has(input:checked) p {{
        color: {palette["text_primary"]} !important;
        font-weight: 700 !important;
    }}

    /* Sidebar Team Box (Pinned on Left Side across all pages) */
    .sidebar-team-box {{
        background-color: {palette["bg_surface"]};
        border: 1px solid {palette["border"]};
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 10px;
    }}
    .team-header-tag {{
        font-size: 0.70rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4E79A7;
        margin-bottom: 8px;
    }}
    .team-member-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 5px 0;
        border-bottom: 1px dashed {palette["border_subtle"]};
    }}
    .team-member-item:last-of-type {{
        border-bottom: none;
    }}
    .member-avatar {{
        font-size: 1.15rem;
        line-height: 1;
    }}
    .team-member-name {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {palette["text_primary"]};
        line-height: 1.25;
    }}
    .team-member-sub {{
        font-size: 0.72rem;
        font-weight: 500;
        color: {palette["text_secondary"]};
    }}
    .team-academic-info {{
        font-size: 0.73rem;
        font-weight: 600;
        color: {palette["text_secondary"]};
        margin-top: 8px;
        line-height: 1.35;
    }}
    .team-subject-info {{
        font-size: 0.69rem;
        color: {palette["text_muted"]};
        margin-top: 2px;
    }}

    /* Main Content Top Heading */
    .header-container {{
        padding: 0 0 6px 0;
        margin-bottom: 12px;
        border-bottom: 1px solid {palette["border"]};
    }}
    .header-title {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {palette["text_primary"]};
        margin: 0 0 2px 0;
        line-height: 1.2;
    }}
    .header-desc {{
        color: {palette["text_secondary"]};
        font-size: 0.85rem;
        margin: 0;
    }}

    /* Compact Responsive KPI Cards */
    .metric-card {{
        background-color: {palette["bg_card"]};
        border: 1px solid {palette["border"]};
        border-radius: 6px;
        padding: 9px 12px;
        margin-bottom: 8px;
        min-height: 78px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.18s ease, border-color 0.18s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        border-color: #4E79A7 !important;
    }}
    .metric-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .metric-title {{
        font-size: 0.74rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: {palette["text_muted"]};
    }}
    .metric-icon {{
        font-size: 0.95rem;
    }}
    .metric-value {{
        font-size: 1.55rem;
        font-weight: 700;
        color: {palette["text_primary"]};
        line-height: 1.15;
        margin: 2px 0;
    }}
    .metric-subtitle {{
        font-size: 0.72rem;
        color: {palette["text_secondary"]};
    }}

    /* Content Panels */
    .panel-box {{
        background-color: {palette["bg_card"]};
        border: 1px solid {palette["border"]};
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 10px;
        transition: border-color 0.18s ease;
    }}
    .panel-box:hover {{
        border-color: #4E79A7;
    }}
    .info-card {{
        background-color: {palette["bg_surface"]};
        border: 1px solid {palette["border"]};
        border-left: 3px solid #4E79A7;
        border-radius: 6px;
        padding: 9px 12px;
        margin-bottom: 8px;
        color: {palette["text_secondary"]};
        font-size: 0.84rem;
        line-height: 1.45;
    }}
    
    /* Team Member Badges on About Page */
    .member-badge {{
        background-color: {palette["bg_surface"]};
        border: 1px solid {palette["border"]};
        border-radius: 6px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
        min-width: 220px;
    }}

    /* High-Contrast Inputs & Dataframes */
    label, [data-testid="stWidgetLabel"] p {{
        color: {palette["text_primary"]} !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
    }}
    
    [data-testid="stExpander"] summary {{
        color: {palette["text_primary"]} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
        background-color: {palette["bg_surface"]} !important;
        color: {palette["text_primary"]} !important;
        border: 1px solid {palette["border"]} !important;
    }}
    
    button[data-baseweb="tab"] {{
        color: {palette["text_secondary"]} !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 5px 12px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {palette["text_primary"]} !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #4E79A7 !important;
    }}
    
    .stButton>button, .stDownloadButton>button {{
        background-color: {palette["bg_card"]} !important;
        color: {palette["text_primary"]} !important;
        border: 1px solid {palette["border"]} !important;
        border-radius: 6px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 5px 12px !important;
        transition: transform 0.15s ease, border-color 0.15s ease !important;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{
        border-color: #4E79A7 !important;
        transform: translateY(-1px);
    }}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)


# Plot Theme Formatter: Clean High-Contrast Monochrome Background with Coordinated Chart Elements
def apply_plot_theme(fig, ax, theme):
    c = get_theme_colors(theme)
    fig.patch.set_facecolor(c["plot_bg"])
    ax.set_facecolor(c["plot_bg"])
    ax.tick_params(colors=c["plot_text"], labelsize=8)
    ax.xaxis.label.set_color(c["plot_text"])
    ax.yaxis.label.set_color(c["plot_text"])
    ax.xaxis.label.set_size(8.5)
    ax.yaxis.label.set_size(8.5)
    ax.title.set_color(c["text_primary"])
    ax.title.set_size(9.8)
    ax.title.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_color(c["plot_spine"])
        spine.set_linewidth(0.8)
    ax.grid(color=c["plot_grid"], linestyle="--", linewidth=0.6, alpha=0.8)


# Data Loading Utility with Multi-path Support & Caching
@st.cache_data
def load_data():
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), "StudentsPerformance.csv"),
        os.path.join(os.path.dirname(__file__), "cleaned_student_performance.csv"),
        "StudentsPerformance.csv",
        "cleaned_student_performance.csv",
        os.path.join("VSEC-project", "StudentsPerformance.csv"),
        os.path.join("..", "StudentsPerformance.csv")
    ]
    
    file_path = None
    for path in candidate_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if file_path is None:
        st.error("Error: Could not locate 'StudentsPerformance.csv'. Please ensure the dataset file is present.")
        return pd.DataFrame()
        
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    if "average score" not in df.columns:
        df["average score"] = np.round((df["math score"] + df["reading score"] + df["writing score"]) / 3.0, 2)
    
    def assign_grade(score):
        if score >= 90: return "A+ (90-100)"
        elif score >= 80: return "A (80-89)"
        elif score >= 70: return "B (70-79)"
        elif score >= 60: return "C (60-69)"
        elif score >= 40: return "D (40-59)"
        else: return "F (<40)"
        
    df["grade"] = df["average score"].apply(assign_grade)
    df["status"] = df["average score"].apply(lambda s: "Pass" if s >= 40 else "Fail")
    
    return df

df = load_data()

if df.empty:
    st.stop()


# Sidebar: Compact Stationary Sidebar with Branding, Theme Toggle, Navigation, and Left-Side Team Badge
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">🎓</div>
        <div class="brand-text-box">
            <div class="brand-title">Student Performance</div>
            <div class="brand-subtitle">Scientific Computing Analysis (VSEC)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme Mode Selector (Segmented Pill)
    selected_theme = st.radio(
        "Theme Selector",
        options=["Dark", "Light"],
        index=0 if st.session_state["theme"] == "Dark" else 1,
        format_func=lambda t: "🌙 Dark" if t == "Dark" else "☀️ Light",
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected_theme != st.session_state["theme"]:
        st.session_state["theme"] = selected_theme
        st.rerun()

    # Subtle Divider
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Navigation Sections
    page = st.radio(
        "Navigation Sections",
        [
            "📊 Overview",
            "📈 Analysis",
            "🗂️ Student Dataset",
            "💡 Insights",
            "ℹ️ About"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Team Names Pinned on Left Side (Always stationary, visible across all pages)
    render_html(f"""
    <div class="sidebar-team-box">
        <div class="team-header-tag">Project Team</div>
        <div class="team-member-item">
            <div class="member-avatar">👨‍💻</div>
            <div>
                <div class="team-member-name">Onkar Pawar</div>
                <div class="team-member-sub">Second Year B.Tech</div>
            </div>
        </div>
        <div class="team-member-item">
            <div class="member-avatar">👨‍💻</div>
            <div>
                <div class="team-member-name">Pratik Shendage</div>
                <div class="team-member-sub">Second Year B.Tech</div>
            </div>
        </div>
        <div class="team-academic-info">Academic Year: 2026–2027</div>
        <div class="team-subject-info">Scientific Computing with Python (VSEC)</div>
    </div>
    """)


# SECTION 1: OVERVIEW
if page == "📊 Overview":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Executive Overview</h1>
        <p class="header-desc">Examination score aggregates and summary statistics computed dynamically from student records.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Actual dynamic calculations from real dataset
    total_students = len(df)
    avg_math = float(np.mean(df["math score"].to_numpy()))
    avg_reading = float(np.mean(df["reading score"].to_numpy()))
    avg_writing = float(np.mean(df["writing score"].to_numpy()))
    avg_overall = float(np.mean(df["average score"].to_numpy()))
    pass_rate = (len(df[df["status"] == "Pass"]) / total_students) * 100.0

    # Compact Responsive KPI Row (5 columns)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Total Students</span>
                <span class="metric-icon">👥</span>
            </div>
            <div class="metric-value">{total_students:,}</div>
            <div class="metric-subtitle">Complete records</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Mathematics Avg</span>
                <span class="metric-icon">📐</span>
            </div>
            <div class="metric-value">{avg_math:.2f}</div>
            <div class="metric-subtitle">Std: {df['math score'].std():.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Reading Avg</span>
                <span class="metric-icon">📖</span>
            </div>
            <div class="metric-value">{avg_reading:.2f}</div>
            <div class="metric-subtitle">Std: {df['reading score'].std():.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Writing Avg</span>
                <span class="metric-icon">✍️</span>
            </div>
            <div class="metric-value">{avg_writing:.2f}</div>
            <div class="metric-subtitle">Std: {df['writing score'].std():.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">Overall Pass Rate</span>
                <span class="metric-icon">🎓</span>
            </div>
            <div class="metric-value">{pass_rate:.1f}%</div>
            <div class="metric-subtitle">&ge; 40 Marks benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    # 2-Column Grid: Subject Comparison Bar Chart + Grade Distribution
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"<div style='font-size: 0.92rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>Subject Average Comparison</div>", unsafe_allow_html=True)
        subjects = ["Math", "Reading", "Writing"]
        averages = [avg_math, avg_reading, avg_writing]
        bar_colors = [palette["math_color"], palette["reading_color"], palette["writing_color"]]
        
        fig, ax = plt.subplots(figsize=(6, 2.7), dpi=140)
        bars = ax.bar(subjects, averages, color=bar_colors, width=0.40, edgecolor=palette["plot_spine"], linewidth=0.8)
        
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.2f}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=palette["plot_text"])
                        
        ax.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
        ax.set_ylim(0, 100)
        apply_plot_theme(fig, ax, current_theme)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_right:
        st.markdown(f"<div style='font-size: 0.92rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>Academic Grade Distribution</div>", unsafe_allow_html=True)
        grade_order = ["A+ (90-100)", "A (80-89)", "B (70-79)", "C (60-69)", "D (40-59)", "F (<40)"]
        grade_counts = df["grade"].value_counts().reindex(grade_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(6, 2.7), dpi=140)
        bars = ax.bar(grade_counts.index, grade_counts.values, color=palette["grade_colors"], width=0.52, edgecolor=palette["plot_spine"], linewidth=0.8)
        
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{int(h)}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=palette["plot_text"])
                        
        ax.set_ylabel("Students", fontsize=8.5, color=palette["plot_text"])
        ax.set_xticklabels(["A+", "A", "B", "C", "D", "F"], fontsize=8.5, color=palette["plot_text"])
        apply_plot_theme(fig, ax, current_theme)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Descriptive Statistics Table
    st.markdown(f"<div style='font-size: 0.92rem; font-weight: 600; color: {palette['text_primary']}; margin: 8px 0 4px 0;'>Descriptive Statistics</div>", unsafe_allow_html=True)
    desc_df = df[["math score", "reading score", "writing score", "average score"]].describe().T
    desc_df = desc_df.rename(columns={
        "count": "Count",
        "mean": "Mean",
        "std": "Std Dev",
        "min": "Min",
        "25%": "25th Pct",
        "50%": "Median",
        "75%": "75th Pct",
        "max": "Max"
    })
    st.dataframe(desc_df.style.format("{:.2f}"), use_container_width=True)

    # Performance Highlights Compact Row
    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 4px; color: {palette['text_primary']};">Top Performers</div>
            <div style="font-size: 0.80rem; line-height: 1.5; color: {palette['text_secondary']};">
                • Perfect 100 in Math: <b>{len(df[df['math score'] == 100])}</b><br>
                • Perfect 100 in Reading: <b>{len(df[df['reading score'] == 100])}</b><br>
                • Perfect 100 in Writing: <b>{len(df[df['writing score'] == 100])}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        prep_avg = df[df["test preparation course"] == "completed"]["average score"].mean()
        none_avg = df[df["test preparation course"] == "none"]["average score"].mean()
        st.markdown(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 4px; color: {palette['text_primary']};">Test Prep Course Advantage</div>
            <div style="font-size: 0.80rem; line-height: 1.5; color: {palette['text_secondary']};">
                • Course Completed Avg: <b>{prep_avg:.2f}</b><br>
                • No Preparation Avg: <b>{none_avg:.2f}</b><br>
                • Net Lift: <b>+{prep_avg - none_avg:.2f} Points</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h3:
        r_rw = df["reading score"].corr(df["writing score"])
        r_mr = df["math score"].corr(df["reading score"])
        st.markdown(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 4px; color: {palette['text_primary']};">Correlation Synergy</div>
            <div style="font-size: 0.80rem; line-height: 1.5; color: {palette['text_secondary']};">
                • Reading & Writing: <b>r = {r_rw:.3f}</b><br>
                • Math & Reading: <b>r = {r_mr:.3f}</b><br>
                • Math & Writing: <b>r = {df['math score'].corr(df['writing score']):.3f}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)


# SECTION 2: ANALYSIS
elif page == "📈 Analysis":
    render_html(f"""
    <div class="header-container">
        <h1 class="header-title">Exploratory Visual Analysis</h1>
        <p class="header-desc">Distributions, correlation heatmaps, test preparation comparisons, and demographic breakdowns.</p>
    </div>
    """)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Score Distribution",
        "Correlation Heatmap",
        "Test Preparation Course",
        "Demographic Factors"
    ])
    
    # TAB 1: Distribution Analysis (Histogram + KDE Density Curve)
    with tab1:
        render_html(f"""
        <div style='font-size: 0.90rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 6px;'>
            Subject Score Distribution & Density (Histogram + KDE)
        </div>
        """)
        
        dist_mode = st.radio(
            "Distribution View Mode:",
            ["Single Subject (Interactive Histogram + KDE)", "All 3 Subjects Side-by-Side Comparison"],
            horizontal=True
        )
        
        if dist_mode == "Single Subject (Interactive Histogram + KDE)":
            c_sub, c_bins = st.columns([2, 1])
            with c_sub:
                selected_subject = st.selectbox(
                    "Subject to Visualize:",
                    ["math score", "reading score", "writing score", "average score"],
                    index=0
                )
            with c_bins:
                num_bins = st.slider("Bins Count:", min_value=5, max_value=30, value=10, step=1)
                
            color_map = {
                "math score": palette["math_color"],
                "reading score": palette["reading_color"],
                "writing score": palette["writing_color"],
                "average score": palette["overall_color"]
            }
            hist_color = color_map.get(selected_subject, palette["math_color"])
            
            fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=140)
            sns.histplot(
                data=df,
                x=selected_subject,
                bins=num_bins,
                kde=True,
                color=hist_color,
                ax=ax,
                edgecolor=palette["plot_spine"],
                linewidth=0.8
            )
            mean_val = df[selected_subject].mean()
            median_val = df[selected_subject].median()
            ax.axvline(mean_val, color=palette["amber_color"], linestyle="--", linewidth=1.2, label=f"Mean: {mean_val:.2f}")
            ax.axvline(median_val, color=palette["writing_color"], linestyle=":", linewidth=1.2, label=f"Median: {median_val:.2f}")
            
            # Title matching original notebook cell 18
            subj_title = "Mathematics Scores" if selected_subject == "math score" else selected_subject.title()
            ax.set_title(f"Distribution of {subj_title}", fontsize=9.5, fontweight='bold', pad=8, color=palette["text_primary"])
            ax.set_xlabel(f"{selected_subject.title()} (Marks)", fontsize=8.5, color=palette["plot_text"])
            ax.set_ylabel("Number of students", fontsize=8.5, color=palette["plot_text"])
            
            legend = ax.legend(frameon=True, fontsize=8)
            if legend:
                legend.get_frame().set_facecolor(palette["plot_bg"])
                legend.get_frame().set_edgecolor(palette["plot_spine"])
                for text in legend.get_texts():
                    text.set_color(palette["plot_text"])
                    
            apply_plot_theme(fig, ax, current_theme)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            render_html(f"""
            <div class="info-card">
                <b>Histogram & KDE Analysis:</b> The histogram bars depict frequency counts across {num_bins} score bins, while the overlaid KDE density curve models the underlying continuous distribution. Scores for <b>{selected_subject}</b> center around a mean of <b>{mean_val:.2f}</b> and median of <b>{median_val:.2f}</b>.
            </div>
            """)
        else:
            # All 3 Subjects Side-by-Side Comparison
            fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.2), dpi=140)
            subj_list = [
                ("math score", "Mathematics Scores", palette["math_color"]),
                ("reading score", "Reading Scores", palette["reading_color"]),
                ("writing score", "Writing Scores", palette["writing_color"])
            ]
            
            for ax, (col_name, title_text, col_color) in zip(axes, subj_list):
                sns.histplot(
                    data=df,
                    x=col_name,
                    bins=10,
                    kde=True,
                    color=col_color,
                    ax=ax,
                    edgecolor=palette["plot_spine"],
                    linewidth=0.8
                )
                m_val = df[col_name].mean()
                ax.axvline(m_val, color=palette["amber_color"], linestyle="--", linewidth=1.2, label=f"Mean: {m_val:.1f}")
                ax.set_title(f"Distribution of {title_text}", fontsize=8.5, fontweight='bold', color=palette["text_primary"])
                ax.set_xlabel(f"{col_name.title()} (Marks)", fontsize=7.8, color=palette["plot_text"])
                ax.set_ylabel("Number of students", fontsize=7.8, color=palette["plot_text"])
                legend = ax.legend(frameon=True, fontsize=7.5)
                if legend:
                    legend.get_frame().set_facecolor(palette["plot_bg"])
                    legend.get_frame().set_edgecolor(palette["plot_spine"])
                    for text in legend.get_texts():
                        text.set_color(palette["plot_text"])
                apply_plot_theme(fig, ax, current_theme)
                
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
            render_html(f"""
            <div class="info-card">
                <b>Tri-Subject Distribution Comparison:</b> Comparative histogram view highlighting Reading's highest central mean (69.17) and Math's broader standard deviation (15.16) compared to Writing (68.05).
            </div>
            """)

    # TAB 2: Correlation Heatmap
    with tab2:
        render_html(f"""
        <div style='font-size: 0.90rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 6px;'>
            Correlation Between Subject Scores (Heatmap)
        </div>
        """)
        
        col_h_ctrl, _ = st.columns([2, 3])
        with col_h_ctrl:
            cmap_choice = st.radio(
                "Heatmap Color Scale:",
                ["Viridis (Original Notebook)", "Theme Coordinated"],
                horizontal=True
            )
            
        selected_cmap = "viridis" if "Viridis" in cmap_choice else ("Blues" if current_theme == "Light" else "mako")
        
        col_h, col_h_info = st.columns([3, 2])
        scores_df = df[["math score", "reading score", "writing score"]]
        corr_matrix = scores_df.corr()
        
        with col_h:
            fig, ax = plt.subplots(figsize=(5.4, 3.4), dpi=140)
            sns.heatmap(
                corr_matrix,
                annot=True,
                fmt=".3f" if "Viridis" in cmap_choice else ".3f",
                cmap=selected_cmap,
                vmin=-1.0,
                vmax=1.0,
                ax=ax,
                cbar_kws={'label': 'Pearson r'},
                linewidths=1.0,
                linecolor=palette["plot_spine"],
                annot_kws={"fontsize": 9.5, "fontweight": "bold"}
            )
            ax.set_title("Correlation Between Subject Scores", fontsize=9.8, fontweight='bold', pad=8, color=palette["text_primary"])
            ax.set_xticklabels(["Math", "Reading", "Writing"], fontsize=8.5, color=palette["plot_text"])
            ax.set_yticklabels(["Math", "Reading", "Writing"], fontsize=8.5, color=palette["plot_text"], rotation=0)
            apply_plot_theme(fig, ax, current_theme)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
        with col_h_info:
            r_rw = df['reading score'].corr(df['writing score'])
            r_mr = df['math score'].corr(df['reading score'])
            r_mw = df['math score'].corr(df['writing score'])
            render_html(f"""
            <div class="panel-box">
                <div style="font-weight: 700; font-size: 0.88rem; margin-bottom: 6px; color: {palette['text_primary']};">Correlation Takeaways</div>
                <div style="font-size: 0.82rem; line-height: 1.6; color: {palette['text_secondary']};">
                    • <b>Reading & Writing (r = {r_rw:.3f}):</b>
                    Near-perfect linear correlation. Demonstrates literacy and language skills transfer seamlessly between reading comprehension and written synthesis.<br><br>
                    • <b>Reading & Math (r = {r_mr:.3f}):</b>
                    Strong positive association. Indicates linguistic comprehension is critical for processing mathematical word problems and contextual reasoning.<br><br>
                    • <b>Writing & Math (r = {r_mw:.3f}):</b>
                    High positive correlation reflecting uniform student diligence across quantitative and qualitative domains.
                </div>
            </div>
            """)

    # TAB 3: Test Preparation Course Comparison
    with tab3:
        render_html(f"""
        <div style='font-size: 0.90rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 6px;'>
            Average Scores by Test Preparation Course
        </div>
        """)
        prep_analysis = df.groupby("test preparation course")[["math score", "reading score", "writing score"]].mean()
        
        c_p1, c_p2 = st.columns([3, 2])
        with c_p1:
            fig, ax = plt.subplots(figsize=(6.0, 3.2), dpi=140)
            x = np.arange(len(prep_analysis.index))
            width = 0.22
            
            b1 = ax.bar(x - width, prep_analysis["math score"], width, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
            b2 = ax.bar(x, prep_analysis["reading score"], width, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
            b3 = ax.bar(x + width, prep_analysis["writing score"], width, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
            
            for bars in [b1, b2, b3]:
                for bar in bars:
                    h = bar.get_height()
                    ax.annotate(f"{h:.1f}",
                                xy=(bar.get_x() + bar.get_width() / 2, h),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=palette["plot_text"])
                                
            ax.set_title("Average Scores by Test Preparation Course", fontsize=9.5, fontweight='bold', pad=8, color=palette["text_primary"])
            ax.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
            ax.set_xlabel("Test Preparation Course", fontsize=8.5, color=palette["plot_text"])
            ax.set_xticks(x)
            ax.set_xticklabels([idx.title() for idx in prep_analysis.index], fontsize=8.5, color=palette["plot_text"])
            ax.set_ylim(0, 100)
            
            legend = ax.legend(title="Subject", frameon=True, fontsize=8)
            if legend:
                legend.get_frame().set_facecolor(palette["plot_bg"])
                legend.get_frame().set_edgecolor(palette["plot_spine"])
                legend.get_title().set_color(palette["plot_text"])
                for text in legend.get_texts():
                    text.set_color(palette["plot_text"])
                    
            apply_plot_theme(fig, ax, current_theme)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
        with c_p2:
            render_html(f"""
            <div style='font-size: 0.85rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>
                Summary Group Table
            </div>
            """)
            st.dataframe(prep_analysis.style.format("{:.2f}"), use_container_width=True)
            
            delta_math = prep_analysis.loc["completed", "math score"] - prep_analysis.loc["none", "math score"]
            delta_reading = prep_analysis.loc["completed", "reading score"] - prep_analysis.loc["none", "reading score"]
            delta_writing = prep_analysis.loc["completed", "writing score"] - prep_analysis.loc["none", "writing score"]
            delta_overall = (delta_math + delta_reading + delta_writing) / 3.0
            
            render_html(f"""
            <div class="panel-box">
                <div style="font-weight: 700; font-size: 0.84rem; margin-bottom: 4px; color: {palette['text_primary']};">
                    Course Advantage (Completed vs None)
                </div>
                <div style="font-size: 0.80rem; line-height: 1.55; color: {palette['text_secondary']};">
                    • <b>Writing Advantage:</b> +{delta_writing:.2f} pts (Largest gain)<br>
                    • <b>Reading Advantage:</b> +{delta_reading:.2f} pts<br>
                    • <b>Math Advantage:</b> +{delta_math:.2f} pts<br>
                    • <b>Net Composite Lift:</b> +{delta_overall:.2f} pts overall average
                </div>
            </div>
            """)

    # TAB 4: Demographic Factors Comparison (Parental Education, Lunch Program, Gender)
    with tab4:
        render_html(f"""
        <div style='font-size: 0.90rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 6px;'>
            Demographic Performance Comparison (Parental Education, Lunch Program & Gender)
        </div>
        """)
        
        demo_view = st.radio(
            "Select Demographic Visualization:",
            ["All 3 Comparisons (Comprehensive View)", "Parental Level of Education", "Lunch Program Impact", "Gender Performance"],
            horizontal=True
        )
        
        edu_order = ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
        edu_grouped = df.groupby("parental level of education")[["math score", "reading score", "writing score", "average score"]].mean().reindex(edu_order)
        lunch_grouped = df.groupby("lunch")[["math score", "reading score", "writing score", "average score"]].mean()
        gender_grouped = df.groupby("gender")[["math score", "reading score", "writing score", "average score"]].mean()
        
        if demo_view == "All 3 Comparisons (Comprehensive View)":
            # 1. Parental Education Multi-Bar Comparison
            st.markdown(f"<div style='font-size: 0.84rem; font-weight: 600; color: {palette['text_primary']}; margin-top: 4px;'>1. Parental Level of Education Score Comparison</div>", unsafe_allow_html=True)
            fig_e, ax_e = plt.subplots(figsize=(10.5, 3.2), dpi=140)
            xe = np.arange(len(edu_grouped.index))
            we = 0.25
            ax_e.bar(xe - we, edu_grouped["math score"], we, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
            ax_e.bar(xe, edu_grouped["reading score"], we, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
            ax_e.bar(xe + we, edu_grouped["writing score"], we, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
            ax_e.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
            ax_e.set_xticks(xe)
            ax_e.set_xticklabels([lbl.title() for lbl in edu_grouped.index], fontsize=8, color=palette["plot_text"])
            ax_e.set_ylim(0, 100)
            leg_e = ax_e.legend(title="Subject", frameon=True, fontsize=8)
            if leg_e:
                leg_e.get_frame().set_facecolor(palette["plot_bg"])
                leg_e.get_frame().set_edgecolor(palette["plot_spine"])
                leg_e.get_title().set_color(palette["plot_text"])
                for text in leg_e.get_texts():
                    text.set_color(palette["plot_text"])
            apply_plot_theme(fig_e, ax_e, current_theme)
            plt.tight_layout()
            st.pyplot(fig_e)
            plt.close(fig_e)
            
            # 2. Lunch & Gender Side-by-Side
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown(f"<div style='font-size: 0.84rem; font-weight: 600; color: {palette['text_primary']};'>2. Lunch Program Comparison</div>", unsafe_allow_html=True)
                fig_l, ax_l = plt.subplots(figsize=(5.4, 3.0), dpi=140)
                xl = np.arange(len(lunch_grouped.index))
                wl = 0.24
                ax_l.bar(xl - wl, lunch_grouped["math score"], wl, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
                ax_l.bar(xl, lunch_grouped["reading score"], wl, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
                ax_l.bar(xl + wl, lunch_grouped["writing score"], wl, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
                ax_l.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
                ax_l.set_xticks(xl)
                ax_l.set_xticklabels([lbl.title() for lbl in lunch_grouped.index], fontsize=8.5, color=palette["plot_text"])
                ax_l.set_ylim(0, 100)
                leg_l = ax_l.legend(title="Subject", frameon=True, fontsize=7.5)
                if leg_l:
                    leg_l.get_frame().set_facecolor(palette["plot_bg"])
                    leg_l.get_frame().set_edgecolor(palette["plot_spine"])
                    leg_l.get_title().set_color(palette["plot_text"])
                    for text in leg_l.get_texts():
                        text.set_color(palette["plot_text"])
                apply_plot_theme(fig_l, ax_l, current_theme)
                plt.tight_layout()
                st.pyplot(fig_l)
                plt.close(fig_l)
                
            with col_d2:
                st.markdown(f"<div style='font-size: 0.84rem; font-weight: 600; color: {palette['text_primary']};'>3. Gender Performance Comparison</div>", unsafe_allow_html=True)
                fig_g, ax_g = plt.subplots(figsize=(5.4, 3.0), dpi=140)
                xg = np.arange(len(gender_grouped.index))
                wg = 0.24
                ax_g.bar(xg - wg, gender_grouped["math score"], wg, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
                ax_g.bar(xg, gender_grouped["reading score"], wg, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
                ax_g.bar(xg + wg, gender_grouped["writing score"], wg, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
                ax_g.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
                ax_g.set_xticks(xg)
                ax_g.set_xticklabels([lbl.title() for lbl in gender_grouped.index], fontsize=8.5, color=palette["plot_text"])
                ax_g.set_ylim(0, 100)
                leg_g = ax_g.legend(title="Subject", frameon=True, fontsize=7.5)
                if leg_g:
                    leg_g.get_frame().set_facecolor(palette["plot_bg"])
                    leg_g.get_frame().set_edgecolor(palette["plot_spine"])
                    leg_g.get_title().set_color(palette["plot_text"])
                    for text in leg_g.get_texts():
                        text.set_color(palette["plot_text"])
                apply_plot_theme(fig_g, ax_g, current_theme)
                plt.tight_layout()
                st.pyplot(fig_g)
                plt.close(fig_g)
                
        elif demo_view == "Parental Level of Education":
            c_de1, c_de2 = st.columns([3, 2])
            with c_de1:
                fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=140)
                bars = ax.barh([idx.title() for idx in edu_grouped.index], edu_grouped["average score"], color=palette["math_color"], height=0.50, edgecolor=palette["plot_spine"])
                for bar in bars:
                    w = bar.get_width()
                    ax.annotate(f"{w:.2f}",
                                xy=(w, bar.get_y() + bar.get_height() / 2),
                                xytext=(4, 0),
                                textcoords="offset points",
                                ha='left', va='center', fontsize=8, fontweight='bold', color=palette["plot_text"])
                ax.set_title("Average Score by Parental Education", fontsize=9.5, fontweight='bold', color=palette["text_primary"])
                ax.set_xlabel("Overall Average Marks", fontsize=8.5, color=palette["plot_text"])
                ax.set_xlim(0, 100)
                apply_plot_theme(fig, ax, current_theme)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with c_de2:
                st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>Parental Education Group Means</div>", unsafe_allow_html=True)
                st.dataframe(edu_grouped.style.format("{:.2f}"), use_container_width=True)
                
        elif demo_view == "Lunch Program Impact":
            c_dl1, c_dl2 = st.columns([3, 2])
            with c_dl1:
                fig, ax = plt.subplots(figsize=(5.8, 3.0), dpi=140)
                xl = np.arange(len(lunch_grouped.index))
                wl = 0.22
                b1 = ax.bar(xl - wl, lunch_grouped["math score"], wl, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
                b2 = ax.bar(xl, lunch_grouped["reading score"], wl, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
                b3 = ax.bar(xl + wl, lunch_grouped["writing score"], wl, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
                for bars in [b1, b2, b3]:
                    for bar in bars:
                        h = bar.get_height()
                        ax.annotate(f"{h:.1f}",
                                    xy=(bar.get_x() + bar.get_width() / 2, h),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=palette["plot_text"])
                ax.set_title("Lunch Program Performance Comparison", fontsize=9.5, fontweight='bold', color=palette["text_primary"])
                ax.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
                ax.set_xticks(xl)
                ax.set_xticklabels([lbl.title() for lbl in lunch_grouped.index], fontsize=8.5, color=palette["plot_text"])
                ax.set_ylim(0, 100)
                leg = ax.legend(title="Subject", frameon=True, fontsize=8)
                if leg:
                    leg.get_frame().set_facecolor(palette["plot_bg"])
                    leg.get_frame().set_edgecolor(palette["plot_spine"])
                    leg.get_title().set_color(palette["plot_text"])
                    for text in leg.get_texts():
                        text.set_color(palette["plot_text"])
                apply_plot_theme(fig, ax, current_theme)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with c_dl2:
                st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>Lunch Program Group Means</div>", unsafe_allow_html=True)
                st.dataframe(lunch_grouped.style.format("{:.2f}"), use_container_width=True)
                
        elif demo_view == "Gender Performance":
            c_dg1, c_dg2 = st.columns([3, 2])
            with c_dg1:
                fig, ax = plt.subplots(figsize=(5.8, 3.0), dpi=140)
                xg = np.arange(len(gender_grouped.index))
                wg = 0.22
                b1 = ax.bar(xg - wg, gender_grouped["math score"], wg, label="Math", color=palette["math_color"], edgecolor=palette["plot_spine"])
                b2 = ax.bar(xg, gender_grouped["reading score"], wg, label="Reading", color=palette["reading_color"], edgecolor=palette["plot_spine"])
                b3 = ax.bar(xg + wg, gender_grouped["writing score"], wg, label="Writing", color=palette["writing_color"], edgecolor=palette["plot_spine"])
                for bars in [b1, b2, b3]:
                    for bar in bars:
                        h = bar.get_height()
                        ax.annotate(f"{h:.1f}",
                                    xy=(bar.get_x() + bar.get_width() / 2, h),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom', fontsize=7.8, fontweight='bold', color=palette["plot_text"])
                ax.set_title("Gender Performance Comparison", fontsize=9.5, fontweight='bold', color=palette["text_primary"])
                ax.set_ylabel("Average Marks", fontsize=8.5, color=palette["plot_text"])
                ax.set_xticks(xg)
                ax.set_xticklabels([lbl.title() for lbl in gender_grouped.index], fontsize=8.5, color=palette["plot_text"])
                ax.set_ylim(0, 100)
                leg = ax.legend(title="Subject", frameon=True, fontsize=8)
                if leg:
                    leg.get_frame().set_facecolor(palette["plot_bg"])
                    leg.get_frame().set_edgecolor(palette["plot_spine"])
                    leg.get_title().set_color(palette["plot_text"])
                    for text in leg.get_texts():
                        text.set_color(palette["plot_text"])
                apply_plot_theme(fig, ax, current_theme)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with c_dg2:
                st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: {palette['text_primary']}; margin-bottom: 4px;'>Gender Group Means</div>", unsafe_allow_html=True)
                st.dataframe(gender_grouped.style.format("{:.2f}"), use_container_width=True)


# SECTION 3: STUDENT DATASET
elif page == "🗂️ Student Dataset":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Student Dataset Explorer</h1>
        <p class="header-desc">Search, filter, and export individual student exam records with responsive cohort selectors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Grid: 4 columns
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        gender_filter = st.multiselect("Gender", options=df["gender"].unique(), default=df["gender"].unique())
        lunch_filter = st.multiselect("Lunch Type", options=df["lunch"].unique(), default=df["lunch"].unique())
    with f2:
        prep_filter = st.multiselect("Test Prep", options=df["test preparation course"].unique(), default=df["test preparation course"].unique())
        status_filter = st.multiselect("Pass/Fail Status", options=["Pass", "Fail"], default=["Pass", "Fail"])
    with f3:
        race_filter = st.multiselect("Race / Group", options=df["race/ethnicity"].unique(), default=df["race/ethnicity"].unique())
        edu_filter = st.multiselect("Parental Education", options=df["parental level of education"].unique(), default=df["parental level of education"].unique())
    with f4:
        score_range = st.slider("Score Range:", min_value=0.0, max_value=100.0, value=(0.0, 100.0), step=1.0)
        search_query = st.text_input("Search (keyword):", placeholder="e.g. bachelor, standard")

    # Filter application
    filtered_df = df[
        (df["gender"].isin(gender_filter)) &
        (df["lunch"].isin(lunch_filter)) &
        (df["test preparation course"].isin(prep_filter)) &
        (df["status"].isin(status_filter)) &
        (df["race/ethnicity"].isin(race_filter)) &
        (df["parental level of education"].isin(edu_filter)) &
        (df["average score"] >= score_range[0]) &
        (df["average score"] <= score_range[1])
    ]
    
    if search_query:
        mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]
        
    st.markdown(f"<div style='font-size: 0.84rem; margin: 4px 0 8px 0; color: {palette['text_secondary']};'>Showing <b>{len(filtered_df):,}</b> of <b>{len(df):,}</b> student records</div>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        # Quick summary metrics for the filtered subset
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Subset Math", f"{filtered_df['math score'].mean():.2f}")
        m2.metric("Subset Reading", f"{filtered_df['reading score'].mean():.2f}")
        m3.metric("Subset Writing", f"{filtered_df['writing score'].mean():.2f}")
        m4.metric("Subset Overall", f"{filtered_df['average score'].mean():.2f}")
        
        st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True, height=350)
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered CSV",
            data=csv_data,
            file_name="filtered_student_performance.csv",
            mime="text/csv"
        )
    else:
        st.info("No records matched the selected criteria. Try adjusting the filter parameters.")


# SECTION 4: INSIGHTS
elif page == "💡 Insights":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Statistical Insights & Educational Observations</h1>
        <p class="header-desc">Data-supported findings and strategic recommendations synthesized from examination records.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c_left, c_right = st.columns(2)
    with c_left:
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: {palette['text_primary']};">
                1. Subject Performance Hierarchy
            </div>
            <div style="font-size: 0.83rem; line-height: 1.55; color: {palette['text_secondary']};">
                • <b>Reading leads overall marks:</b> Average of <b>69.17</b>, closely followed by Writing at <b>68.05</b>.<br>
                • <b>Mathematics exhibits lowest average:</b> Average of <b>66.09</b> with the highest score volatility (Std Dev: 15.16).
            </div>
        </div>
        """)
        
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: {palette['text_primary']};">
                2. Cross-Disciplinary Synergy
            </div>
            <div style="font-size: 0.83rem; line-height: 1.55; color: {palette['text_secondary']};">
                • <b>Reading & Writing (r = 0.955):</b> Near-perfect linear correlation indicating literacy skills transfer directly between comprehension and composition.<br>
                • <b>Math interdependence (r = 0.818):</b> High correlation with Reading demonstrates reading comprehension is vital for word problems.
            </div>
        </div>
        """)

    with c_right:
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: {palette['text_primary']};">
                3. Test Preparation Impact
            </div>
            <div style="font-size: 0.83rem; line-height: 1.55; color: {palette['text_secondary']};">
                • <b>Systematic lift across all subjects:</b> Course completion raised overall average by <b>+7.63 points</b> (72.67 vs 65.04).<br>
                • <b>Writing gained the most:</b> +9.91 points increase, followed by Reading (+7.36 pts) and Math (+5.62 pts).
            </div>
        </div>
        """)
        
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: {palette['text_primary']};">
                4. Socioeconomic Indicators
            </div>
            <div style="font-size: 0.83rem; line-height: 1.55; color: {palette['text_secondary']};">
                • <b>Nutrition Factor:</b> Standard lunch students averaged <b>70.84</b> vs <b>62.20</b> for free/reduced lunch recipients (8.64 point difference).<br>
                • <b>Parental Education:</b> Master's degree background averaged <b>73.60</b> vs <b>63.10</b> for high school level.
            </div>
        </div>
        """)

    st.markdown(f"<div style='font-size: 0.94rem; font-weight: 700; color: {palette['text_primary']}; margin: 8px 0 6px 0;'>Strategic Recommendations for Educators</div>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="info-card">
            <b>1. Universal Exam Prep</b><br>
            Facilitate accessible test preparation sessions, specifically supporting first-generation college students.
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="info-card">
            <b>2. Math Literacy Integration</b><br>
            Embed linguistic problem-solving modules into math instruction to support word problem comprehension.
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="info-card">
            <b>3. Equity & Mentorship</b><br>
            Offer peer tutoring and academic resources to bridge gaps linked to socioeconomic indicators.
        </div>
        """, unsafe_allow_html=True)


# SECTION 5: ABOUT (High Visibility & Prominent Team Member Names)
elif page == "ℹ️ About":
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">About the Project</h1>
        <p class="header-desc">Academic background, project team members, and technical specifications for the VSEC coursework.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        render_html(f"""
        <div class="panel-box">
            <div style="font-size: 1.05rem; font-weight: 700; color: {palette['text_primary']}; margin-bottom: 10px;">
                👥 Project Team Members
            </div>
            <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
                <div class="member-badge">
                    <span style="font-size: 1.45rem;">👨‍💻</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.05rem; color: {palette['text_primary']};">Onkar Pawar</div>
                        <div style="font-size: 0.82rem; font-weight: 500; color: {palette['text_secondary']};">Second Year B.Tech • Engineering</div>
                    </div>
                </div>
                <div class="member-badge">
                    <span style="font-size: 1.45rem;">👨‍💻</span>
                    <div>
                        <div style="font-weight: 700; font-size: 1.05rem; color: {palette['text_primary']};">Pratik Shendage</div>
                        <div style="font-size: 0.82rem; font-weight: 500; color: {palette['text_secondary']};">Second Year B.Tech • Engineering</div>
                    </div>
                </div>
            </div>
            <div style="font-size: 1.02rem; font-weight: 700; color: {palette['text_primary']}; margin-bottom: 6px;">
                🎓 Academic Information
            </div>
            <div style="font-size: 0.88rem; line-height: 1.8; color: {palette['text_secondary']};">
                • <b>Project Title:</b> <span style="color: {palette['text_primary']}; font-weight: 600;">Student Performance Analysis Using Python</span><br>
                • <b>Subject:</b> <span style="color: {palette['text_primary']}; font-weight: 600;">Scientific Computing with Python (VSEC)</span><br>
                • <b>Class:</b> <span style="color: {palette['text_primary']}; font-weight: 600;">Second Year B.Tech</span><br>
                • <b>Academic Year:</b> <span style="color: {palette['text_primary']}; font-weight: 600;">2026–2027</span>
            </div>
        </div>
        """)
        
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.96rem; margin-bottom: 6px; color: {palette['text_primary']};">
                🎯 Project Objectives
            </div>
            <div style="font-size: 0.85rem; line-height: 1.65; color: {palette['text_secondary']};">
                1. Inspect data quality and check for missing/duplicate records with <b>Pandas</b>.<br>
                2. Execute vector statistics and mean calculations dynamically using <b>NumPy</b>.<br>
                3. Render statistical distributions and correlation matrices with <b>Matplotlib & Seaborn</b>.<br>
                4. Build an interactive, responsive monochrome web dashboard via <b>Streamlit</b>.
            </div>
        </div>
        """)

    with col_a2:
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.96rem; margin-bottom: 6px; color: {palette['text_primary']};">
                🛠️ Technologies Used
            </div>
            <div style="font-size: 0.85rem; line-height: 1.7; color: {palette['text_secondary']};">
                • <b>Python:</b> Core analytical programming language<br>
                • <b>Streamlit:</b> Web application framework<br>
                • <b>Pandas:</b> Data wrangling and grouping<br>
                • <b>NumPy:</b> Vectorized numerical calculations<br>
                • <b>Matplotlib / Seaborn:</b> Statistical plotting
            </div>
        </div>
        """)
        
        render_html(f"""
        <div class="panel-box">
            <div style="font-weight: 700; font-size: 0.96rem; margin-bottom: 6px; color: {palette['text_primary']};">
                📚 Dataset Reference
            </div>
            <div style="font-size: 0.85rem; line-height: 1.7; color: {palette['text_secondary']};">
                • <b>Source:</b> Kaggle — <i>Students Performance in Exams</i><br>
                • <b>Records:</b> 1,000 Students, 8 Columns<br>
                • <b>Dataset Integrity:</b> Actual data verified, 0 nulls, 0 duplicates
            </div>
        </div>
        """)
