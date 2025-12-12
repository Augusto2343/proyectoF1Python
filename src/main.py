import flet as ft
from utilities import filterSessionsData 
import datetime
def main(page: ft.Page):
    page.title="Paginita F1"
    fechaInicio=""
    fechaFinal=""
    eventos ={"practicas":[{}],"qualys":[{}],"carreras":[{}]}
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
    #Añadiduras a la página
    text =ft.Text(value="Bienvenido a la app F1",color="white")
    page.controls.append(text)
    def updateEventView():
        nonlocal eventos
        page.add(
            ft.Container(
                content= ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Practicas",weight=ft.FontWeight.BOLD),
                                    *(
                                    ft.Card(
                                        content=ft.Container(
                                            padding=10,
                                            content=ft.Column(
                                                [
                                                    ft.Text(f"{practica["session_name"]}  {practica["ubicacion"]}  {practica["pais"]}")
                                                ]
                                            )
                                        )
                                    )
                                    for practica in eventos["practicas"]
                                    
                                )
                                ]
                            )
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Qualys",weight=ft.FontWeight.BOLD),
                                    *(
                                    ft.Card(
                                        content=ft.Container(
                                            padding=10,
                                            content=ft.Column(
                                                [
                                                    ft.Text(f"{practica["session_name"]} {practica["ubicacion"]}  {practica["pais"]}")
                                                ]
                                            )
                                        )
                                    )
                                    for practica in eventos["qualys"]
                                )
                                ]
                            )
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Carreras",weight=ft.FontWeight.BOLD),
                                    *(
                                    ft.Card(
                                        content=ft.Container(
                                            padding=10,
                                            content=ft.Column(
                                                [
                                                    ft.Text(f"{practica["session_name"]}  {practica["ubicacion"]}  {practica["pais"]}")
                                                ]
                                            )
                                        )
                                    )
                                    for practica in eventos["carreras"]
                                )
                                ]
                            )
                        )
                    ]
                )
            )

        )

    page.add(
        ft.Row(
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
                )
                ]
                ),
            ft.Button(
                    "Buscar Eventos",
                    on_click=searchEvents
                )
    ]
            )
    )

    page.update()
ft.app(target=main)
