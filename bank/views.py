from django.shortcuts import render, redirect
from .forms import IdeaForm 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Idea
import json


def ideas(request):
    ideas = Idea.objects.filter(category__isnull=False)
    return render(request, 'ideas.html', {'ideas': ideas})

def cleanup(request):
    ideas = Idea.objects.all().order_by('complexity')
    
    context = {
        "ideas": ideas,
    }
    
    return render(request, "cleanup.html", context)

def data(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cleanup')
    else:
        form = IdeaForm()
    
    return render(request, 'data.html', {'form': form})

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