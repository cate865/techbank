from rest_framework.decorators import api_view
from rest_framework.response import Response
import dropbox
import os
from dotenv import load_dotenv
from rest_framework import status


load_dotenv()     # loading environment variables from .env
token = os.getenv('DBX_ACCESS_TOKEN')

dbx = dropbox.Dropbox(token)    # initializing Dropbox API Object


def create_binary_file_and_path(fname, category, f):
    path = os.path.join('/',category,fname)
    print("Path " + str(path))
    file_dict = {"category":category,
                 "f": f.read(),
                "path": path,
                }
    
    return file_dict


@api_view(['POST'])
def upload_resource(request):

    categories = ['FrontendDevelopment', 'BackendDevelopment', 'DevOps', 'UI-UX', 'ProductMgt', 'CareerDevelopment', 'MobileDevelopment']
    if request.data['category'] not in categories:
        raise Exception('Category is invalid.')
    
    data = create_binary_file_and_path(request.data['fname'],request.data['category'],request.data['file'])
    result = dbx.files_upload(data["f"], data["path"])  # upload file to Dropbox
    res_name = result.name
    res_path = result.path_display

    return Response({"name":res_name, "path_display":res_path },status=status.HTTP_200_OK)
    

@api_view(['GET'])
def fetch_resources(request):

    result = dbx.files_list_folder('')    # retrieves a list of all the folders in the current app
    result_arr = []

    for entry in result.entries:
        entry_dict = {'category': str(entry.name), 'files':[]}
        result_arr.append(entry_dict)
        result2 = dbx.files_list_folder(os.path.join('/', str(entry.name)))   # retrieves children of the current folder in iteration

        if len(result2.entries) > 0:
            for entry2 in result2.entries:
                
                entry_dict['files'].append({"name":entry2.name, 
                                            "lastModified":entry2.client_modified, 
                                            "link":dbx.sharing_create_shared_link_with_settings(entry2.path_display).url})
                
    return Response({"resources":result_arr},status=status.HTTP_200_OK)


@api_view(['POST'])
def search_by_category(request):

    categories = ['FrontendDevelopment', 'BackendDevelopment', 'DevOps', 'UI-UX', 'ProductMgt', 'CareerDevelopment', 'MobileDevelopment']
    if request.data['category'] not in categories:
        raise Exception('Category is invalid.')
    
    options = dropbox.files.SearchOptions(path=os.path.join('/', request.data['category']),filename_only=True)  # category and query specified in this search
    result = dbx.files_search_v2(request.data['query'],options=options)    # search function

    result_arr = []

    for match in result.matches:
        file_dict = {"name":match.metadata.get_metadata().name,
                    "lastModified":match.metadata.get_metadata().client_modified, 
                    "link":dbx.sharing_create_shared_link_with_settings(match.metadata.get_metadata().path_display).url}
        result_arr.append(file_dict)

    return Response({'resources': result_arr}, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_by_filename(request):

    options=dropbox.files.SearchOptions(filename_only=True)     
    result = dbx.files_search_v2(request.data['query'],options=options)    # query only specified in this search

    result_arr = []

    for match in result.matches:
        file_dict = {"name":match.metadata.get_metadata().name,
                    "lastModified":match.metadata.get_metadata().client_modified, 
                    "link":dbx.sharing_create_shared_link_with_settings(match.metadata.get_metadata().path_display).url}
        result_arr.append(file_dict)

    return Response({'resources': result_arr}, status=status.HTTP_200_OK)

