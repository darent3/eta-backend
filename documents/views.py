from django.shortcuts import render
from django.db.models import Q
from .models import Document


def search_documents(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search in both title and extracted text
        results = Document.objects.filter(
            Q(title__icontains=query) | Q(extracted_text__icontains=query)
        )

    context = {
        'query': query,
        'results': results,
        'result_count': len(results),  # ← CHANGE .count() to len()
    }
    return render(request, 'documents/search.html', context)
