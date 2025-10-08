
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import uuid
import io
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="Risk Management Comparison Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= ENHANCED CSS STYLING =============
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #dc3545, #ff6b35, #f7931e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
    }

    .sub-header {
        font-size: 1.4rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .session-badge {
        background: linear-gradient(135deg, #dc3545 0%, #ff6b35 100%);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 25px;
        text-align: center;
        font-family: 'Monaco', monospace;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }

    .metric-card-critical {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        transition: transform 0.3s ease;
    }

    .metric-card-success {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        transition: transform 0.3s ease;
    }

    .metric-card-warning {
        background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
        transition: transform 0.3s ease;
    }

    .metric-card-info {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);
        transition: transform 0.3s ease;
    }

    .metric-number {
        font-size: 2.8rem;
        font-weight: bold;
        display: block;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    .success-msg {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #28a745;
        box-shadow: 0 2px 10px rgba(40, 167, 69, 0.1);
    }

    .warning-msg {
        background: linear-gradient(90deg, #fff3cd, #ffeaa7);
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #ffc107;
        box-shadow: 0 2px 10px rgba(255, 193, 7, 0.1);
    }

    .error-msg {
        background: linear-gradient(90deg, #f8d7da, #f1c2c7);
        border: 1px solid #f1c2c7;
        color: #721c24;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #dc3545;
        box-shadow: 0 2px 10px rgba(220, 53, 69, 0.1);
    }

    .info-msg {
        background: linear-gradient(90deg, #cce7f0, #b8daff);
        border: 1px solid #b8daff;
        color: #004085;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 2px 10px rgba(23, 162, 184, 0.1);
    }

    .upload-area {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        border: 3px dashed #dc3545;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .upload-area:hover {
        background: linear-gradient(45deg, #e9ecef, #dee2e6);
        border-color: #c82333;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.1);
    }

    .footer {
        background: linear-gradient(135deg, #343a40 0%, #212529 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.1);
    }

    .sidebar-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .stButton > button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============= SESSION MANAGEMENT =============
def initialize_session():
    """Initialize session dengan unique ID untuk multi-user support"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8].upper()

    # Initialize comparison data containers
    if 'dataset_a' not in st.session_state:
        st.session_state.dataset_a = None
    if 'dataset_b' not in st.session_state:
        st.session_state.dataset_b = None
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    if 'file_a_info' not in st.session_state:
        st.session_state.file_a_info = None
    if 'file_b_info' not in st.session_state:
        st.session_state.file_b_info = None

# ============= DATA COMPARISON FUNCTIONS =============
def validate_dataset_structure(df, filename):
    """Validate if dataset has required risk management columns"""
    required_columns = ['Risk_ID', 'Asset', 'Threat', 'Status', 'Risk_Rating']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, f"Missing required columns in {filename}: {missing_columns}"

    return True, "Valid dataset structure"

def compare_risk_datasets(df_old, df_new, old_name="Previous", new_name="Current"):
    """Compare two risk management datasets and identify changes"""

    # Use Risk_ID as the key for comparison
    if 'Risk_ID' not in df_old.columns or 'Risk_ID' not in df_new.columns:
        return None, "Both datasets must have Risk_ID column"

    # Create comparison results dictionary
    results = {
        'summary': {},
        'new_risks': pd.DataFrame(),
        'resolved_risks': pd.DataFrame(),
        'modified_risks': pd.DataFrame(),
        'unchanged_risks': pd.DataFrame(),
        'status_changes': pd.DataFrame(),
        'rating_changes': pd.DataFrame()
    }

    # Get Risk_IDs from both datasets
    old_ids = set(df_old['Risk_ID'].unique())
    new_ids = set(df_new['Risk_ID'].unique())

    # Identify new, resolved, and common risks
    new_risk_ids = new_ids - old_ids
    resolved_risk_ids = old_ids - new_ids
    common_risk_ids = old_ids & new_ids

    # Get new risks
    if new_risk_ids:
        results['new_risks'] = df_new[df_new['Risk_ID'].isin(new_risk_ids)].copy()

    # Get resolved risks  
    if resolved_risk_ids:
        results['resolved_risks'] = df_old[df_old['Risk_ID'].isin(resolved_risk_ids)].copy()

    # Analyze changes in common risks
    modified_risks = []
    unchanged_risks = []
    status_changes = []
    rating_changes = []

    for risk_id in common_risk_ids:
        old_risk = df_old[df_old['Risk_ID'] == risk_id].iloc[0]
        new_risk = df_new[df_new['Risk_ID'] == risk_id].iloc[0]

        # Check for any changes
        changes = {}
        has_changes = False

        for col in df_old.columns:
            if col in df_new.columns and col != 'Risk_ID':
                old_val = str(old_risk[col])
                new_val = str(new_risk[col])

                if old_val != new_val:
                    changes[col] = {'old': old_val, 'new': new_val}
                    has_changes = True

        if has_changes:
            risk_change = new_risk.to_dict()
            risk_change['changes'] = changes
            modified_risks.append(risk_change)

            # Track specific status changes
            if 'Status' in changes:
                status_changes.append({
                    'Risk_ID': risk_id,
                    'Asset': new_risk.get('Asset', ''),
                    'Threat': new_risk.get('Threat', ''),
                    'Old_Status': changes['Status']['old'],
                    'New_Status': changes['Status']['new'],
                    'Risk_Rating': new_risk.get('Risk_Rating', 0)
                })

            # Track rating changes
            if 'Risk_Rating' in changes:
                try:
                    old_rating = float(changes['Risk_Rating']['old'])
                    new_rating = float(changes['Risk_Rating']['new'])
                    rating_changes.append({
                        'Risk_ID': risk_id,
                        'Asset': new_risk.get('Asset', ''),
                        'Threat': new_risk.get('Threat', ''),
                        'Old_Rating': old_rating,
                        'New_Rating': new_rating,
                        'Rating_Change': new_rating - old_rating,
                        'Status': new_risk.get('Status', '')
                    })
                except:
                    pass
        else:
            unchanged_risks.append(new_risk.to_dict())

    # Convert lists to DataFrames
    if modified_risks:
        # Create a clean DataFrame without the nested changes column for display
        modified_df = pd.DataFrame([{k:v for k,v in risk.items() if k != 'changes'} for risk in modified_risks])
        results['modified_risks'] = modified_df

    if unchanged_risks:
        results['unchanged_risks'] = pd.DataFrame(unchanged_risks)

    if status_changes:
        results['status_changes'] = pd.DataFrame(status_changes)

    if rating_changes:
        results['rating_changes'] = pd.DataFrame(rating_changes)

    # Calculate summary statistics
    results['summary'] = {
        'total_old_risks': len(df_old),
        'total_new_risks': len(df_new),
        'new_risks_count': len(new_risk_ids),
        'resolved_risks_count': len(resolved_risk_ids),
        'modified_risks_count': len(modified_risks),
        'unchanged_risks_count': len(unchanged_risks),
        'status_changes_count': len(status_changes),
        'rating_changes_count': len(rating_changes),
        'comparison_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'old_dataset_name': old_name,
        'new_dataset_name': new_name
    }

    return results, "Comparison completed successfully"

def create_comparison_visualizations(results):
    """Create visualizations for risk comparison results - FIXED VERSION"""

    if not results or 'summary' not in results:
        return []

    figures = []
    summary = results['summary']

    # 1. Overview Summary Chart
    categories = ['New Risks', 'Resolved Risks', 'Modified Risks', 'Unchanged Risks']
    values = [
        summary['new_risks_count'],
        summary['resolved_risks_count'], 
        summary['modified_risks_count'],
        summary['unchanged_risks_count']
    ]
    colors = ['#dc3545', '#28a745', '#ffc107', '#17a2b8']

    fig_overview = px.pie(
        values=values,
        names=categories,
        title="Risk Comparison Overview",
        color_discrete_sequence=colors
    )
    fig_overview.update_layout(
        font=dict(size=14),
        title_font_size=18,
        showlegend=True
    )
    figures.append(('overview', fig_overview))

    # 2. Status Changes Chart
    if not results['status_changes'].empty:
        status_df = results['status_changes']

        # Count status transitions
        status_transitions = status_df.groupby(['Old_Status', 'New_Status']).size().reset_index(name='Count')

        if not status_transitions.empty:
            fig_status = px.bar(
                status_transitions,
                x='Count',
                y=[f"{row['Old_Status']} → {row['New_Status']}" for _, row in status_transitions.iterrows()],
                orientation='h',
                title="Status Changes",
                color='Count',
                color_continuous_scale='Reds'
            )
            fig_status.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=12),
                title_font_size=16
            )
            figures.append(('status_changes', fig_status))

    # 3. Risk Rating Changes Chart - FIXED VERSION
    if not results['rating_changes'].empty:
        rating_df = results['rating_changes']

        # FIX: Use absolute value for size to avoid negative size error
        rating_df_plot = rating_df.copy()
        rating_df_plot['Rating_Change_Abs'] = rating_df_plot['Rating_Change'].abs()

        # Use color for direction instead of problematic size
        rating_df_plot['Change_Direction'] = rating_df_plot['Rating_Change'].apply(
            lambda x: 'Increased' if x > 0 else 'Decreased' if x < 0 else 'No Change'
        )

        fig_rating = px.scatter(
            rating_df_plot,
            x='Old_Rating',
            y='New_Rating',
            size='Rating_Change_Abs',  # Use absolute value for size
            color='Change_Direction',  # Use direction for color
            hover_data=['Risk_ID', 'Asset', 'Threat', 'Rating_Change'],
            title="Risk Rating Changes",
            color_discrete_map={
                'Increased': '#dc3545',    # Red for risk increase
                'Decreased': '#28a745',    # Green for risk decrease  
                'No Change': '#17a2b8'     # Blue for no change
            }
        )

        # Add diagonal line for no change
        max_val = max(rating_df[['Old_Rating', 'New_Rating']].max())
        min_val = min(rating_df[['Old_Rating', 'New_Rating']].min())

        fig_rating.add_shape(
            type="line",
            x0=min_val, y0=min_val,
            x1=max_val, y1=max_val,
            line=dict(color="gray", dash="dash", width=1),
            name="No Change Line"
        )

        fig_rating.update_layout(
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )
        figures.append(('rating_changes', fig_rating))

    return figures

# ============= MAIN STREAMLIT APP =============
def main():
    # Initialize session
    initialize_session()

    # Header
    st.markdown('<h1 class="main-header">📊 Risk Management Comparison Tool</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compare risk assessment datasets and track progress over time</p>', unsafe_allow_html=True)

    # Session badge
    st.markdown(f'<div class="session-badge">🔒 Session: {st.session_state.session_id} | Comparison Ready</div>', unsafe_allow_html=True)

    # Sidebar configuration
    st.sidebar.markdown("### ⚙️ Configuration")
    st.sidebar.markdown('<div class="sidebar-section"><h4>📋 Instructions</h4><p>1. Upload two risk assessment datasets</p><p>2. Review comparison results</p><p>3. Download comparison report</p></div>', unsafe_allow_html=True)

    # Info box about required format
    st.markdown("""
    <div class="info-msg">
    💡 <strong>Required Dataset Format:</strong><br>
    Both files must contain these columns: Risk_ID, Asset, Threat, Status, Risk_Rating<br>
    Additional columns: Cause, Impact, Likelihood, Control, Risk_Owner, Risk_Treatment, Comments
    </div>
    """, unsafe_allow_html=True)

    # File upload section
    st.markdown("## 📤 Upload Risk Assessment Datasets")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📁 Dataset A (Previous/Historical)")
        st.markdown("""
        <div class="upload-area">
            <h4>📅 Upload Previous Dataset</h4>
            <p>e.g., risk_assessment_2024-09-25.csv</p>
        </div>
        """, unsafe_allow_html=True)

        file_a = st.file_uploader(
            "Choose Dataset A",
            type=['csv', 'xlsx'],
            key=f"file_a_{st.session_state.session_id}"
        )

        if file_a:
            try:
                if file_a.name.endswith('.csv'):
                    df_a = pd.read_csv(file_a)
                else:
                    df_a = pd.read_excel(file_a)

                # Validate structure
                is_valid, message = validate_dataset_structure(df_a, file_a.name)

                if is_valid:
                    st.session_state.dataset_a = df_a
                    st.session_state.file_a_info = {
                        'name': file_a.name,
                        'size': f"{file_a.size / 1024:.1f} KB",
                        'rows': len(df_a),
                        'columns': len(df_a.columns)
                    }

                    st.markdown('<div class="success-msg">✅ Dataset A loaded successfully!</div>', unsafe_allow_html=True)

                    # Show dataset info
                    col1_1, col1_2 = st.columns(2)
                    with col1_1:
                        st.markdown(f'<div class="metric-card-info"><span class="metric-number">{len(df_a):,}</span><span class="metric-label">Total Risks</span></div>', unsafe_allow_html=True)
                    with col1_2:
                        open_risks = len(df_a[df_a['Status'] == 'Open']) if 'Status' in df_a.columns else 0
                        st.markdown(f'<div class="metric-card-critical"><span class="metric-number">{open_risks:,}</span><span class="metric-label">Open Risks</span></div>', unsafe_allow_html=True)

                    # Show preview
                    st.markdown("#### 👀 Preview")
                    st.dataframe(df_a.head(3), use_container_width=True)

                else:
                    st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="error-msg">❌ Error loading Dataset A: {str(e)}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📁 Dataset B (Current/Recent)")
        st.markdown("""
        <div class="upload-area">
            <h4>📅 Upload Current Dataset</h4>
            <p>e.g., risk_assessment_2024-09-26.csv</p>
        </div>
        """, unsafe_allow_html=True)

        file_b = st.file_uploader(
            "Choose Dataset B",
            type=['csv', 'xlsx'],
            key=f"file_b_{st.session_state.session_id}"
        )

        if file_b:
            try:
                if file_b.name.endswith('.csv'):
                    df_b = pd.read_csv(file_b)
                else:
                    df_b = pd.read_excel(file_b)

                # Validate structure
                is_valid, message = validate_dataset_structure(df_b, file_b.name)

                if is_valid:
                    st.session_state.dataset_b = df_b
                    st.session_state.file_b_info = {
                        'name': file_b.name,
                        'size': f"{file_b.size / 1024:.1f} KB",
                        'rows': len(df_b),
                        'columns': len(df_b.columns)
                    }

                    st.markdown('<div class="success-msg">✅ Dataset B loaded successfully!</div>', unsafe_allow_html=True)

                    # Show dataset info
                    col2_1, col2_2 = st.columns(2)
                    with col2_1:
                        st.markdown(f'<div class="metric-card-info"><span class="metric-number">{len(df_b):,}</span><span class="metric-label">Total Risks</span></div>', unsafe_allow_html=True)
                    with col2_2:
                        open_risks = len(df_b[df_b['Status'] == 'Open']) if 'Status' in df_b.columns else 0
                        st.markdown(f'<div class="metric-card-critical"><span class="metric-number">{open_risks:,}</span><span class="metric-label">Open Risks</span></div>', unsafe_allow_html=True)

                    # Show preview
                    st.markdown("#### 👀 Preview")
                    st.dataframe(df_b.head(3), use_container_width=True)

                else:
                    st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="error-msg">❌ Error loading Dataset B: {str(e)}</div>', unsafe_allow_html=True)

    # Comparison section
    if st.session_state.dataset_a is not None and st.session_state.dataset_b is not None:
        st.markdown("---")
        st.markdown("## 🔍 Dataset Comparison")

        if st.button("🚀 Compare Datasets", use_container_width=True, key=f"compare_{st.session_state.session_id}"):
            with st.spinner("🔄 Comparing datasets..."):
                results, status_message = compare_risk_datasets(
                    st.session_state.dataset_a, 
                    st.session_state.dataset_b,
                    st.session_state.file_a_info['name'],
                    st.session_state.file_b_info['name']
                )

                if results:
                    st.session_state.comparison_results = results
                    st.markdown('<div class="success-msg">✅ Dataset comparison completed successfully!</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-msg">❌ {status_message}</div>', unsafe_allow_html=True)

    # Display comparison results
    if st.session_state.comparison_results:
        results = st.session_state.comparison_results
        summary = results['summary']

        st.markdown("---")
        st.markdown("## 📈 Comparison Results")

        # Summary metrics
        st.markdown("### 📊 Summary Overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f'<div class="metric-card-critical"><span class="metric-number">{summary["new_risks_count"]}</span><span class="metric-label">New Risks</span></div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div class="metric-card-success"><span class="metric-number">{summary["resolved_risks_count"]}</span><span class="metric-label">Resolved Risks</span></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(f'<div class="metric-card-warning"><span class="metric-number">{summary["modified_risks_count"]}</span><span class="metric-label">Modified Risks</span></div>', unsafe_allow_html=True)

        with col4:
            st.markdown(f'<div class="metric-card-info"><span class="metric-number">{summary["unchanged_risks_count"]}</span><span class="metric-label">Unchanged Risks</span></div>', unsafe_allow_html=True)

        with col5:
            st.markdown(f'<div class="metric-card-warning"><span class="metric-number">{summary["status_changes_count"]}</span><span class="metric-label">Status Changes</span></div>', unsafe_allow_html=True)

        # Detailed analysis tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", "🆕 New Risks", "✅ Resolved Risks", 
            "🔄 Modified Risks", "📈 Status Changes", "💾 Export"
        ])

        with tab1:
            st.markdown("### 📊 Visual Overview")

            # Create and display visualizations
            figures = create_comparison_visualizations(results)

            for fig_name, fig in figures:
                st.plotly_chart(fig, use_container_width=True)

            # Comparison summary table
            st.markdown("### 📋 Comparison Summary")
            summary_data = {
                'Metric': [
                    'Total Risks (Previous)',
                    'Total Risks (Current)', 
                    'New Risks Added',
                    'Risks Resolved',
                    'Risks Modified',
                    'Status Changes',
                    'Rating Changes'
                ],
                'Count': [
                    summary['total_old_risks'],
                    summary['total_new_risks'],
                    summary['new_risks_count'],
                    summary['resolved_risks_count'],
                    summary['modified_risks_count'],
                    summary['status_changes_count'],
                    summary['rating_changes_count']
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)

        with tab2:
            st.markdown("### 🆕 New Risks")

            if not results['new_risks'].empty:
                st.markdown(f"**{len(results['new_risks'])} new risks identified**")
                st.dataframe(results['new_risks'], use_container_width=True)

                # Show risk distribution
                if 'Risk_Rating' in results['new_risks'].columns:
                    fig_new_risks = px.histogram(
                        results['new_risks'],
                        x='Risk_Rating',
                        title="New Risks by Rating",
                        nbins=20,
                        color_discrete_sequence=['#dc3545']
                    )
                    st.plotly_chart(fig_new_risks, use_container_width=True)

            else:
                st.markdown('<div class="info-msg">🎉 No new risks identified!</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown("### ✅ Resolved Risks")

            if not results['resolved_risks'].empty:
                st.markdown(f"**{len(results['resolved_risks'])} risks resolved**")
                st.dataframe(results['resolved_risks'], use_container_width=True)

                # Show resolved risks by asset
                if 'Asset' in results['resolved_risks'].columns:
                    resolved_by_asset = results['resolved_risks']['Asset'].value_counts().head(10)
                    fig_resolved = px.bar(
                        x=resolved_by_asset.values,
                        y=resolved_by_asset.index,
                        orientation='h',
                        title="Resolved Risks by Asset",
                        color_discrete_sequence=['#28a745']
                    )
                    st.plotly_chart(fig_resolved, use_container_width=True)

            else:
                st.markdown('<div class="warning-msg">⚠️ No risks were resolved between datasets.</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown("### 🔄 Modified Risks")

            if not results['modified_risks'].empty:
                st.markdown(f"**{len(results['modified_risks'])} risks modified**")
                st.dataframe(results['modified_risks'], use_container_width=True)
            else:
                st.markdown('<div class="info-msg">ℹ️ No risks were modified between datasets.</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown("### 📈 Status Changes")

            if not results['status_changes'].empty:
                st.markdown(f"**{len(results['status_changes'])} status changes**")
                st.dataframe(results['status_changes'], use_container_width=True)

                # Status change summary
                status_summary = results['status_changes'].groupby(['Old_Status', 'New_Status']).size().reset_index(name='Count')
                st.markdown("#### 📊 Status Transition Summary")
                st.dataframe(status_summary, use_container_width=True)

            else:
                st.markdown('<div class="info-msg">ℹ️ No status changes found between datasets.</div>', unsafe_allow_html=True)

            # Rating changes section
            if not results['rating_changes'].empty:
                st.markdown("### 🎯 Risk Rating Changes")
                st.markdown(f"**{len(results['rating_changes'])} rating changes**")

                # Show rating changes with direction
                rating_df = results['rating_changes'].copy()
                rating_df['Change_Direction'] = rating_df['Rating_Change'].apply(
                    lambda x: '📈 Increased' if x > 0 else '📉 Decreased' if x < 0 else '➖ No Change'
                )

                st.dataframe(rating_df, use_container_width=True)

        with tab6:
            st.markdown("### 💾 Export Comparison Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Export summary to CSV
                summary_export = pd.DataFrame([summary])
                csv_summary = summary_export.to_csv(index=False)

                st.download_button(
                    label="📄 Download Summary (CSV)",
                    data=csv_summary,
                    file_name=f"risk_comparison_summary_{st.session_state.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key=f"summary_download_{st.session_state.session_id}",
                    use_container_width=True
                )

            with col2:
                # Export detailed comparison to Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    # Write each comparison result to different sheets
                    if not results['new_risks'].empty:
                        results['new_risks'].to_excel(writer, sheet_name='New_Risks', index=False)
                    if not results['resolved_risks'].empty:
                        results['resolved_risks'].to_excel(writer, sheet_name='Resolved_Risks', index=False)
                    if not results['modified_risks'].empty:
                        results['modified_risks'].to_excel(writer, sheet_name='Modified_Risks', index=False)
                    if not results['status_changes'].empty:
                        results['status_changes'].to_excel(writer, sheet_name='Status_Changes', index=False)
                    if not results['rating_changes'].empty:
                        results['rating_changes'].to_excel(writer, sheet_name='Rating_Changes', index=False)

                    # Summary sheet
                    pd.DataFrame([summary]).to_excel(writer, sheet_name='Summary', index=False)

                excel_data = output.getvalue()
                st.download_button(
                    label="📊 Download Full Report (Excel)",
                    data=excel_data,
                    file_name=f"risk_comparison_report_{st.session_state.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"excel_download_{st.session_state.session_id}",
                    use_container_width=True
                )

            with col3:
                # Export status changes as JSON
                if not results['status_changes'].empty:
                    json_data = {
                        'comparison_metadata': summary,
                        'status_changes': results['status_changes'].to_dict('records'),
                        'rating_changes': results['rating_changes'].to_dict('records') if not results['rating_changes'].empty else []
                    }

                    st.download_button(
                        label="🔗 Download Changes (JSON)",
                        data=json.dumps(json_data, indent=2, default=str),
                        file_name=f"risk_changes_{st.session_state.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key=f"json_download_{st.session_state.session_id}",
                        use_container_width=True
                    )
                else:
                    st.info("No changes to export as JSON")

    # Footer
    st.markdown("""
    <div class="footer">
        <h3>📊 Risk Management Comparison Tool</h3>
        <p>Created by Vito Devara | Phone: 081259795994</p>
        <p>Professional risk assessment comparison • Session management • Multi-format export</p>
        <p><small>Compare datasets • Track progress • Monitor risk mitigation effectiveness</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
