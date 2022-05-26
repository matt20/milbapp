from multiprocessing.sharedctypes import Value
import streamlit as st
import os



root = os.path.join(os.path.dirname(__file__))

dashboards = {
    "Main Page": os.path.join(root, "app.py"),
    "AAA": os.path.join(root, "app_aaa.py"),
    "AA": os.path.join(root, "app_aa.py"),
    "A+": os.path.join(root, "app_hia.py"),
    "A": os.path.join(root, "app_a.py"),
    # "License Key": os.path.join(root, "licensing_example.py"),
    # "Two grids in page": os.path.join(root, "two_grids_example.py"),
    # "Virtual Columns": os.path.join(root, "virtual_columns.py"),
    # "Highlight Editions": os.path.join(root, "example_highlight_change.py"),
    # "Inside st.form": os.path.join(root, "forms.py"),
    # "Pinned Row": os.path.join(root, "pinned_rows.py"),
    # "Theming & Pre-Selection": os.path.join(root, "themes_and_pre_selection.py"),
    # "Nested Grids" : os.path.join(root, "nested_grids.py"), 
    # "Rich Cell Editor" : os.path.join(root, "rich_cell_editor.py") 
}

choice_from_url = query_params = st.experimental_get_query_params().get("example", ["Main Page"])[0]
index = list(dashboards.keys()).index(choice_from_url)

choice = st.sidebar.radio("Levels", list(dashboards.keys()), index=index)

path = dashboards[choice]

#c = code.read()
exec(path)
st.set_page_config(layout="wide")

#     with st.expander('Code for this example:'):
#         st.markdown(f"""``` python
# {c}```""")