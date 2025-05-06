from django.shortcuts import render, redirect, get_object_or_404
from .models import JournalEntry
from .forms import JournalEntryForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@login_required
@never_cache
def journal_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request
    if search_query:
        # Filter journals by title or content based on the search query
        journals = JournalEntry.objects.filter(title__icontains=search_query) | JournalEntry.objects.filter(content__icontains=search_query)
    else:
        journals = JournalEntry.objects.filter(user = request.user)
    return render(request, 'journal/journal-main.html', {'journals': journals, 'search_query': search_query})



@login_required
@never_cache
def journal_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Initialize form with data to validate manually
        form = JournalEntryForm({'title': title, 'content': content})
        
        if form.is_valid():
            journal = form.save(commit=False)
            journal.user = request.user
            journal.save()
            return redirect('journal_list')
        
    else:
        form = JournalEntryForm()  # Initialize an empty form for GET requests

    return render(request, 'journal/journal-create.html', {'form': form})

@login_required
@never_cache
def journal_detail(request, pk):
    journal = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    return render(request, 'journal/journal-detail.html', {'journal': journal})