from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Idea, Label
from .forms import IdeaForm, LinkInlineFormSet, IdeaCreateForm
import json
from django.db.models import F
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ideas = Idea.objects.filter(user=request.user).order_by('order')
    context = {
        "ideas": ideas,
    }
    return render(request, "dashboard.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        form = IdeaCreateForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.order = Idea.objects.count()
            idea.name = form.cleaned_data['name']
            idea.description = form.cleaned_data['description']
            idea.user = request.user
            idea.save()
            return redirect('idea_detail', idea_id=idea.id)
    else:
        form = IdeaCreateForm()
    return render(request, 'create.html', {'form': form})

@login_required
def update_idea(request, idea_id):
    try:
        idea = get_object_or_404(Idea, id=idea_id)
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def delete_idea(request, idea_id):
    try:
        idea = Idea.objects.get(id=idea_id)
        idea.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        link_formset = LinkInlineFormSet(request.POST, instance=idea)
        if form.is_valid() and link_formset.is_valid():
            form.save()
            link_formset.save()
            return redirect('idea_detail', idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)
        link_formset = LinkInlineFormSet(instance=idea)
    
    return render(request, 'idea_detail.html', {
        'idea': idea,
        'form': form,
        'link_formset': link_formset,
    })

@require_POST
def update_idea_order(request):
    try:
        data = json.loads(request.body)
        idea_id = data['ideaId']
        new_index = data['newIndex']

        idea = Idea.objects.get(id=idea_id)
        old_index = idea.order

        if new_index > old_index:
            Idea.objects.filter(
                order__gt=old_index,
                order__lte=new_index
            ).update(order=F('order') - 1)
        else:
            Idea.objects.filter(
                order__gte=new_index,
                order__lt=old_index
            ).update(order=F('order') + 1)

        idea.order = new_index
        idea.save()

        ideas = Idea.objects.all().order_by('order')
        for index, idea in enumerate(ideas):
            idea.order = index
            idea.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def label_ideas(request, label_name):
    label = get_object_or_404(Label, name=label_name)
    ideas = Idea.objects.filter(labels=label).order_by('order')
    context = {
        "ideas": ideas,
        "label": label,
    }
    return render(request, "label.html", context)