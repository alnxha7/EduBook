from django.contrib import admin
from .models import Course, user_profile, registered_students, register_3freeday, booking_students, Page, PageLock
from django import forms
from django.contrib.auth.models import User

class PageLockForm(forms.ModelForm):
    pages = forms.ModelMultipleChoiceField(
        queryset=Page.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = PageLock
        fields = ['username', 'pages', 'is_locked']

class PageLockAdmin(admin.ModelAdmin):
    form = PageLockForm
    list_display = ['username', 'is_locked']

admin.site.register(Course)
admin.site.register(user_profile)
admin.site.register(registered_students)
admin.site.register(register_3freeday)
admin.site.register(booking_students)
admin.site.register(Page)
admin.site.register(PageLock, PageLockAdmin)
