from django.http import Http404, JsonResponse, HttpRequest
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import os, json, uuid

def home_page(request:HttpRequest):
    if request.method == "POST":
        file : pd.DataFrame = None
        uploaded_File = request.FILES['dataset']
        file_uuid = uuid.uuid4()
        # print(uploaded_File.name,uploaded_File.size) 
        # print(os.path.abspath(__file__), 'file \t ',__file__)
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # get base dir name    

        mediaPath = os.path.join(baseDir, 'media')
        # print(os.listdir(mediaPath))
        dirSize:int = __getDirSize(mediaPath)
        size_limit_mb = 200                                                       # max size in mb 
        size_limit_bytes:int = size_limit_mb * 1024 * 1024

        # print(f'{size_limit_bytes}  {dirSize}')
        if size_limit_bytes < dirSize:                                            # delete all files when the size goes above size_limi_mb limit
            try:
                for f in os.listdir(mediaPath):
                    os.remove(os.path.join(mediaPath, f))
            except Exception as e:
                print(e)


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
        
        except FileNotFoundError as e:
            return render(request, '404.html')
        except Exception as e:
            return JsonResponse({'error': f'Failed to process file: {str(e)}'}, status=400)
        
        fs = FileSystemStorage()
        fs.save(f'{file_uuid}_{uploaded_File.name}', uploaded_File)
        
        return JsonResponse({'file_id': file_uuid,'data': file_json})    # return json response of the columns of the dataset

    return render(request, 'web/index.html')

def __getDirSize(dirname) -> int:
    size:int = 0

    for root, dirs, files in os.walk(dirname):
        for file in files:
            size += os.path.getsize(os.path.join(root,file))
    
    return size

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)