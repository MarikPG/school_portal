from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


def ensure_tables():
    with connection.cursor() as c:
        c.execute("CREATE TABLE IF NOT EXISTS school_diary_subject (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100) NOT NULL, teacher VARCHAR(150) NOT NULL DEFAULT '')")
        c.execute("CREATE TABLE IF NOT EXISTS school_diary_grade (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, value INTEGER NOT NULL, date DATE NOT NULL DEFAULT CURRENT_DATE, comment VARCHAR(255) NOT NULL DEFAULT '')")


def staff(user):
    return user.is_authenticated and user.is_staff


def page(title, body):
    return "<!doctype html><html lang='uk'><head><meta charset='utf-8'><title>"+escape(title)+"</title><style>body{font-family:Arial;margin:30px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #aaa;padding:8px}input,select,textarea{padding:6px;width:300px}</style></head><body>"+body+"</body></html>"


@login_required
def diary(request):
    ensure_tables()
    with connection.cursor() as c:
        if request.user.is_staff:
            c.execute("SELECT g.id,u.username,s.name,g.value,g.date,g.comment FROM school_diary_grade g JOIN auth_user u ON u.id=g.student_id JOIN school_diary_subject s ON s.id=g.subject_id ORDER BY g.date DESC,g.id DESC")
        else:
            c.execute("SELECT g.id,u.username,s.name,g.value,g.date,g.comment FROM school_diary_grade g JOIN auth_user u ON u.id=g.student_id JOIN school_diary_subject s ON s.id=g.subject_id WHERE g.student_id=%s ORDER BY g.date DESC,g.id DESC",[request.user.id])
        rows=c.fetchall()
    body="<h1>Електронний щоденник</h1><p>Користувач: <b>"+escape(request.user.username)+"</b></p>"
    if request.user.is_staff:
        body+='<p><a href="/diary/subjects/">Предмети</a> | <a href="/diary/grades/add/">Додати оцінку</a> | <a href="/admin/">Адмінка</a></p>'
    body+="<table><tr><th>Учень</th><th>Предмет</th><th>Оцінка</th><th>Дата</th><th>Коментар</th>"
    if request.user.is_staff: body+="<th>Дії</th>"
    body+="</tr>"
    for r in rows:
        body+="<tr><td>"+escape(r[1])+"</td><td>"+escape(r[2])+"</td><td>"+str(r[3])+"</td><td>"+escape(str(r[4]))+"</td><td>"+escape(r[5])+"</td>"
        if request.user.is_staff:
            body+=f'<td><a href="/diary/grades/{r[0]}/delete/">Видалити</a></td>'
        body+="</tr>"
    if not rows: body+='<tr><td colspan="6">Оцінок поки немає.</td></tr>'
    body+="</table>"
    return HttpResponse(page("Щоденник",body))


@csrf_exempt
@login_required
@user_passes_test(staff)
def subjects(request):
    ensure_tables()
    if request.method=="POST":
        name=request.POST.get("name","").strip()
        teacher=request.POST.get("teacher","").strip()
        if not name: return HttpResponseBadRequest("Вкажіть назву предмета.")
        with connection.cursor() as c: c.execute("INSERT INTO school_diary_subject(name,teacher) VALUES(%s,%s)",[name,teacher])
        return redirect("/diary/subjects/")
    with connection.cursor() as c:
        c.execute("SELECT id,name,teacher FROM school_diary_subject ORDER BY name")
        rows=c.fetchall()
    body='<h1>Предмети</h1><form method="post"><input name="name" placeholder="Предмет" required> <input name="teacher" placeholder="Викладач"><button>Додати</button></form><p><a href="/diary/">Щоденник</a></p><table><tr><th>Предмет</th><th>Викладач</th><th>Дії</th></tr>'
    for r in rows:
        body+=f'<tr><td>{escape(r[1])}</td><td>{escape(r[2])}</td><td><a href="/diary/subjects/{r[0]}/delete/">Видалити</a></td></tr>'
    body+="</table>"
    return HttpResponse(page("Предмети",body))


@csrf_exempt
@login_required
@user_passes_test(staff)
def subject_delete(request,pk):
    ensure_tables()
    if request.method=="POST":
        with connection.cursor() as c: c.execute("DELETE FROM school_diary_subject WHERE id=%s",[pk])
        return redirect("/diary/subjects/")
    return HttpResponse(page("Видалення",'<h1>Видалити предмет?</h1><form method="post"><button>Так</button></form><a href="/diary/subjects/">Назад</a>'))


@csrf_exempt
@login_required
@user_passes_test(staff)
def grade_add(request):
    ensure_tables()
    with connection.cursor() as c:
        c.execute("SELECT id,username FROM auth_user WHERE is_staff=0 ORDER BY username"); students=c.fetchall()
        c.execute("SELECT id,name FROM school_diary_subject ORDER BY name"); subjects=c.fetchall()
    if request.method=="POST":
        try:
            sid=int(request.POST["student"]); sub=int(request.POST["subject"]); value=int(request.POST["value"])
            if not 1<=value<=12: raise ValueError
        except (KeyError,ValueError): return HttpResponseBadRequest("Неправильна оцінка.")
        comment=request.POST.get("comment","").strip()
        with connection.cursor() as c: c.execute("INSERT INTO school_diary_grade(student_id,subject_id,value,comment) VALUES(%s,%s,%s,%s)",[sid,sub,value,comment])
        return redirect("/diary/")
    opts1="".join(f'<option value="{x[0]}">{escape(x[1])}</option>' for x in students)
    opts2="".join(f'<option value="{x[0]}">{escape(x[1])}</option>' for x in subjects)
    body='<h1>Додати оцінку</h1><form method="post"><p>Учень:<br><select name="student" required>'+opts1+'</select></p><p>Предмет:<br><select name="subject" required>'+opts2+'</select></p><p>Оцінка:<br><input type="number" name="value" min="1" max="12" required></p><p>Коментар:<br><textarea name="comment"></textarea></p><button>Зберегти</button></form><p><a href="/diary/">Назад</a></p>'
    return HttpResponse(page("Додати оцінку",body))


@csrf_exempt
@login_required
@user_passes_test(staff)
def grade_delete(request,pk):
    ensure_tables()
    if request.method=="POST":
        with connection.cursor() as c: c.execute("DELETE FROM school_diary_grade WHERE id=%s",[pk])
        return redirect("/diary/")
    return HttpResponse(page("Видалення",'<h1>Видалити оцінку?</h1><form method="post"><button>Так</button></form><a href="/diary/">Назад</a>'))

def login_view(request):
    csrf_token = get_token(request)

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/diary/")

        return HttpResponse(
            page(
                "Помилка входу",
                """
                <h1>Помилка входу</h1>
                <p>Неправильний логін або пароль.</p>
                <a href="/accounts/login/">Спробувати ще раз</a>
                """
            )
        )

    return HttpResponse(
        page(
            "Вхід",
            f"""
            <h1>Вхід до електронного щоденника</h1>

            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken"
                       value="{csrf_token}">

                <p>
                    Логін:<br>
                    <input type="text" name="username" required>
                </p>

                <p>
                    Пароль:<br>
                    <input type="password" name="password" required>
                </p>

                <button type="submit">Увійти</button>
            </form>
            """
        )
    )

def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


urlpatterns=[
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("admin/",admin.site.urls),
    path("diary/",diary,name="diary"),
    path("diary/subjects/",subjects,name="subjects"),
    path("diary/subjects/<int:pk>/delete/",subject_delete,name="subject_delete"),
    path("diary/grades/add/",grade_add,name="grade_add"),
    path("diary/grades/<int:pk>/delete/",grade_delete,name="grade_delete"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
