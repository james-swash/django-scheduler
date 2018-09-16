from django.shortcuts import render, redirect
from .models import Schedule
from django.contrib.auth.decorators import login_required
from . import forms, controller


def schedule_list(request):
    schedules = Schedule.objects.all().order_by('started')
    return render(request, 'toca_schedule/schedule_list.html', {'schedules': schedules})


def schedule_detail(request, job_id):
    schedule = Schedule.objects.get(id=job_id)
    return render(request, 'toca_schedule/schedule_detail.html', {'schedule': schedule})


def schedule_delete(request, job_id):
    Schedule.objects.get(id=job_id).delete()
    controller.remove_job(str(job_id))
    return redirect('toca_schedule:list')


@login_required(login_url="/accounts/login/")
def schedule_create(request):
    actions_table = controller.get_table()
    workflow_id = request.GET.get('id')
    if request.method == 'POST':
        form = forms.CreateSchedule(request.POST)#, request.FILES) <-- include if upload field on the form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            chronic = controller.CronObj(action_id=workflow_id, scheduled=instance.scheduled, job_id=instance.id)
            chronic.start_job()
            return redirect('toca_schedule:list')
    else:
        form = forms.CreateSchedule()
    return render(request, 'toca_schedule/schedule_create.html', {'form': form, 'action_table': actions_table})
