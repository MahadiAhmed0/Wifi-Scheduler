import requests
from bs4 import BeautifulSoup

students = [
    {'id': 'userName', 'password': 'userPassword'},
    {'id': 'userName', 'password': 'userPassword'},
    {'id': 'userName', 'password': 'userPassword'},
    {'id': 'userName', 'password': 'userPassword'}
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
    min_usage = min(student_usage.values())
    min_students = [student for student, usage in student_usage.items() if usage == min_usage]
    
    if len(min_students) > 1:
        print(f"Students with minimum usage are: {', '.join(min_students)} with {min_usage} minutes each.")
    else:
        print(f"Student with minimum usage is {min_students[0]} with {min_usage} minutes.")
else:
    print("No student data found.")
