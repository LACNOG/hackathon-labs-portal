from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from io import StringIO
from .models import Workshop

@user_passes_test(lambda u: u.is_staff)
def import_lab_equipment(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
        else:
            file_data = csv_file.read().decode("utf-8")
            csv_data = StringIO(file_data)
            imported_count = workshop.import_lab_equipment(csv_data)
            messages.success(request, f'Lab equipment imported successfully. {imported_count} items added.')
    return redirect('admin:portal_workshop_change', object_id=workshop.id)