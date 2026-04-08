import flet as ft
from views.reusable.commonSideBar import commonSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from database.queries import validarUserCodigo


def login_page(page: ft.Page):

    async def ir_register(e):
        codigo = txtFieldCodigoUsuario.value
        if not codigo:
            txtFieldCodigoUsuario.error = "Ingresa un codigo"
            return
        else:
            existe, data = validarUserCodigo(codigo)
            # PRUEBAS CAMBIAR DESPUES OOJOOOOOOO
            page.session.store.set("codigo_usuario", codigo)
            if existe:
                await page.push_route("/userDashboard")
            else:
                await page.push_route("/register")
                
    txtFieldCodigoUsuario = ft.TextField(
        height=58,
        autofocus=True,
        max_length=9,
        label_style=ft.TextStyle(
            size=14,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="Ingresa tu código estudiantil",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
        input_filter=ft.NumbersOnlyInputFilter(),
        on_submit=ir_register,
    )

    return ft.View(
        route="/",
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
                        # SideBar normalito
                        commonSideBar(page),
                        # Contenido Main
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(controls=[
                                soyAdminBtn(page),
                                ft.Container(
                                    width=1000,
                                    height=580,
                                    content=ft.Column(
                                        spacing=0,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                spans=[
                                                    ft.TextSpan(
                                                        text="¡Bienvenido a ",
                                                        style=ft.TextStyle(
                                                            size=40,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.Colors.GREY_900,
                                                        ),
                                                    ),
                                                    ft.TextSpan(
                                                        text="BiblioGestor",
                                                        style=ft.TextStyle(
                                                            size=40,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.Colors.LIGHT_GREEN_600,
                                                        ),
                                                    ),
                                                    ft.TextSpan(
                                                        text="!",
                                                        style=ft.TextStyle(
                                                            size=40,
                                                            weight=ft.FontWeight.BOLD,
                                                            color=ft.Colors.GREY_900,
                                                        ),
                                                    ),
                                                ]
                                            ),
                                            ft.Text(
                                                value="Ingresa tu codigo estudiantil",
                                                size=20,
                                                weight=ft.FontWeight.W_400,
                                                color=ft.Colors.GREY_900,
                                            ),
                                            ft.Container(
                                                width=250,
                                                height=200,
                                                margin=ft.Margin(
                                                    0, 20, 0, 0),
                                                content=ft.Column(
                                                    spacing=0,
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.Text(
                                                            value="Código",
                                                            align=ft.Alignment.CENTER_LEFT,
                                                            size=13,
                                                            weight=ft.FontWeight.W_400,
                                                            color=ft.Colors.GREY_900,
                                                            margin=ft.Margin(
                                                                0, 0, 0, 8),
                                                        ),
                                                        txtFieldCodigoUsuario,
                                                        ft.Button(
                                                            width=250,
                                                            on_click=ir_register,
                                                            margin=ft.Margin(
                                                                0, 30, 0, 0),
                                                            content="Enviar",
                                                            style=ft.ButtonStyle(
                                                                    color={
                                                                        ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                                    },
                                                                bgcolor={
                                                                        ft.ControlState.DEFAULT: ft.Colors.GREY_900,
                                                                        },
                                                                shape=ft.ContinuousRectangleBorder(
                                                                        radius=10),
                                                                mouse_cursor=ft.MouseCursor.CLICK,
                                                                shadow_color=ft.Colors.TRANSPARENT,
                                                                text_style=ft.TextStyle(
                                                                        weight=ft.FontWeight.W_500
                                                                        )
                                                            )
                                                        )
                                                    ]
                                                )
                                            )
                                        ])
                                )
                            ])
                        )
                    ]
                )
            )
        ]
    )
