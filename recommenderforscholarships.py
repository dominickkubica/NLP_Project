# -*- coding: utf-8 -*-
"""SCU Scholarship Finder"""

import pandas as pd
import streamlit as st
from datetime import datetime
from openai import OpenAI
from scholarship_pipeline import run_pipeline

# Configure the page
st.set_page_config(
    page_title="SCU Scholarship Finder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Prompt the user for their API Key in the sidebar
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.error("Please enter your OpenAI API Key in the sidebar.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Add some global styling and a banner image or color
st.markdown("""
<style>
/* Global style */
body {
    background: #fafafa;
    font-family: "Helvetica Neue", Arial, sans-serif;
}

/* A nice red divider */
hr.custom-hr {
    border: none;
    border-top: 2px solid #f44336;
    width: 50px;
    margin: 20px 0;
}

/* Table styling */
.styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    width: 100%;
    font-size: 1em;
    font-family: sans-serif;
}

/* Table header background & text */
.styled-table thead tr {
    background-color: #f44336;
    color: #ffffff;
    text-align: left;
    font-weight: bold;
}

/* Table cells */
.styled-table th, .styled-table td {
    border: 1px solid #dddddd;
    padding: 12px;
}

/* Alternate row background */
.styled-table tbody tr:nth-of-type(even) {
    background-color: #fef2f2;
}

/* Hover effect on rows */
.styled-table tbody tr:hover {
    background-color: #fde0e0;
}

/* Highlight first column or specific text if you want */
.styled-table tbody tr td:first-child {
    font-weight: bold;
    color: #c62828;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📚 Navigation")
nav_option = st.sidebar.radio("Go to:", ["🏠 Home", "🎓 Find Scholarships", "📊 Statistics", "ℹ️ About"])

# Home Page
if nav_option == "🏠 Home":
    st.markdown("<h1 style='color:#c62828; text-align:center;'>🎓 Welcome to SCU Scholarship Finder!</h1>", unsafe_allow_html=True)

    # Personalized greeting based on time of day
    st.subheader("Hello!👋")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)

    # Introductory Text
    st.markdown("""
    **Discover scholarships tailored for Santa Clara University students.**  
    Use this platform to explore funding opportunities, get personalized recommendations, and plan for upcoming deadlines.
    """)

    # Quick Links Section
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
    - [SCU Financial Aid Office](https://www.scu.edu/financialaid/)
    - [Scholarship Application Tips](https://www.scu.edu/globalengagement/study-abroad/get-started/affording-study-abroad/apply-to-scholarships/#:~:text=Scholarships%20can%20be%20local%2C%20regional,application%20as%20a%20starting%20place.)
    - [SCU Career Center](https://www.scu.edu/careercenter/)
    """)

    # Scholarship Tips Section
    st.markdown("### 💡 Scholarship Tips")
    st.markdown("""
    - **Start Early**: Begin your search and application process well in advance.
    - **Tailor Your Applications**: Match essays and responses to each scholarship's requirements.
    - **Leverage SCU Resources**: Reach out to the financial aid office or academic advisors for guidance.
    """)

    # Upcoming Deadlines
    st.markdown("### 📅 Upcoming Deadlines")
    st.markdown("""
    - **SCU Merit Scholarship**: December 15, 2024  
    - **Diversity in Tech Award**: December 20, 2024  
    - **Graduate Assistantship Grant**: January 10, 2025  
    """)

    # FAQs Section
    st.markdown("### ❓ FAQs")
    st.markdown("""
    - **Who can apply for scholarships?**  
      Most are available to SCU students who meet specific criteria.
    - **Do I need to file FAFSA?**  
      Yes, for need-based scholarships and federal aid.
    - **Where can I get help with my application?**  
      Visit the [SCU Financial Aid Office](https://www.scu.edu/financialaid/) or contact your academic advisor.
    """)

    st.balloons()

# Scholarship Finder Page
elif nav_option == "🎓 Find Scholarships":
    st.header("🎓 Find Scholarships")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)

    # Collect user input
    user_query = st.text_area("Describe the type of scholarship you're looking for (e.g., major, GPA, financial need):")
    
    # Submit and display results
    if st.button("🔍 Find Scholarships"):
        with st.spinner("Searching for scholarships..."):
            # Pass the query and client to the pipeline
            search_results = run_pipeline(user_query, client)

            # Debug: Log the raw output for verification
            print("Processed Search Results:", search_results)

        # Handle DataFrame-based output
        if isinstance(search_results, pd.DataFrame) and not search_results.empty:
            st.subheader("✨ Search Results (Table View)")
            # Convert DataFrame to HTML with classes for styling
            html_table = search_results.to_html(classes="styled-table", index=False, escape=False)
            st.markdown(html_table, unsafe_allow_html=True)

        # Handle dictionary-based or structured list-based output
        elif isinstance(search_results, list) and search_results:
            st.subheader("✨ Search Results (Detailed View)")
            # If you want to style each scholarship in red and with padding:
            for i, scholarship in enumerate(search_results, start=1):
                name = scholarship.get("Name", "N/A")
                description = scholarship.get("Description", "No description provided.")
                eligibility = scholarship.get("Eligibility", "No eligibility criteria provided.")
                url = scholarship.get("URL", "No URL provided.")

                # Use HTML to style each scholarship card
                scholarship_html = f"""
                <div style="border:2px solid #f44336; border-radius:5px; background:#fff5f5; padding:15px; margin-bottom:20px;">
                    <h3 style="color:#c62828;">{i}. {name}</h3>
                    <p><strong>Description:</strong> {description}</p>
                    <p><strong>Eligibility:</strong> {eligibility}</p>
                    {'<p><strong>URL:</strong> <a href="'+url+'" target="_blank">'+url+'</a></p>' if url != "No URL provided." else ""}
                </div>
                """
                st.markdown(scholarship_html, unsafe_allow_html=True)
        else:
            st.subheader("🚫 No Results Found")
            st.markdown("Sorry, no scholarships matched your query. Please try a different description.")

# Statistics Page
elif nav_option == "📊 Statistics":
    st.header("📊 Scholarship Statistics")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("Explore trends and insights related to SCU scholarships.")
    st.markdown("""
    - **Merit-Based Scholarships**: 30% of total scholarships.
    - **Need-Based Scholarships**: 20%.
    - **Diversity Scholarships**: 15%.
    - **Graduate Aid**: 10%.
    """)

    # You could add a simple chart or a progress bar
    st.progress(0.3)  # For merit-based scholarships, as an example

# About Page
elif nav_option == "ℹ️ About":
    st.header("ℹ️ About This App")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)
    st.markdown("""
    **SCU Scholarship Finder** is designed to assist Santa Clara University students in finding and applying for scholarships.

    ### Features:
    - Explore SCU-specific scholarships.
    - View simple statistics on funding opportunities.
    - Receive tailored recommendations based on your profile.

    Built with ❤️ for SCU students.
    """)
    st.markdown("[Visit SCU Financial Aid Office](https://www.scu.edu/financial-aid/)")
    st.markdown("Feel free to [contact us](mailto:info@scu.edu) for more information or assistance.")
