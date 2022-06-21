from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import UploadFileForm
from django.core import serializers
from .models import Contact, Page, Company_number, Log, Euralcode
from django.http import JsonResponse
from .services import get_api
import pandas as pd
from datetime import datetime

def pages(request):
    return redirect(reverse_lazy('home'))
    #return render(request, 'pages/pages.html', {'pages':pages})

def page(request, page_id, page_slug):
    page = get_object_or_404(Page, id=page_id)
    return render(request, 'pages/page.html', {'page':page})

def send(request):  
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    return render(request, 'pages/form.html', {'send':send})

def upload_file_test(request):   
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


def upload_contact(request):
    if request.method == 'POST':  
        try:
            Contact.objects.create(name=request.POST['name'], email=request.POST['email'], tel=request.POST['phone'] );
            return JsonResponse({'response': True }) 
        except:
            return JsonResponse({'response': False })      


def companys(wg_klnam):
    result = Company_number.objects.filter(naam__icontains = wg_klnam)
    limit = 100000
    returns = ""    
    for search in result:      
        if len( search.naam ) < limit:
            limit = len( search.naam )
            returns = search
    return returns 

def eurals(wg_prnam):
    result = Euralcode.objects.filter(afvalstof__icontains = wg_prnam).first()  
    return result 

def convertDate(warde):

    dia = warde[:2]
    mes = warde[3:6]
    año = str(2000 + int(warde[-2:]))

    if mes == "Jan":
        return año+"-01-"+dia
    elif dia == "Feb":
        return año+"-02-"+dia
    elif dia == "Mar":
        return año+"-03-"+dia
    elif dia == "Apr":
        return año+"-04-"+dia
    elif dia == "May":
        return año+"-05-"+dia
    elif dia == "Jun":
        return año+"-06-"+dia
    elif dia == "Jul":
        return año+"-07-"+dia
    elif dia == "Aug":
        return año+"-08-"+dia
    elif dia == "Sep":
        return año+"-09-"+dia
    elif dia == "Oct":
        return año+"-10-"+dia
    elif dia == "Nov":
        return año+"-11-"+dia   
    else:
        return año+"-12-"+dia

    return año+"-"+mes+"-"+dia


def upload_file(request):   

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('home'))

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
                is_defined = pd.isna((df[4][i]))
                if i <= 0:
                    continue
                if is_defined:
                    break  

                wg_nr   =   df[4][i]
                wg_wg1a =   df[37][i]
                wg_wg2a =   df[45][i]
                wg_hkwerf = df[106][i]
                wg_klnam =  df[30][i]
                wg_datum =  df[6][i]
                wg_netto=   df[56][i]
                wg_prnam =  df[33][i]


                company =   companys(wg_klnam)  
                eural =     eurals(wg_prnam)       
                warde =     convertDate(wg_datum)      
                
                data = {
                        "referentie":               "70c67101-21e0-4c30-9ccf-63363f93fa82",
                        "identificatie":            "UIT-" + wg_nr,
                        "meldingType":              ("UIT", "IN")[wg_wg2a > wg_wg1a] ,
                        "oorsprong": {
                            "type":                 ("WERF", "BELGISCHE_VESTIGING")[wg_hkwerf == 'KLANT' or  'BOX' in wg_hkwerf] ,     
                            "vestigingsnummer":     company.vestiging,   
                            "btwNummer":            company.ondernemin,
                            "naam":                 company.naam,
                            "straat":               company.straat,
                            "huisnummer":           company.huisnummer,
                            # //CharSequence.notBlank[]
                            "uitbreiding":          "company.adresuitbreiding", 
                            "postcode":             company.postcode,
                            "gemeente":             company.gemeente,
                            "land":                 company.landcode,
                            # //CharSequence.notBlank[]
                            "commentaar":           "dwedwedw"
                        },
                        "bestemming": {
                            "type":                 ("WERF", "BELGISCHE_VESTIGING")[wg_hkwerf == 'KLANT' or  'BOX' in wg_hkwerf] ,     
                            "vestigingsnummer":     company.vestiging,
                            "btwNummer":            company.ondernemin,
                            "naam":                 company.naam,
                            "straat":               company.straat,
                            "huisnummer":           company.huisnummer,
                            # //CharSequence.notBlank[]
                            "uitbreiding":          "company.adresuitbreiding", 
                            "postcode":             company.postcode,
                            "gemeente":             company.gemeente,
                            "land":                 company.landcode,
                            # //CharSequence.notBlank[]
                            "commentaar":           "dewdwddwed"
                        },
                        "periode": {
                            "eenheid":              "DAG",
                            "waarde":               warde
                        },
                        "tonnage":                  wg_netto,
                        "materiaal": {
                            "materiaalcode":        "M01.14",
                            "euralcode":            eural.eural,
                            "omschrijving":         "string",
                            "kwaliteit":            "string"
                        },
                        "ihm": {
                            "btwNummer":            "string"
                        },
                        "verwerking": {
                            "rdCode":               eural.rd,
                            "wijze":                eural.verwer.upper(),
                            "omschrijving":         "string",
                            "inputInRecyclage":     "string"
                        },
                        "vervoerswijze":            "WATERWEG",
                        "toepassingswijze":         "DISPERS_GEBRUIK"
                    }               
                #print("ARMA UNO", i , " ", df[4][i], " ", df[45][i], " ", df[106][i], " ")              
                request_in.append(data)
              
            

            response = get_api(request_in)


            # try:
            #     query = Company_number.objects.get(id = 1)

                
            #     print(query.ondernemin)
               
            # except Exception as e:
            #     print(e)

            status = str(response.get('status'))
            inputs = str(response.get('input'))
            errors = str(response.get('errors'))
            try:
                Log.objects.create(id_user=request.user.id, name_user= request.user.username, log_description=errors );
            except Exception as e:
                json_response = {'response': False, 'msg': e}
            json_response = {'response': True, 'status': status, 'inputs': inputs, 'errors': errors}
        except Exception as e:
            return JsonResponse({'response': False, 'msg': repr(e)}) 
               
    else:
        json_response = {'response': False}
    return JsonResponse(json_response) 