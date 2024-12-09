# -*- coding: utf-8 -*-
"""SCU Scholarship Finder"""

import pandas as pd
import streamlit as st
from datetime import datetime
from openai import OpenAI
from scholarship_pipeline import run_pipeline
from streamlit_calendar import calendar

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

# Global CSS and styling
st.markdown("""
<style>
body {
    background: #fafafa;
    font-family: "Helvetica Neue", Arial, sans-serif;
}
hr.custom-hr {
    border: none;
    border-top: 2px solid #f44336;
    width: 50px;
    margin: 20px 0;
}
.styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    width: 100%;
    font-size: 1em;
    font-family: sans-serif;
}
.styled-table thead tr {
    background-color: #f44336;
    color: #ffffff;
    text-align: left;
    font-weight: bold;
}
.styled-table th, .styled-table td {
    border: 1px solid #dddddd;
    padding: 12px;
}
.styled-table tbody tr:nth-of-type(even) {
    background-color: #fef2f2;
}
.styled-table tbody tr:hover {
    background-color: #fde0e0;
}
.styled-table tbody tr td:first-child {
    font-weight: bold;
    color: #c62828;
}
</style>
""", unsafe_allow_html=True)

# Prepare the data for the calendar page BEFORE the navigation logic
datacal = {
    "Scholarship Name": [
        "🎓 Kuru Footsteps to Your Future Scholarship",
        "💡 Alert1 Students for Seniors Scholarship",
        "⭐ Blankstyle Scholarship Opportunity #1",
        "🚀 Innovation In Education Scholarship",
        "📘 The Bert & Phyllis Lamb Prize in Political Science",
        "🌍 New Beginnings Immigrant Scholarship",
    ],
    "Date Due": [
        "2024-12-20",
        "2025-01-10",
        "2024-12-31",
        "2024-10-15",
        "2025-02-14",
        "2024-10-18",
    ],
    "Summary": [
        "This scholarship awards $1,000 to high school seniors or college students pursuing their academic goals. Prepare a personal statement and apply by December 20, 2024.",
        "A $500 award for students dedicated to improving senior care. Write a 300-word essay. Deadline: January 10, 2025.",
        "A $1,000 bi-annual scholarship for college expenses. Explain how this scholarship helps your goals. Deadline: December 31, 2024.",
        "A $500 scholarship for innovative community projects. Describe your project and submit by October 15, 2024.",
        "Honors excellence in Political Science. Submit a well-researched paper by February 14, 2025.",
        "Supports first-generation immigrant students. Write an essay about your immigrant experience, due October 18, 2024.",
    ],
}
dfcal = pd.DataFrame(datacal)
dfcal["Date Due"] = pd.to_datetime(dfcal["Date Due"])

# Sidebar navigation
st.sidebar.title("📚 Navigation")
nav_option = st.sidebar.radio("Go to:", ["🏠 Home", "🎓 Find Scholarships", "📊 Statistics", "ℹ️ About", "📅 Calendar View"])

# Navigation logic
if nav_option == "🏠 Home":
    st.markdown("<h1 style='color:#c62828; text-align:center;'>🎓 Welcome to SCU Scholarship Finder!</h1>", unsafe_allow_html=True)
    st.subheader("Hello!👋")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)

    st.markdown("""
    **Discover scholarships tailored for Santa Clara University students.**  
    Use this platform to explore funding opportunities, get personalized recommendations, and plan for upcoming deadlines.
    """)

    # Quick Links
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
    - [SCU Financial Aid Office](https://www.scu.edu/financialaid/)
    - [Scholarship Application Tips](https://www.scu.edu/globalengagement/study-abroad/get-started/affording-study-abroad/apply-to-scholarships/#:~:text=Scholarships%20can%20be%20local%2C%20regional,application%20as%20a%20starting%20place.)
    - [SCU Career Center](https://www.scu.edu/careercenter/)
    """)

    # Scholarship Tips
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

    # FAQs
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

elif nav_option == "🎓 Find Scholarships":
    st.header("🎓 Find Scholarships")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)

    user_query = st.text_area("Describe the type of scholarship you're looking for (e.g., major, GPA, financial need):")

    if st.button("🔍 Find Scholarships"):
        with st.spinner("Searching for scholarships..."):
            search_results = run_pipeline(user_query, client)

        if isinstance(search_results, pd.DataFrame) and not search_results.empty:
            st.subheader("✨ Search Results (Table View)")
            html_table = search_results.to_html(classes="styled-table", index=False, escape=False)
            st.markdown(html_table, unsafe_allow_html=True)
        elif isinstance(search_results, list) and search_results:
            st.subheader("✨ Search Results (Detailed View)")
            for i, scholarship in enumerate(search_results, start=1):
                name = scholarship.get("Name", "N/A")
                description = scholarship.get("Description", "No description provided.")
                eligibility = scholarship.get("Eligibility", "No eligibility criteria provided.")
                url = scholarship.get("URL", "No URL provided.")

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

    # Example progress indicator
    st.progress(0.3)

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

elif nav_option == "📅 Calendar View":
    st.title("📅 Scholarship Calendar")
    st.markdown("<hr class='custom-hr'>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    if "current_month" not in st.session_state:
        st.session_state.current_month = datetime.now().month
    if "current_year" not in st.session_state:
        st.session_state.current_year = datetime.now().year

    # Prepare events
    events = {}
    for _, row in dfcal.iterrows():
        event_date = row["Date Due"].strftime("%Y-%m-%d")
        if event_date not in events:
            events[event_date] = []
        events[event_date].append(row["Scholarship Name"])

    # Combine scholarships for each date
    events = {date: "\n".join(sch) for date, sch in events.items()}

    with col1:
        st.subheader("📆 Calendar")
        selected_event = calendar(events)

        if selected_event and "currentStart" in selected_event:
            new_start_date = selected_event["currentStart"].split("T")[0]
            new_start_datetime = pd.Timestamp(new_start_date)
            st.session_state.current_month = new_start_datetime.month
            st.session_state.current_year = new_start_datetime.year

    with col2:
        st.subheader("📋 All Scholarships")
        for _, row in dfcal.iterrows():
            st.markdown(
                f"**{row['Scholarship Name']}**  \n"
                f"🗓 **Due Date**: {row['Date Due'].strftime('%B %d, %Y')}"
            )

    st.subheader("🎯 Selected Date Details")
    if selected_event and "dateClick" in selected_event:
        selected_date = selected_event["dateClick"]["date"].split("T")[0]
        selected_scholarships = dfcal[dfcal["Date Due"] == pd.Timestamp(selected_date)]
        if not selected_scholarships.empty:
            for _, row in selected_scholarships.iterrows():
                st.markdown(
                    f"""
                    ### {row['Scholarship Name']}
                    - **Due Date**: {row['Date Due'].strftime('%B %d, %Y')}
                    - **Details**: {row['Summary']}
                    """
                )
        else:
            st.write(f"No scholarships due on {selected_date}.")
    else:
        st.write("Click on a date in the calendar to view details.")
