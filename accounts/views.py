from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# LOGIN (session-based for browser dashboard)
def login_page(request):
    print("AUTH RESULT:", user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # creates Django session
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# LOGOUT (GET + POST — NEVER gives 405)
def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_page(request):
    # Redirect authenticated users directly to dashboard
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    next_url = request.GET.get('next', '/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # DEBUG PRINT — ONLY INSIDE POST, SAFE
        print("DEBUG LOGIN:", username, user)

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
