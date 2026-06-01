import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from views.reusable.dropDownCarrera import getOptionsDropDown
from views.user.dashboard import obtenerIconoUsuario
from database.queries import obtenerUsuarioInfo, actualizarUsuario, eliminarUsuario
from views.reusable.succesful import open_succesful_dialog, open_confirm_dialog


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

    # Inputs de textField
    txtFieldnombreApellido = ft.TextField(
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
    )

    txtFieldCorreo = ft.TextField(
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
        )
    )
    dropDownCarreras = ft.Dropdown(
        options=getOptionsDropDown(),
        text=carrera,
        text_size=14,
        width=315,
        height=40,
        bgcolor=ft.Colors.GREY_900,
        border_color=ft.Colors.GREY_400,
        color=ft.Colors.GREY_900,
        menu_height=200,
    )

    def separar_nombre_apellido(texto):
        partes = texto.strip().split()

        if len(partes) == 1:
            return partes[0], ""
        
        nombre = partes[0]
        apellido = " ".join(partes[1:])
        return nombre, apellido

    def _on_eliminar_cuenta(e):
        def _confirmar_eliminar(ev):
            success, msg = eliminarUsuario(codigoSesionUsuario)
            if success:
                page.session.store.clear()
                page.go("/")
            else:
                page.show_dialog(ft.SnackBar(content=ft.Text(f"Error al eliminar: {msg}"), bgcolor=ft.Colors.RED_600))

        open_confirm_dialog(
            page,
            titulo="Eliminar cuenta",
            mensaje="¿Estás seguro de que deseas eliminar tu cuenta?\nEsta acción es irreversible.",
            on_confirm=_confirmar_eliminar,
        )

    def _on_guardar(e):
        # Leer valores actuales de los campos
        texto_nombre = txtFieldnombreApellido.value.strip()
        nuevo_correo = txtFieldCorreo.value.strip()
        nueva_carrera = dropDownCarreras.value or carrera  # mantiene la actual si no cambia

        # Limpiar errores previos
        txtFieldnombreApellido.error_text = None
        txtFieldCorreo.error_text = None

        # Validaciones básicas
        has_error = False
        if not texto_nombre:
            txtFieldnombreApellido.error = "El nombre no puede estar vacío"
            has_error = True
        if not nuevo_correo:
            txtFieldCorreo.error = "El correo no puede estar vacío"
            has_error = True

        if has_error:
            page.update()
            return

        nuevo_nombre, nuevo_apellido = separar_nombre_apellido(texto_nombre)

        success, msg = actualizarUsuario(
            codigoSesionUsuario, nuevo_nombre, nuevo_apellido, nuevo_correo, nueva_carrera
        )
        if success:
            open_succesful_dialog(page, "Tu perfil se ha actualizado correctamente.")
        else:
            page.show_dialog(ft.SnackBar(content=ft.Text(f"Error al guardar: {msg}"), bgcolor=ft.Colors.RED_600))

    

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
                                    txtFieldnombreApellido
                                ]
                            )
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
                                                txtFieldCorreo,
                                                ft.Text(
                                                    value="Carrera",
                                                    size=14,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                dropDownCarreras
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
                            on_click=_on_eliminar_cuenta,
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
                            on_click=_on_guardar,
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
