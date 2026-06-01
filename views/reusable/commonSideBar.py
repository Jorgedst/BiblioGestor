import flet as ft
def commonSideBar(page: ft.Page):
    async def ir_inicio(e):
        await page.push_route("/")

    return ft.Container(
        width=230,
        height=670,
        content=ft.Column(controls=[
            ft.Container(
                content=ft.Text(
                    "BiblioGestor",
                    size=25,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.Margin(10, 5, 0, 0),
            ),
            ft.Container(
                content=ft.Text(
                    "Descubrir",
                    size=15,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.Margin(10, 10, 0, 0),
            ),
            # Botón Inicio
            ft.Container(
                margin=ft.Margin(8, 0, 0, 0),
                border_radius=10,
                bgcolor=ft.Colors.WHITE_54,
                content=ft.Row(controls=[
                    ft.Icon(ft.Icons.HOME,
                            color=ft.Colors.BLACK,
                            align=ft.Alignment.CENTER_LEFT,
                            ),
                    ft.Button(
                        width=190,
                        content="Inicio",
                        on_click = ir_inicio,
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT: ft.Colors.BLACK,
                            },
                            bgcolor={
                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                            },
                            shape=ft.ContinuousRectangleBorder(),
                            mouse_cursor=ft.MouseCursor.CLICK,
                            padding=ft.Padding(0),
                            shadow_color=ft.Colors.TRANSPARENT,
                            alignment=ft.Alignment.CENTER_LEFT,
                        )
                    )
                ])
            ),
        ]
        )
    )
