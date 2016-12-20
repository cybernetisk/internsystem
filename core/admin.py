from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from core.models import User, Semester, Card, NfcCard, Group

from django.utils.translation import ugettext_lazy as _


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('realname', 'email', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )

    list_display = ('username', 'email', 'realname', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('username', 'realname', 'email')

    add_form = UserCreationForm
    add_form_template = None


admin.site.register(User, UserAdmin)
admin.site.register(Semester)
admin.site.register(Card)
admin.site.register(NfcCard)
admin.site.register(Group)
