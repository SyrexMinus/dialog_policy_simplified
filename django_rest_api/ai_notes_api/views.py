from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteSerializer
from .utils import DateTimeExtractor


class NoteView(APIView):
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response({"notes": serializer.data})

    def post(self, request):
        input_text = request.data.get('input_text')

        date_time_extractor = DateTimeExtractor(input_text)
        extracted_times = "".join(date_time_extractor.extracted_times)
        extracted_dates = "".join(date_time_extractor.extracted_dates)
        # Create an article from the above data
        note = {'input_text': input_text, 'times': extracted_times, 'dates': extracted_dates}

        serializer = NoteSerializer(data=note)
        if serializer.is_valid(raise_exception=True):
            saved_note = serializer.save()
            return Response({"success": f"Note '{saved_note}' created successfully"})

    def put(self, request, pk):
        saved_note = get_object_or_404(Note.objects.all(), pk=pk)
        data = request.data.get('note')
        serializer = NoteSerializer(instance=saved_note, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_note = serializer.save()
            return Response({
                "success": f"Note '{saved_note}' updated successfully"
            })

    def delete(self, request, pk):
        note = get_object_or_404(Note.objects.all(), pk=pk)
        note.delete()
        return Response({
            "success": f"Note with id '{pk}' has been deleted."
        })
