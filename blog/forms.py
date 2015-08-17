import datetime
from blog.models import BlogEntry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Button
from django import forms
from events.middlewares import get_current_request


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        exclude = ['published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.attrs = {'onsubmit': "prepareForm()"}

        fields = [
            Fieldset(
                'Blog post',
                'title',
                'content',
            ),
            Fieldset(
                'Options',
                'tags',
                'slug',
                'date_published',
            ),
            ]
        if get_current_request().user.is_staff:
            fields += [ButtonHolder(Fieldset('Staff', 'personal'),)]
        fields += [ButtonHolder(Submit('submit', 'Save'),)]
        self.helper.layout = Layout(*fields)


class BlogPostFormCreate(BlogPostForm):
    date_published = forms.DateField(initial=datetime.date.today)
