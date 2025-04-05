if __name__ == '__main__' :
    from main import fraction_convert,read_data

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
        print(List[right])

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
                    print('awd', List[i][VK],'  ',pivot[VK] ,right,i,j)
                    i += 1
                while j > left and List[j][VK] >= pivot[VK]:
                    j -= 1
                if i < j:
                    print(List[i][VK],List[j][VK])
                    List[i],List[j] = List[j],List[i]
                    print(List[i][VK],List[j][VK])
            if List[i][VK] > pivot[VK]:
                List[i], List[right] = List[right], List[i]
        return i


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

def Sort_data(DataList,ValueLoc=None,accending=True,left=0,right=None):
    if type(DataList) == list:
        quick_sort(DataList,left,right)
        if not accending:
            DataList.reverse()

def printDict(dict):
    for i in dict:
        print(i['id'],'|',i['Subject'],'|',i['Identifiers'],'|','\033[93m',i['Grade'],'| \033[0m')

if __name__ == '__main__':
    # List = [10, 20, 30, 50, 50, 19]
    List = []
    # quick_sort(List)
    # print(List)

    content = read_data('Maindata.json')
    Grades = content['Grades']
    for i in Grades:
        List.append(fraction_convert(str(i['Grade'])))
    quick_sort(List)
    print(List)
    printDict(Grades)
    quickDictSoct(Grades,'Grade',True)
    printDict(Grades)