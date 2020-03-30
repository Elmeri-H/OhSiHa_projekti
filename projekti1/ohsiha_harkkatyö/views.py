from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Question
from .forms import QuestionForm


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def list_questions(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})

def create_question(request):
    form = QuestionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_questions')

    return render(request, 'questions-form.html', {'form': form})

def update_question(request, id):
    question = Question.objects.get(id=id)
    form = QuestionForm(request.POST or None, instance=question)

    if form.is_valid():
        form.save()
        return redirect('list_questions')

    return render(request, 'questions-form.html', {'form': form, 'question': question})

def delete_question(request, id):
    question = Question.objects.get(id=id)

    if request.method == 'POST':
        question.delete()
        return redirect('list_questions')

    return render(request, 'q-delete-confirm.html', {'question':question})