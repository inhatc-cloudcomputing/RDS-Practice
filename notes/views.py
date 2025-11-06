from django.shortcuts import render, get_object_or_404, redirect
from .models import Note


def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'note_list.html', {'notes': notes})


def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        Note.objects.create(title=title, content=content)
        return redirect('note_list')
    return render(request, 'note_form.html')


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content', '')
        note.save()
        return redirect('note_list')
    return render(request, 'note_form.html', {'note': note})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

