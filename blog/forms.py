from django import forms
from .models import Post, Comment

# PostForm이라는 ModelForm을 선언
class PostForm(forms.ModelForm):
    
    # 이 Form을 만들기 위해 어떤 Model이 쓰이는지 Django에 알려주는 구문
    class Meta:
        model = Post
        fields = ('title', 'text', )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', )