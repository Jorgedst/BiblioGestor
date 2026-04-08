import flet as ft
from views.reusable.btnSalir import btnSalir

def userSideBar(
    page: ft.Page,
    on_inicio=None,
    on_devolver_libro=None,
    on_historial=None,
    on_editar_perfil=None,
):
    async def ir_inicio(e):
        if on_inicio is not None:
            await on_inicio(e)
        else:
            await page.push_route("/userDashboard")

    async def irDevolucionLibro(e):
        if on_devolver_libro is not None:
            await on_devolver_libro(e)
        else:
            await page.push_route("/devolverLibro")

    async def irHistorial(e):
        if on_historial is not None:
            await on_historial(e)
        else:
            await page.push_route("/historial")
    async def irEditarPerfil(e):
        if on_editar_perfil is not None:
            await on_editar_perfil(e)
        else:
            await page.push_route("/editarPerfil")

    return ft.Container(
        width=230,
        height=670,
        content=ft.Column(controls=[
            ft.Container(
                content=ft.Text(
                    value = "BiblioGestor",
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
                        on_click=ir_inicio,
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
            # Boton devolución
            ft.Container(
                content=ft.Text(
                    "Devolución",
                    size=15,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.Margin(10, 5, 0, 0),
            ),
            ft.Container(
                margin=ft.Margin(8, 0, 0, 0),
                border_radius=10,
                bgcolor=ft.Colors.WHITE_54,
                content=ft.Row(controls=[
                    ft.Icon(ft.Icons.BOOK,
                            color=ft.Colors.BLACK,
                            align=ft.Alignment.CENTER_LEFT,
                            ),
                    ft.Button(
                        width=190,
                        content="Devolver un libro",
                        on_click = irDevolucionLibro,
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
            # Botón Historial
            ft.Container(
                content=ft.Text(
                    "Mi historial de prestamos",
                    size=15,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.Margin(10, 5, 0, 0),
            ),
            ft.Container(
                margin=ft.Margin(8, 0, 0, 0),
                border_radius=10,
                bgcolor=ft.Colors.WHITE_54,
                content=ft.Row(controls=[
                    ft.Icon(ft.Icons.HISTORY,
                            color=ft.Colors.BLACK,
                            align=ft.Alignment.CENTER_LEFT,
                            ),
                    ft.Button(
                        width=190,
                        content="Historial",
                        on_click=irHistorial,
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
                    ),

                ])
            ),
            # Botón Editar
            ft.Container(
                content=ft.Text(
                    "Editar",
                    size=15,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                margin=ft.Margin(10, 5, 0, 0),
            ),
            ft.Container(
                margin=ft.Margin(8, 0, 0, 0),
                border_radius=10,
                bgcolor=ft.Colors.WHITE_54,
                content=ft.Row(controls=[
                    ft.Icon(ft.Icons.EDIT,
                            color=ft.Colors.BLACK,
                            align=ft.Alignment.CENTER_LEFT,
                            ),
                    ft.Button(
                        width=190,
                        content="Editar perfil",
                        on_click=irEditarPerfil,
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
                    ),

                ])
            ),
            #Boton de salir
            ft.Container(
                margin = ft.Margin(0,220,0,0),
                content= ft.Row(
                    alignment= ft.MainAxisAlignment.START,
                    controls= [
                        btnSalir(page)]),
            )
        ]
        )
    )
