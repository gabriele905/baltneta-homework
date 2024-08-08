import pandas
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pydantic_core._pydantic_core import ValidationError

from .forms import UploadFileForm
from .models import PandasValidator, Category


def list(request):
    return render(request, 'list_categories.html', {'object_list': Category.objects.all()})


def upload_categories(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            errors, data_frame = validate_uploaded_file(request.FILES['file'])

            if errors:
                return render(request, 'upload.html', {'form': UploadFileForm(), 'errors': errors})

            not_valid_categories, valid_categories = handle_data_frame(data_frame)

            Category.objects.bulk_create([
                Category(category=row['category'], number=row['number'], create_user=request.user) for _, row in
                valid_categories.iterrows()
            ])

            if not not_valid_categories.empty:
                return render(request, 'not_valid_dataframe.html',
                              {'df': not_valid_categories,
                               'message': 'These categories need to be saved through admin panel.'})

            return HttpResponseRedirect('/categories/')
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def validate_uploaded_file(file):
    errors = None
    df = pandas.read_excel(file, na_filter=False)

    try:
        PandasValidator(df_dict=df.to_dict(orient='records'))
    except ValidationError as e:
        errors = e.errors()

    return errors, df


def handle_data_frame(df):
    not_valid_categories = df[df['category'].map(df['category'].value_counts()) <= 1]
    valid_categories = df[df.duplicated(['category'], keep=False)]

    return not_valid_categories, valid_categories
