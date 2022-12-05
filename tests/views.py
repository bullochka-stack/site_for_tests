from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .forms import *
from .models import *


def index(request):
    tests = TestsBase.objects.all()
    return render(request, 'tests/index.html', {'tests': tests,
                                                'title': 'Тестовик',
                                                'title_tests': 'Список тестов'})


def get_category(request, category_id):
    tests = TestsBase.objects.filter(category_id=category_id)
    return render(request, 'tests/category.html', {'tests': tests,
                                                   'title': 'Тестовик',
                                                   'title_tests': 'Список тестов'})


def get_question(test_id, number_question):
    test = TestsBase.objects.get(pk=test_id)
    questions = Questions.objects.filter(test_id=test_id)
    answers = {}
    question_dict = {}
    answers_and_questions = []
    for question in questions:
        pk = question.pk
        answers_list = Answers.objects.filter(question_id=pk)

        for i in answers_list:
            answers[f'{i.pk}'] = i

        question_dict['question'] = question
        question_dict['answers'] = answers
        answers = {}
        answers_and_questions.append(question_dict)
        question_dict = {}

    result = []
    result.append(answers_and_questions[number_question])

    flag = True

    if number_question < len(answers_and_questions) - 1:
        number_question += 1
    else:
        flag = False

    return test, result, answers, flag, answers_and_questions, number_question


count = 0


@login_required(login_url='/login/')
def test_page(request, test_id, number_question):
    if request.method == 'POST':
        form = QuestionTestForm(request.POST)
        if form.data.getlist('answer'):
            data = get_question(test_id, number_question)

            flag = True
            global count
            if len(data[4])-1 == number_question and count == 0:
                flag = True
                count += 1
            elif len(data[4])-1 == number_question and count == 1:
                flag = False
                count -= 1

            record = RecordAnswers.objects.create(user=request.user,
                                                  test=TestsBase.objects.get(pk=test_id),
                                                  question=data[1][0]['question'])

            for i in form.data.getlist('answer'):
                Record.objects.create(answer_rec=record,
                                      answer=Answers.objects.get(pk=int(i)),
                                      is_correct=Answers.objects.get(pk=int(i)).correct_answer)
            if not flag:
                return redirect('show_results', test_id=test_id)
        else:
            return redirect(request.META['HTTP_REFERER'])
    else:

        data = get_question(test_id, number_question)

    context = {
        'test': data[0],
        'answers_and_questions': data[1],
        'len_answers': list(range(0, len(data[2]))),
        'count_quest': data[5],
        'title': 'Тестовик',
        'flag': data[3],
        'form': QuestionTestForm()
    }

    return render(request, 'tests/test_page.html', context)


def delete_answers(request, test_id):
    user = request.user
    record_answers = RecordAnswers.objects.filter(user=user, test=test_id)
    for r_a in record_answers:
        Record.objects.filter(answer_rec=r_a.pk).delete()
        RecordAnswers.objects.filter(pk=r_a.pk).delete()


@login_required(login_url='/login/')
def show_results(request, test_id):
    data = get_question(test_id, 0)
    record_answers = RecordAnswers.objects.filter(user=request.user, test=test_id)
    record = []
    for r_a in record_answers:
        record.append(Record.objects.filter(answer_rec=r_a.pk))

    corrects = 0
    incorrects = 0
    for r in record:
        correct = -1
        for i in r:
            if i.is_correct:
                correct = 1
            else:
                correct = 0
                break
        if correct == 1:
            corrects += 1
        else:
            incorrects += 1
    context = {
        'correct': corrects,
        'incorrect': incorrects,
        'percents': f'{(corrects / (corrects + incorrects)) * 100}% правильных ответов!',
        'title': 'Тестовик',
        'test': data[0]
    }
    delete_answers(request, test_id)
    return render(request, 'tests/results.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    context = {'title': 'Тестовик', 'form': form}
    return render(request, 'tests/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации!')
    else:
        form = UserLoginForm()
    context = {'title': 'Тестовик', 'form': form}
    return render(request, 'tests/login.html', context)


def user_profile(request):
    tests = TestsBase.objects.filter()
    return render(request, 'tests/profile_user.html', {'title': 'Тестовик', 'tests': tests})
