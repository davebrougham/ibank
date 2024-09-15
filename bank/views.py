from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms import inlineformset_factory
from .models import Idea, Link
from .forms import IdeaForm
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

def delete_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        idea.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    LinkFormSet = inlineformset_factory(Idea, Link, fields=['url'], extra=1, can_delete=True)
    
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        link_formset = LinkFormSet(request.POST, instance=idea)
        
        if form.is_valid() and link_formset.is_valid():
            form.save()
            
            # Check if all existing links are marked for deletion
            existing_links = Link.objects.filter(idea=idea)
            all_deleted = all(
                form.cleaned_data.get('DELETE', False) 
                for form in link_formset.forms 
                if form.instance.pk
            )
            
            if all_deleted and existing_links.exists():
                # If all links are deleted, remove them manually
                existing_links.delete()
            else:
                # Otherwise, save the formset as usual
                link_formset.save()
            
            return redirect('idea_detail', idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)
        link_formset = LinkFormSet(instance=idea)
    
    return render(request, 'idea_detail.html', {
        'idea': idea,
        'form': form,
        'link_formset': link_formset,
    })