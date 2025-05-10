import pandas as pd
import streamlit as st
from difflib import SequenceMatcher

# Load ICD-10 lookup table
df = pd.read_excel("2025 Midyear_Final ICD-10-CM Mappings.xlsx", skiprows=3, usecols=[0, 1])
df.columns = ["Diagnosis Code", "Description"]

st.title("ICD-10 Code & Description Lookup")

option = st.radio("Search by:", ("Diagnosis Code", "Description Keyword"))

def match_score(input_text, description):
    input_words = input_text.lower().split()
    desc_text = str(description).lower()
    return sum(1 for word in input_words if word in desc_text)

def fuzzy_score(input_text, description):
    return SequenceMatcher(None, input_text.lower(), str(description).lower()).ratio()

if option == "Diagnosis Code":
    code = st.text_input("Enter ICD-10 Code")
    if code:
        result = df[df["Diagnosis Code"].str.upper() == code.upper()]
        st.write(result if not result.empty else "No match found.")

elif option == "Description Keyword":
    keyword = st.text_input("Enter keyword(s) (e.g., diabetes mellitus type 2)")
    if keyword:
        df["Match Score"] = df["Description"].apply(lambda desc: match_score(keyword, desc))
        df["Fuzzy Score"] = df["Description"].apply(lambda desc: fuzzy_score(keyword, desc))

        # Combine scores: prioritize full word matches, break ties with fuzzy similarity
        result = df[(df["Match Score"] > 0) | (df["Fuzzy Score"] > 0.4)]  # show only relevant ones
        result = result.sort_values(by=["Match Score", "Fuzzy Score"], ascending=False)

        st.write(result[["Diagnosis Code", "Description"]] if not result.empty else "No match found.")
