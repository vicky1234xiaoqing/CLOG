from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from teacher.models import User
from course.models import Course
from student.models import Student
from grade.models import Grade
from feedback.models import Feedbcak
import json
import re
import math

#{'csrfmiddlewaretoken': ['0UVsZsgUCkyeF4dQg9BlS9QxH5eoWZuncixuLF13bWzRVWzhWdnLkDNkjjhfDBwu'], 
# 'Email': ['123@qq.com'], 'Password': ['123'], 'StudentID': ['123'], 'password2': ['123'], 
# 'Grade': ['Undergraduate'], 'newer': ['newer1'], 'remind': ['yes']}

class UserForm(forms.Form): 
    Email = forms.CharField(label='Email', max_length=500)
    Password = forms.CharField(label='Password', max_length=500)
    StudentID = forms.CharField(label='StudentID', max_length=500)
    password2 = forms.CharField(label='password2', max_length=500)
    Grade = forms.CharField(label='Grade', max_length=500)
    newer = forms.CharField(label='newer', max_length=500)

#{'csrfmiddlewaretoken': ['qPh5L19Lzcnu7bfjbycCPJKMwKdKdTu6CdT7xeUU8Oo7n3BKRCY2hdHz8YgBUvwd'], 
#'email': ['571102482@qq.com'], 'password': ['123']}

class loginForm(forms.Form): 
    email = forms.CharField(label='Email', max_length=500)
    password = forms.CharField(label='Password', max_length=500)
    who = forms.CharField(label='who', max_length=500)

# <QueryDict: {'csrfmiddlewaretoken': ['AzXDzKKjFnVuyzGgJEa5Xu3FnF1NxnLpMXzFlXvseZW7Or2HpIWvpY0sZT4EeZNw'],
# 'c_name': ['123'], 'c_id': ['123'], 'c_type': ['Engineering'], 'c_format': ['Teach'], 
# 'home': ['0', '1'], 'exper': ['0', '1'], 'attend': ['0'], 'exam': ['0'], 
# 'c_intr': ['1'], 'c_req': ['2'], 'others': ['3']}>

class new_tForm(forms.Form): 
    c_name = forms.CharField(label='c_name', max_length=500)
    c_id = forms.CharField(label='c_id', max_length=500)
    c_type = forms.CharField(label='c_type', max_length=500)
    c_format = forms.CharField(label='c_format', max_length=500)
    home = forms.CharField(label='home', max_length=500)
    exper = forms.CharField(label='exper', max_length=500)
    exam = forms.CharField(label='exam', max_length=500)
    attend = forms.CharField(label='attend', max_length=500)
    ass_type = forms.CharField(label='ass_type', max_length=500)
    c_intr = forms.CharField(label='c_intr', max_length=500)
    c_req = forms.CharField(label='c_req', max_length=500)
    others = forms.CharField(label='others', max_length=500)

class new_sForm(forms.Form): 
    c_name = forms.CharField(label='c_name', max_length=500)
    c_id = forms.CharField(label='c_id', max_length=500)
    c_type = forms.CharField(label='c_type', max_length=500)
    c_intr = forms.CharField(label='c_intr', max_length=500)
    c_req = forms.CharField(label='c_req', max_length=500)
    others = forms.CharField(label='others', max_length=500)
    e_grade = forms.CharField(label='e_grade', max_length=500)

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'sign.html')

def regist(req):
    if req.method == 'POST':
        #print(req.POST)
        uf = UserForm(req.POST)
        if uf.is_valid():
            email = uf.cleaned_data['Email']
            password = uf.cleaned_data['Password']
            ID = uf.cleaned_data['StudentID']
            password2 = uf.cleaned_data['password2']
            grade = uf.cleaned_data['Grade']
            newer = uf.cleaned_data['newer']
            User.objects.create(Email=email, Password = password, StudentID = ID, password2 = password2, Grade = grade, newer = newer)
            '''
            print(email)
            print(password)
            print(ID)
            print(password2)
            print(grade)
            print(newer)
            print(remind)
            '''
            return HttpResponse('<script>alert("Successful regist! Please Login.");location.href="/login/";</script>')
        else:
            return HttpResponse('<script>alert("Fail to regist! Please fill up all information.");location.href="/";</script>')
    else:
        uf = UserForm()
    return render(req, 'sign.html')

def login(req):
    if req.method == 'POST':
        #print(req.POST)
        uf = loginForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            who = uf.cleaned_data['who']
            user = User.objects.filter(Email__exact = username,Password__exact = password)
            if user:
                if who == 'teacher':
                    #return HttpResponse('teacher!!')
                    response = HttpResponseRedirect('/teacher_new/')
                else:
                    #return HttpResponse('student!!')
                    response = HttpResponseRedirect('/student_new/')
                response.set_cookie('username',username,3600)
                return response
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render(req, 'login.html')

def teacher_new(req):
    if req.method == 'POST':
        #print(req.POST)
        username = req.COOKIES.get('username','')
        uf = new_tForm(req.POST)
        if uf.is_valid():
            c_name = uf.cleaned_data['c_name']
            c_id = uf.cleaned_data['c_id']
            c_type = uf.cleaned_data['c_type']
            c_format = uf.cleaned_data['c_format']
            home = uf.cleaned_data['home'][-1]
            exper = uf.cleaned_data['exper'][-1]
            exam = uf.cleaned_data['exam'][-1]
            attend = uf.cleaned_data['attend'][-1]
            c_intr = uf.cleaned_data['c_intr']
            c_req = uf.cleaned_data['c_req']
            others = uf.cleaned_data['others']
            ass_type = uf.cleaned_data['ass_type']
            #print("@@@@")
            #print(ass_type)
            Course.objects.create(teacher=username, c_name=c_name, c_id = c_id, c_type = c_type, c_format = c_format, home = home, exper = exper, exam = exam, attend = attend, c_intr = c_intr, c_req = c_req, others = others, ass_type = ass_type)
            response = HttpResponseRedirect('/LR_t/')
            response.set_cookie('c_id',c_id,3600)
            return response
    else:
        uf = UserForm()
    return render(req, 'Newer_teacher.html',{'uf':uf})

def LR_t(req):
    username = req.COOKIES.get('username','')
    c_id = req.COOKIES.get('c_id','')
    #print(c_id)
    all_course = Course.objects.all()
    for course in all_course:
        if course.c_id == c_id:
            #print('yes')
            c_name = course.c_name
            c_id = course.c_id
            c_type = course.c_type
            c_format = course.c_format
            home = course.home
            exper = course.exper
            exam = course.exam
            attend = course.attend
            c_intr = course.c_intr
            c_req = course.c_req
            others = course.others
            #print(home)
            type_ = ""
            if course.home == '1':
                type_ += 'homework, '
            if course.exper == '1':
                type_ += 'experiment, '
            if course.exam == '1':
                type_ += 'exam, '
            if course.attend == '1':
                type_ += 'attend, '
            c_type = [x.strip() for x in course.ass_type.split(',')]
            for _ in c_type:
                type_ += _ 
                type_ += ', '
    type_ = type_[0:-2]
    c_intr_res = [x.strip() for x in c_intr.split(',')]
    c_req_res = [x.strip() for x in c_req.split(',')]
    intr = ""
    if len(c_intr_res) > 1:
        intr = c_intr_res[0]
        for i in range(1, len(c_intr_res)-1):
            intr = intr + ', ' + c_intr_res[i]
        intr = intr + ' and ' + c_intr_res[-1]
    else:
        intr = c_intr_res[0]
    reqir = ""
    if len(c_req_res) > 1:
        reqir = c_req_res[0]
        for i in range(1, len(c_req_res)-1):
            reqir = reqir + ', ' + c_req_res[i]
        reqir = reqir + ' and ' + c_req_res[-1]
    else:
        reqir = c_req_res[0]

    LR = "This course is " + intr + ". In my course, you should have been " + reqir + ". Pay attention, it will include "+ type_ +" and so on. Hope you can get a good grade."
    
    all_student = Student.objects.all()
    if all_student:
        for course in all_student:
            #print('yes')
            c_name = course.c_name
            c_id = course.c_id
            c_type = course.c_type
            c_intr = course.c_intr
            c_req = course.c_req
            others = course.others
            e_grade = course.e_grade
            #print(home)
                
        c_intr_res = [x.strip() for x in c_intr.split(',')]
        c_req_res = [x.strip() for x in c_req.split(',')]
        intr = ""
        if len(c_intr_res) > 1:
            intr = c_intr_res[0]
            for i in range(1, len(c_intr_res)-1):
                intr = intr + ', ' + c_intr_res[i]
            intr = intr + ' and ' + c_intr_res[-1]
        else:
            intr = c_intr_res[0]
        reqir = ""
        if len(c_req_res) > 1:
            reqir = c_req_res[0]
            for i in range(1, len(c_req_res)-1):
                reqir = reqir + ', ' + c_req_res[i]
            reqir = reqir + ' and ' + c_req_res[-1]
        else:
            reqir = c_req_res[0]

        ER = "Students want a " + intr + " class. The advantage and disadvantage are the import things for them. They hope " + reqir + ". Most of them want to get a grade as " + e_grade +'.'
    else:
        ER = ""
    
    return render(req, 'LR_teacher.html', {'LR':LR, 'ER':ER})

def student_new(req):
    if req.method == 'POST':
        #print(req.POST)
        username = req.COOKIES.get('username','')
        uf = new_sForm(req.POST)
        if uf.is_valid():
            c_name = uf.cleaned_data['c_name']
            c_id = uf.cleaned_data['c_id']
            c_type = uf.cleaned_data['c_type']
            c_intr = uf.cleaned_data['c_intr']
            c_req = uf.cleaned_data['c_req']
            others = uf.cleaned_data['others']
            e_grade = uf.cleaned_data['e_grade']
            Student.objects.create(student=username, c_name=c_name, c_id = c_id, c_type = c_type, c_intr = c_intr, c_req = c_req, others = others, e_grade=e_grade)
            response = HttpResponseRedirect('/ER_s/')
            response.set_cookie('c_id',c_id,3600)
            return response
    else:
        uf = UserForm()
    return render(req, 'Newer_student.html',{'uf':uf})

def ER_s(req):
    username = req.COOKIES.get('username','')
    c_id = req.COOKIES.get('c_id','')
    #print(c_id)
    all_student = Student.objects.all()
    for course in all_student:
        if course.student == username:
            #print('yes')
            c_name = course.c_name
            c_id = course.c_id
            c_type = course.c_type
            c_intr = course.c_intr
            c_req = course.c_req
            others = course.others
            e_grade = course.e_grade
            #print(home)
    all_course = Course.objects.all()
    for course in all_course:
        if course.c_id == c_id:
            #print('yes')
            c_name = course.c_name
            c_id = course.c_id
            c_type = course.c_type
            c_format = course.c_format
            home = course.home
            exper = course.exper
            exam = course.exam
            attend = course.attend
            c_intr = course.c_intr
            c_req = course.c_req
            others = course.others
    c_intr_res = [x.strip() for x in c_intr.split(',')]
    c_req_res = [x.strip() for x in c_req.split(',')]
    intr = ""
    if len(c_intr_res) > 1:
        intr = c_intr_res[0]
        for i in range(1, len(c_intr_res)-1):
            intr = intr + ', ' + c_intr_res[i]
        intr = intr + ' and ' + c_intr_res[-1]
    else:
        intr = c_intr_res[0]
    reqir = ""
    if len(c_req_res) > 1:
        reqir = c_req_res[0]
        for i in range(1, len(c_req_res)-1):
            reqir = reqir + ', ' + c_req_res[i]
        reqir = reqir + ' and ' + c_req_res[-1]
    else:
        reqir = c_req_res[0]

    ER = "Students want a " + intr + " class. The advantage and disadvantage are the import things for them. They hope " + reqir + ". Most of them want to get a grade as " + e_grade +'.'
    return render(req, 'ER_student.html', {'ER':ER})

def grade_t(req):
    if req.method == 'POST':
        #print(req.POST)
        grade = req.POST.getlist('abc')
        username = req.COOKIES.get('username','')
        c_id = req.COOKIES.get('c_id','')
        #print(c_id)
        all_student = Student.objects.all()
        number = 0
        name = ""
        for course in all_student:
            #print("student:")
            #print(course.c_id)
            #print(course.c_id==c_id)
            #print(course.student)
            if c_id == course.c_id:
                #print('yes')
                number += 1
                if number == 1:
                    name += course.student
                else:
                    name += "#"
                    name += course.student
        #print(name)
        #print(number)
        all_course = Course.objects.all()
        for course in all_course:
            coll = 0
            coll_name = ""
            if c_id == course.c_id:
                if course.home == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'homework'
                    else:
                        coll_name += '#homework'
                if course.exper == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'experiment'
                    else:
                        coll_name += '#experiment'
                if course.exam == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'exam'
                    else:
                        coll_name += '#exam'
                if course.attend == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'attend'
                    else:
                        coll_name += '#attend'
                c_type = [x.strip() for x in course.ass_type.split(',')]
                for _ in c_type:
                    coll += 1
                    if coll == 1:
                        coll_name += _
                    else:
                        coll_name += '#'
                        coll_name += _ 
        #print(grade)
        #print(name)
        #print(coll_name)
        GGG = Grade.objects.create(grade = grade, name = name, item = coll_name, c_id = c_id)
        number = 0
        coll = 0
        return render(req, 'grades_teacher.html', {'row':json.dumps(number),'col':json.dumps(coll),'student':json.dumps(name),'col_name':json.dumps(coll_name)})
    else:
        username = req.COOKIES.get('username','')
        c_id = req.COOKIES.get('c_id','')
        #print(c_id)
        all_student = Student.objects.all()
        number = 0
        name = ""
        for course in all_student:
            #print("student:")
            #print(course.c_id)
            #print(course.c_id==c_id)
            #print(course.student)
            if c_id == course.c_id:
                #print('yes')
                number += 1
                if number == 1:
                    name += course.student
                else:
                    name += "#"
                    name += course.student
        #print(name)
        #print(number)
        all_course = Course.objects.all()
        for course in all_course:
            coll = 0
            coll_name = ""
            if c_id == course.c_id:
                if course.home == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'homework'
                    else:
                        coll_name += '#homework'
                if course.exper == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'experiment'
                    else:
                        coll_name += '#experiment'
                if course.exam == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'exam'
                    else:
                        coll_name += '#exam'
                if course.attend == '1':
                    coll += 1
                    if coll == 1:
                        coll_name += 'attend'
                    else:
                        coll_name += '#attend'
                c_type = [x.strip() for x in course.ass_type.split(',')]
                for _ in c_type:
                    coll += 1
                    if coll == 1:
                        coll_name += _
                    else:
                        coll_name += '#'
                        coll_name += _ 
        #print(coll_name)
        return render(req, 'grades_teacher.html', {'row':json.dumps(number),'col':json.dumps(coll),'student':json.dumps(name),'col_name':json.dumps(coll_name)})
            
    
        #print(home)
    return render(req, 'grades_teacher.html')

def feedback_t(req):
    all_feed = Feedbcak.objects.all()
    number = len(all_feed)
    if number ==0:
        return HttpResponse('<script>alert("No feedback!");location.href="/feedback_t/";</script>')
    else:
        items = ""
        coll = 2    
        coll_name = "Problem#Need Help"
        i = 0
        for feed in all_feed:
            i += 1
            if i==1:
                items += feed.problem
                items += "#"
                items += feed.hepl
            else:
                items += "#"
                items += feed.problem
                items += "#"
                items += feed.hepl
        #print(coll_name)
        print(number)
        print(coll)
        print(items)
        return render(req, 'feedback_teacher.html', {'row':json.dumps(number),'col':json.dumps(coll),'items':json.dumps(items)})


def LR_s(req):
    username = req.COOKIES.get('username','')
    c_id = req.COOKIES.get('c_id','')
    all_course = Course.objects.all()
    type_=""
    for course in all_course:
        if course.c_id == c_id:
            #print('yes')
            c_name = course.c_name
            c_id = course.c_id
            c_type = course.c_type
            c_format = course.c_format
            home = course.home
            exper = course.exper
            exam = course.exam
            attend = course.attend
            c_intr = course.c_intr
            c_req = course.c_req
            others = course.others
            type_ = ""
            if course.home == '1':
                type_ += 'homework, '
            if course.exper == '1':
                type_ += 'experiment, '
            if course.exam == '1':
                type_ += 'exam, '
            if course.attend == '1':
                type_ += 'attend, '
            c_type = [x.strip() for x in course.ass_type.split(',')]
            for _ in c_type:
                type_ += _ 
                type_ += ', '
    type_ = type_[0:-2]
            #print(home)
            
    c_intr_res = [x.strip() for x in c_intr.split(',')]
    c_req_res = [x.strip() for x in c_req.split(',')]
    intr = ""
    if len(c_intr_res) > 1:
        intr = c_intr_res[0]
        for i in range(1, len(c_intr_res)-1):
            intr = intr + ', ' + c_intr_res[i]
        intr = intr + ' and ' + c_intr_res[-1]
    else:
        intr = c_intr_res[0]
    reqir = ""
    if len(c_req_res) > 1:
        reqir = c_req_res[0]
        for i in range(1, len(c_req_res)-1):
            reqir = reqir + ', ' + c_req_res[i]
        reqir = reqir + ' and ' + c_req_res[-1]
    else:
        reqir = c_req_res[0]

    LR = "This course is " + intr + ". In my course, you should have been " + reqir + ". Pay attention, it will include "+type_ +" and so on. Hope you can get a good grade."
    
    return render(req, 'LR_student.html',{'LR':LR})

def grade_s(req):
    if req.method == 'POST':
        g_grade = req.POST.get('e_grade')
        g_grade = eval(g_grade)
        username = req.COOKIES.get('username','')
        c_id = req.COOKIES.get('c_id','')
        all_grade = Grade.objects.all()
        all_student = Student.objects.all()
        a = 0.1
        b = 0.1
        c = 0.1
        sum_e = 0
        for student in all_student:
            sum_e += eval(student.e_grade)
            if username == student.student:
                e_grade = student.e_grade
        sum_e = sum_e / len(all_student)
        for grade in all_grade:
            if c_id == grade.c_id:
                names = grade.name
                items = grade.item
                grades = grade.grade
                grades = grades[1:-1]
                #print(grades)
                grades = [x.strip() for x in grades.split(',')]
                grades = [x[1:-1] for x in grades]
        names = names.split('#')
        items = items.split('#')
        n = len(names)
        m = len(items)
        i = 0
        for _ in names:
            if username == _:
                break
            else:
                i += 1
        own_grade = grades[i:i+m]
        final = 0
        for res in own_grade:
            final += eval(res)
        final = final / len(own_grade)
        #print(grades)
        #print(own_grade)
        #print(own_grade)
        #print(items)
        #print(e_grade)
        e_grade = eval(e_grade)
        report_grade = 85
        cha = g_grade - e_grade
        nuli = (cha / 50) * 100
        zixin = (g_grade + e_grade) / 2 / sum_e * 100
        if zixin>100:
            zixin = 100
        if nuli > 100:
            nuli = 100
        if nuli < -100:
            nuli = -100
        q = ((g_grade + e_grade) / 2 - final)/sum_e
        q = abs(q)
        final_final = q * (a*report_grade+b*nuli + c*zixin) + 0.9*final
        final_final = int(final_final)
        str_nuli = ""
        if nuli <= 0:
            str_nuli += "&#10005"
            fzb1 = 0
        else:
            fzb1 = 1
            str_nuli += "&#9733" * math.ceil(int(nuli) / 20) + "&#9734" * (5-(int(nuli) // 20))
        str_zixin = ""
        if zixin <= 0:
            fzb2 = 0
            str_zixin += "&#10005"
        else:
            fzb2 = 1
            str_zixin += "&#9733" * math.ceil(int(zixin) / 20) + "&#9734" * (5-(int(zixin) // 20))
        message = ""
        if ((int(nuli) // 20)<3):
            message = "You are less work-harding. Hope you can work harder and behave better."
        else:
            if ((int(zixin) // 20)<3):
                message = "You are work-harding but unconfident. Hope you can be more active and confident."
            else:
                message = "You are really good. Hope you can stidk to it!"        
        return render(req, 'grades_student.html',{"str_nuli":json.dumps(str_nuli), "str_zixin":json.dumps(str_zixin), "message":message,"grade":final_final})
    else:
        return render(req, 'compute_grade.html')

def feedback_s(req):
    if req.method == 'POST':
        print(req.POST)
        problem = req.POST.get('problem')
        help = req.POST.get('help')
        Feedbcak.objects.create(problem = problem, hepl = help)
        return HttpResponse('<script>alert("Successful feedback!");location.href="/feedback_s/";</script>')
    else:
        return render(req, 'feedback_student.html')
