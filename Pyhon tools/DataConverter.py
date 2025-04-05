import os
import json
from main import CurrentVersion,read_data,write_data

def convert(dataLocation:str,DataVersion:float='',ConvertVersion:float=CurrentVersion):
    if os.path.exists(dataLocation):
        Data = read_data(dataLocation)
        if DataVersion == '' :
            try:
                DataVersion = Data['Version']
            except KeyError:
                DataVersion = 1.0
        if ConvertVersion == CurrentVersion:
            if DataVersion < ConvertVersion :
                KeepUserData = input('Would you like to convert settings in a new file? (Y/N) >> ')
                if KeepUserData == 'y' or 'Y' :
                    try:
                        UserData = {"User-Settings" :Data['User-settings']}
                    except:
                        UserData = {"Theme": "system", "Color-scheme": "purple"}
                        NoUserSettings = True
                    with open(f'{dataLocation.replace('.json','')}UserData.Json','w') as f:
                        f.write(json.dumps(UserData))
                    # if not NoUserSettings:
                    try:
                        Data.pop('User-settings')
                    except: pass
                elif KeepUserData == 'N' or 'n' or '' :
                    try:
                        Data.pop('User-settings')
                        print('User Settings Deleted')
                    except : pass
                
                print(Data)
                try:
                    Data.update({'Identifiers' : Data['Types']})
                    Data.pop('Types')
                except: pass

                try:
                    Data.update({'ExtraMarks' : {}})
                    for i in Data['Subjects']:
                        Data['ExtraMarks'].update({i:0})
                except: pass

                #Updating grades
                if DataVersion == 1.0:
                    for grade in Data['Grades']:
                        print(grade)
                        try:
                            grade.update({'Identifiers' : grade['Type']})
                            grade.pop('Type')
                        except: pass
                        try:
                            grade.update({'Comments' : ''})
                        except: pass

                Data['Version'] = DataVersion

                print(Data)
                write_data(Data,dataLocation)

            if DataVersion > ConvertVersion:
                convert = input('Are you sure you want to convert to a past version? (Y/n) >> ')
            if DataVersion == ConvertVersion:
                print('\033[93 mVersions are the same \033[0m')
            
            write_data(Data,dataLocation)
    else : 
        print('\033[91mLocatioin does not exist \033[0m')

convert('Maindata.json',1.0)