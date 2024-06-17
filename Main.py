from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from fpdf import FPDF
import os


def extract_emails(text):
    # Regular expression patterns for matching email addresses
    email_patterns = [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Standard email format
        r'[a-zA-Z0-9._%+-]+\s*\[\s*at\s*\]\s*[a-zA-Z0-9.-]+\s*\[\s*dot\s*\]\s*[a-zA-Z]{2,}',  # Obfuscated format
    ]

    emails = []
    for pattern in email_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Clean obfuscated emails
            cleaned_email = match.replace("[at]", "@").replace("[dot]", ".").replace(" ", "")
            emails.append(cleaned_email)

    return emails


def extract_emails_from_url(url):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        # Open the webpage
        driver.get(url)
        time.sleep(3)  # Allow time for the page to load

        # Get page source
        page_source = driver.page_source

        # Print the HTML content for debugging
        print(page_source[:2000])  # Print the first 2000 characters
    except Exception as e:
        print(f"Failed to retrieve webpage: {e}")
        return []
    finally:
        driver.quit()

    # Parse the webpage content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all text in the webpage
    text = soup.get_text()

    # Extract emails from the text
    emails = extract_emails(text)

    return emails


def save_emails_to_pdf(emails, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for email in emails:
        pdf.cell(200, 10, txt=email, ln=True)

    pdf.output(file_path)


# Example usage
url = 'https://www.mmarau.ac.ke/'  # Replace with the target URL
emails = extract_emails_from_url(url)

print("Extracted emails:")
for email in emails:
    print(email)

# Save emails to PDF
pdf_file_path = r'C:\Users\princ\Desktop\rpt\extracted_emails.pdf'
save_emails_to_pdf(emails, pdf_file_path)

print(f"Emails saved to {pdf_file_path}")
