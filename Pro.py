import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from data import load_and_merge_data  # adjust to your actual import path

# --- Dynamic Color Function for Completion Rate ---
def get_dynamic_color(value):
    """Return color intensity based on completion %."""
    if value < 30:
        return '#E74C3C'  
    elif 30 <= value < 50:
        return '#F39C12'  
    elif 50 <= value < 75: 
        return "#A3E676"  # yellow-green
    else:
        return '#27AE60'  # dark green


# --- Donut Chart Function ---
def make_donut(value, label, color=None, suffix="%"):
    """Creates a donut chart KPI with centered value and label."""
    if label.lower().startswith("completion"):
        # Dynamic color for completion rate
        color_main = get_dynamic_color(value)
        color_fade = "#D1CAFF"
    else:
        # Use provided static color for delay donut
        color_map = {
            'green': ['#27AE60', '#12783D'],
            'red': ["#E76F3C", "#FAC5FD"]
        }
        colors = color_map.get(color, ['#BDC3C7', '#7F8C8D'])
        color_main, color_fade = colors

    fig = go.Figure(data=[go.Pie(
        values=[value, max(0, 100 - value)],
        hole=0.7,
        marker_colors=[color_main, color_fade],
        textinfo='none'
    )])

    fig.add_annotation(
        text=f"<b>{value:.1f}{suffix}</b>",
        showarrow=False,
        font=dict(size=24, color=color_main)
    )

    fig.update_layout(
        height=180,
        width=180,
        showlegend=False,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    st.markdown(
        f"""
        <div style='text-align:center; color:#ddd; font-weight:600; margin-bottom:-15px; margin-top:10px;'>
            {label}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, use_container_width=False)


# --- Main Page ---
def ProPage():
    st.title("🏗️ Project Overview Dashboard")
    df = load_and_merge_data()

    # --- Clean Dates ---
    for col in ['Start_Date', 'End_Date', 'Est_Start', 'Est_End', 'Act_Start', 'Act_End']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)

    # --- Project Filter ---
    projects = sorted(df['Project_Name'].dropna().unique().tolist())
    selected_project = st.selectbox("📂 Select Project", projects, index=0 if projects else None)
    filtered_df = df[df['Project_Name'] == selected_project].copy()

    if filtered_df.empty:
        st.warning("No data available for the selected project.")
        return

    # --- KPI Calculations ---
    total_tasks = len(filtered_df)
    completed = (filtered_df['Status'].str.lower() == 'completed').sum()
    completion_rate = round((completed / total_tasks) * 100, 1) if total_tasks else 0
    delay_rate = round(filtered_df['Delay_Days'].mean(), 1) if 'Delay_Days' in filtered_df else 0

    # --- Donut KPI Row ---
  
    col1, col2 = st.columns(2)

    with col1:
        make_donut(completion_rate, "Completion Rate", color="green")
    with col2:
        delay_score = min((delay_rate / 10) * 100, 100)
        make_donut(delay_score, f"Avg Delay ({delay_rate} Days)", color="red", suffix="")

    # --- KPI Summary ---
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Total Tasks", total_tasks)
    col2.metric("✅ Completed", completed)
    col3.metric("🚧 In Progress", (filtered_df['Status'].str.lower() == 'in progress').sum())
    col4.metric("🗓️ Planned", (filtered_df['Status'].str.lower() == 'planned').sum())

    # --- Insights ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Pie: Task Status Distribution
    with col1:
        status_counts = filtered_df['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig1 = px.pie(
            status_counts,
            names='Status',
            values='Count',
            title="Task Status Distribution",
            color='Status',
            color_discrete_map={
                'Completed': '#2E86AB',
                'In Progress': '#E9C46A',
                'Planned': '#F4A261',
                'Started': '#2A9D8F'
            },
            hole=0.4
        )
        fig1.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig1, use_container_width=True)

    # Bar: Delay by Department
    with col2:
        if 'Delay_Days' in filtered_df.columns:
            dept_delay = filtered_df.groupby('Department_Name')['Delay_Days'].sum().reset_index()
            fig2 = px.bar(
                dept_delay,
                x='Department_Name',
                y='Delay_Days',
                title="Total Delay by Department",
                color='Department_Name',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig2.update_layout(template="plotly_white", height=400, xaxis_title=None)
            st.plotly_chart(fig2, use_container_width=True)

    # --- Gantt Chart ---
    st.markdown("---")
    st.subheader("📅 Project Timeline (Gantt Chart)")
    gantt_df = filtered_df.dropna(subset=['Start_Date', 'End_Date'])
    gantt_df['Duration'] = (gantt_df['End_Date'] - gantt_df['Start_Date']).dt.days

    fig4 = px.timeline(
        gantt_df,
        x_start='Start_Date',
        x_end='End_Date',
        y='Task_Name',
        color='Status',
        title=f"Timeline – {selected_project}",
        color_discrete_map={
            'Completed': '#2E86AB',
            'In Progress': '#E9C46A',
            'Planned': '#F4A261',
            'Started': '#2A9D8F'
        },
        hover_data=['Department_Name', 'Duration']
    )
    fig4.update_yaxes(autorange="reversed")
    fig4.update_layout(template="plotly_white", height=700, margin=dict(l=100, r=30, t=50, b=50))
    st.plotly_chart(fig4, use_container_width=True)


