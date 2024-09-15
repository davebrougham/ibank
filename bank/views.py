from django.shortcuts import render, redirect, get_object_or_404
from .forms import IdeaForm 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Idea
import json

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
@csrf_exempt
def update_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        data = json.loads(request.body)
        setattr(idea, data['field'], data['value'])
        category_changed = idea.save()  # This now returns whether the category changed
        return JsonResponse({'status': 'success', 'category_changed': category_changed})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
@csrf_exempt
def delete_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        idea.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    return render(request, 'idea_detail.html', {'idea': idea})