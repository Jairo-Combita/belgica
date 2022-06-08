from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from .forms import UploadFileForm
from django.core import serializers
from .models import Page, Company_number
from django.http import JsonResponse
from .services import get_api
import pandas as pd

def pages(request):
    pages = get_list_or_404(Page)
    return render(request, 'pages/pages.html', {'pages':pages})

def page(request, page_id, page_slug):
    page = get_object_or_404(Page, id=page_id)
    return render(request, 'pages/page.html', {'page':page})

def send(request):
    return render(request, 'pages/form.html', {'send':send})

def upload_file(request):   
    if request.method == 'POST':          
        try:
            datas = [
                        {
                            "referentie": "string",
                            "identificatie": "string",
                            "meldingType": "IN",
                            "oorsprong": {
                            "type": "INZAMELRONDE",
                            "vestigingsnummer": "string",
                            "btwNummer": "string",
                            "naam": "string",
                            "straat": "string",
                            "huisnummer": "string",
                            "uitbreiding": "string",
                            "postcode": "string",
                            "gemeente": "string",
                            "land": "string",
                            "commentaar": "string"
                            },
                            "bestemming": {
                            "type": "BELGISCHE_VESTIGING",
                            "vestigingsnummer": "string",
                            "btwNummer": "string",
                            "naam": "string",
                            "straat": "string",
                            "huisnummer": "string",
                            "uitbreiding": "string",
                            "postcode": "string",
                            "gemeente": "string",
                            "land": "string",
                            "commentaar": "string"
                            },
                            "periode": {
                            "eenheid": "JAAR",
                            "waarde": "string"
                            },
                            "tonnage": "string",
                            "materiaal": {
                            "materiaalcode": "M00.00",
                            "euralcode": "01 01 01",
                            "omschrijving": "string",
                            "kwaliteit": "string"
                            },
                            "ihm": {
                            "btwNummer": "string"
                            },
                            "verwerking": {
                            "rdCode": "D1",
                            "wijze": "ANDERE_AFVALVERBRANDING",
                            "omschrijving": "string",
                            "inputInRecyclage": "string"
                            },
                            "vervoerswijze": "WATERWEG",
                            "toepassingswijze": "DISPERS_GEBRUIK"
                        }
                    ]                
                
            response = get_api(datas)            
            status = str(response.get('status'))
            inputs = str(response.get('input'))
            errors = str(response.get('errors'))

            json_response = {'response': True, 'status': status, 'inputs': inputs, 'errors': errors}
        except:
            json_response = {'response': False}
               
    else:
        json_response = {'response': False}
    return JsonResponse(json_response) 






def upload_file_test(request):   
    if request.method == 'POST':  
        
        try:
            request_in = []  
            form = UploadFileForm(request.POST, request.FILES)       
            data = request.FILES['file']        
            sheet_name = 0 
            header = 0
        
            df = pd.read_excel(data, sheet_name = sheet_name, header = header)
            #print("THIS ROW ========>   "+ df["PRUEBA"][i])
            
            for i in df.index: 
                data = {
                        "referentie": "string",
                        "identificatie": df["wg_nr"][i],
                        "meldingType": ("UIT", "IN")[df["wg_wg2a"][i] > df["wg_wg2a"][i]] ,
                        "oorsprong": {
                            "type": (df["wg_hkwerf"][i], "Belgische vestiging")[df["wg_hkwerf"][i] == 'KLANT' or  'BOX' in df["wg_hkwerf"][i]] ,     
                            "vestigingsnummer": "wg_trnam se compara contra naam en tabla company nummer y retorna VESTIGING (ERROR: MAS DE UN REGISTRO)",   
                            "btwNummer": "wg_trnam se compara contra naam en tabla company nummer y retorna ONDERNEMIN (ERROR: MAS DE UN REGISTRO)",
                            "naam": "wg_trnam se compara contra naam en tabla company nummer y retorna ADRESUITBREDING (ERROR: MAS DE UN REGISTRO)",
                            "straat": "string",
                            "huisnummer": "string",
                            "uitbreiding": "string",
                            "postcode": "wg_trnam se compara contra naam en tabla company nummer y retorna POSTCODE (ERROR: MAS DE UN REGISTRO)",
                            "gemeente": "string",
                            "land": "wg_trnam se compara contra naam en tabla company nummer y retorna LANDCODE (ERROR: MAS DE UN REGISTRO)",
                            "commentaar": "string"
                        },
                        "bestemming": {
                            "type": (df["wg_hkwerf"][i], "Belgische vestiging")[df["wg_hkwerf"][i] == 'KLANT' or  'BOX' in df["wg_hkwerf"][i]] ,
                            "vestigingsnummer": "string",
                            "btwNummer": "string",
                            "naam": "string",
                            "straat": "string",
                            "huisnummer": "string",
                            "uitbreiding": "string",
                            "postcode": "string",
                            "gemeente": "string",
                            "land": "string",
                            "commentaar": "string"
                        },
                        "periode": {
                            "eenheid": "JAAR",
                            "waarde": "string"
                        },
                        "tonnage": "string",
                        "materiaal": {
                            "materiaalcode": "M00.00",
                            "euralcode": "01 01 01",
                            "omschrijving": "string",
                            "kwaliteit": "string"
                        },
                        "ihm": {
                            "btwNummer": "string"
                        },
                        "verwerking": {
                            "rdCode": "D1",
                            "wijze": "ANDERE_AFVALVERBRANDING",
                            "omschrijving": "string",
                            "inputInRecyclage": "string"
                        },
                        "vervoerswijze": "WATERWEG",
                        "toepassingswijze": "DISPERS_GEBRUIK"
                    }               
                
                request_in.append(data)
                
            response = get_api(request_in)

            try:
                query = Company_number.objects.get(id = 1)

                
                print(query.ondernemin)
               
            except Exception as e:
                print(e)

            status = str(response.get('status'))
            inputs = str(response.get('input'))
            errors = str(response.get('errors'))

            json_response = {'response': True, 'status': status, 'inputs': inputs, 'errors': errors}
        except:
            json_response = {'response': False}
               
    else:
        json_response = {'response': False}
    return JsonResponse(json_response) 