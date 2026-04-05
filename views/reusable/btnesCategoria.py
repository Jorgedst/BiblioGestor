import flet as ft


def botonesCategoria(texto: str):
    return ft.Button(
        width=105,
        content=ft.Text(
            value= texto,
            size = 11,
            weight= ft.FontWeight.W_600),
        style=ft.ButtonStyle(
            alignment=ft.Alignment(-1, 0), 
            mouse_cursor=ft.MouseCursor.CLICK,
            color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE,
            },
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.LIGHT_GREEN_600,
                ft.ControlState.HOVERED: ft.Colors.LIGHT_GREEN_900,
                ft.ControlState.PRESSED: ft.Colors.GREY_700,
            },
            shape=ft.ContinuousRectangleBorder(
                radius=10),
        ),
    )
