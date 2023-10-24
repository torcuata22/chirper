from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'chirper/home.html', {})


#10/24 stopped here: https://www.youtube.com/watch?v=H8MmNqDyra8&list=PLCC34OHNcOtoQCR6K4RgBWNi3-7yGgg7b&index=3