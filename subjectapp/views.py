from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.db.models.query import QuerySet
from django.template.loader import render_to_string

from studentapp.models import Stream
from subjectapp.models import Subject

# Create your views here.
def subject_list(request):
    streams: QuerySet = Stream.objects.all()
    subjects: QuerySet = Subject.objects.select_related("stream")
    return render(request, "subjectapp/add_subject.html", {"streams" : streams, "subjects": subjects})

def get_total_sem(request):
    stream_id = request.GET.get('stream_id')
    # total_sem = Stream.objects.all()
    selected_sem:Stream = Stream.objects.get(id=stream_id)
    total_sem = selected_sem.semester
    sem_data:list = list(range(1,total_sem+1))
    # print(sem_data)
    return JsonResponse({"sem_data":sem_data}, status=200)

def add_subject(request):
    if request.method == "POST":
        stream_id = request.POST.get("stream_id")   # coming from DropDown
        subject_name = request.POST.get("subject_name")
        subject_semester = request.POST.get("subject_semester")
        
        # print(request.POST)
        if stream_id and subject_name and subject_semester:
            try:
                stream_found: Stream = Stream.objects.get(id=stream_id) # It returns an instance of the Stream model that matches
                print(f'Stream found: {stream_found}')
                print(f'Stream Type: {type(stream_found)}')
                
                if Subject.objects.filter(name=subject_name, stream=stream_found, semester=subject_semester).exists():
                    return JsonResponse({"message": "Subject with this name exist for the selected Stream found"}, status=400)
                    # message:str = "Subject with this name exist for the selected Stream found"
                else:
                    Subject.objects.create(name=subject_name, stream=stream_found, semester=subject_semester)
                    message:str = "Subject added successfully"
                
                # select_related('foreign_key) this function will collect all the instances of the Primary Key Model in association with the Foreign Key Model
                subjects: QuerySet = Subject.objects.select_related("stream")
                html_string: str = render_to_string("partial/subject_rows.html",{"subjects":subjects})
                
                return JsonResponse({
                    "subjects": html_string,
                    "message": message
                }, status=200)
            except Stream.DoesNotExist:
                return JsonResponse({"message": "Stream not found"}, status=400)
        

def edit_subject(request: HttpRequest, id: int):
    if request.method == 'POST':
        subject_name: str = request.POST.get('subject_name')
        stream_id = request.POST.get('stream_id')
        subject_semester = request.POST.get('subject_semester')
        # print(id,stream_id)
                
        if not Subject.objects.filter(name=subject_name, semester=subject_semester).exclude(id=id).exists():
            subject = Subject.objects.get(id=id)
            subject.name = subject_name
            stream_found: Stream = Stream.objects.get(id=stream_id)
            subject.stream = stream_found
            subject.semester = subject_semester
            subject.save()
            message:str = "Subject updated successfully"
        else:
            message:str = "Subject name already exist..."

        subjects: QuerySet = Subject.objects.all()
        html_string = render_to_string("partial/subject_rows.html", {"subjects": subjects})
        return JsonResponse({"subjects": html_string, "message": message}, status=201)
        
def delete_subject(request: HttpRequest, id=None):
    subject = get_object_or_404(Subject, pk=id)
    print(subject)
    subject.delete()
    
    subjects: QuerySet = Subject.objects.all()
    html_string = render_to_string("partial/subject_rows.html", {"subjects": subjects})
    return JsonResponse({
        "subjects": html_string,
        "message": "Subject deleted successfully"
    })