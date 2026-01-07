"""
LinkedIn Job Scraper
Scrapes LinkedIn for DevOps and Cloud Engineer jobs
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from urllib.parse import quote
import json

class LinkedInJobScraper:
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
    def build_search_url(self, job_title, location=""):
        """Build LinkedIn job search URL"""
        params = {
            'keywords': job_title,
            'location': location,
            'f_TPR': 'r86400',  # Last 24 hours (fresh jobs only)
            'f_E': '2%2C3',  # Entry level (2) AND Associate (3) - filters for both experience levels
            'position': '1',
            'pageNum': '0'
        }
        
        query_string = '&'.join([f"{k}={quote(str(v))}" for k, v in params.items()])
        return f"{self.base_url}?{query_string}"
    
    def scrape_jobs(self, job_titles, location="India"):
        """Scrape jobs for given titles"""
        all_jobs = []
        
        for job_title in job_titles:
            print(f"🔍 Searching for: {job_title}")
            url = self.build_search_url(job_title, location)
            
            try:
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(2, 5))
                
                response = requests.get(url, headers=self.headers, timeout=15)
                
                if response.status_code == 200:
                    jobs = self.parse_job_listings(response.text, job_title)
                    all_jobs.extend(jobs)
                    print(f"✅ Found {len(jobs)} jobs for {job_title}")
                else:
                    print(f"⚠️ Status code {response.status_code} for {job_title}")
                    
            except Exception as e:
                print(f"❌ Error scraping {job_title}: {str(e)}")
                
        return all_jobs
    
    def parse_job_listings(self, html_content, search_term):
        """Parse job listings from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Find job cards
        job_cards = soup.find_all('div', class_='base-card')
        
        if not job_cards:
            # Try alternative selectors
            job_cards = soup.find_all('div', {'class': lambda x: x and 'job' in x.lower()})
        
        for card in job_cards[:10]:  # Limit to first 10 jobs
            try:
                job = self.extract_job_info(card, search_term)
                if job:
                    jobs.append(job)
            except Exception as e:
                print(f"⚠️ Error parsing job card: {str(e)}")
                continue
        
        return jobs
    
    def extract_job_info(self, card, search_term):
        """Extract job information from a card"""
        try:
            # Extract job title
            title_elem = card.find('h3', class_='base-search-card__title')
            if not title_elem:
                title_elem = card.find('a')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Clean up title - remove asterisks if present
            if title and '*' in title:
                title = "Job Title Hidden"
            
            # Extract company name
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            if not company_elem:
                company_elem = card.find('a', {'class': lambda x: x and 'company' in x.lower()})
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Clean up company - remove asterisks if present
            if company and '*' in company:
                company = "Company Name Hidden"
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Clean up location - remove asterisks if present
            if location and '*' in location:
                location = "Location Hidden"
            
            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            if not link_elem:
                link_elem = card.find('a', href=True)
            job_url = link_elem['href'] if link_elem and link_elem.get('href') else "N/A"
            
            # Extract job ID from URL
            job_id = None
            if job_url != "N/A" and 'linkedin.com' in job_url:
                try:
                    job_id = job_url.split('/')[-1].split('?')[0]
                except:
                    job_id = str(hash(job_url))
            else:
                job_id = str(hash(f"{title}{company}"))
            
            # Extract posting time
            time_elem = card.find('time')
            posted_date = time_elem.get_text(strip=True) if time_elem else "Recently"
            
            job_data = {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'posted_date': posted_date,
                'search_term': search_term,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return job_data
            
        except Exception as e:
            print(f"⚠️ Error extracting job info: {str(e)}")
            return None
    
    def get_user_agent_list(self):
        """Return list of user agents for rotation"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    def rotate_user_agent(self):
        """Rotate user agent"""
        self.headers['User-Agent'] = random.choice(self.get_user_agent_list())


if __name__ == "__main__":
    scraper = LinkedInJobScraper()
    
    job_titles = ["DevOps Engineer", "Cloud Engineer"]
    location = "India"
    
    print("=" * 60)
    print("🚀 LinkedIn Job Scraper Started")
    print("=" * 60)
    
    jobs = scraper.scrape_jobs(job_titles, location)
    
    print("\n" + "=" * 60)
    print(f"📊 Total Jobs Found: {len(jobs)}")
    print("=" * 60)
    
    for job in jobs:
        print(f"\n📌 {job['title']}")
        print(f"   🏢 {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['url']}")
        print(f"   🕒 Posted: {job['posted_date']}")
