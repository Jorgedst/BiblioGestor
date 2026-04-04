import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from database.queries import obtenerNombreUsuario


def dashBoardPage(page: ft.Page):
    # codigo de la sesion actual
    codigoSesionUsuario = page.session.store.get("codigo_usuario")
    nombreUsuario = obtenerNombreUsuario(codigoSesionUsuario)
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
                        # Sidebar Usuario
                        userSideBar(page),
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    soyAdminBtn(page),
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Container(
                                                    bgcolor = ft.Colors.GREY_400,
                                                    border_radius = 100,
                                                    content=ft.Image(
                                                        src=f"https://api.dicebear.com/9.x/lorelei/png?seed={codigoSesionUsuario}",
                                                        width=180,
                                                        height=180,
                                                        margin=0,
                                                        fit=ft.BoxFit.COVER,
                                                    ),
                                                ),

                                                ft.Text(
                                                    value=f"¡Hola {nombreUsuario}!",
                                                    size=50,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREY_900,
                                                )
                                            ]
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )
