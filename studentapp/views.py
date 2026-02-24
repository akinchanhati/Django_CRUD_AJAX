from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import QuerySet
from django.template.loader import render_to_string

from .models import Stream

# Function Based View
def stream_list(request: HttpRequest) -> HttpResponse:
    streams: QuerySet = Stream.objects.all()    # ORM (ModelName Data Adapter which connects the ORM)
    return render(request,'studentapp/add_stream.html',{'streams': streams})               # HttpResponse
    
def add_stream(request: HttpRequest):
    if request.method == 'POST':
        stream_name: str = request.POST['stream_name']
        stream_description: str = request.POST['stream_description']
        stream_semester: str = request.POST['stream_semester']

        if stream_name:
            if not Stream.objects.filter(name=stream_name).exists():
                Stream.objects.create(name=stream_name, description=stream_description, semester=stream_semester)
                # Updated list after saving new Stream
                streams: QuerySet = Stream.objects.all()
                # TypeError: Object of type QuerySet is not JSON serializable
                html_string = render_to_string("partial/stream_rows.html", {"streams": streams})
                return JsonResponse({"streams": html_string, "message": "Stream added successfully"}, status=201)
            else:
                return JsonResponse({"message":"Stream already exist"}, status = 400)
        else:
            return JsonResponse({
                "success": True,
                "message":"Stream name should be provided"}, status= 400)
    else:        
        return render(request,'studentapp/add_stream.html')

def edit_stream(request: HttpRequest, id: int):
    if request.method == 'POST':
        stream_name: str = request.POST['stream_name']  #request.POST.get('stream_name','')
        stream_description: str = request.POST['stream_description']
        stream_semester: str = request.POST['stream_semester']
        
        if not Stream.objects.filter(name=stream_name).exclude(id=id).exists():
            stream = Stream.objects.get(id=id)
            stream.name = stream_name
            stream.description = stream_description
            stream.semester = stream_semester
            stream.save()
            streams: QuerySet = Stream.objects.all()
            html_string = render_to_string("partial/stream_rows.html", {"streams": streams})
            return JsonResponse({"streams": html_string, "message": "Stream updated successfully"}, status=201)
        
def delete_stream(request: HttpRequest, stream_id=None):
    stream = get_object_or_404(Stream, pk=stream_id)
    stream.delete()
    
    streams: QuerySet = Stream.objects.all()
    html_string = render_to_string("partial/stream_rows.html", {"streams": streams})
    return JsonResponse({
        "streams": html_string,
        "message": "Stream deleted successfully"
    })
