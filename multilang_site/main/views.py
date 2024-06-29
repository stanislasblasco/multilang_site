from django.shortcuts import render
from .models import Article
from django.utils.translation import gettext_lazy as _
from .forms import ChatForm
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
# Create your views here.

def article_list(request):
    articles = Article.objects.values('title', 'content', 'publication_date')
    return render(request, 'main/article_list.html', {'articles': articles,'redirect_to' : request.path})


def chat(request):
    response = None
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            response = get_gpt_response(message)
    else:
        form = ChatForm()

    return render(request, 'main/chat.html', {'form': form, 'response': response})


def get_gpt_response(message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        print(f"GPT Completion: {completion}")  # Debugging line
        response = completion.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging line
        response = str(e)
    return response