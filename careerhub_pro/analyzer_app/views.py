from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Resume
import PyPDF2

def index(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")

from django.shortcuts import get_object_or_404

@login_required
def resume_report(request, resume_id):
    # Uploaded resume ko fetch karo
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    # Resume se text extract karo
    text = extract_text_from_resume(resume.file)

    # Suggestions nikal lo
    suggestions = analyze_resume(text)

    # Example jobs (hardcoded, tum DB se bhi le sakte ho)
    jobs = [
        {"title": "Python Developer", "skills": ["Python", "Django", "SQL"]},
        {"title": "Frontend Developer", "skills": ["HTML", "CSS", "JavaScript"]},
        {"title": "Full Stack Developer", "skills": ["Python", "Django", "HTML", "CSS", "JavaScript"]}
    ]

    # Recommended jobs
    recommended_jobs = recommend_jobs(text, jobs)

    # HTML me bhejne ke liye context
    context = {
        "resume": resume,
        "suggestions": suggestions,
        "recommended_jobs": recommended_jobs
    }

    return render(request, "resume_report.html", context)


def extract_text_from_resume(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(text):
    suggestions = []
    
    required_skills = ["Python", "Django", "SQL", "HTML", "CSS", "JavaScript"]
    
    for skill in required_skills:
        if skill.lower() not in text.lower():
            suggestions.append(f"Add {skill} to your resume.")
    
    if "github" not in text.lower():
        suggestions.append("Add your GitHub profile link.")
        
    if "linkedin" not in text.lower():
        suggestions.append("Add your LinkedIn profile link.")
    
    return suggestions

def recommend_jobs(text, jobs):
    recommended = []
    for job in jobs:
        match_count = sum(skill.lower() in text.lower() for skill in job["skills"])
        if match_count > 0:
            recommended.append(job["title"])
    return recommended


def resume_success(request):
    return render(request, "resume_success.html")

@login_required
def upload_resume(request):
    if request.method == "POST" and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        resume = Resume.objects.create(user=request.user, file=resume_file)
        return redirect('resume_report', resume_id=resume.id)  # Resume ID pass ki
    return render(request, 'upload_resume.html')

# Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! You can login now.")
        return redirect('login')

    return render(request, 'registration/signup.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # after login, go to base page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'registration/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')
