from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from blogpost.models import BlogPost


class CrispyFormMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))


class BlogPostForm(CrispyFormMixin, forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']
