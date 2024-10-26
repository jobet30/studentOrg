from django.shortcuts import render, get_object_or_404, redirect
from .models import EmailTemplate
from .forms import EmailTemplateForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def email_template_list(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'email_templates/template_list.html', {'templates': templates})

@require_http_methods(["GET", "POST"])
def email_template_create(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save()
            messages.success(request, 'Email template created successfully.')
            return JsonResponse({
                'status': 'success',
                'message': 'Email template created successfully.',
                'data': {
                    'id': template.id,
                    'name': template.name,
                    'logo': template.logo.url if template.logo else None,
                    'html_content': template.html_content,
                }
            }, status=201)
        else:
            messages.error(request, 'Please correct the errors below.')
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }, status=400)
    else:
        form = EmailTemplateForm()
    return render(request, 'e-templates/template_form.html', {'form': form})

@require_http_methods(["GET", "PUT"])
def email_template_update(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    if request.method == 'PUT':
        data = json.loads(request.body)  # Assuming JSON data
        form = EmailTemplateForm(data, request.FILES, instance=template)  # Handle file uploads
        if form.is_valid():
            updated_template = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Email template updated successfully.',
                'data': {
                    'id': updated_template.id,
                    'name': updated_template.name,
                    'logo': updated_template.logo.url if updated_template.logo else None,
                    'html_content': updated_template.html_content,
                }
            }, status=200)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }, status=400)
    else:
        return render(request, 'e-templates/template_form.html', {'form': EmailTemplateForm(instance=template)})

@require_http_methods(["DELETE"])
def email_template_delete(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    template.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Email template deleted successfully.'
    }, status=204)
