import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------
# Constants & Config
# ---------------------------
FINAL_PATH = "final_ranked_candidates.csv"
PAPERS_PATH = "phase3/outputs/phase3_papers.csv"
PAGE_TITLE = "NeuroScreen | Alzheimer's Prioritization"
LAYOUT = "wide"

# ---------------------------
# Page Setup & Custom CSS
# ---------------------------
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT, page_icon="🧬")

# Custom CSS for the Futuristic/Dark/Medical Theme
st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Headers - Medical Cyan */
        h1, h2, h3 {
            color: #00E5FF !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }
        
        /* Metric Cards */
        div[data-testid="stMetricValue"] {
            color: #00E5FF;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
        
        /* Custom Cards for Paper Evidence */
        .evidence-card {
            background-color: #1F2937;
            border-left: 4px solid #00E5FF;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .evidence-title {
            color: #E6FFFA;
            font-weight: bold;
            font-size: 1.1em;
        }
        .evidence-meta {
            color: #9CA3AF;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .highlight {
            color: #00E5FF;
            font-weight: bold;
        }
        
        /* DataFrame Styling */
        .dataframe {
            font-family: 'Courier New', monospace;
        }
        
        /* Enlarge Table Font */
        div[data-testid="stDataFrame"] {
            font-size: 1.2rem !important;
        }

        /* --- SIDEBAR NAVIGATION STYLING --- */
        /* Target the Radio Button Text in Sidebar */
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            font-size: 1.35rem !important;
            color: #00E5FF !important; /* Theme Cyan */
            font-weight: 700 !important;
            padding: 10px 0;
        }
        /* Style the radio options container */
        [data-testid="stSidebar"] [data-testid="stRadio"] {
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Data Loading (Cached)
# ---------------------------
@st.cache_data
def load_data():
    """Loads data with error handling for missing files."""
    try:
        if not os.path.exists(FINAL_PATH):
            return pd.DataFrame(), pd.DataFrame()
            
        final_df = pd.read_csv(FINAL_PATH)
        papers_df = pd.read_csv(PAPERS_PATH) if os.path.exists(PAPERS_PATH) else pd.DataFrame()
        return final_df, papers_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# ---------------------------
# SIDEBAR NAVIGATION & CONTROLS
# ---------------------------
with st.sidebar:
    st.title("🎛️ Navigation")
    
    # Page Toggle (Sidebar Radio)
    page_selection = st.radio(
        "Go to", 
        ["🏠 Project Overview", "📊 Analysis Dashboard"], 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Show Controls ONLY if we are on the Dashboard page
    if page_selection == "📊 Analysis Dashboard":
        st.subheader("Filter Candidates")
        top_n = st.slider("Display Top N Candidates", 5, 100, 15)
        min_confidence = st.slider("Min. Confidence Score", 0.0, 1.0, 0.0)
        st.markdown("---")

    st.markdown(" **System Status**")
    st.info("🟢 **ONLINE**")
    st.caption(f"Pipeline: v2.4.0-Beta")
    st.caption(f"Sources: ChEMBL, DisGeNET, EuropePMC")


# ---------------------------
# Global Header
# ---------------------------
st.markdown("""
<div style='margin-bottom: 30px;'>
    <h1 style='font-size: 5rem; margin: 0; color: #00E5FF;'>🧠 NeuroScreen</h1>
    <p style='font-size: 1.2rem; color: #9CA3AF;'>AI-Powered Alzheimer’s Drug Prioritization System</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: PROJECT OVERVIEW (Home)
# ==========================================
if page_selection == "🏠 Project Overview":
    st.markdown("### Accelerating Alzheimer’s Drug Discovery with AI")
    st.divider()

    # The Problem Framing
    col_prob, col_img = st.columns([2, 1])
    with col_prob:
        st.subheader("The Challenge")
        st.markdown("""
        Developing a single Alzheimer’s drug takes **over a decade** and costs **billions of dollars**, yet **99.6% of candidates fail** in human trials. 
        
        The traditional "trial and error" method on animal models is slow, expensive, and often poor at predicting human outcomes. We are facing a crisis in neurodegenerative therapeutics that requires a radically different approach.
        """)
        
        st.info("""
        **FDA Modernization Act 2.0:** New regulations now allow computer models (AI) to replace certain animal testing phases, opening the door for purely computational "Virtual Scientists."
        """)

    with col_img:
        # Metric 1
        st.metric("Avg. Time to Market", "~13 Years")
        st.markdown("""
        <div style="font-size: 0.75em; color: #9CA3AF; margin-bottom: 15px;">
        <em>Cummings, J., Reiber, C., & Kumar, P. (2016). Drug development in Alzheimer’s disease: The path to 2025. Alzheimer’s Research & Therapy, 8, Article 39. https://doi.org/10.1186/s13195-016-0207-9</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Metric 2
        st.metric("Avg. Cost per Drug", "~$5.7 Billion")
        st.markdown("""
        <div style="font-size: 0.75em; color: #9CA3AF; margin-bottom: 15px;">
        <em>Scott, T. J., O'Connor, A. C., Link, A. N., & Beaulieu, T. J. (2014). Economic analysis of opportunities to accelerate Alzheimer's disease research and development. Annals of the New York Academy of Sciences, 1313(1), 17–34. https://doi.org/10.1111/nyas.12417</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Metric 3
        st.metric("Clinical Failure Rate", "99.6%")
        st.markdown("""
        <div style="font-size: 0.75em; color: #9CA3AF; margin-bottom: 15px;">
        <em>Cummings, J. L., Morstorf, T., & Zhong, K. (2014). Alzheimer’s drug-development pipeline: Few candidates, frequent failures. Alzheimer’s Research & Therapy, 6(4), 37. https://doi.org/10.1186/alzrt269</em>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # The Solution (Pipeline)
    st.subheader("ℹ️ Our Solution: The NeuroScreen Pipeline")
    st.markdown("We built an automated pipeline to identify safe, existing drugs that can be repurposed for Alzheimer's.")

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown("""
        <div style="text-align: center; border: 1px solid #30363D; padding: 20px; border-radius: 8px; background-color: #161B22; height: 100%;">
            <div style="font-size: 3em; margin-bottom: 15px;">🛡️</div>
            <h4 style="color: #00E5FF; margin: 0; font-size: 1.2em;">Phase 1</h4>
            <div style="font-weight: bold; color: #FAFAFA; margin-bottom: 5px;">BBB Screening</div>
            <p style="font-size: 0.9em; color: #9CA3AF; margin: 0;">Filters drugs for Blood-Brain Barrier permeability using ML classifiers.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div style="text-align: center; border: 1px solid #30363D; padding: 20px; border-radius: 8px; background-color: #161B22; height: 100%;">
            <div style="font-size: 3em; margin-bottom: 15px;">🧬</div>
            <h4 style="color: #00E5FF; margin: 0; font-size: 1.2em;">Phase 2</h4>
            <div style="font-weight: bold; color: #FAFAFA; margin-bottom: 5px;">Bio-Plausibility</div>
            <p style="font-size: 0.9em; color: #9CA3AF; margin: 0;">Matches drugs to known Alzheimer's targets (e.g., Amyloid, Tau).</p>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div style="text-align: center; border: 1px solid #30363D; padding: 20px; border-radius: 8px; background-color: #161B22; height: 100%;">
            <div style="font-size: 3em; margin-bottom: 15px;">📚</div>
            <h4 style="color: #00E5FF; margin: 0; font-size: 1.2em;">Phase 3</h4>
            <div style="font-weight: bold; color: #FAFAFA; margin-bottom: 5px;">Literature AI</div>
            <p style="font-size: 0.9em; color: #9CA3AF; margin: 0;">Mines thousands of papers for efficacy signals using NLP.</p>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown("""
        <div style="text-align: center; border: 1px solid #00E5FF; padding: 20px; border-radius: 8px; background-color: #1F2937; height: 100%; box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);">
            <div style="font-size: 3em; margin-bottom: 15px;">🏆</div>
            <h4 style="color: #FAFAFA; margin: 0; font-size: 1.2em;">Final Rank</h4>
            <div style="font-weight: bold; color: #00E5FF; margin-bottom: 5px;">Prioritization</div>
            <p style="font-size: 0.9em; color: #D1D5DB; margin: 0;">Aggregates biological & text scores to shortlist candidates.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: ANALYSIS DASHBOARD (The Tool)
# ==========================================
elif page_selection == "📊 Analysis Dashboard":
    final_df, papers_df = load_data()

    col_head_1, col_head_2 = st.columns([3, 1])
    with col_head_1:
        st.markdown("### Real-time Candidate Prioritization")
    
    # --- Data Status Check ---
    if final_df.empty:
        with col_head_2:
            st.metric("Candidates", 0)
        st.warning(f"⚠️ Data Pipeline Output Not Found: `{FINAL_PATH}`")
        st.stop()
    else:
        with col_head_2:
            st.metric("Candidates Screened", len(final_df))

    st.divider()

    # ---------------------------
    # 1. Macro Analysis (Visualization)
    # ---------------------------
    st.subheader("Landscape Analysis")
    st.markdown("Visualizing candidate distribution: **Biological Mechanism** vs. **Literature Evidence**.")

    # Filter data
    filtered_df = final_df[final_df['confidence'] >= min_confidence].copy()

    if not filtered_df.empty:
        fig = px.scatter(
            filtered_df,
            x="phase2_score",
            y="signed_score",
            size="final_score",
            color="final_score",
            hover_name="drug_name",
            hover_data=["models", "n_papers"],
            color_continuous_scale="Teal",
            template="plotly_dark",
            labels={
                "phase2_score": "Mechanism Plausibility (Bio)",
                "signed_score": "Literature Sentiment (Text)",
                "final_score": "Composite Rank"
            },
            title="Candidate Cluster Analysis"
        )
        
        # Customize Layout
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=16, family="Helvetica Neue"),
            title=dict(font=dict(size=24)),
            xaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14)),
            legend=dict(font=dict(size=14))
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No drugs meet the confidence threshold.")

    # ---------------------------
    # 2. Ranked Leaderboard
    # ---------------------------
    st.subheader("🏆 Priority Leaderboard")

    if filtered_df.empty:
        st.info("No candidates match filters.")
    else:
        display_cols = [
            "drug_name", "final_score", "phase2_score", 
            "signed_score", "n_papers", "confidence"
        ]
        
        leaderboard_df = filtered_df[display_cols].head(top_n)
        
        st.dataframe(
            leaderboard_df,
            column_config={
                "drug_name": st.column_config.TextColumn("Candidate Drug", width="medium"),
                "final_score": st.column_config.ProgressColumn(
                    "NeuroScreen Score", format="%.3f", min_value=0, max_value=1
                ),
                "phase2_score": st.column_config.NumberColumn("Bio-Plausibility", format="%.3f"),
                "signed_score": st.column_config.NumberColumn("Lit. Evidence", format="%.2f"),
                "n_papers": st.column_config.NumberColumn("Papers"),
                "confidence": st.column_config.NumberColumn("AI Confidence", format="%.0f%%"),
            },
            use_container_width=True,
            height=500
        )

    # ---------------------------
    # 3. Deep Dive (Drill Down)
    # ---------------------------
    st.markdown("---")
    st.subheader("🔬 Candidate Inspector")

    col_search, col_select = st.columns(2)
    with col_search:
        search_query = st.text_input("🔍 Search Database", placeholder="Type drug name...")

    if search_query:
        dropdown_options = final_df[final_df["drug_name"].str.contains(search_query, case=False, na=False)]
    else:
        dropdown_options = final_df.head(top_n)

    if not dropdown_options.empty:
        selected_drug = st.selectbox("Select Candidate for Analysis", dropdown_options["drug_name"].unique())
        
        drug_row = final_df[final_df["drug_name"] == selected_drug].iloc[0]
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Composite Score", f"{drug_row['final_score']:.3f}")
        with m2:
            st.metric("Bio-Plausibility", f"{drug_row['phase2_score']:.3f}")
        with m3:
            st.metric("Lit. Sentiment", f"{drug_row['signed_score']:.2f}")
        with m4:
            st.metric("Evidence Count", f"{int(drug_row['n_papers'])} Papers")

        with st.expander("📋 Technical Profile", expanded=True):
            st.markdown(f"""
            **Drug Name:** `{selected_drug}`  
            **Biological Models:** `{drug_row['models']}`  
            **Net Evidence Direction:** `{int(drug_row['net_positive'])}` (Positive - Negative mentions)  
            **AI Confidence:** `{drug_row['confidence']:.2f}`
            """)

        st.subheader(f"📄 Evidence Stream: {selected_drug}")
        
        drug_papers = papers_df[papers_df["drug"] == selected_drug]
        
        if drug_papers.empty:
            st.info("No specific literature entries found in the indexed window.")
        else:
            for _, row in drug_papers.head(5).iterrows():
                direction_color = "#00E5FF" if row['direction'] == 'positive' else "#FF5252"
                
                st.markdown(f"""
                <div class="evidence-card" style="border-left: 4px solid {direction_color}">
                    <div class="evidence-title">{row['title']}</div>
                    <div class="evidence-meta">
                        <span class="highlight">{row['pub_year']}</span> | 
                        Model: {row['model']} | 
                        <span style="color:{direction_color}">{row['direction'].upper()}</span>
                    </div>
                    <div style="margin-top:8px; font-size:0.95em; color: #D1D5DB;">
                        <em>"{row['outcomes']}"</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    else:
        st.info("No drugs found matching criteria.")