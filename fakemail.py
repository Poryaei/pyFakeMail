import yaml, requests

class DatabaseManager:
    def __init__(self, filename='db.yaml'):
        self.filename = filename
        self.load_db()
        
    def load_db(self):
        try:
            with open(self.filename) as f:
                self.data = yaml.safe_load(f)  
        except FileNotFoundError:
            self.data = {}
            
    def save_db(self):
        with open(self.filename, 'w') as f:      
            yaml.dump(self.data, f)
            
    def get(self, key):
        return self.data[key] 
        
    def set(self, key, value):  
        self.data[key] = value
        self.save_db()
    
    def delete(self, key):
        del self.data[key]
        self.save_db()

proxies = None

session = requests.Session()
session.headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

session.proxies = proxies

db = DatabaseManager()



def create_mail():
    # global session
    session = requests.Session()
    session.headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    session.proxies = proxies
    
    r = session.get('https://www.fakemail.net/', timeout=5)
    h = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    h['Cookie'] = r.headers['Set-Cookie']
    r = session.get('https://www.fakemail.net/index/index', headers=h)
    email = json.loads(r.text.encode())['email']
    db.set(f'temp_mail_cookie_{email}', r.headers['Set-Cookie'])
    db.set('temp_mail_address', email)
    add_expire(email)
    return email

def add_expire(email: str):
    h = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        'Cookie': db.get(f'temp_mail_cookie_{email}')
    }
    
    r = session.get('https://www.fakemail.net/expirace/1209600', headers=h)

def get_emails(email: str):
    h = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        'Cookie': db.get(f'temp_mail_cookie_{email}')
    }
    
    r = session.get('https://www.fakemail.net/index/refresh', headers=h)
    h['Reffer'] = 'https://www.fakemail.net/window/id/2'
    r = session.get('https://www.fakemail.net/email/id/2', headers=h)
    add_expire(email)
    return r.text
