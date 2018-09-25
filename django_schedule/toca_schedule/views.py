from django.shortcuts import render, redirect
from .models import Schedule
from django.contrib.auth.decorators import login_required
from . import forms, controller
from django.views.decorators.clickjacking import xframe_options_exempt


@login_required(login_url="/accounts/login/")
@xframe_options_exempt
def schedule_list(request):
    schedules = Schedule.objects.all().order_by('started')
    return render(request, 'toca_schedule/schedule_list.html', {'schedules': schedules})


@xframe_options_exempt
def schedule_detail(request, job_id):
    schedule = Schedule.objects.get(id=job_id)
    return render(request, 'toca_schedule/schedule_detail.html', {'schedule': schedule})


@xframe_options_exempt
def schedule_delete(request, job_id):
    Schedule.objects.get(id=job_id).delete()
    controller.remove_job(str(job_id))
    return redirect('toca_schedule:list')


@login_required(login_url="/accounts/login/")
@xframe_options_exempt
def schedule_create(request):
    actions_table = controller.get_table(request.user.get_username())
    if request.method == 'POST':
        form = forms.CreateSchedule(request.POST)#, request.FILES) <-- include if upload field on the form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            chronic = controller.CronObj(
                action_id=instance.action_id,
                scheduled=instance.scheduled,
                job_id=instance.id,
                username=request.user.get_username()
            )
            chronic.start_job()
            return redirect('toca_schedule:list')
    else:
        form = forms.CreateSchedule()
    return render(request, 'toca_schedule/schedule_create.html', {'form': form, 'action_table': actions_table})
