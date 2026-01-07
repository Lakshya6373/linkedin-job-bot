"""
Database Handler
Tracks seen jobs to avoid duplicate notifications
"""
import sqlite3
from datetime import datetime
import json

class JobDatabase:
    def __init__(self, db_path="jobs.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                url TEXT,
                posted_date TEXT,
                search_term TEXT,
                scraped_at TEXT,
                notified_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scrape_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scrape_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                jobs_found INTEGER,
                new_jobs INTEGER,
                search_terms TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized")
    
    def is_job_seen(self, job_id):
        """Check if job has been seen before"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT job_id FROM jobs WHERE job_id = ?', (job_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        return result is not None
    
    def add_job(self, job):
        """Add a new job to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO jobs (job_id, title, company, location, url, 
                                 posted_date, search_term, scraped_at, notified_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job['job_id'],
                job['title'],
                job['company'],
                job['location'],
                job['url'],
                job['posted_date'],
                job['search_term'],
                job['scraped_at'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            # Job already exists
            return False
        except Exception as e:
            print(f"❌ Error adding job to database: {str(e)}")
            return False
        finally:
            conn.close()
    
    def get_new_jobs(self, jobs):
        """Filter out jobs that have been seen before"""
        new_jobs = []
        
        for job in jobs:
            if not self.is_job_seen(job['job_id']):
                new_jobs.append(job)
                self.add_job(job)
        
        return new_jobs
    
    def log_scrape(self, jobs_found, new_jobs, search_terms):
        """Log scraping activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scrape_history (jobs_found, new_jobs, search_terms)
            VALUES (?, ?, ?)
        ''', (jobs_found, new_jobs, json.dumps(search_terms)))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total jobs tracked
        cursor.execute('SELECT COUNT(*) FROM jobs')
        total_jobs = cursor.fetchone()[0]
        
        # Total scrapes
        cursor.execute('SELECT COUNT(*) FROM scrape_history')
        total_scrapes = cursor.fetchone()[0]
        
        # Recent jobs (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM jobs 
            WHERE datetime(created_at) > datetime('now', '-1 day')
        ''')
        recent_jobs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_jobs': total_jobs,
            'total_scrapes': total_scrapes,
            'recent_jobs': recent_jobs
        }
    
    def get_recent_jobs(self, limit=10):
        """Get most recent jobs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, company, location, posted_date, created_at
            FROM jobs
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        jobs = cursor.fetchall()
        conn.close()
        
        return jobs
    
    def clear_old_jobs(self, days=30):
        """Clear jobs older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM jobs 
            WHERE datetime(created_at) < datetime('now', ? || ' days')
        ''', (f'-{days}',))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"🗑️ Cleared {deleted} old jobs")
        return deleted


if __name__ == "__main__":
    # Test database
    db = JobDatabase("test_jobs.db")
    
    # Test job
    test_job = {
        'job_id': 'test123',
        'title': 'DevOps Engineer',
        'company': 'Test Company',
        'location': 'Mumbai',
        'url': 'https://linkedin.com/jobs/test123',
        'posted_date': '2 days ago',
        'search_term': 'DevOps Engineer',
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("Testing database operations...")
    print(f"Is job seen? {db.is_job_seen('test123')}")
    print(f"Adding job: {db.add_job(test_job)}")
    print(f"Is job seen now? {db.is_job_seen('test123')}")
    
    stats = db.get_stats()
    print(f"\nDatabase stats: {stats}")
