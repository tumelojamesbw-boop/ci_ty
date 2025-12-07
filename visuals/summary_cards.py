import streamlit as st

# visuals/summary_cards.py


import streamlit as st

import streamlit as st

def show_summary_cards(df):
    # --- KPIs ---
    total_projects = df['Project_ID'].nunique()
    total_tasks = len(df)
    avg_delay = round(df['Delay_Days'].sum())
    avg_completion = round(df['percent_complete'].mean(), 1)

    # --- Custom CSS for button-like card styling ---
    st.markdown("""
        <style>
        .kpi-container {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }

        .kpi-card {
            flex: 1;
            min-width: 180px;
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1.5px solid rgba(59,130,246,0.6);
            border-radius: 12px;
            padding: 0.9rem 1.2rem;
            box-shadow: 0 2px 8px rgba(59,130,246,0.15);
            text-align: center;
            transition: all 0.25s ease-in-out;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: #60a5fa;
            box-shadow: 0 0 14px rgba(96,165,250,0.4);
            cursor: pointer;
        }

        .kpi-title {
            color: #e2e8f0;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.3rem;
        }

        .kpi-value {
            color: #3b82f6;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0;
        }

        .emoji {
            display: block;
            font-size: 1.4rem;
            margin-bottom: 0.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HTML KPI Layout ---
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <span class="emoji">🧱</span>
                <div class="kpi-title">Total Projects</div>
                <div class="kpi-value">{total_projects}</div>
            </div>
            <div class="kpi-card">
                <span class="emoji">📋</span>
                <div class="kpi-title">Total Tasks</div>
                <div class="kpi-value">{total_tasks}</div>
            </div>
            <div class="kpi-card">
                <span class="emoji">⏱️</span>
                <div class="kpi-title">Avg Delay (Days)</div>
                <div class="kpi-value">{avg_delay}</div>
            </div>
            <div class="kpi-card">
                <span class="emoji">✅</span>
                <div class="kpi-title">Avg % Complete</div>
                <div class="kpi-value">{avg_completion}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
