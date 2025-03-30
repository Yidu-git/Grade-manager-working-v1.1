import json
import eel
import os

data_file_dir = 'data.json'

dirname  = os.path.dirname(__file__ + 'Gui')

# eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

eel.init('Ui', allowed_extensions=['.html','.css','.js','.json'], js_result_timeout=1000)
Grade_count = 0

@eel

@eel.expose
def get_Grade_count():
    content  = read_data()
    Grade_count = len(content['Grades'])
    print(Grade_count)
    return str(Grade_count)

def read_data():
    with open(data_file_dir,'r') as f:
        content = json.loads(f.read())
        return content
 
def write_data(content):
    with open(data_file_dir,'w') as f:
        f.write(json.dumps(content))
    return content

if not os.path.exists(data_file_dir):
    with open(data_file_dir,'x') as file:
        file.write(json.dumps({'Grades':[],'Subjects':[],'Types': [],'User-settings':{'Theme':'Systemm','Color-scheme':"purple"}}))

else:
    content  = read_data()
    Grade_count = len(content['Grades'])

def clean_up_grades():
    content = read_data()
    for grade in content['Grades']:
        if not '/' in grade['Grade']:
            grade['Grade'] = str(int(grade['Grade']))
    write_data(content)

clean_up_grades()

@eel.expose
def check_gradecount():
    global Grade_count

    content = read_data()
    for grade in content['Grades']:
        if int(grade['id']) > (Grade_count + 1):
            grade['id'] = Grade_count + 1
            Grade_count += 1
    write_data(content)

@eel.expose
def get_average(subject,type):
    content = read_data()
    grades = []

    if subject == '' and type == '' :
        average = get_grades_average()
        return average

    elif subject == '':
        average = get_type_average(type)
        print(type)
    elif type == '':
        average = get_subject_average(subject)
        print(subject)
    
    else:
        for grade in content['Grades']:
            if grade['Subject'] == subject and grade['Type'] == type :
                grades.append(grade['Grade'])
        average = calculate_average(grades)
    print(calculate_average(grades))
    return average

@eel.expose
def print_test():
    print('Test successful')

# @eel.expose
# def return_test():
#     return 'Science'

@eel.expose
def read_subjects():
    content = read_data()
    return content['Subjects']

@eel.expose
def add_subject(subject):
    content = read_data()
    content['Subjects'].append(subject)
    write_data(content)

@eel.expose
def remove_subject(subject):
    content = read_data()
    content['Subjects'].remove(subject)
    write_data(content)

@eel.expose
def reset_subjects():
    content = read_data()
    content['Subjects'].clear()
    write_data(content)

@eel.expose
def check_rating(score) :
    if isinstance(score,str):
        score = float(score)
    if score >= 90:
        return 'A'
    if score >= 80:
        return 'B'
    if score >= 70:
        return 'C'
    if score >= 56:
        return 'D'
    if score <= 55:
        return 'F'

@eel.expose
def save_type(type):
    content = read_data()
    content['Types'].append(type)
    write_data(content)

@eel.expose
def get_types():
    content = read_data()
    return content['Types']

eel.expose
def type_exists(type):
    content = read_data()
    if type in content['Types'] : return True
    else : return False

@eel.expose
def get_type_average(type):
    if type_exists(type):
        content = read_data()
        grades = []
        for grade in content['Grades'] :
            if grade['Type'] == type:
                grades.append(grade['Grade'])
        average = calculate_average(grades)
        return average
    else : return 'Type does not exist'

#saves a grade based on given data
@eel.expose
def save_grade(subject,grade,type):
    global Grade_count

    new_grade = {
        'id': Grade_count +1,
        'Subject' : subject,
        'Grade' : grade,
        'Type' : type,
    }

    content = read_data()
    content['Grades'].append(new_grade)

    write_data(content)
    Grade_count += 1

@eel.expose 
def get_grades():
    return read_data()

def is_fraction(string:str):
    if '/' in string : return True
    else : return False

def fraction_convert(value:str):
    v,t = value.split('/')
    newValue = (float(v)/float(t))*100
    return newValue

def calculate_average(grades:list):
    total = 0
    for grade in grades:
        if type(grade) == str:
            if is_fraction(grade):
                grade = fraction_convert(grade)
            else:
                grade = float(grade)
        total += grade
    if len(grades) != 0:
        average = round(total/len(grades),2)
        return average
    else: return 0

@eel.expose
def get_grades_average():
    content = read_data()
    grades = []
    for grade in content['Grades']:
        grades.append(grade['Grade'])
    #     print(grade)
    # print(grades)
    average = calculate_average(grades)
    return average

def subject_exists(subject):
    content = read_data()
    if subject in content['Subjects']: return True
    else: return False


@eel.expose
def get_subject_average(subject):
    if subject_exists(subject):
        content = read_data()
        grades = []
        for grade in content['Grades'] :
            if grade['Subject'] == subject:
                grades.append(grade['Grade'])
        average = calculate_average(grades)
        return average
    else : return 'Subject does not exist'

# print(get_grades_average())

# deletes grades based on given id
@eel.expose
def delete_grade(id):
    global Grade_count

    check_gradecount()

    print(id)

    content = read_data()
    for grade in content['Grades']:
        if grade['id'] == int(id):
            content['Grades'].remove(grade)

    write_data(content)
    Grade_count -= 1


#Removes all grades
@eel.expose
def reset_grades():
    global Grade_count
    Grade_count = 0
    
    content = read_data()
    content['Grades'].clear()
    write_data(content)

@eel.expose 
def save_settings(theme,scheme) :
    content = read_data()
    content["User-settings"]["Theme"] = theme
    content["User-settings"]["Color-scheme"] = scheme
    write_data(content)

@eel.expose
def get_settings():
    content = read_data()
    return content['User-settings']

@eel.expose
def reset_settings():
    content = read_data()
    content['User-settings'].clear()
    write_data(content)

eel.start("Gui.html",size=(500,600))