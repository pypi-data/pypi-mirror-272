def ArabuEn(Input):
    Num_Map = {
        '௦': '0',
        '௧':'1',
        '௨': '2',
        '௩': '3',
        '௪': '4',
        '௫': '5',
        '௬': '6',
        '௭': '7',
        '௮': '8',
        '௯': '9',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        if '.' not in result:
            return int(result)
        else:
            return float(result)
    else:
        return 'தவறான உள்ளீடு'


def ArabuSutru(Input):
    Num_Map = {
        '௦': '0',
        '௧':'1',
        '௨': '2',
        '௩': '3',
        '௪': '4',
        '௫': '5',
        '௬': '6',
        '௭': '7',
        '௮': '8',
        '௯': '9',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        result=float(result)
        return round(result)
    else:
        return 'தவறான உள்ளீடு'


def Eevu(a,b):
    Input= a/b
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.' or Input[i]=='-':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if result!=None:
        return result
    else:
        return 'தவறான உள்ளீடு'

def Kazhithal(a,b):
    Input= a-b
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.' or Input[i]=='-':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if result!=None:
        return result
    else:
        return 'தவறான உள்ளீடு'


def Koottal(a,b):
    Input= a+b
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        return result
    else:
        return 'தவறான உள்ளீடு'


def Meedhi(a,b):
    Input= a%b
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.' or Input[i]=='-':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if result!=None:
        return result
    else:
        return 'தவறான உள்ளீடு'


def Perukkal(a,b):
    Input= a*b
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.' or Input[i]=='-':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if result!=None:
        return result
    else:
        return 'தவறான உள்ளீடு'


def Perumam(a,b):
    Input=max(a,b)
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        return result
    else:
        return 'தவறான உள்ளீடு'


def Sirumam(a,b):
    Input=min(a,b)
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        return result
    else:
        return 'தவறான உள்ளீடு'


def TamilEn(Input):
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        return result
    else:
        return 'தவறான உள்ளீடு'


def TamilSutru(Input):
    Num_Map = {
        '0': '௦',
        '1': '௧',
        '2': '௨',
        '3': '௩',
        '4': '௪',
        '5': '௫',
        '6': '௬',
        '7': '௭',
        '8': '௮',
        '9': '௯',
        '-': '-',
        '.': '.'
    }
    Input=round(Input)
    Input=str(Input)
    result=''
    Length=len(Input)
    Count=0
    for i in range(Length):
        if Input[i].isdigit() or Input[i]=='.':
            result+=str(Num_Map[Input[i]])
            Count+=1
        else:
            break
    if Length==Count:
        return result
    else:
        return 'தவறான உள்ளீடு'
