import flet as ft


def botonesCategoria(texto: str, seleccionado: bool = False, on_click=None):
    """
    Botón de categoría con estado toggle.
    - seleccionado=False → verde (por defecto)
    - seleccionado=True  → gris oscuro (activo)
    """
    if seleccionado:
        bg_default = ft.Colors.GREY_800
        bg_hover = ft.Colors.GREY_900
        text_color = ft.Colors.WHITE
    else:
        bg_default = ft.Colors.LIGHT_GREEN_600
        bg_hover = ft.Colors.LIGHT_GREEN_900
        text_color = ft.Colors.WHITE

    btn = ft.Button(
        width=125,
        content=ft.Text(
            value=texto,
            size=11,
            weight=ft.FontWeight.W_600),
        style=ft.ButtonStyle(
            alignment=ft.Alignment(-1, 0),
            mouse_cursor=ft.MouseCursor.CLICK,
            color={
                ft.ControlState.DEFAULT: text_color,
            },
            bgcolor={
                ft.ControlState.DEFAULT: bg_default,
                ft.ControlState.HOVERED: bg_hover,
            },
            shape=ft.ContinuousRectangleBorder(
                radius=10),
        ),
        on_click=on_click,
    )
    return btn
