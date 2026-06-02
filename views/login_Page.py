import flet as ft
from views.reusable.commonSideBar import commonSideBar
from views.reusable.soyAdminBtn import soyAdminBtn
from database.queries import validarUser


def login_page(page: ft.Page):

    async def ir_register(e):
        codigo = txtFieldCodigoUsuario.value
        if not codigo:
            txtFieldCodigoUsuario.error = "Ingresa un codigo"
            return
        else:
            existe, data = validarUser(codigo, "codigo")
            
            if existe:
                user_estado = data[0][6]
                if user_estado == 0:
                    from database.queries import obtenerMotivoBloqueo
                    motivo = obtenerMotivoBloqueo(codigo)
                    
                    def _close_dlg(e=None):
                        overlay_ref = getattr(page, "_block_overlay", None)
                        if overlay_ref and overlay_ref in page.overlay:
                            page.overlay.remove(overlay_ref)
                        page._block_overlay = None
                        page.update()

                    modal_content = ft.Container(
                        width=400,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=18,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        padding=ft.Padding(30, 32, 30, 28),
                        shadow=ft.BoxShadow(
                            spread_radius=2, blur_radius=20,
                            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK), offset=ft.Offset(0, 4)
                        ),
                        content=ft.Column(
                            spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True,
                            controls=[
                                ft.Container(
                                    width=80, height=80, border_radius=40, bgcolor=ft.Colors.RED_50,
                                    border=ft.Border.all(3, ft.Colors.RED_300), alignment=ft.Alignment.CENTER,
                                    content=ft.Icon(ft.Icons.BLOCK_ROUNDED, size=48, color=ft.Colors.RED_600)
                                ),
                                ft.Text("Cuenta bloqueada", size=22, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_900),
                                ft.Text(f"Tu cuenta ha sido bloqueada.\nMotivo: {motivo}", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                                ft.FilledButton("Entendido", width=140, on_click=_close_dlg,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=10)))
                            ]
                        )
                    )
                    
                    dim_panel = ft.Container(
                        margin=0, bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK), alignment=ft.Alignment.CENTER,
                        content=ft.Stack(
                            width=1280, height=1280, alignment=ft.Alignment.CENTER,
                            controls=[ft.GestureDetector(content=ft.Container(width=1280, height=1280), on_tap=_close_dlg), modal_content]
                        )
                    )
                    backdrop = ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=dim_panel)
                    page._block_overlay = backdrop
                    page.overlay.append(backdrop)
                    page.update()
                    return
                    
                # PRUEBAS CAMBIAR DESPUES OOJOOOOOOO
                page.session.store.set("codigo_usuario", codigo)
                await page.push_route("/userDashboard")
            else:
                # PRUEBAS CAMBIAR DESPUES OOJOOOOOOO
                page.session.store.set("codigo_usuario", codigo)
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
