import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from database.queries import obtenerNombreUsuario
from views.reusable.btnesCategoria import botonesCategoria


def dashBoardPage(page: ft.Page):
    # codigo de la sesion actual
    codigoSesionUsuario = page.session.store.get("codigo_usuario")
    apellidoUsuario = page.session.store.get("apellido_usuario")
    nombreUsuario = obtenerNombreUsuario(codigoSesionUsuario)

    async def ir_dashBoardUsuario(e):
        await page.push_route("/userDashboard")
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
                                                    margin=ft.Margin(
                                                        0, 0, 0, 10),
                                                    bgcolor=ft.Colors.GREY_400,
                                                    border_radius=100,
                                                    content=ft.Image(
                                                        src=f"https://ui-avatars.com/api/?background=A2CF97&name={nombreUsuario}&size=180&bold=true",
                                                        width=180,
                                                        height=180,
                                                        margin=0,
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
                                    ),
                                    # Contenedor de busqueda
                                    ft.Container(
                                        width=1000,
                                        height=120,
                                        content=ft.Column(
                                            spacing=5,
                                            margin=ft.Margin(15, 0, 0, 0),
                                            controls=[
                                                ft.Text(
                                                    margin=ft.Margin(
                                                        8, 0, 0, 0),
                                                    value="Buscar libro",
                                                    size=15,
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.Container(
                                                    content=ft.Row(
                                                        controls=[
                                                            ft.SearchBar(
                                                                bar_trailing=[
                                                                    ft.IconButton(
                                                                        icon=ft.Icons.SEARCH,
                                                                        icon_color=ft.Colors.GREY_600,
                                                                    )
                                                                ],
                                                                height=40,
                                                                bar_elevation=2,
                                                                bar_overlay_color=ft.Colors.GREY_200,
                                                                bar_hint_text="Busca un libro",
                                                                bar_bgcolor=ft.Colors.WHITE,
                                                                bar_text_style=ft.TextStyle(
                                                                    color=ft.Colors.BLACK
                                                                ),
                                                                bar_hint_text_style=ft.TextStyle(
                                                                    color=ft.Colors.GREY_400
                                                                )
                                                            ),
                                                            ft.Container(
                                                                content=ft.Row(
                                                                    margin=ft.Margin(
                                                                        15, 0, 0, 0),
                                                                    controls=[
                                                                        ft.Text(
                                                                            value="Mostrar Solo\nDisponibles",
                                                                            size=12,
                                                                            weight=ft.FontWeight.W_400,
                                                                            color=ft.Colors.GREY_900,
                                                                        ),
                                                                        ft.CupertinoSwitch(
                                                                            value=False,
                                                                            active_track_color=ft.Colors.BLACK,)
                                                                    ]
                                                                )
                                                            )
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    width=1000,
                                                    height=40,
                                                    content=ft.Row(
                                                        spacing=3,
                                                        controls=[
                                                            botonesCategoria(
                                                                "Todos"),
                                                            botonesCategoria(
                                                                "67"),
                                                            botonesCategoria(
                                                                "mibombo"),
                                                            botonesCategoria(
                                                                "Son"),
                                                            botonesCategoria(
                                                                "Sybau")
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        margin=ft.Margin(20, 0, 0, 0),
                                        width=960,
                                        height=270,
                                        bgcolor=ft.Colors.GREY_400,

                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )
