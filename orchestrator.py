# main.py

import os
from extract_and_summarize import extract_and_summarize
from analyze_profile import analyze_profile

def main():
    directory = '.'
    extracted_file = 'all_profile_lines.txt'
    summaries_file = 'summaries.txt'
    analysis_file = 'profile_analysis.txt'
    name_pattern = 'Francisco Gonzalez:'  # This can be changed to analyze different profiles

    try:
        # Step 1: Extract and summarize
        extract_and_summarize(directory, extracted_file, summaries_file, name_pattern)
        
        # Ask user if they want to continue with the analysis
        user_input = input("Extraction and summarization completed. Do you want to continue with the profile analysis? (y/n): ")
        
        if user_input.lower() == 'y':
            # Step 2: Analyze profile
            analyze_profile(summaries_file, analysis_file)
            print("Profile analysis completed successfully.")
        else:
            print("Profile analysis skipped. You can run it later using the analyze_profile.py script.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()