from urllib.request import urlopen
import json



def filterSessionsData (date_start, date_end):
    practicas=[]
    qualy=[]
    race=[]
    response = urlopen(f"https://api.openf1.org/v1/sessions?date_start>={date_start}&date_end<={date_end}")
    data= json.loads(response.read().decode("utf-8"))
    for i in data:
        if(i["session_type"] == "Practice"):
            practicas.append({"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
        if(i["session_type"] =="Qualifying"):
            qualy.append({"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
        if(i["session_type"] =="Race"):
            race.append({"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
    eventos ={"practicas":practicas,"qualys":qualy,"carreras":race}
    return eventos