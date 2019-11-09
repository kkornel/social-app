from django.shortcuts import render

# from .admin import UserCreationForm


def register(request):
    # if request.method == 'POST':
    #     form = UseCreationForm(request.POST)
    #     if form.is_valid():
    #         print()
    # else:
    #     form = UserCreationForm()
    return render(request, 'users/register.html')
