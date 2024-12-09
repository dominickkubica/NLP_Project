from rapidfuzz import fuzz
from rapidfuzz import process
import re
import pandas as pd
from openai import OpenAI
import json

# Load the scholarship CSV
try:
    scholarship_df = pd.read_csv("scholarships.csv")
    print("Scholarship CSV loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Error loading the scholarship CSV: {e}")

def refine_prompt(user_input, client):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at refining prompts specifically for finding scholarships and grants."},
                {"role": "user", "content": f"Please refine this query to find more scholarships generally, only respond with the refined prompt, no other comments: {user_input}"}
            ],
        )
        print(f"API Response: {response}")  # Debugging log
        refined_prompt = response.choices[0].message.content.strip()
        return refined_prompt
    except Exception as e:
        print(f"Error refining prompt: {e}")
        return None

def search_scholarships(refined_prompt, df, client):
    try:
        scholarships = df.to_dict(orient="records")

        messages = [
            {"role": "system", "content": "You are an expert in finding scholarships for users."},
            {
                "role": "user",
                "content": (
                    f"The user's refined query is: '{refined_prompt}'. Below is the list of scholarships:\n\n{scholarships}\n\n"
                    "Please identify and return ONLY the scholarships most relevant to the user's query. "
                    "Return the results as a JSON array of objects, with each object containing EXACTLY the following four fields: "
                    "\"Title\", \"Description\", \"Eligibility\", and \"URL\". "
                    "Do not include any extra fields, explanations, comments, code blocks, or any text outside of the JSON array. "
                    "Make sure the JSON is syntactically valid and properly formatted."
                )
            }
        ]

        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)

        raw_output = response.choices[0].message.content.strip()
        print("Raw Output from Model 2:", raw_output)  # Debugging log

        # Strip Markdown code block delimiters if present
        if raw_output.startswith("```") and raw_output.endswith("```"):
            raw_output = raw_output.strip("```").strip("json").strip()

        # Clean up common issues with raw JSON-like output
        raw_output = raw_output.replace("\n", "").replace("\t", "").strip()

        try:
            parsed_output = json.loads(raw_output)
            print("Parsed JSON Output:", parsed_output)
            return parsed_output
        except json.JSONDecodeError as e:
            print(f"Error: Raw output is not valid JSON. {e}")
            print("Raw Output (Debug):", repr(raw_output))  # Log raw output for debugging
            return []

    except Exception as e:
        print(f"Error in search_scholarships: {e}")
        return []

def run_pipeline(user_query, client):
    """
    End-to-end pipeline: Refine prompt, search scholarships, and return results.
    """
    # Step 1: Refine the prompt
    refined_prompt = refine_prompt(user_query, client)
    if not refined_prompt:
        print("Error: Refined prompt is empty or invalid.")
        return pd.DataFrame({"Message": ["Failed to refine the prompt."]})

    print(f"Refined Prompt: {refined_prompt}")  # Debugging log

    # Step 2: Search scholarships
    parsed_results = search_scholarships(refined_prompt, scholarship_df, client)

    print(f"Parsed Results: {parsed_results}")  # Debugging log

    # Step 3: Convert to DataFrame and return
    if parsed_results:
        formatted_results = [
            {
                "Name": entry.get("Title", "Unknown"),
                "Description": entry.get("Description", "No description provided."),
                "Eligibility": entry.get("Eligibility", "No eligibility criteria provided."),
                "URL": entry.get("URL", "No URL provided.")
            }
            for entry in parsed_results
        ]
        return pd.DataFrame(formatted_results)
    else:
        return pd.DataFrame({"Message": ["No scholarships found."]})
