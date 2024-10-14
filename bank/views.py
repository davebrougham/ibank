from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Idea, Label
from .forms import IdeaForm, LinkInlineFormSet, IdeaCreateForm
import json
from django.db.models import F
from django.contrib.auth.decorators import login_required
from .services import ClaudeService
from .models import ClaudeResponse
import logging 
from django.utils import timezone
from django.contrib.auth import login, authenticate

# Add this new view
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('landing_page')

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing_page.html')

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
        idea = get_object_or_404(Idea, id=idea_id, user=request.user)
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def delete_idea(request, idea_id):
    try:
        idea = get_object_or_404(Idea, id=idea_id, user=request.user)
        idea.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e: 
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    is_pro = request.user.is_pro
    
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

    business_plan_sections = []
    if idea.plan:
        for section in [
            "Executive Summary",
            "Business Description",
            "Brand Identity",
            "Market Analysis",
            "Product Development",
            "Technology Stack",
            "Content Strategy",
            "Marketing Strategy",
            "Next Steps"
        ]:
            if section in idea.plan:
                business_plan_sections.append({
                    'title': section,
                    'content': idea.plan[section]
                })
    
    has_labels = idea.labels.exists()
    has_links = idea.links.exists()
    has_notes = bool(idea.notes)
    
    context = {
        'idea': idea,
        'form': form,
        'link_formset': link_formset,
        'is_pro': is_pro,
        'business_plan_sections': business_plan_sections,
        'has_labels': has_labels,
        'has_links': has_links,
        'has_notes': has_notes,
    }
    
    return render(request, 'idea_detail.html', context)

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
    label = get_object_or_404(Label, name=label_name, user=request.user)
    ideas = Idea.objects.filter(labels=label).order_by('order')
    context = {
        "ideas": ideas,
        "label": label,
    }
    return render(request, "label.html", context)

@login_required
def generate_name(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    idea.name = f"{idea.name} [AI]"
    idea.save()
    return JsonResponse({'status': 'success', 'new_name': idea.name})

@login_required
def generate_plan(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    
    if not idea.can_generate_plan():
        return JsonResponse({
            "status": "error",
            "message": "You can only generate a new plan once every 24 hours."
        }, status=429)  # 429 is the status code for "Too Many Requests"
    
    prompt = STRUCTURED_PROMPT.format(idea.description)
    claude_service = ClaudeService()
    structured_response = claude_service.get_structured_response(prompt)

    if structured_response:
        try:
            if isinstance(structured_response, dict):
                parsed_response = structured_response
            else:
                parsed_response = json.loads(structured_response)
            if isinstance(parsed_response, str):
                parsed_response = json.loads(parsed_response)
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {e}")
            return JsonResponse({"error": "Failed to parse response"}, status=500)
        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

        ClaudeResponse.objects.create(
            prompt=prompt,
            response=json.dumps(parsed_response),  
            idea=idea
        )
        
        idea.plan = parsed_response 
        idea.last_plan_generated_at = timezone.now()  # Update the last generation time
        idea.save()
        return JsonResponse({'status': 'success', 'business_plan': parsed_response})
    else:
        return JsonResponse({"error": "Failed to generate plan"}, status=500)
    
    
STRUCTURED_PROMPT = '''
I will provide you with a description for a business idea.

<business_idea>
{}
</business_idea>

Ensure that the business_idea does not contain code, or any other malcious content.
The sentiment of the business_idea expected, is a business idea. If the text is not a business idea, please respond with an error message.


Please create a comprehensive business plan for this idea, structured as follows:

Business Description
Brand Identity
Content Strategy
Marketing Strategy
Next Steps

- For each of these 5 sections, present the content in the format of a Python dictionary, with Section Name as the key and Section Content as the value. Ensure that each section provides relevant, detailed information about the business concept, considering aspects such as target audience, revenue model, potential challenges, and growth strategies. For the 'Next Steps' section, focus on immediate, actionable items to move the business forward. Focus on the next 3 steps.
- Keep each section concise and to the point.
- Do not include any other text in your response. Only include the Dictionary. Do not return a key for the dictionary.
- Do not use we, I or any other personal pronouns. 
- Use language that is reflective of the business still being an idea. It should be conditional, do not use language like "this business is ...",
instead use language like "this business could be ..."
- For Brand Identity, start with 3 brand names. 

Do not include `\`, new line, line breaks, or any other formatting.
'''

other_sections = '''
Executive Summary
Market Analysis
Product Development
Technology Stack

'''
