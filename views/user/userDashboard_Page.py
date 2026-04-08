import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from views.user.dashboard import build_dashboard_main_body
from views.user.devolver_libro import devolver_libro_body_after_sidebar
from views.user.historial import historial_body_after_sidebar
from views.user.editarPerfil import editar_perfil_body_after_sidebar


def dashBoardPage(page: ft.Page):

    main_body_ref = ft.Ref[ft.Container]()

    def _mostrar_cuerpo(content: ft.Control):
        body = main_body_ref.current
        if body:
            body.content = content
            page.update()

    async def abrir_inicio(e):
        _mostrar_cuerpo(build_dashboard_main_body(page))
    async def abrir_devolver_libro(e):
        _mostrar_cuerpo(devolver_libro_body_after_sidebar(page))
    async def abrir_historial(e):
        _mostrar_cuerpo(historial_body_after_sidebar(page))
    async def abrir_editar_perfil(e):
        _mostrar_cuerpo(editar_perfil_body_after_sidebar(page))

    return ft.View(
        route="/userDashboard",
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
                        userSideBar(
                            page,
                            on_inicio=abrir_inicio,
                            on_devolver_libro=abrir_devolver_libro,
                            on_historial=abrir_historial,
                            on_editar_perfil=abrir_editar_perfil,
                        ),
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    soyAdminBtn(page),
                                    ft.Container(
                                        ref=main_body_ref,
                                        width=1000,
                                        height=700,
                                        content=build_dashboard_main_body(page),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
