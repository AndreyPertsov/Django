# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.student import Student
from ..models.group import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from PIL import Image
from django.contrib import messages

# Views for Students


def students_list(request):
    students = Student.objects.all()
    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    # Якщо форма була запощена:
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # TODO: validate input from user
            # errors collection
            errors = {}

            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if not photo:
                errors['photo'] = u'Додайте фото'
            if photo:
                mime = ['image/jpeg', 'image/pjpeg', 'image/png']
                if photo.content_type not in mime:
                    errors['photo'] = u'Невірний тип файлу'
                if photo.size > 2000000:
                    errors['photo'] = u'Розмір файлу не може бути більшим за 2 мб'

                original = Image.open(photo)
                s = original.size
                max_width = 512
                max_height = 512

                if s > (max_height, max_width):
                    errors['photo'] = u'Максимальній розмір зображення %s x %s пікселів.' % (max_height, max_width)
                else:
                    data['photo'] = photo

            # save student
            if not errors:
                student = Student(**data)
                student.save()
                # redirect to students list
                messages.success(request, u'Студента %s %s успішно додано!' % (student.first_name, student.last_name))
                return HttpResponseRedirect(u'%s?status_message=Студента {0} {1} успішно додано!'.format
                                            (student.first_name, student.last_name) % reverse('home'))

            else:
                messages.error(request, 'Будь-ласка, виправте наступні помилки')
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            messages.info(request, u'Додавання студента скасовано!')
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!'
                                        % reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


              # Якщо кнопка Скасувати була натиснута:



      # Якщо кнопка Додати була натиснута:

          # Перевіряємо дані на коректність та збираємо помилки

          # Якщо дані були введені некоректно:
              # Віддаємо шаблон форми разом із знайденими помилками

          # Якщо дані були введені коректно:
              # Створюємо та зберігаємо студента в базу

          # Повертаємо користувача до списку студентів

          # Якщо форма не була запощена:
            # повертаємо код початкового стану форми



def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

