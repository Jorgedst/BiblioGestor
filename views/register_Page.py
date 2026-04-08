import flet as ft
from views.reusable.commonSideBar import commonSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from views.reusable.dropDownCarrera import getOptionsDropDown
from database.queries import validarUserIdentificacion
from database.queries import registrar_Usuario


def register_Page(page: ft.Page):
    # codigo de la sesion actual
    codigoSesionUsuario = page.session.store.get("codigo_usuario")

    # Inputs de usuario
    # ID
    txtFieldId = ft.TextField(
        height=60,
        max_length=10,
        label_style=ft.TextStyle(
            size=13,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="ID",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    # Nombre
    txtFieldNombre = ft.TextField(
        height=42,
        label_style=ft.TextStyle(
            size=13,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="Nombre",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
    )
    # Apellido
    txtFieldApellido = ft.TextField(
        height=42,
        label_style=ft.TextStyle(
            size=13,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="Apellido",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
    )
    # Correo
    txtFieldCorreo = ft.TextField(
        height=42,
        label_style=ft.TextStyle(
            size=13,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="Correo",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
    )
    # Switch estudiante (soy estudiante)
    switchEstudiante = ft.CupertinoSwitch(
        value=False,
        active_track_color=ft.Colors.BLACK,)
    # Carreera
    dropDownCarrera = ft.Dropdown(
            options= getOptionsDropDown(),
            margin=ft.Margin(
                30, 0, 0, 0),
            width=220,
            bgcolor=ft.Colors.GREY_900,
            border_color=ft.Colors.GREY_400,
            color=ft.Colors.GREY_900,
            label="Carrera (Opcional)",
            menu_height=300,)

    async def ir_dashBoardUsuario(e):
        if (not txtFieldId.value):
            txtFieldId.error = "Ingresa un ID"
            return
        if (not txtFieldNombre.value):
            txtFieldNombre.error = "Ingresa un nombre"
            return
        if (not txtFieldApellido.value):
            txtFieldApellido.error = "Ingresa un apellido"
            return
        if (not txtFieldCorreo.value):
            txtFieldCorreo.error = "Ingresa un correo"
            return
        existe, data = validarUserIdentificacion(txtFieldId.value)
        if existe:
            return
        else:
            registrar_Usuario(codigoSesionUsuario, txtFieldId.value, txtFieldNombre.value, txtFieldApellido.value,
                              txtFieldCorreo.value, switchEstudiante.value, True, dropDownCarrera.value)
            await page.push_route("/userDashboard")

    # Enter en cualquier campo = click en Enviar
    txtFieldId.on_submit = ir_dashBoardUsuario
    txtFieldNombre.on_submit = ir_dashBoardUsuario
    txtFieldApellido.on_submit = ir_dashBoardUsuario
    txtFieldCorreo.on_submit = ir_dashBoardUsuario
    return ft.View(
        route="/register",
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
                        commonSideBar(page),
                        # Contenido Register
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    soyAdminBtn(page),
                                    ft.Container(
                                        width=1000,
                                        height=100,
                                        content=ft.Column(
                                            spacing=0,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    size=50,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREY_900,
                                                    value="Regístrate"
                                                ),
                                                ft.Text(
                                                    value="Completa la información necesaria",
                                                    size=20,
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.LIGHT_GREEN_600,
                                                )

                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        margin=ft.Margin(0, 10, 0, 0),
                                        width=1000,
                                        height=335,
                                        content=ft.Column(
                                            spacing=0,
                                            controls=[
                                                ft.TextField(
                                                    value=codigoSesionUsuario,
                                                    read_only=True,
                                                    height=45,
                                                    label="Tu código de estudiante",
                                                    text_size=13,
                                                    color=ft.Colors.GREY_300,
                                                    border_color=ft.Colors.GREY_300,
                                                    border_radius=10,
                                                ),
                                                ft.Text(
                                                    value="Identificación (Cédula)",
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                txtFieldId,
                                                ft.Text(
                                                    value="Nombre",
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                txtFieldNombre,
                                                ft.Text(
                                                    value="Appelido",
                                                    margin=ft.Margin(
                                                        0, 12, 0, 0),
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                txtFieldApellido,
                                                ft.Text(
                                                    value="Correo",
                                                    margin=ft.Margin(
                                                        0, 10, 0, 0),
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                txtFieldCorreo
                                            ]

                                        )
                                    ),
                                    ft.Container(
                                        height=60,
                                        width=1000,
                                        content=ft.Row(
                                            margin=ft.Margin(270, 0, 0, 0),
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Container(
                                                    width=230,
                                                    content=ft.Column(
                                                        spacing=0,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Text(
                                                                value="Soy estudiante",
                                                                weight=ft.FontWeight.W_400,
                                                                color=ft.Colors.GREY_900,
                                                            ),
                                                            ft.Text(
                                                                value="Marcar si eres estudiante",
                                                                weight=ft.FontWeight.W_300,
                                                                color=ft.Colors.GREY_900,
                                                                size=12,
                                                            ),
                                                        ]
                                                    )
                                                ),
                                                switchEstudiante,
                                                dropDownCarrera
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        margin=ft.Margin(0, 20, 0, 0),
                                        height=40,
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.Button(
                                            on_click=ir_dashBoardUsuario,
                                            width=250,
                                            content="Enviar",
                                            color=ft.Colors.WHITE,
                                            bgcolor=ft.Colors.GREY_900,
                                            style=ft.ButtonStyle(
                                                shape=ft.ContinuousRectangleBorder(
                                                    radius=10),
                                                mouse_cursor=ft.MouseCursor.CLICK,
                                            )
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
