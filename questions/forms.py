from django import forms
from questions.models import Question, Tag, Answer
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime 

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [ "content" ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = "Text"
        self.fields["content"].required = True

    def success_url(self):
        return reverse("questions:questions")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.created_at = datetime.now()
        answer.updated_at = datetime.now()
        if commit:
            super().save()
        return answer
    
class QuestionForm(forms.ModelForm):
    tags = forms.CharField()
    class Meta:
        model = Question
        fields = [ "title", "content" ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Title"
        self.fields["title"].required = True
        self.fields["content"].label = "Text"
        self.fields["content"].required = True
        self.fields["tags"].required = False

        
    def success_url(self):
        return reverse("questions:questions")

    def clean(self):
        cleaned_data = super().clean()
        tags = []
        tags_list = self.cleaned_data['tags'].strip()
        if not tags_list:
            self.cleaned_data['tags'] = tags
            return cleaned_data
        print(tags_list)
        tags = tags_list.split(',')
        for (i, tag) in enumerate(tags):
            tag = tag.strip()
            print(tag)
            if ' ' in tag:
                raise forms.ValidationError({"tags": "Incorrect tags. Use , to separate tags"})
            if tag == '':
                raise forms.ValidationError({"tags": "You can't add empty tag"})
            tags[i] = tag
        cleaned_data["tags"] = tags  
        print(tags) 
        return cleaned_data
    
    def save(self, commit=True):
        question = super().save(commit=commit)
        question.created_at = datetime.now()

        for tag in self.cleaned_data["tags"]:
            tag_obj = Tag.objects.filter(name=tag).first()
            if not tag_obj:
                tag_obj = Tag.objects.create(name=tag)
            question.tags.add(tag_obj)
        print(question)

        if commit:
            super().save()
            
        return question