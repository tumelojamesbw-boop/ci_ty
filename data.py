import pandas as pd

def load_and_merge_data():
    # Load datasets
    projects_df = pd.read_csv("projects.csv", parse_dates=["Start_Date", "End_Date"])
    for col in ["Start_Date", "End_Date"]:
     
     projects_df[col] = pd.to_datetime(projects_df[col], dayfirst=True, errors='coerce')

    

    tasks_df = pd.read_csv("tasks.csv")
    for col in ["Est_Start", "Est_End", "Act_Start", "Act_End",]:
     if col in tasks_df.columns:
        tasks_df[col] = tasks_df[col].astype(str).str.replace('/', '-')
        tasks_df[col] = pd.to_datetime(tasks_df[col], dayfirst=True, errors='coerce')


    costs_df = pd.read_csv("costs.csv")
    departments_df = pd.read_csv("departments.csv")

    # Merge tasks with projects
    merged = tasks_df.merge(projects_df, on="Project_ID", how="left", suffixes=('', '_Project'))

    # Merge with departments
    merged = merged.merge(departments_df, on="Department_ID", how="left")

    # Merge with costs
    merged = merged.merge(costs_df, on="Task_ID", how="left", suffixes=('', '_Cost'))

    return merged

