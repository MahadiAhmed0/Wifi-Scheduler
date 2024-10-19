import requests
from bs4 import BeautifulSoup

students = [
    {'id': 'mahadiahmed', 'password': 'Mahadisea123'},
    {'id': 'hasibulkarim', 'password': 'Hasrim809'},
    {'id': 'ridwankhan', 'password': 'Ridhan736'},
    {'id': 'muhtasimzawad', 'password': 'Muhwad445'}
]

def login_to_iut_user(username, password):
    login_url = "http://10.220.20.12/index.php/home/loginProcess"
    session = requests.Session()

    payload = {
        'username': username,
        'password': password
    }

    response = session.post(login_url, data=payload)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        total_use_row = soup.find('td', string='Total Use:')
        
        if total_use_row:
            total_use_text = total_use_row.find_next('td').text
            return total_use_text.strip()  # Correctly calling strip()
    
    return None

def fetch_user_data(student, student_usage):
    total_use = login_to_iut_user(student['id'], student['password'])
    if total_use is not None:
        student_usage[student['id']] = int(total_use.split()[0])  # Assuming the format is "X Minutes"
        print(f"{student['id']} has used {total_use}.")
    else:
        print(f"Failed to log in as {student['id']}.")

student_usage = {}

for student in students:
    fetch_user_data(student, student_usage)

if student_usage:
    min_student = min(student_usage, key=student_usage.get)
    print(f"Student with minimum usage is {min_student} with {student_usage[min_student]} minutes.")
else:
    print("No student data found.")
