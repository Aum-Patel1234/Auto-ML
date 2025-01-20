from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os,json

def home_page(request):            
    if request.method == "POST":
        file : pd.DataFrame = None
        uploaded_File = request.FILES['dataset']
        # print(uploaded_File.name,uploaded_File.size) 
        # print(os.path.abspath(__file__), 'file \t ',__file__)
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        mediaPath = os.path.join(baseDir, 'media')
        # print(os.listdir(mediaPath))
        for f in os.listdir(mediaPath):
            os.remove(os.path.join(mediaPath, f))

        file_json = None        # to convert pd.Dataframe to json

        try:
            extension = uploaded_File.name.split('.')[-1]

            if extension == 'csv':
                file = pd.read_csv(uploaded_File)
            elif extension == 'xlsx':
                file = pd.read_excel(uploaded_File)
            elif extension == 'xls':
                file = pd.read_excel(uploaded_File, engine='xlrd')
            else:
                return JsonResponse({'error': 'Unsupported file format'}, status=400)
            
            file_json = json.dumps(list(file.columns))      # convert columns to json
                
        except Exception as e:
            return JsonResponse({'error': f'Failed to process file: {str(e)}'}, status=400)
        
        fs = FileSystemStorage()
        fs.save(uploaded_File.name, uploaded_File)
        
        return JsonResponse({'data': file_json})    # return json response of the columns of the dataset

    return render(request, 'web/index.html')