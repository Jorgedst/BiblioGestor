import flet as ft
from views.reusable.btnSalir import btnSalir

def loginAdmin(page: ft.Page):
    #CLAVE DE ADMINISTRADOR 
    claveAdmin = "skywalker66"
    
        
    async def irDashboardAdmin(e):
        codigoAdmin = txtFieldCodigoAdmin.value
        if not codigoAdmin:
            txtFieldCodigoAdmin.error = "Ingresa un codigo"
            return
        else:
            if codigoAdmin == claveAdmin:
                await page.push_route("/dashboardAdmin")
            else:
                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_600, size=28),
                            ft.Text("Código incorrecto", size=18, weight=ft.FontWeight.W_700,
                                    color=ft.Colors.RED_600),
                        ],
                    ),
                    content=ft.Text(
                        "El código de administrador es incorrecto.\nIntenta de nuevo.",
                        size=14, color=ft.Colors.GREY_800, text_align=ft.TextAlign.CENTER,
                    ),
                    actions=[
                        ft.FilledButton(
                            content="Aceptar",
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREY_900, color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda ev: (setattr(dlg, 'open', False), page.update()),
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.CENTER,
                )
                page.overlay.append(dlg)
                dlg.open = True
                page.update()
    
    txtFieldCodigoAdmin = ft.TextField(
        password= True,
        can_reveal_password= True,
        height=58,
        autofocus=True,
        label_style=ft.TextStyle(
            size=14,
            weight=ft.FontWeight.W_400,
            color=ft.Colors.GREY_400,
        ),
        label="Ingresa un codigo",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.GREY_400,
        border_radius=10,
        on_submit= irDashboardAdmin
    )

    return ft.View(
        route="/loginAdmin",
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
                        ft.Container(
                            width=230,
                            height=670,
                            content=ft.Column(controls=[
                                ft.Container(
                                    content=ft.Text(
                                        "BiblioGestor",
                                        size=25,
                                        color=ft.Colors.BLACK,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    margin=ft.Margin(10, 5, 0, 0),
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "Descubrir",
                                        size=15,
                                        color=ft.Colors.BLACK,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    margin=ft.Margin(10, 10, 0, 0),
                                ),
                                # Botón Inicio
                                ft.Container(
                                    margin=ft.Margin(8, 0, 0, 0),
                                    border_radius=10,
                                    bgcolor=ft.Colors.WHITE_54,
                                    content=ft.Row(controls=[
                                        ft.Icon(ft.Icons.HOME,
                                                color=ft.Colors.BLACK,
                                                align=ft.Alignment.CENTER_LEFT,
                                                ),
                                        ft.Button(
                                            width=190,
                                            content="Inicio",
                                            style=ft.ButtonStyle(
                                                color={
                                                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                                },
                                                bgcolor={
                                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                },
                                                shape=ft.ContinuousRectangleBorder(),
                                                mouse_cursor=ft.MouseCursor.CLICK,
                                                padding=ft.Padding(0),
                                                shadow_color=ft.Colors.TRANSPARENT,
                                                alignment=ft.Alignment.CENTER_LEFT,
                                            )
                                        )
                                    ])
                                ),
                                ft.Container(
                                    margin=ft.Margin(0, 450, 0, 0),
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            btnSalir(page)]),
                                )
                            ]
                            )
                        ),
                        # Contenido Main
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(controls=[
                                ft.Container(
                                    width=1000,
                                    height=580,
                                    content=ft.Column(
                                        spacing=0,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(
                                                icon = ft.Icons.ADMIN_PANEL_SETTINGS,
                                                color = ft.Colors.GREY_800,
                                                size = 60
                                            ),
                                            ft.Text(
                                                value="Ingresa tu código de",
                                                size=40,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREY_900,
                                            ),
                                            ft.Text(
                                                value="Administrador",
                                                size=40,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.LIGHT_GREEN_600,
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
                                                        txtFieldCodigoAdmin,
                                                        ft.Button(
                                                            width=250,
                                                            on_click=irDashboardAdmin,
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
