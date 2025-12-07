import streamlit as st
import matplotlib.pyplot as plt

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_summary_charts(df):
    # ======== Row 1: Task Status & Delays ========
    col1, col2, col3 = st.columns(3)

    with col1:
        dept_delay = (
            df.groupby('Department_Name')['Delay_Days']
            .sum()
            .reset_index()
            .sort_values(by='Delay_Days', ascending=False)
        )

        fig1 = px.pie(
            dept_delay,
            names='Department_Name',
            values='Delay_Days',
            title="Delay Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            hole=0.3  # donut style for Power BI look
        )

        fig1.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=[0.02] * len(dept_delay)
        )
        
        

        st.plotly_chart(fig1, use_container_width=True)

    # --- COL 2: Average Project Completion (Vertical Bar Chart) ---
    with col2:
        completion_data = df.groupby('Project_Name')['percent_complete'].mean().reset_index()

        fig4 = px.bar(
            completion_data,
            y='Project_Name',
            x='percent_complete',
            orientation='h',
            title="Average Project Completion (%)",
            color='percent_complete',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig4, use_container_width=True)
        

    # --- COL 3: Budgeted vs Actual Cost ---
    with col3:
        cost_data = df.groupby('Project_Name')[['Budgeted_Cost', 'Actual_Cost']].sum().reset_index()

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=cost_data['Project_Name'], y=cost_data['Budgeted_Cost'], name='Budgeted Cost'))
        fig3.add_trace(go.Bar(x=cost_data['Project_Name'], y=cost_data['Actual_Cost'], name='Actual Cost'))

        fig3.update_layout(
            barmode='group',
            title="Budgeted vs Actual Cost per Project",
            xaxis_title="Project",
            yaxis_title="Cost (Pula)"
        )
        st.plotly_chart(fig3, use_container_width=True) 
        

    
    
    st.divider()

    kpi1, kpi2, = st.columns(2)

    with kpi1:
        heatmap_data = (
            df.pivot_table(
                index="Department_Name",
                columns="Project_Name",
                values="Delay_Days",
                aggfunc="mean"
            ).fillna(0)
        )

        fig_heat = go.Figure(
            data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='RdYlBu_r',
                hoverongaps=False,
                colorbar=dict(title="Avg Delay (Days)")
            )
        )
        fig_heat.update_layout(
            title="🔥 Delay Distribution (Projects vs Departments)",
            template="plotly_white",
            height=300,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with kpi2:
        dept_summary = df.groupby('Department_Name').agg({
            'Task_ID': 'count',
            'percent_complete': 'mean',
            'Delay_Days': 'mean'
        }).reset_index()

        fig5 = px.scatter(
            dept_summary,
            x='percent_complete',
            y='Delay_Days',
            size='Task_ID',
            color='Department_Name',
            hover_name='Department_Name',
            title='Department Performance (Completion vs Delays)',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig5.update_layout(
            template="plotly_white",
            height=300,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.divider()
        
    
        # Calculate cost overrun ratio
    df['Cost_Impact'] = (df['Actual_Cost'] - df['Budgeted_Cost']) / df['Budgeted_Cost'] * 100

        # Group by Department or Project
    impact_data = df.groupby('Department_Name').agg({
            'Delay_Days': 'mean',
            'Cost_Impact': 'mean'
        }).reset_index()

    fig4 = px.scatter(
            impact_data,
            x='Delay_Days',
            y='Cost_Impact',
            color='Department_Name',
            size='Delay_Days',
            title="💸 Delay Impact on Budget (%)",
            labels={'Delay_Days': 'Average Delay (Days)', 'Cost_Impact': 'Average Cost Overrun (%)'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )

    fig4.update_layout(
            template="plotly_white",
            height=300,
            margin=dict(l=10, r=10, t=40, b=10)
        )
    st.plotly_chart(fig4, use_container_width=True)   


 




    
    