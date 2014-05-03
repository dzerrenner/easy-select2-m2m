from django.contrib import admin
from django import forms
from easy_select2 import Select2TextInput
import six
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
            },
        )
        self.initial = {
            'tags': ', '.join([six.u(t.name) for t in self.instance.tags.all()]),
        }

        # remove the "Use Ctrl for multiple selections" help text
        self.fields['tags'].help_text = ""

        # option to create tags if there is one in the list which is not created yet
        self.fields['tags'].create = True

    def full_clean(self):
        #
        # Tags input should be a list of ids (ints), but for now
        # it is list of single unicode strings, so we should convert
        # it to correct format.
        #
        # Althought this approach is working, it is better to create
        # custom field type that will do appropriate conversions.
        #
        tags_names = self.data.get('tags')
        if tags_names is not None:
            tags_names = tags_names.split(',')

            tags_ids = []
            for name in tags_names:
                try:
                    # It is possible to use get_or_create here.
                    if self.fields['tags'].create:
                        t, created = Tag.objects.get_or_create(name=name)
                    else:
                        t = Tag.objects.get(name=name)
                except Tag.DoesNotExist:
                    pass
                else:
                    tags_ids.append(str(t.id))

            self.data['tags'] = tags_ids

        super(ParentForm, self).full_clean()


class ParentAdmin(admin.ModelAdmin):
    form = ParentForm

admin.site.register(Parent, ParentAdmin)


admin.site.register(Tag)
