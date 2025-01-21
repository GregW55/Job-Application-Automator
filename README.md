# Job Application Automator
- The Job Application Automator is a Python-based tool that streamlines the process of finding and applying for jobs.
- By leveraging web scraping, PDF parsing, and AI-driven decision-making, this tool helps job seekers locate job listings that match their qualifications and apply to them automatically, all while tracking the progress and outcomes.

## Key features:
1. Resume Parsing: Extract text from a PDF resume to use for context when applying to jobs.
2. Job Search & Application: Automates the search for jobs on platforms like LinkedIn and Indeed, applying to relevant jobs based on your resume.
3. Job Data Storage: Keeps track of applied jobs in a CSV file for reference.
4. Browser Automation: Uses a browser automation tool to interact with job application forms and submit resumes.

## Features:
1. CV Parsing: Extracts relevant details from your resume (in PDF format) for use in applications.
2. Job Search Automation: Locates job postings that match your profile across multiple platforms (LinkedIn, Indeed, etc.).
3. Automated Applications: Automatically applies to the jobs that are a good fit based on the analysis of your resume and job descriptions.
4. Job Tracking: Saves job application data, including job titles, companies, links, and more, to a CSV file for easy reference.
5. Scroll and Find Elements: Uses scrolling to find elements on web pages when direct interactions don’t work.

## Technologies Used:
- Python: The main programming language used for implementing the automation logic.
- PyPDF2: A library for reading and extracting text from PDF files (used to parse your resume).
- Langchain (OpenAI): AI models (using Azure OpenAI) to guide the automation and decision-making for job applications.
- Browser Automation (browser_use): A tool for controlling a headless browser to fill out forms and interact with job application sites.

## Setup:
1. Clone the repository: git clone https://github.com/GregW55/Job-Application-Automator.git
2. Navigate to the directory: cd Job-Application-Automator
3. Install dependencies
4. Set up environment variables for Azure OpenAI:
- Create an .env file and include your Azure OpenAI API key and endpoint:
- AZURE_OPENAI_KEY=your-api-key
- AZURE_OPENAI_ENDPOINT=your-endpoint
5. Download your resume (in PDF format) and place it in the project directory as new_resume.pdf.

## How It Works:
1. CV Parsing: The tool reads your resume (in PDF format) and extracts relevant text. This data is then used to understand your skills, experience, and job preferences.
2. Job Search: The tool automates browsing platforms like LinkedIn and Indeed to search for jobs that fit your profile. You can customize the search locations and job types in the script.
3. Automated Applications: Once relevant jobs are found, the tool automatically applies to those positions using the resume you uploaded. The browser is controlled using Python to fill out forms and submit your resume.
4. Job Data Storage: The tool stores data on the jobs you've applied to, including job titles, companies, links, and salary information (if available) in a CSV file for easy tracking.

## Usage:
- Run the tool: python job_application_automator.py
- Monitor the process: The automation will begin searching for jobs based on the criteria set in the script. The progress is logged, and you can view which jobs are being applied to and saved.

## Contributing:
- Contributions are welcome! Please feel free to fork the repository, create a pull request, or open an issue if you encounter any bugs or have feature requests.

## License
- This project is licensed under the MIT License - see the LICENSE file for details.

## Example Use Case:
1. After setting up the necessary environment variables and preparing your resume, the tool will:
- Read the resume (new_resume.pdf).
- Search job listings on LinkedIn and Indeed for positions like "Python Developer" or "Data Analyst."
- Apply to relevant listings automatically.
- Track all applied jobs in a jobs.csv file for later review.
- By using this automation tool, you can save time and increase your chances of landing your dream job!
