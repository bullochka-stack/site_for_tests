from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Имя пользователя', help_text='Максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        fields = ['title', 'description']
        model = TestsBase


class QuestionTestForm(forms.Form):

    answer = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )


class QuestionForm(forms.ModelForm):
    class Meta:
        fields = ['question_text']
        model = Questions


class AnswerForm(forms.ModelForm):
    class Meta:
        fields = ['answer_text', 'correct_answer']
        model = Answers


class BaseQuestionFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not all(self.cleaned_data):
            raise forms.ValidationError('Заполните все поля вопросов')


class BaseAnswerFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not all(self.cleaned_data):
            raise forms.ValidationError('Заполните все поля ответов')
        if list(map(lambda a: a['correct_answer'], self.cleaned_data)).count(True) == 0:
            raise forms.ValidationError('На вопрос должен быть хотя бы 1 правильный ответ')
        elif list(map(lambda a: a['correct_answer'], self.cleaned_data)).count(True) == len(list(
                map(lambda a: a['correct_answer'], self.cleaned_data))):
            raise forms.ValidationError('Все варианты не могут быть правильными')


QuestionFormSet = forms.inlineformset_factory(TestsBase,
                                              Questions,
                                              form=QuestionForm,
                                              formset=BaseQuestionFormset,
                                              can_delete=False,
                                              )

AnswerFormSet = forms.inlineformset_factory(Questions,
                                            Answers,
                                            form=AnswerForm,
                                            extra=4,
                                            can_delete=False,
                                            formset=BaseAnswerFormset,
                                            )
