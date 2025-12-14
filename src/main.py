import flet as ft
from utilities import filterSessionsData,filterSessionsByCircuit,obtainRaceData
import datetime
def main(page: ft.Page):
    results_columns = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    raceData=ft.Column(expand=True,scroll=ft.ScrollMode.ADAPTIVE)
    page.title="Paginita F1"
    fechaInicio=""
    fechaFinal=""
    eventos ={"practicas":[{}],"qualys":[{}],"carreras":[{}]}
    dataRaceObj=None
    page.scroll=None
    def handle_change(e):
        nonlocal fechaFinal,fechaInicio
        match e.control.data:
            case "inicio":
                fechaInicio = e.control.value.strftime('%m/%d/%Y')
            case "limite":
                fechaFinal = e.control.value.strftime('%m/%d/%Y')
            case _:
                print(f"Uhmm 🤔 {e.control.data}")
    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    def searchEvents (e):
        nonlocal eventos
        print(fechaInicio,fechaFinal)
        eventos =filterSessionsData(fechaInicio,fechaFinal)
        print(eventos)
        updateEventView()

    def updateEventView():
        nonlocal eventos
        results_columns.controls.clear()
        results_columns.controls.append(
                ft.Text("Resultados de la búsqueda",size=25,color=ft.Colors.CYAN)
            )
        results_columns.controls.extend(
            [
                ft.Button(
                    f"Carrera de:{carrera["circuito"]}",
                    on_click=updateRaceData,
                    data=carrera["session_nro"]
                )
                for carrera in eventos["carreras"]
            ]

        )
        page.update()
    def updateRaceData(e):
        nonlocal dataRaceObj
        raceId=e.control.data
        print(raceId)
        raceData.controls.clear()
        dataRaceObj=obtainRaceData(raceId)
        raceData.controls.extend(

                    ft.Card(
                            content=ft.Column(
                                [
                                    ft.Text(f"Corredor N°:{driver["numeroPiloto"]}"),
                                    ft.Image(
                                        src=driver["foto"]  
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(f"Nombre piloto: {driver["nombre"]}"),
                                            ft.Text(f"Acrónimo: {driver["acronimo"]}")
                                        ]
                                    )
                                ]
                            )
                        )
                    
                    for driver in dataRaceObj["pilotos"]
            # ft.Container(
            #     content=[
            #         ft.Text(f"Ubicacion: {dataRaceObj['general']["location"]} Código de país: {dataRaceObj["general"]["country_code"]}"),
            #         ft.Text(f"Circuito: {dataRaceObj["general"]["circuit_short_name"]}")
            #     ]
            # )
        )
        page.update()
    #Añadiduras a la página
    text =ft.Text(value="Bienvenido a la app F1",color="white",size=ft.FontWeight.BOLD)
    page.controls.append(text)
    page.add(
        ft.Text(
            "Buscar carreras por fechas",
            size=40,

        ),
        ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START, 
            controls=[
            
        ft.Column(
            [
            ft.Row(
                [ft.Container(
                    content=ft.ElevatedButton(
                    "Fecha Inicio",
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda e: page.open(
                        ft.DatePicker(
                            data="inicio",
                            first_date=datetime.datetime(year=2000, month=10, day=1),
                            last_date=datetime.datetime(year=2025, month=12, day=7),
                            on_change=handle_change,
                            on_dismiss=handle_dismissal,
                        )
                    ),
                )
                ),
                ft.Container(
                    content=ft.Button(
                    "Fecha Limite",
                    on_click=lambda e: page.open(
                        ft.DatePicker(
                            data="limite",
                            first_date=datetime.datetime(year=2000, month=10, day=1),
                            last_date=datetime.datetime(year=2025, month=12, day=7),
                            on_change=handle_change,
                            on_dismiss=handle_dismissal,
                        )
                    )
                )
                ),
            ft.Button(
                    "Buscar Eventos",
                    on_click=searchEvents
                )
                ]
                ),

            results_columns
        ]
            ),
            raceData
            ]
            )
    )

    page.update()
ft.app(target=main)
