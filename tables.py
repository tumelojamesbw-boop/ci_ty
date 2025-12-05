import pandas as pd
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

def render_table_editor(
    file_path,
    key_prefix,
    id_column,
    date_columns=None,
    editable_columns=None
):
    # Load data
    df = pd.read_csv(file_path)

    # Explicitly parse date columns
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # Add filter
    filtered_df = dataframe_explorer(df, case=False)

    # Init session state for new rows
    if f"{key_prefix}_added_rows" not in st.session_state:
        st.session_state[f"{key_prefix}_added_rows"] = pd.DataFrame()

    # Add empty row
    if st.button(f"➕ Add Empty Row ({key_prefix})"):
        empty_row = {col: "" for col in df.columns}
        for col in date_columns or []:
            empty_row[col] = pd.to_datetime("01/01/2025", dayfirst=True)
        st.session_state[f"{key_prefix}_added_rows"] = pd.concat(
            [st.session_state[f"{key_prefix}_added_rows"], pd.DataFrame([empty_row])],
            ignore_index=True
        )
        st.rerun()

    # Combine for display
    display_df = pd.concat(
        [filtered_df, st.session_state[f"{key_prefix}_added_rows"]],
        ignore_index=True
    )

    # Convert date columns for display
    for col in date_columns or []:
        if col in display_df.columns:
            display_df[col] = pd.to_datetime(display_df[col], errors="coerce").dt.strftime("%d/%m/%Y")

    edited_df = st.data_editor(
        display_df,
        num_rows="dynamic",
        width="stretch",
        key=f"{key_prefix}_editor"
    )

    # Save
    if st.button(f"💾 Save Changes ({key_prefix})"):
        if edited_df[id_column].astype(str).str.strip().eq("").any():
            st.error(f"❌ One or more rows have an empty {id_column}.")
        elif edited_df[id_column].astype(str).duplicated().any():
            st.error(f"❌ Duplicate {id_column}s found.")
        else:
            old_df = pd.read_csv(file_path)
            if date_columns:
                for col in date_columns:
                    if col in old_df.columns:
                        old_df[col] = pd.to_datetime(old_df[col], format="%d %m %Y", errors="coerce")

            updated_ids = edited_df[id_column].astype(str).tolist()
            old_df = old_df[~old_df[id_column].astype(str).isin(updated_ids)]
            full_df = pd.concat([old_df, edited_df], ignore_index=True)
            full_df.to_csv(file_path, index=False)
            st.session_state[f"{key_prefix}_added_rows"] = pd.DataFrame()
            st.success(f"✅ Saved {key_prefix} successfully.")
            st.rerun()

    # Delete
    to_delete = st.text_input(f"Enter {id_column} to delete ({key_prefix})")
    if st.button(f"🗑️ Delete {key_prefix}") and to_delete:
        df = df[df[id_column].astype(str) != str(to_delete)]
        df.to_csv(file_path, index=False)
        st.success(f"✅ {id_column} {to_delete} deleted.")
        st.rerun()
