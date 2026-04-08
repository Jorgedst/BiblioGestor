import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from views.reusable.dropDownCarrera import getOptionsDropDown
from views.user.dashboard import obtenerIconoUsuario
from database.queries import obtenerUsuarioInfo


def editar_perfil_body_after_sidebar(page: ft.Page) -> ft.Column:
    """Formulario editar perfil (sin sidebar ni soyAdmin). Reutilizable embebido en el dashboard."""
    codigoSesionUsuario = page.session.store.get("codigo_usuario")
    infoUsuario = obtenerUsuarioInfo(codigoSesionUsuario)
    idUsuario = infoUsuario[0][1]
    nombreUsuario = infoUsuario[0][2]
    apellidoUsuario = infoUsuario[0][3]
    correoUsuario = infoUsuario[0][4]
    carrera = infoUsuario[0][7]
    iconoUsario = obtenerIconoUsuario(nombreUsuario)

    return ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=1000,
                            content=ft.Row(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        icon=ft.Icons.EDIT,
                                        color=ft.Colors.GREY_900,
                                        size=40,
                                        align=ft.Alignment.CENTER,
                                    ),
                                    ft.TextField(
                                        border_color=ft.Colors.WHITE,
                                        height=85,
                                        width=350,
                                        value=f"{nombreUsuario} {apellidoUsuario}",
                                        color=ft.Colors.BLACK,
                                        text_style=ft.TextStyle(
                                            size=45,
                                            color=ft.Colors.GREY_900,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        border_radius=100,
                                        content=ft.Image(
                                            src=iconoUsario,
                                            width=210,
                                            height=210,
                                            margin=0,
                                            fit=ft.BoxFit.COVER,
                                        ),
                                    ),
                                ],
                            )
                        ),
                        ft.Container(
                            width=1000,
                            height=65,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Row(
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            spacing=10,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    value="Código",
                                                    size=14,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.TextField(
                                                    height=40,
                                                    width=150,
                                                    read_only=True,
                                                    border_color=ft.Colors.GREY_400,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    value=f"{codigoSesionUsuario}",
                                                    color=ft.Colors.BLACK,
                                                    text_style=ft.TextStyle(
                                                        size=14,
                                                        color=ft.Colors.BLACK,
                                                        weight=ft.FontWeight.W_400,
                                                    ),
                                                ),
                                            ],
                                        )
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    value="Identificación",
                                                    size=14,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.TextField(
                                                    height=40,
                                                    width=150,
                                                    read_only=True,
                                                    border_color=ft.Colors.GREY_400,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    value=f"{idUsuario}",
                                                    color=ft.Colors.BLACK,
                                                    text_style=ft.TextStyle(
                                                        size=14,
                                                        color=ft.Colors.BLACK,
                                                        weight=ft.FontWeight.W_400,
                                                    ),
                                                ),
                                            ],
                                        )
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            width=1000,
                            height=135,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Row(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    value="Correo",
                                                    size=14,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.TextField(
                                                    height=40,
                                                    width=315,
                                                    border_color=ft.Colors.GREY_400,
                                                    bgcolor=ft.Colors.WHITE,
                                                    value=f"{correoUsuario}",
                                                    color=ft.Colors.BLACK,
                                                    text_style=ft.TextStyle(
                                                        size=14,
                                                        color=ft.Colors.BLACK,
                                                        weight=ft.FontWeight.W_400,
                                                    ),
                                                ),
                                                ft.Text(
                                                    value="Carrera",
                                                    size=14,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.Dropdown(
                                                    options=getOptionsDropDown(),
                                                    text=carrera,
                                                    text_size=14,
                                                    width=315,
                                                    height=40,
                                                    bgcolor=ft.Colors.GREY_900,
                                                    border_color=ft.Colors.GREY_400,
                                                    color=ft.Colors.GREY_900,
                                                    menu_height=200,
                                                ),
                                            ],
                                        )
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            ),
            ft.Container(
                width=1000,
                height=70,
                alignment=ft.Alignment.CENTER,
                content=ft.Row(
                    spacing=25,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Button(
                            width=182,
                            icon=ft.Icons.DELETE,
                            content=ft.Text(
                                value="Eliminar Cuenta",
                                size=15,
                                weight=ft.FontWeight.W_600,
                            ),
                            style=ft.ButtonStyle(
                                alignment=ft.Alignment.CENTER,
                                mouse_cursor=ft.MouseCursor.CLICK,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.RED_600,
                                    ft.ControlState.HOVERED: ft.Colors.RED_900,
                                    ft.ControlState.PRESSED: ft.Colors.GREY_700,
                                },
                                shape=ft.ContinuousRectangleBorder(radius=10),
                            ),
                        ),
                        ft.Button(
                            width=130,
                            icon=ft.Icons.SAVE,
                            content=ft.Text(
                                value="Guardar",
                                size=15,
                                weight=ft.FontWeight.W_600,
                            ),
                            style=ft.ButtonStyle(
                                alignment=ft.Alignment.CENTER,
                                mouse_cursor=ft.MouseCursor.CLICK,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: ft.Colors.LIGHT_GREEN_600,
                                    ft.ControlState.HOVERED: ft.Colors.LIGHT_GREEN_900,
                                    ft.ControlState.PRESSED: ft.Colors.GREY_700,
                                },
                                shape=ft.ContinuousRectangleBorder(radius=10),
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


def editarPerfil(page: ft.Page):
    return ft.View(
        route="/editarPerfil",
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
                        userSideBar(page),
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    soyAdminBtn(page),
                                    editar_perfil_body_after_sidebar(page),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
