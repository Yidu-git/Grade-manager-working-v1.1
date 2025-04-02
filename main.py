import json
import eel
import os

# default_data_file_dir = 'data.json'
default_data_file_dir = ''
user_data_file_dir = 'UserData.json'
CurrentVersion = 1.2

dirname  = os.path.dirname(__file__ + 'Gui')

# eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

if __name__ == '__main__' :
    eel.init('Ui', allowed_extensions=['.html','.css','.js','.json'], js_result_timeout=1000)
Grade_count = 0

@eel.expose
def get_Grade_count():
    content  = read_data()
    Grade_count = len(content['Grades'])
    print(Grade_count)
    return str(Grade_count)

def read_data(dataLocation=''):
    print(default_data_file_dir)
    if dataLocation == '':
        dataLocation = default_data_file_dir
    with open(dataLocation,'r') as f:
        content = json.loads(f.read())
        # print(content)
        return content

@eel.expose
def openFile(path):
    global default_data_file_dir
    print(path)
    print(read_data())
    content = read_data(user_data_file_dir)
    content['User-settings']['Current-File'] = path
    write_data(content,user_data_file_dir)
    default_data_file_dir = path

def write_data(content,dataLocation=''):
    if dataLocation == '':
        dataLocation = default_data_file_dir
    with open(dataLocation,'w') as f:
        f.write(json.dumps(content))
    return content

def applySettings():
    global default_data_file_dir
    data = read_data(user_data_file_dir)
    default_data_file_dir = data['User-settings']['Current-File']

if __name__ == '__main__':
    applySettings()
    print(default_data_file_dir)
    if not os.path.exists(default_data_file_dir):
        with open(default_data_file_dir,'x') as file:
            file.write(json.dumps({'Grades':[],'Subjects':[],'Identifiers': [],'Version':CurrentVersion}))

    else:
        content  = read_data()
        Grade_count = len(content['Grades'])

    if not os.path.exists(user_data_file_dir):
        with open(user_data_file_dir,'x') as file:
            file.write(json.dumps({'User-settings':{'Theme':'Systemm','Color-scheme':"purple",'Current-File' : 'data.json'}}))

def clean_up_grades():
    content = read_data()
    for grade in content['Grades']:
        if not '/' in grade['Grade']:
            grade['Grade'] = str(int(grade['Grade']))
        if grade['Subject'] not in content['Subjects']:
            content['Subjects'].append(grade['Subject'])
    write_data(content)

if __name__ == '__main__':
    applySettings()
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
def get_average(subject,identifier,absolute=False):
    content = read_data()
    grades = []

    if subject == '' and identifier == '' :
        average = get_grades_average()
        return average

    elif subject == '':
        average = get_identifier_average(identifier,absolute)
        print(identifier)
    elif identifier == '':
        average = get_subject_average(subject)
        print(subject)
    
    else:
        for grade in content['Grades']:
            gradeIdentifiers = grade['Identifiers'].split(' ')
            if absolute:
                identifierCount = 0
                Identifier = False
                for i in gradeIdentifiers:
                    if i in identifier.split(' '):
                        identifierCount += 1
                if identifierCount == len(identifier.split(' ')): Identifier = True
                if grade['Subject'] == subject and Identifier :
                    grades.append(grade['Grade'])
            else:
                Identifier = False
                for i in gradeIdentifiers:
                    if i in identifier.split(' '):
                        Identifier = True
                if Identifier and grade['Subject'] == subject:
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
def save_identifier(identifier):
    content = read_data()
    Identifiers = identifier.split(' ')
    for i in Identifiers:
        content['Identifiers'].append(i)
    write_data(content)

@eel.expose
def get_identifiers():
    content = read_data()
    return content['Identifiers']

@eel.expose
def identifier_exists(type):
    content = read_data()
    if type in content['Identifiers'] : return True
    else : return False

@eel.expose
def get_identifier_average(identifiers,Absolute=True):
    if ' ' in identifiers:
        Identifiers = identifiers.split(' ')
        print(identifiers)
        print(Identifiers)
        exists = False
        existsCount = 0
        for i in identifiers.split(' '):
            if identifier_exists(identifiers): existsCount += 1
            else : return 'One or more Identifiers do not exist'
        
        if existsCount == len(identifiers): exists = True

        if exists:
            content = read_data()
            grades = []

            for grade in content['Grades'] :
                gradeIdentifiers = grade['Identifiers'].split(' ')
                Exists = False
                ExistCount = 0
                for i in gradeIdentifiers:
                    if Absolute:
                        if i in identifiers: ExistCount += 1
                        if ExistCount == len(identifiers): Exists = True
                    else:
                        if i in identifiers: Exists = True
                if Exists:
                    grades.append(grade['Grade'])
            average = calculate_average(grades)
            return average
    else:
        if identifier_exists(identifiers):
            content = read_data()
            grades = []
            for grade in content['Grades'] :
                gradeIdentifiers = grade['Identifiers']
                if Absolute:
                    if grade['Identifiers'] == identifiers:
                        grades.append(grade['Grade'])
                else: 
                    if identifiers in gradeIdentifiers:
                        grades.append(grade['Grade'])
            average = calculate_average(grades)
            return average
        else : return 'identifier does not exist'

#saves a grade based on given data
@eel.expose
def save_grade(subject,grade,identifiers='',tags=''):
    global Grade_count

    new_grade = {
        'id': Grade_count +1,
        'Subject' : subject,
        'Grade' : grade,
        'Identifiers' : identifiers,
        'Tags' : tags,
    }

    content = read_data()
    content['Grades'].append(new_grade)

    write_data(content)
    Grade_count += 1

@eel.expose
def get_grades(sorted=False,accending=False):
    content = read_data()['Grades']
    print(sorted)
    if sorted:
        quickDictSoct(content,'Grade',True)
        printDict(content)
        if accending:
            content.reverse()
    return content

def is_fraction(string:str):
    if '/' in string : return True
    else : return False

@eel.expose
def fraction_convert(value:str):
    v,t = value.split('/')
    newValue = (float(v)/float(t))*100
    return round(newValue,2)

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
    content = read_data(user_data_file_dir)
    content["User-settings"]["Theme"] = theme
    content["User-settings"]["Color-scheme"] = scheme
    write_data(content,user_data_file_dir)

@eel.expose
def get_settings():
    content = read_data(user_data_file_dir)
    return content['User-settings']

@eel.expose
def reset_settings():
    content = read_data(user_data_file_dir)
    content['User-settings'].clear()
    write_data(content,user_data_file_dir)

@eel.expose
def quick_sort(List,left=0,right=None ):
    if right == None : right=len(List) - 1
    if left < right :
        paratitionPos = praratition(List,left,right)
        quick_sort(List,left,paratitionPos - 1)
        quick_sort(List,paratitionPos + 1,right)

def praratition(List,left,right,dict=False,VK=None,DictList=False):
        i = left
        j = right - 1
        pivot = List[right]
        # print(List[right])

        if not dict:
            while i < j:
                while i < right and List[i] < pivot:
                    i += 1
                while j > left and List[j] >= pivot:
                    j -= 1
                if i < j:
                    List[i],List[j] = List[j],List[i]
            if List[i] > pivot:
                List[i], List[right] = List[right], List[i]
        if dict and VK != None and not DictList:
            while i < j:
                while i < right and List[i][VK] < pivot[VK]:
                    i += 1
                while j > left and List[j][VK] >= pivot[VK]:
                    j -= 1
                if i < j:
                    List[i],List[j] = List[j],List[i]
        if dict and VK != None and DictList:
            while i < j:
                while i < right and List[i][VK] < pivot[VK]:
                    # print('awd', List[i][VK],'  ',pivot[VK] ,right,i,j)
                    i += 1
                while j > left and List[j][VK] >= pivot[VK]:
                    j -= 1
                if i < j:
                    # print(List[i][VK],List[j][VK])
                    List[i],List[j] = List[j],List[i]
                    # print(List[i][VK],List[j][VK])
            if List[i][VK] > pivot[VK]:
                List[i], List[right] = List[right], List[i]
        return i

@eel.expose
def quickDictSoct(Dict,ValueKey,List=False,left=0,right=None):
    if right == None:
        right = len(Dict) - 1
    # print('L & R : ',left,right)

    if not List:
        for i in Dict:
            if '/' in str(Dict[ValueKey]):
                Dict[ValueKey] = fraction_convert(Dict[ValueKey])
            if type(Dict[ValueKey]) == str:
                Dict[ValueKey] == float(Dict[ValueKey])
    
        if left < right:
            praratitionPos = praratition(Dict,left,right,True,ValueKey)
            quickDictSoct(Dict,ValueKey,False,left, praratitionPos - 1)
            quickDictSoct(Dict,ValueKey,False, praratitionPos + 1,right)
    if List:
        for i in Dict:
            if '/' in str(i[ValueKey]):
                i[ValueKey] = fraction_convert(i[ValueKey])
            if type(i[ValueKey]) == str:
                i[ValueKey] == float(i[ValueKey])
        if left < right:
            praratitionPos = praratition(Dict,left,right,True,ValueKey,True)
            quickDictSoct(Dict,ValueKey,True,left, praratitionPos - 1)
            quickDictSoct(Dict,ValueKey,True, praratitionPos + 1,right)

def printDict(dict):
    for i in dict:
        print(i['id'],'|',i['Subject'],'|',i['Identifiers'],'|','\033[93m',i['Grade'],'| \033[0m')

if __name__ == '__main__' :
    eel.start("Gui.html",size=(500,600))