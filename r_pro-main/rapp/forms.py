from django import forms
from .models import Questions

class DynamicQuestionForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super(DynamicQuestionForm, self).__init__(*args, **kwargs)
        question = questions
        self.fields[f'question_{question.id}'] = forms.ChoiceField(
            label=question.que,
            choices=[(question.option1, question.option1),
                        (question.option2, question.option2),
                        (question.option3, question.option3),
                        (question.option4, question.option4)],
            required=True
        )
        self.fields['current_question'] = forms.CharField(widget=forms.HiddenInput(), initial=question.id)
        print(self.fields)
        