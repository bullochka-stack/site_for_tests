from django.contrib import admin
from .models import *
from .forms import BaseAnswerFormset
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.forms.widgets import Textarea


class AnswersInline(NestedTabularInline):
    model = Answers
    formset = BaseAnswerFormset
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }
    extra = 0


class QuestionsInline(NestedTabularInline):
    model = Questions
    inlines = [AnswersInline]
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }
    extra = 0


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'test_title', 'question', 'correct_answer')
    list_filter = ('test_title', 'question',)
    list_display_links = ['id', 'answer_text']


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'test')
    list_filter = ('test',)
    list_display_links = ['id', 'question_text']
    inlines = [AnswersInline]


class TestsBaseAdmin(NestedModelAdmin):
    inlines = [QuestionsInline]
    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }


admin.site.register(TestsBase, TestsBaseAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Categories)
