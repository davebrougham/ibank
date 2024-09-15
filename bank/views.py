import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Idea, Link
from .forms import IdeaForm, LinkForm
from django.views.decorators.http import require_POST

def dashboard(request):
    ideas = Idea.objects.filter(category__isnull=False)
    return render(request, 'dashboard.html', {'ideas': ideas})

def workshop(request):
    ideas = Idea.objects.all().order_by('complexity')
    context = {
        "ideas": ideas,
    }
    return render(request, "workshop.html", context)

def create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workshop')
    else:
        form = IdeaForm()
    return render(request, 'create.html', {'form': form})

@require_POST
def update_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        data = json.loads(request.body)
        
        for field, value in data.items():
            setattr(idea, field, value)
        
        category_changed = idea.save()
        return JsonResponse({'status': 'success', 'category_changed': category_changed})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
def delete_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        idea.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    links = idea.links.all()
    
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        
        if form.is_valid():
            form.save()
            return redirect('idea_detail', idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)
    
    return render(request, 'idea_detail.html', {
        'idea': idea,
        'form': form,
    })

@require_POST
def add_link(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.idea = idea
            link.save()
            messages.success(request, 'Link added successfully.')
    return redirect('idea_detail', idea_id=idea.id)

@require_POST
def delete_link(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    idea_id = link.idea.id
    link.delete()
    messages.success(request, 'Link deleted successfully.')
    return redirect('idea_detail', idea_id=idea_id)

@require_POST
def update_notes(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        data = json.loads(request.body)
        idea.notes = data['notes']
        idea.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})