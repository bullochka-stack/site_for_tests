from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class TestsBase(models.Model):
    title = models.CharField(max_length=200,
                             help_text='Введите название теста',
                             verbose_name='Название теста')
    description = models.TextField(max_length=300,
                                   help_text='Введите описание теста',
                                   verbose_name='Краткое описание теста', null=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT,
                                 help_text='Выберите категорию',
                                 verbose_name='Категория', null=True)
    amount_questions = models.IntegerField(help_text='Введите количество вопросов',
                                            verbose_name='Количество вопросов', null=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Возвращает URL-адрес
        # Функция reverse и тег url в шаблонах - одно и то же, но reverse предпочтительнее
        return reverse('test_page', kwargs={'test_id': self.pk, 'number_question': 0})


class Categories(models.Model):
    name = models.CharField(max_length=100,
                            help_text='Выберите категорию',
                            verbose_name='Категория')

    # наличие такой функции позволит сопоставить URL-aдpeca на страницы с соответствующим представлением и шаблоном
    # НТМL-страницы
    def get_absolute_url(self):
        # Возвращает URL-адрес
        # Функция reverse и тег url в шаблонах - одно и то же, но reverse предпочтительнее
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Questions(models.Model):
    question_text = models.TextField(max_length=1000,
                                     verbose_name='Текст вопроса')
    test = models.ForeignKey('TestsBase', on_delete=models.CASCADE,
                             help_text='Выберите тест',
                             verbose_name='Тест')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    answer_text = models.TextField(max_length=1000,
                                   help_text='Введите ответ на вопрос',
                                   verbose_name='Ответ на вопрос', blank=True)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE,
                                 help_text='Выберите вопрос',
                                 verbose_name='Вопрос')
    test_title = models.ForeignKey('TestsBase', on_delete=models.CASCADE,
                                   help_text='Выберите тест',
                                   verbose_name='Тест', null=True)
    correct_answer = models.BooleanField(default=False,
                                         verbose_name='Правильность ответа', blank=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count_passed_test = models.PositiveIntegerField(verbose_name="Количество пройденных тестов", default=0)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class RecordAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(TestsBase, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)


class Record(models.Model):
    answer_rec = models.ForeignKey(RecordAnswers, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
