# Generated by Django 4.1.1 on 2022-09-19 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answers',
            options={'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='testsbase',
            options={'verbose_name': 'Тест', 'verbose_name_plural': 'Тесты'},
        ),
        migrations.AddField(
            model_name='answers',
            name='test_title',
            field=models.ForeignKey(help_text='Выберите тест', null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.testsbase'),
        ),
    ]