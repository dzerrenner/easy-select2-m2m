from django.contrib import admin
from django import forms
from easy_select2 import Select2TextInput
from demoapp.models import Tag, Parent


class ParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)

        def get_choices():
            values = Tag.objects.values_list('name', flat=True).distinct().order_by('name')
            return [x for x in values]

        # set select2attrs as stated in https://github.com/asyncee/django-easy-select2/issues/4
        self.fields['tags'].widget = Select2TextInput(
            select2attrs={
                'tags': get_choices(),
                # 'width': '250px',
            },
        )

        # remove the "Use Ctrl for multiple selections" help text
        self.fields['tags'].help_text = ""

    def clean_tags(self):
        """
        this only seems to be called with an empty input, .split fails in this case, because name_list is a QuerySet.
        """

        print("clean_tags")
        data = self.cleaned_data
        name_list = data.get('tags', None)
        print("name_list", name_list)
        print(type(name_list))
        if name_list is not None:
            for name in name_list.split(','):
                try:
                    name = Tag.objects.get(name=name)
                except Tag.DoesNotExist:
                    Tag(name=name).save()
        return name_list

    def save(self, commit=True):
        print("save")
        instance = super(ParentForm, self).save(commit=False)
        name_list = self.cleaned_data.get('pre_names_male', None)
        if name_list is not None:
            for name in name_list.split(','):
                name_obj = Tag.objects.get(name=name)
                instance.pre_names_male.add(name_obj)

        if commit:
            instance.save()
        return instance


class ParentAdmin(admin.ModelAdmin):
    form = ParentForm

admin.site.register(Parent, ParentAdmin)


admin.site.register(Tag)