import datetime
from blog.models import BlogEntry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Button
from django import forms


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

        self.helper.layout = Layout(
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
                'published'
            ),
            ButtonHolder(
                Submit('submit', 'Save'),
            )
        )


class BlogPostFormCreate(BlogPostForm):
    date_published = forms.DateField(initial=datetime.date.today)
