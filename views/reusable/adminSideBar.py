import flet as ft
from views.reusable.btnSalir import btnSalir


def adminSideBar(
    page: ft.Page,
    on_inicio=None,
    on_libros=None,
    on_prestamos=None,
    on_devoluciones=None,
    on_disponibles=None,
    on_prestados=None,
    on_perdidos=None,
):
    async def _inicio(e):
        if on_inicio is not None:
            await on_inicio(e)

    async def _libros(e):
        if on_libros is not None:
            await on_libros(e)

    async def _prestamos(e):
        if on_prestamos is not None:
            await on_prestamos(e)

    async def _devoluciones(e):
        if on_devoluciones is not None:
            await on_devoluciones(e)

    async def _disponibles(e):
        if on_disponibles is not None:
            await on_disponibles(e)

    async def _prestados(e):
        if on_prestados is not None:
            await on_prestados(e)

    async def _perdidos(e):
        if on_perdidos is not None:
            await on_perdidos(e)

    def _nav_row(icon, label, on_click):
        return ft.Container(
            margin=ft.Margin(8, 0, 0, 0),
            border_radius=10,
            bgcolor=ft.Colors.WHITE_54,
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=ft.Colors.BLACK, align=ft.Alignment.CENTER_LEFT),
                    ft.Button(
                        width=190,
                        content=label,
                        on_click=on_click,
                        style=ft.ButtonStyle(
                            color={ft.ControlState.DEFAULT: ft.Colors.BLACK},
                            bgcolor={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                            shape=ft.ContinuousRectangleBorder(),
                            mouse_cursor=ft.MouseCursor.CLICK,
                            padding=ft.Padding(0),
                            shadow_color=ft.Colors.TRANSPARENT,
                            alignment=ft.Alignment.CENTER_LEFT,
                        ),
                    ),
                ]
            ),
        )

    return ft.Container(
        width=230,
        height=670,
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Container(
                    content=ft.Text(
                        value="BiblioGestor",
                        size=25,
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                    ),
                    margin=ft.Margin(10, 5, 0, 0),
                ),
                ft.Container(
                    content=ft.Text("Descubrir", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                    margin=ft.Margin(10, 10, 0, 0),
                ),
                _nav_row(ft.Icons.HOME_OUTLINED, "Inicio", _inicio),
                ft.Container(
                    content=ft.Text("Administrar", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                    margin=ft.Margin(10, 5, 0, 0),
                ),
                _nav_row(ft.Icons.LIBRARY_BOOKS_OUTLINED, "Libros", _libros),
                ft.Container(
                    content=ft.Text("Solicitudes", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                    margin=ft.Margin(10, 5, 0, 0),
                ),
                _nav_row(ft.Icons.PAN_TOOL_OUTLINED, "Préstamos", _prestamos),
                _nav_row(ft.Icons.ASSIGNMENT_RETURN_OUTLINED, "Devoluciones", _devoluciones),
                ft.Container(
                    content=ft.Text("Inventario", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                    margin=ft.Margin(10, 5, 0, 0),
                ),
                _nav_row(ft.Icons.CHECK_CIRCLE_OUTLINE, "Disponibles", _disponibles),
                _nav_row(ft.Icons.SCHEDULE, "Prestados", _prestados),
                _nav_row(ft.Icons.ERROR_OUTLINE, "Perdidos", _perdidos),
                ft.Container(
                    margin=ft.Margin(0, 150, 0, 0),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[btnSalir(page)],
                    ),
                ),
            ],
        ),
    )
