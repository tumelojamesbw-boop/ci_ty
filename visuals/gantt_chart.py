import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_gantt_chart(df):
    st.subheader("📅 Project Timeline (Gantt Chart)")

    # ---- Filters ----
    col1, col2 = st.columns(2)
    with col1:
        selected_proj = st.selectbox("Filter by Project", ["All"] + sorted(df['Project_Name'].dropna().unique().tolist()))
    with col2:
        selected_dept = st.selectbox("Filter by Department", ["All"] + sorted(df['Department_Name'].dropna().unique().tolist()))

    if selected_proj != "All":
        df = df[df['Project_Name'] == selected_proj]
    if selected_dept != "All":
        df = df[df['Department_Name'] == selected_dept]

    # ---- Validate Columns ----
    required_cols = ['Task_Name', 'Project_Name', 'Department_Name', 'Start_Date', 'End_Date', 'Status']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns for Gantt chart: {', '.join(missing)}")
        return

    # ---- Clean & Format ----
    df['Start_Date'] = pd.to_datetime(df['Start_Date'], errors='coerce')
    df['End_Date'] = pd.to_datetime(df['End_Date'], errors='coerce')
    df = df.dropna(subset=['Start_Date', 'End_Date'])
    df['Duration_Days'] = (df['End_Date'] - df['Start_Date']).dt.days

    if df.empty:
        st.warning("No valid timeline data found for selected filters.")
        return

    # ---- Build Gantt Chart ----
    fig = px.timeline(
        df,
        x_start="Start_Date",
        x_end="End_Date",
        y="Task_Name",
        color="Status",
        hover_data={
            "Project_Name": True,
            "Department_Name": True,
            "Start_Date": True,
            "End_Date": True,
            "Duration_Days": True
        },
        color_discrete_map={
            "Planned": "#F4A261",
            "Started": "#2A9D8F",
            "In Progress": "#E9C46A",
            "Completed": "#2E86AB"
        },
    )

    # ---- Axis Formatting ----
    fig.update_yaxes(
        categoryorder='total ascending',
        title=None,
        showgrid=True,
        gridcolor="lightgray"
    )
    fig.update_xaxes(
        title="Timeline (Weeks)",
        tickformat="%b %d",
        showgrid=True,
        gridcolor="#D3D3D3",
        dtick="W1",
        tickangle=-45
    )

    # ---- Add Milestones ----
    completed = df[df['Status'].str.lower().isin(['completed', 'done', 'finished'])]
    for _, row in completed.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['End_Date']],
            y=[row['Task_Name']],
            mode="markers",
            marker_symbol="diamond",
            marker_size=10,
            marker_color="#264653",
            name="Milestone",
            showlegend=False
        ))

    # ---- Add Phase Bands (Optional, like Excel example) ----
    min_date, max_date = df['Start_Date'].min(), df['End_Date'].max()
    total_days = (max_date - min_date).days
    phase_length = total_days // 4
    colors = ["#D8E2DC", "#FFE5D9", "#FFCAD4", "#F4ACB7"]
    for i in range(4):
        start = min_date + pd.Timedelta(days=i * phase_length)
        end = start + pd.Timedelta(days=phase_length)
        fig.add_vrect(
            x0=start, x1=end,
            fillcolor=colors[i],
            opacity=0.2,
            layer="below",
            line_width=0,
            annotation_text=f"Phase {i+1}",
            annotation_position="top left",
        )

    # ---- Layout ----
    fig.update_layout(
        template="plotly_white",
        height=700,
        margin=dict(l=120, r=30, t=60, b=60),
        title_x=0.5,
        bargap=0.3,
        font=dict(size=12),
        legend_title_text="Task Status",
        hoverlabel=dict(bgcolor="white", font_size=11),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    