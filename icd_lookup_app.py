import pandas as pd
import streamlit as st

# Load ICD-10 lookup table
df = pd.read_excel(r"2025 Midyear_Final ICD-10-CM Mappings.xlsx",skiprows=3, usecols=[0, 1])  # Replace with your filename
df.columns = ["Diagnosis Code", "Description"]

st.title("ICD-10 Code & Description Lookup")

option = st.radio("Search by:", ("Diagnosis Code", "Description Keyword"))

if option == "Diagnosis Code":
    code = st.text_input("Enter ICD-10 Code")
    if code:
        result = df[df["Diagnosis Code"].str.upper() == code.upper()]
        st.write(result if not result.empty else "No match found.")

elif option == "Description Keyword":
    keyword = st.text_input("Enter keyword (e.g., diabetes)")
    if keyword:
        result = df[df["Description"].str.contains(keyword, case=False, na=False)]
        st.write(result if not result.empty else "No match found.")
