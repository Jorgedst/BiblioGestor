import flet as ft
from views.reusable.adminSideBar import adminSideBar
from views.reusable.btnUsuario import btnUsuario
from views.admin.admin_section_bodies import (
    build_admin_gestion_home,
    build_admin_libros,
    build_admin_prestamos,
    build_admin_devoluciones,
    build_admin_disponibles,
    build_admin_prestados,
    build_admin_perdidos,
)


def dashBoardAdmin(page: ft.Page):
    main_body_ref = ft.Ref[ft.Container]()

    def _mostrar_cuerpo(content: ft.Control):
        body = main_body_ref.current
        if body:
            body.content = content
            page.update()

    async def abrir_inicio(e):
        _mostrar_cuerpo(build_admin_gestion_home(page))

    async def abrir_libros(e):
        _mostrar_cuerpo(build_admin_libros(page))

    async def abrir_prestamos(e):
        _mostrar_cuerpo(build_admin_prestamos(page))

    async def abrir_devoluciones(e):
        _mostrar_cuerpo(build_admin_devoluciones(page))

    async def abrir_disponibles(e):
        _mostrar_cuerpo(build_admin_disponibles(page))

    async def abrir_prestados(e):
        _mostrar_cuerpo(build_admin_prestados(page))

    async def abrir_perdidos(e):
        _mostrar_cuerpo(build_admin_perdidos(page))

    return ft.View(
        route="/dashboardAdmin",
        spacing=0,
        padding=0,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                width=1280,
                height=670,
                content=ft.Row(
                    spacing=0,
                    controls=[
                        adminSideBar(
                            page,
                            on_inicio=abrir_inicio,
                            on_libros=abrir_libros,
                            on_prestamos=abrir_prestamos,
                            on_devoluciones=abrir_devoluciones,
                            on_disponibles=abrir_disponibles,
                            on_prestados=abrir_prestados,
                            on_perdidos=abrir_perdidos,
                        ),
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    btnUsuario(page),
                                    ft.Container(
                                        ref=main_body_ref,
                                        width=1000,
                                        height=590,
                                        padding=ft.Padding(16, 0, 16, 16),
                                        content=build_admin_gestion_home(page),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
