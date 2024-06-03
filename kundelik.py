from kunapipy.kundelik import kundelik
from datetime import datetime
from datetime import timedelta, date

# Получаем доступ через логин и пароль

def get_token(login, password):
    dn = kundelik.KunAPI(login=login, password=password) 
    return dn.get_token(login=login, password=password)

def get_schools(token):
    dn = kundelik.KunAPI(token=token)
    return dn.get_school()

def get_hw(token, date):

    dn = kundelik.KunAPI(token=token)
    lessons = [];
    lessonid = [];
    school = get_schools(token=token)[0]['id']
    day = str(date).split()[0]

    for i in range (0, len(dn.get_school_homework(school, date, date)['subjects'])):
        if dn.get_school_homework(school, date, date)['subjects']:
            lessons.append(dn.get_school_homework(school, date, date)['subjects'][i]['name'])
            lessonid.append(dn.get_school_homework(school, date, date)['subjects'][i]['id'])

    homework =[]
    for i in range (0, len(dn.get_school_homework(school, date, date)['works'])):

        if dn.get_school_homework(school, date, date)['works'][i]['targetDate'] == f"{day}T00:00:00":
            if dn.get_school_homework(school, date, date)['works'][i]['type'] == "Homework":
                homework.append([dn.get_school_homework(school, date, date)['works'][i]['text'], lessons[lessonid.index(dn.get_school_homework(school, date, date)['works'][i]['subjectId'])]])
                
    
    lessons.clear()
    lessonid.clear()
    return homework



def get_marks(token):
    out = """"""

    dn = kundelik.KunAPI(token=token)

    school = get_schools(token=token)[0]['id']
    
    context = dn.get_context()
    user_id = context["personId"]
    school_id = context["schoolIds"][0]



    # все оценки юзера
    marks = dn.get_person_marks(
        user_id,
        school_id,
        start_time=datetime.now() - timedelta(weeks=10),
    )
    goodmarks = 0
    allmarks = 0
    for i in range(0,len(marks)):
        
        first_mark = marks[i]
        color = ""
        a = i+1
        
        mark_subject = dn.get_lesson_info(first_mark["lesson"])
            
        if int(first_mark['textValue']) > 0:
            color = "🔴"

        if int(first_mark['textValue']) > 4:
            color = "🟡"

        if int(first_mark['textValue']) > 6 :
            color = "🟢"
            goodmarks = goodmarks + 1
        
        allmarks = allmarks + 1
        out = out + f"{first_mark['textValue']} по предмету {mark_subject['subject']['name']}" +f" {color} " + '\n'

    out = out + "\n"
    out = out + str(int((goodmarks*100)/allmarks)) + "%" + " Хороших оценок"

    return out


if __name__ == "__main__":
    print(get_marks("keEOMuKoSD2IesMI5DxcUm20qRQtDe4N"))
    
    

#print(get_token(login, password))
#get_hw("DtD3kJfO0SJHlRCyJKnL3dGek28VnXNX", date=datetime(2023, 10, 11))



#print(dn.get_classmates())
#dn.get_person_homework()
#print(dn.get_organization_info(2112087604271526837))
#  Получение групп обучения текущего пользователя