# Real LinkedIn scraper using Selenium (headless, Edge)
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import time

load_dotenv()

linkedin_username = os.getenv('LINKEDIN_USERNAME')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

def find_prospects(campaign):

    # NOTE: This is a placeholder. Real scraping requires valid LinkedIn credentials and is against LinkedIn's TOS. Use at your own risk.
    edge_options = Options()
    # edge_options.add_argument('--headless')  # Disable headless for debugging
    edge_options.add_argument('--disable-gpu')
    # Use a persistent Edge user profile directory (ensure this folder exists)
    edge_options.add_argument(r'--user-data-dir=C:\Users\srini\edge_profile')
    # Use a common user-agent string
    edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    # Update the path below to the actual location of msedgedriver.exe
    service = Service("C:/Users/srini/Downloads/edgedriver_win64 (1)/msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.maximize_window()

    print("[DEBUG] Navigating to LinkedIn login page...")
    driver.get('https://www.linkedin.com/login')
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    try:
        # Wait for login form or check if already logged in
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'username')))
        driver.find_element(By.ID, 'username').send_keys(linkedin_username)
        driver.find_element(By.ID, 'password').send_keys(linkedin_password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        print("[DEBUG] Submitted login form.")
        time.sleep(5)
        print(f"[DEBUG] After login, current URL: {driver.current_url}")
    except Exception as e:
        # If login form not found, maybe already logged in
        print(f"[WARN] Login form not found or error: {e}")
        print(f"[DEBUG] Current URL: {driver.current_url}")
        # If already on feed or search, continue; else, quit
        if not ("feed" in driver.current_url or "search" in driver.current_url):
            print("[ERROR] Not logged in and not on search/feed page. Exiting.")
            driver.quit()
            return []

    # Step 1: Try to close overlays/popups if present
    try:
        close_btns = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Dismiss"], button[aria-label="Close"], button.msg-overlay-bubble-header__control--new-convo-btn')
        for btn in close_btns:
            try:
                btn.click()
                print("[DEBUG] Closed overlay/popup.")
            except Exception:
                pass
    except Exception as e:
        print(f"[DEBUG] No overlays to close or error: {e}")


    # Build a more targeted search query using industry and job roles
    job_roles = ''
    if hasattr(campaign, 'ideal_job_roles'):
        if isinstance(campaign.ideal_job_roles, list):
            job_roles = ' '.join([str(j).strip() for j in campaign.ideal_job_roles])
        else:
            job_roles = str(campaign.ideal_job_roles)
    keywords = f"{campaign.target_industry} {job_roles}".strip().replace(',', ' ')
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords.replace(' ', '%20')}"
    print(f"[DEBUG] Navigating to search URL: {search_url}")
    driver.get(search_url)
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.reusable-search__result-container, div.entity-result')))
    except Exception as e:
        print(f"[ERROR] Timed out waiting for search results: {e}")

    # Step 2: Scroll to load more results
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Step 3: Use robust selectors for profile cards
    prospects = []
    profiles = driver.find_elements(By.CSS_SELECTOR, 'div.siGDJRxnpwpECUuMWIuTIEYAEgtgJGVUk')
    print(f"[DEBUG] Found {len(profiles)} profiles on search page.")
    if len(profiles) == 0:
        print("[DEBUG] No profiles found. Dumping page HTML for inspection:")
        print(driver.page_source)
        print("[ACTION REQUIRED] No profiles found. Please check the browser window for popups, overlays, or captchas. Solve any captcha or close overlays, then press Enter here to continue...")
        input("Press Enter to close the browser and continue...")
    for profile in profiles[:5]:  # Limit to 5 for demo
        try:
            # Try multiple selectors for name/title/company
            name = ""
            try:
                name = profile.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text, span[dir="ltr"]').text
            except Exception:
                pass
            title = ""
            try:
                title = profile.find_element(By.CSS_SELECTOR, 'div.entity-result__primary-subtitle, div.t-14.t-black.t-normal').text
            except Exception:
                pass
            company = ""
            try:
                company = profile.find_element(By.CSS_SELECTOR, 'div.entity-result__secondary-subtitle, div.t-14.t-black.t-normal.t-entity-company-name').text
            except Exception:
                pass
            profile_url = ""
            try:
                profile_url = profile.find_element(By.CSS_SELECTOR, 'a.app-aware-link, a[data-control-name="search_srp_result"]').get_attribute('href')
            except Exception:
                pass
            print(f"[DEBUG] Prospect: {name}, {title}, {company}, {profile_url}")
            if name and profile_url:
                prospects.append({
                    'name': name,
                    'title': title,
                    'company': company,
                    'location': '',
                    'profile_url': profile_url,
                    'summary': '',
                })
        except Exception as e:
            print(f"[ERROR] Error extracting profile: {e}")
            continue

    print("[ACTION REQUIRED] Review the browser window. When you are done, press Enter here to close the browser and continue...")
    input("Press Enter to close the browser and continue...")
    driver.quit()
    print(f"[DEBUG] Returning {len(prospects)} prospects.")
    return prospects
