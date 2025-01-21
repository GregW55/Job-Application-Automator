"""
Find and apply to jobs.
"""

import csv
import os
import re
import sys
from pathlib import Path

from PyPDF2 import PdfReader

from browser_use.browser.browser import Browser, BrowserConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from typing import List, Optional

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic import BaseModel, SecretStr

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.context import BrowserContext

import logging

logger = logging.getLogger(__name__)
# full screen mode
controller = Controller()
CV = Path.cwd() / 'new_resume.pdf'


class Job(BaseModel):
	title: str
	link: str
	company: str
	fit_score: float
	location: Optional[str] = None
	salary: Optional[str] = None


@controller.action(
	'Save jobs to file - with a score how well it fits to my profile', param_model=Job
)
def save_jobs(job: Job):
	with open('jobs.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerow([job.title, job.company, job.link, job.salary, job.location])

	return 'Saved job to file'


@controller.action('Read jobs from file')
def read_jobs():
	with open('jobs.csv', 'r') as f:
		return f.read()


@controller.action('Read my cv for context to fill forms')
def read_cv():
	pdf = PdfReader(CV)
	text = ''
	for page in pdf.pages:
		text += page.extract_text() or ''
	logger.info(f'Read cv with {len(text)} characters')
	return ActionResult(extracted_content=text, include_in_memory=True)


@controller.action(
	'Upload cv to element - call this function to upload if element is not found, try with different index of the same upload element',
	requires_browser=True,
)
async def upload_cv(index: int, browser: BrowserContext):
	path = str(CV.absolute())
	dom_el = await browser.get_dom_element_by_index(index)

	if dom_el is None:
		return ActionResult(error=f'No element found at index {index}')

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)

	if file_upload_el is None:
		logger.info(f'No file upload element found at index {index}')
		return ActionResult(error=f'No file upload element found at index {index}')

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file to index {index}'
		logger.info(msg)
		return ActionResult(extracted_content=msg)
	except Exception as e:
		logger.debug(f'Error in set_input_files: {str(e)}')
		return ActionResult(error=f'Failed to upload file to index {index}')


@controller.action('Scroll page to find elements', requires_browser=True)
async def scroll_page(browser: BrowserContext, scroll_amount: int = 300):
	"""
    Scrolls the page by a specified amount to find more elements.
    Returns True if scroll was successful, False if reached end of page.
    """
	try:
		# Get current scroll position using JavaScript
		current_scroll = await browser.evaluate_javascript('window.pageYOffset')

		# Scroll down by scroll_amount pixels
		await browser.evaluate_javascript(f'window.scrollBy(0, {scroll_amount})')

		# Get new scroll position
		new_scroll = await browser.evaluate_javascript('window.pageYOffset')

		# If we couldn't scroll further (reached bottom), return False
		if new_scroll == current_scroll:
			return ActionResult(extracted_content="Reached end of page", success=False)

		return ActionResult(extracted_content="Scrolled successfully", success=True)

	except Exception as e:
		return ActionResult(error=f"Error scrolling page: {str(e)}", success=False)


@controller.action('Find elements with scrolling', requires_browser=True)
async def find_elements_with_scroll(browser: BrowserContext, selector: str, max_scrolls: int = 10):
	"""
    Attempts to find elements matching the selector, scrolling if none are found.
    Returns the found elements or None if none are found after scrolling.
    """
	for i in range(max_scrolls):
		# Try to find elements using get_elements
		elements = await browser.get_elements(selector)

		if elements and len(elements) > 0:
			return ActionResult(
				extracted_content=f"Found {len(elements)} elements",
				success=True,
				elements=elements
			)

		# If no elements found, scroll and try again
		scroll_result = await scroll_page(browser)

		# If we can't scroll anymore, break
		if not scroll_result.success:
			break

		# Wait a bit for content to load
		await browser.evaluate_javascript('await new Promise(resolve => setTimeout(resolve, 1000))')

	return ActionResult(
		error="No elements found after scrolling",
		success=False
	)

browser = Browser(
	config=BrowserConfig(
		chrome_instance_path='C:/Program Files/Google/Chrome/Application/chrome.exe',
		disable_security=True,
	)
)


async def main():
	location = "Oakdale, Newyork"
	apply_task = (
	 	'You are a professional job researcher. '
	 	'1. Read my resume with read_cv'
	 	'2. Read the saved jobs file '
	 	'3. start applying to the links '
	 	'You can and should navigate through pages e.g. by scrolling '
	)
	ground_task = (
		'You are a professional job researcher. '
		'1. review my resume with read_cv'
		'2. Help me search for available junior python developer and data analyst jobs, or any positions that would fit my resume by looking at LinkedIn, Indeed, and other relevant sites'
		'3. Start applying to all jobs found and do not stop until you cannot find any more suitable jobs'
		'NEVER click element index:0 '
		'If you cannot find job listings or next/submit application buttons: '
		'   - Use find_elements_with_scroll to look for job listings '
		'   - Use scroll_page to navigate through the page '
		#'4. Save any relevant listings in a format for easy reference'
		'go to: '
		#f'search near {location}'
	)
	tasks = [
		# ground_task + '\n' + 'Start applying to jobs, or in the saved jobs file',
		#apply_task
		ground_task + '\n' + 'https://www.linkedin.com/jobs/search/?currentJobId=4119844312&distance=25&f_AL=true&f_WT=1%2C3&geoId=105241852&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&spellCorrectionEnabled=true',
		#ground_task + '\n' + 'https://www.indeed.com/',
		# ground_task + '\n' + 'Microsoft',
		# ground_task
		# + '\n'
		# + 'go to https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Taiwan%2C-Remote/Fulfillment-Analyst---New-College-Graduate-2025_JR1988949/apply/autofillWithResume?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7 NVIDIA',
		# ground_task + '\n' + 'Meta',
	]
	model = AzureChatOpenAI(
		model='gpt-4o',
		api_version='2024-10-21',
		api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
		azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
	)

	agents = []
	for task in tasks:
		agent = Agent(task=task, llm=model, controller=controller, browser=browser)
		agents.append(agent)

	await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':

	asyncio.run(main())