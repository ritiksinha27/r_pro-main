from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from rapp.models import Questions, Answer, dscore
from .forms import DynamicQuestionForm

import joblib

def load_model():
    try:
        with open('path/to/your/model.joblib', 'rb') as f: # fath for the joblib file 
            model = joblib.load(f)
        return model
    except FileNotFoundError:
        raise Exception('Model file not found. Please ensure the model exists.')
# Create your views here.
def calculate_depression_score(x):
    model = load_model()
    depression_score = model.predict([[x]])[0]  # Assuming model accepts a single value for prediction
    return depression_score
    
def home(request):
    return render(request, 'home.html')

# questions and next questions , ocv logic for the video also has to save , 
# @login
def depressionque(request):
    all_questions = Questions.objects.all().order_by('id')
    if request.method == 'POST':
        current_question_num = int(request.POST.get('current_question')) 
        next_questions = all_questions.filter(id__gt=current_question_num)
        print(current_question_num,next_questions)  
        form = DynamicQuestionForm(request.POST, questions=all_questions[current_question_num-1])
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for question_id, answer in cleaned_data.items():
                if question_id != 'current_question':
                    question = Questions.objects.get(pk=int(question_id.split('_')[1]))
                    client_id=request.user
                    print(client_id)
                    weight = 0 if answer == question.option1 else 1 if answer == question.option2 else 2 if answer == question.option3 else 3
                    Answer.objects.create(question=question, client=login_user, option_text=answer, weight=weight)  # Replace login_user with your authentication mechanism
                    
                    total_weight = sum(answer.weight for answer in Answer.objects.filter(client=request.user))
                    depression_score = calculate_depression_score(total_weight)
                    
                    s= dscore.objects.create(client=login_user, score = depression_score)
                    
            if not next_questions:
                return redirect('result')  # Pass all answers to AI model here
            return redirect('depressionque',question_num=current_question_num)
    else:
        if not all_questions:
            # Handle the case where there are no questions

            return render(request, 'depressionque.html', {'message': 'No questions available'})
        print(all_questions[0].id)
        dynamic_forms = []
        form = DynamicQuestionForm(questions=all_questions[0], initial={'label': all_questions[0].que})
        dynamic_forms.append(form)
        
        question_num = 1
        print(dynamic_forms)

    context = {'dynamic_forms': dynamic_forms, 'question_num': question_num}
    # print(form)
    return render(request, 'depressionque.html', context)

#score, most common emotion(images) from the video, (lifestyle change (text), information, causes ) : link
def result(request):
    depression_score= dscore.objects.get(client=login_user).score
    if 0 < depression_score <= 25:
        context = {'depression_score': depression_score, 'severity': 'No depression'}
    elif 25 < depression_score <= 50:
        context = {'depression_score': depression_score, 'severity': 'Mild depression'}
    elif 50 < depression_score <= 75:
        context = {'depression_score': depression_score, 'severity': 'Moderate depression'}
    elif 75 < depression_score <= 100:
        context = {'depression_score': depression_score, 'severity': 'Severe depression'}
    elif 100 < depression_score <= 125:
        context = {'depression_score': depression_score, 'severity': 'Extreme depression'}
    else:
        context = {'depression_score': depression_score, 'severity': 'Unknown severity'}
            
    return render(request, 'result.html', context)

# all the videos in line 
def calming_video(request):
    return render(request, 'calming_video.html')


# only faq
def faq(request):
    return render(request, 'faq.html')

# about
def about_us(request):
    return render(request, 'about_us.html')

def causes(request):
    depression_score= dscore.objects.get(client=login_user).score
    # Logic for handling causes page
    return render(request, 'causes.html')

# lifestyle changes on result 
def lifestyle_changes(request):
    return render(request, 'lifestyle_changes.html')

# general information on result 
def information(request):
    return render(request, 'information.html')


def login_user(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,('Login Successful !!!'))
            return redirect('index')
        else:
            messages.success(request,('Login UN-Successful !!!'))
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def register_user(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if name and email and mobile and username and password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=name)
                user.save()
                user = authenticate(username=username, password= password1)
                login(request, user)
                messages.success(request, ("Registration Successful, you have been Loged in !!!"))
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
            
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('home')