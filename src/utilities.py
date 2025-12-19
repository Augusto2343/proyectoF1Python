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
            practicas.append({"circuito":i["circuit_short_name"],"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
        if(i["session_type"] =="Qualifying"):
            qualy.append({"circuito":i["circuit_short_name"],"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
        if(i["session_type"] =="Race"):
            race.append({"circuito":i["circuit_short_name"],"session_name":i["session_name"],"session_nro":i["session_key"],"ubicacion":i["location"],"pais":i["country_name"],"abreviacionPais":i["country_code"],"fechaInicio":i["date_start"],"fechaFin":i["date_end"]})
    eventos ={"practicas":practicas,"qualys":qualy,"carreras":race}

    return eventos

def filterSessionsByCircuit (sessions) :
    filteredSession={}
    
    for i in sessions:
        filteredSession[i["circuito"]]=i
        
    print(f"Sesiones filtradas por circuito {filteredSession}")

def obtainRaceData (idSess):
    raceData={"pilotos":[],"resultados":[],"general":{}}
    response = urlopen(f"https://api.openf1.org/v1/sessions?session_key={idSess}")
    data= json.loads(response.read().decode("utf-8"))
    for i in data:
        raceData["general"] = {
            "meeting_key": i.get("meeting_key"),
            "session_key": i.get("session_key"),
            "location": i.get("location"),
            "session_type": i.get("session_type"),
            "date_start": i.get("date_start"),
            "date_end": i.get("date_end"),
            "session_name": i.get("session_name"),
            "country_key": i.get("country_key"),
            "country_name": i.get("country_name"),
            "country_code": i.get("country_code"),
            "circuit_key": i.get("circuit_key"),
            "circuit_short_name": i.get("circuit_short_name"),
            "year": i.get("year"),
        }


    response = urlopen(f"https://api.openf1.org/v1/drivers?session_key={idSess}")
    data= json.loads(response.read().decode("utf-8"))

    for i in data:
        raceData["pilotos"].append({"nombre":i["full_name"],"acronimo":i["name_acronym"],"foto":i["headshot_url"],"numeroPiloto":i["driver_number"],"equipo":i["team_name"],"color_equipo":i["team_colour"]})

        
    response = urlopen(f"https://api.openf1.org/v1/session_result?session_key={idSess}")
    data= json.loads(response.read().decode("utf-8"))
    for i in data:
        datosPilotos = extrDatosPilotos(raceData["pilotos"],i["driver_number"])
        print(i,datosPilotos)
        raceData["resultados"].append({**i,**datosPilotos})
        print(raceData["resultados"])
    print(raceData["general"])
    return raceData

def extrDatosPilotos(arrayPilotos,numeroPiloto):
        for racer in arrayPilotos:
            if (racer["numeroPiloto"] == numeroPiloto):
                elementosPiloto={"nombre":racer["nombre"],"acronimo":racer["acronimo"],"color_equipo":racer["color_equipo"],"foto":racer["foto"]}
                return elementosPiloto
        