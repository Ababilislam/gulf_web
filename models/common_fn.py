# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from random import randint



def getStrSl():
    slStr=''
    #-------------- get random number
    randNum=randint(100, 999)            
    #date_fixed = 2012-07-01 11:48:10.000012
    yy=str(date_fixed)[2:4]
    mm=str(date_fixed)[5:7]  
    dd=str(date_fixed)[8:10]
    hh=str(date_fixed)[11:13] 
    mn=str(date_fixed)[14:16] 
    ss=str(date_fixed)[17:19] 
    ms=str(date_fixed)[20:26]        
    slStr=yy+mm+dd+'.'+hh+mn+ss+'.'+ms+'.'+str(randNum)
    
    return slStr


#-------------------------------- role access check
def check_role(task_id):
    t_id=task_id
    
    is_valid_role=False
    
    task_listStr=session.task_listStr
#    return task_listStr
    taskList=str(task_listStr).split(',')
    for i in range(len(taskList)):
        taskid=taskList[i]
        if taskid==t_id:
            is_valid_role=True
            break
        else:
            continue
    
    return is_valid_role

#-------------------------------
def get_mydate(gmt_time):
    import datetime;
    if gmt_time==None:
        gmt_time=0
    
    my_date =datetime.datetime.now()+ datetime.timedelta(hours=gmt_time);
    session.my_date=my_date
    return my_date;


#======================
def check_special_char(strData):
    strData=strData.replace("@", " ")
    strData=strData.replace("<", " ")
    strData=strData.replace(">", " ")
    strData=strData.replace("(", " ")
    strData=strData.replace(")", " ")
    strData=strData.replace("{", " ")
    strData=strData.replace("}", " ")
    strData=strData.replace("[", " ")
    strData=strData.replace("]", " ")
    strData=strData.replace(",", " ")
    strData=strData.replace("`", " ")
    strData=strData.replace("'", " ")
    strData=strData.replace('"', ' ')
    strData=strData.replace("*", " ")
    strData=strData.replace("#", " ")
    strData=strData.replace(";", " ")
    strData=strData.replace("-", " ")    
    return strData

def check_special_char_id(strData):
    strData=strData.replace("@", "")
    strData=strData.replace("<", "")
    strData=strData.replace(">", "")
    strData=strData.replace("(", "")
    strData=strData.replace(")", "")
    strData=strData.replace("{", "")
    strData=strData.replace("}", "")
    strData=strData.replace("[", "")
    strData=strData.replace("]", "")
    strData=strData.replace(",", "")
    strData=strData.replace("`", "")
    strData=strData.replace("'", "")
    strData=strData.replace('"', '')
    strData=strData.replace("*", "")
    strData=strData.replace("#", "")
    strData=strData.replace(";", "")
    strData=strData.replace(" ", "")
    strData=strData.replace("/", "")
    strData = strData.replace(".", "")
    return strData
#---------------------Encript data
import random

def get_encript(mystr):
    randNumberLength=2
    add_with_ascii=333
    add_eightbit_string='34523434'
    ascii_for_string_full=''
    
    str_single_char=list(mystr)
    
    total=len(str_single_char)
    
    for i in range(total):
        str_single= ord(str_single_char[i])+add_with_ascii
        ascii_for_string_full=ascii_for_string_full+str(str_single)
    
    strlength=len(ascii_for_string_full)

    randNumber = random.randint(1, 99)

    if (randNumber > strlength):
        randNumber = random.randint(1, strlength-1)
    
    if(randNumber<10):
        randNumber='0'+str(randNumber)
   
    firstpart=ascii_for_string_full[0:int(randNumber)]
    secondpart=ascii_for_string_full[int(randNumber):]    
    encripted=str(randNumber)+firstpart+add_eightbit_string+secondpart    
    
    return encripted


#-------------------------------- Decript data
def get_decript(mystr):
    
    digit_flag=mystr.isdigit()
    string_for_ascii_full=''
    
    if digit_flag:
        add_with_ascii=333
        add_eightbit_string='34523434'
        randNumber=int(mystr[0:2])
        ascii_with_eightbit_string=mystr[2:]
        
        firstPart=ascii_with_eightbit_string[0:randNumber]        
        secondPart_withstring=ascii_with_eightbit_string[randNumber:]
        
        eight_bit_string=secondPart_withstring[0:8]

        if(eight_bit_string==add_eightbit_string):

            secondPart=secondPart_withstring[8:]
            mainString=str(firstPart)+str(secondPart)
        
            
            ascii_single=[]
            chval=''
            for ch in mainString:
                chval+=ch
                if len(chval)==3:
                    ascii_single.append(chval)
                    chval=''
                else:
                    continue
                
            total=len(ascii_single)
        
            for i in range(total):
                
                single_ascii= int(ascii_single[i])-add_with_ascii
                single_ascii=unichr(single_ascii)
                string_for_ascii_full=string_for_ascii_full+single_ascii

            return string_for_ascii_full

        else:
            return string_for_ascii_full
      
    else:
        return string_for_ascii_full
