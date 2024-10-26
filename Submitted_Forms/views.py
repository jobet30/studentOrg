from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SubmittedForm
from .forms import SubmittedFormForm

@login_required
def submit_form(request):
    if request.method == 'POST':
        form = SubmittedFormForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('submitted_forms:submission_success')
    else:
        form = SubmittedFormForm()
    return render(request, 'submitted_forms/submit_form.html', {'form': form})

@login_required
def view_submissions(request):
    submissions = SubmittedForm.objects.filter(user=request.user)
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        admin_comments = request.POST.get('admin_comments')
        submission = SubmittedForm.objects.get(id=submission_id)
        submission.is_reviewed = True
        submission.admin_comments = admin_comments
        submission.reviewed_at = timezone.now()
        submission.save()
        messages.success(request, 'Submission reviewed successfully.')
        return redirect('submitted_forms:review_submissions')
        
    return render(request, 'submitted_forms/view_submissions.html', {'submissions': submissions})

def submission_success(request):
    return render(request, 'submitted_forms/submission_success.html')
