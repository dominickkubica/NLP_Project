# NLPProject



SCU Scholarship Finder
Welcome to the SCU Scholarship Finder! This app is designed to help Santa Clara University students explore and find scholarships tailored to their unique profiles. By leveraging AI and web scraping, the app provides personalized scholarship recommendations based on your preferences and academic information.

Features
Personalized Recommendations: Tailored results based on your major, GPA, financial need, and other preferences.
Dynamic Query Refinement: Your queries are enhanced by AI to maximize the relevance of results.
Easy Navigation: Intuitive interface with clear sections for searching scholarships, viewing statistics, and exploring deadlines.
SCU-Specific Resources: Includes links and tips from SCU’s financial aid office, career center, and other trusted sources.

Setup Instructions
Clone the Repository:

bash
Copy code
git clone [https://github.com/your-repo-url/scholarship-finder.git](https://github.com/dominickkubica/NLPProject.git)
cd scholarship-finder

Install Dependencies: Ensure you have Python 3.7+ installed, then run:

Copy code
pip install -r requirements.txt
Add Your OpenAI API Key: Create a .env file in the root directory and add your OpenAI API key:

makefile
Copy code
OPENAI_API_KEY=your_openai_api_key
Run the Application: Start the Streamlit app:

arduino
Copy code
streamlit run app/streamlit_app.py
How to Use
Navigate the App:

Use the sidebar to access different sections: Home, Find Scholarships, Statistics, and About.
Find Scholarships:

Enter a description of the type of scholarship you're looking for (e.g., "need-based scholarships for engineering majors").
Click the "Find Scholarships" button to see results.
Explore Results:

View tailored scholarship recommendations in an easy-to-read table.
Statistics & Deadlines:

Explore SCU-specific scholarship trends and upcoming application deadlines.
Project Structure
bash
Copy code
/scholarship-finder/
  /app/
    streamlit_app.py          # Main Streamlit application
  /models/
    scholarship_pipeline.py   # Pipeline for refining prompts and searching the scholarship data
  /data/
    scholarships.csv          # CSV file with scraped scholarship data
  .env                        # API key (add to .gitignore)
  requirements.txt            # Python dependencies
README.md                     # Project documentation
Dependencies
The following Python packages are required:

streamlit – For the front-end web app.
pandas – For handling the scholarship data.
python-dotenv – For securely managing API keys.
openai – For AI-powered query refinement.
Install them all with:

Copy code
pip install -r requirements.txt
