from django.shortcuts import render, redirect
from .models import ActivityCategory
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.templatetags.static import static
from django.views.decorators.cache import never_cache
#from .forms import TaskForm, ActivityForm

@login_required
@never_cache
def activities(request):
    # Fetch all activity categories
    categories = ActivityCategory.objects.all()

    # For each category, get the related tasks
    # This assumes that each category has a related 'Task' through the ForeignKey in Task
    activities = []
    for category in categories:
        # For each category, fetch its related tasks
        tasks = category.tasks.all()  # This uses the related_name from the Task model
        activities.append({
            'category': category,
            'tasks': tasks,
        })
    
    return render(request, 'activities/activities.html', {'activities': activities})

@login_required
def meditation_guide(request):
    return render(request, 'activities/meditation.html')

@login_required
def yoga_guide(request):
    return render(request, 'activities/yoga.html')

@login_required
def breathing_guide(request):
    return render(request, 'activities/breathing.html')

@login_required
def music_player(request):
    # Define directories for audio and cover files
    audio_dir = 'activities/music/assets/'
    cover_dir = 'activities/music/cover/'

    # Dynamically generate a list of audio files with metadata
    audio_files = []
    for file_name in os.listdir(f'static/{audio_dir}'):
        if file_name.endswith('.mp3'):  # Only include MP3 files
            title = os.path.splitext(file_name)[0]  # Extract filename without extension
            cover_path = f'{cover_dir}{title}.jpg'  # Match cover image by filename

            audio_files.append({
                'file': (f'{audio_dir}{file_name}'),  # Path to the audio file
                'title': title,  # Track title (filename without extension)
                'artist': 'Unknown Artist',  # Placeholder for artist info
                'cover': cover_path if os.path.exists(f'static/{cover_path}') else None,  # Path to the cover image or None
            })

    return render(request, 'activities/music.html', {'audio_files': audio_files})

@login_required
def tictactoe(request):
    return render(request, 'activities/games/tictac.html')

@login_required
def game_2048(request):
    return render(request, 'activities/games/2048.html')

@login_required
def snake(request):
    return render(request, 'activities/games/snake.html')



# def create_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('activities')  # Redirect to the activities page
#     else:
#         form = TaskForm()
#     return render(request, 'activities/create_task.html', {'form': form})

# def create_activity(request):
#     if request.method == 'POST':
#         form = ActivityForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('activities')  # Redirect to the activities page
#     else:
#         form = ActivityForm()
#     return render(request, 'activities/create_activity.html', {'form': form})