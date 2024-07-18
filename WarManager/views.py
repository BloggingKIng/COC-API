from django.shortcuts import redirect

def home(request):
    return redirect('clan_members_page')