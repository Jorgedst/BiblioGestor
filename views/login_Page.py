import flet as ft
from views.commonSideBar import commonSideBar
def login_page(page: ft.Page):
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
                            #SideBar normalito
                            commonSideBar(),
                            # Contenido Main
                            ft.VerticalDivider(),
                            ft.Container(
                                width=1000,
                                height=700,
                                content=ft.Column(controls=[
                                    ft.Container(
                                        alignment=ft.Alignment.TOP_RIGHT,
                                        content=ft.Button(
                                            width=150,
                                            margin=ft.Margin(0, 10, 0, 0),
                                            content="Soy Administrador",
                                            style=ft.ButtonStyle(
                                                color={
                                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                },
                                                bgcolor={
                                                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                                },
                                                shape=ft.ContinuousRectangleBorder(
                                                    radius=10),
                                                mouse_cursor=ft.MouseCursor.CLICK,
                                                padding=ft.Padding(0),
                                                shadow_color=ft.Colors.TRANSPARENT,
                                                alignment=ft.Alignment.CENTER,
                                                text_style=ft.TextStyle(
                                                    weight=ft.FontWeight.W_400
                                                )
                                            )
                                        )
                                    ),
                                    ft.Container(
                                        width=1000,
                                        height=580,
                                        content=ft.Column(
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    value="Ingresa tu código de usuario",
                                                    size=40,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.Text(
                                                    value="¡Bienvenido a BiblioGestor!",
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
                                                            ft.TextField(
                                                                height=58,
                                                                autofocus=True,
                                                                max_length=10,
                                                                label_style=ft.TextStyle(
                                                                    size=14,
                                                                    weight=ft.FontWeight.W_400,
                                                                    color=ft.Colors.GREY_400,
                                                                ),
                                                                label="Ingresa tu código de usuario",
                                                                color=ft.Colors.BLACK,
                                                                border_color=ft.Colors.GREY_400,
                                                                border_radius=10,
                                                                input_filter=ft.NumbersOnlyInputFilter(),
                                                            ),
                                                            ft.Button(
                                                                width=250,
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
                                                                        weight=ft.FontWeight.W_400
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
        