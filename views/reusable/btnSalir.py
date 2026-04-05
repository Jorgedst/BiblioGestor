import flet as ft


def btnSalir(page: ft.Page):
    async def ir_inicio(e):
        await page.push_route("/")
        
    return ft.Container(
        content=ft.Button(
            on_click= ir_inicio,
            icon= ft.Icons.EXIT_TO_APP,
            content=ft.Text(
                value="Salir",
                size=15,
                weight=ft.FontWeight.W_600),
            style=ft.ButtonStyle(
                alignment=ft.Alignment(-1, 0),
                mouse_cursor=ft.MouseCursor.CLICK,
                color={
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                },
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                },
                shadow_color=ft.Colors.TRANSPARENT,
                shape=ft.ContinuousRectangleBorder(
                    radius=10),
            ),
        )
    )
