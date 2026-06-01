import flet as ft
from database.queries import (
    obtenerHistorialPrestamosUsuario,
    estaEjemplarReservado,
    ampliarPrestamo
)

_CARD_BG = ft.Colors.WHITE
_CARD_WIDTH = 300
_CARD_HEIGHT = 390
_PORTADA_H = 100


def card_historial_prestamo(
    titulo: str,
    autores: str,
    fecha_prestamo: str,
    fecha_devolucion: str,
    descripcion: str,
    devuelto: bool = False,
    imagen_src: str | None = None,
    estado_prestamo: str = 'Aprobada',
    on_ampliar=None,
) -> ft.Container:
    """Tarjeta de registro del historial con opción de ampliación."""
    portada = (
        ft.Container(
            height=_PORTADA_H,
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.GREY_300,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=imagen_src,
                width=_CARD_WIDTH - 28,
                height=_PORTADA_H,
                fit=ft.BoxFit.COVER,
            ),
        )
        if imagen_src
        else ft.Container(
            height=_PORTADA_H,
            border_radius=12,
            bgcolor=ft.Colors.GREY_300,
            alignment=ft.Alignment.CENTER,
            content=ft.Stack(
                width=_CARD_WIDTH - 28,
                height=_PORTADA_H,
                alignment=ft.Alignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.MENU_BOOK, size=40, color=ft.Colors.GREY_700),
                ],
            ),
        )
    )

    # Badge de estado
    if devuelto:
        badge_color = ft.Colors.BLUE_600
        badge_text = "Devuelto"
    elif estado_prestamo == 'En solicitud':
        badge_color = ft.Colors.ORANGE_600
        badge_text = "Solicitado"
    elif estado_prestamo == 'Rechazada':
        badge_color = ft.Colors.RED_600
        badge_text = "Rechazado"
    else:
        badge_color = ft.Colors.GREEN_600
        badge_text = "Activo"

    # Botón de ampliación si el préstamo está Aprobado y no devuelto
    btn_ampliar = ft.Container()
    if not devuelto and estado_prestamo == 'Aprobada' and on_ampliar is not None:
        btn_ampliar = ft.Container(
            alignment=ft.Alignment.CENTER,
            margin=ft.Margin(0, 4, 0, 0),
            content=ft.FilledButton(
                content="Ampliar Préstamo",
                on_click=on_ampliar,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.LIGHT_GREEN_600,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding(8, 4, 8, 4),
                )
            )
        )

    return ft.Container(
        width=_CARD_WIDTH,
        height=_CARD_HEIGHT,
        margin=ft.Margin(0, 0, 12, 0),
        padding=ft.Padding(14, 14, 14, 12),
        bgcolor=_CARD_BG,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=14,
        content=ft.Column(
            spacing=8,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            titulo,
                            size=15,
                            weight=ft.FontWeight.W_700,
                            color=ft.Colors.GREY_900,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            expand=True,
                        ),
                        ft.Container(
                            padding=ft.Padding(8, 3, 8, 3),
                            border_radius=6,
                            bgcolor=badge_color,
                            content=ft.Text(
                                badge_text, size=9,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.WHITE,
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    autores,
                    size=12,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_900,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                portada,
                ft.Text(
                    value=f"Fecha préstamo: {fecha_prestamo}",
                    size=11,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text(
                    value=f"Fecha vencimiento: {fecha_devolucion}",
                    size=11,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text(
                    descripcion,
                    size=10,
                    color=ft.Colors.GREY_800,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                btn_ampliar,
            ],
        ),
    )


def fila_historial_scroll(page: ft.Page) -> ft.Container:
    """Zona scroll horizontal con datos reales del historial y opción de ampliación."""
    body_container_ref = ft.Ref[ft.Container]()

    def _refrescar_historial():
        codigo_usuario = page.session.store.get("codigo_usuario")
        prestamos = obtenerHistorialPrestamosUsuario(codigo_usuario) if codigo_usuario else []

        if not prestamos:
            content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
                    ft.Text(
                        "No tienes préstamos en tu historial",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_500,
                    ),
                ],
            )
        else:
            cards = []
            for p in prestamos:
                id_pres = p[0]
                id_ej = p[1]
                fecha_p = p[2].strftime("%d/%m/%y") if hasattr(p[2], "strftime") else str(p[2])
                fecha_v = p[3].strftime("%d/%m/%y") if hasattr(p[3], "strftime") else str(p[3])
                dev_val = bool(p[7])
                est_pres = p[8] if len(p) > 8 else 'Aprobada'

                def _ampliar_factory(p_id=id_pres, ej_id=id_ej):
                    def _handler(e):
                        from views.reusable.succesful import open_succesful_dialog
                        from views.user.prestar_dialog import _open_error_dialog

                        if estaEjemplarReservado(ej_id):
                            _open_error_dialog(
                                page,
                                "No se puede ampliar el préstamo porque este ejemplar ya tiene una reserva activa de otro usuario."
                            )
                        else:
                            ok, msg = ampliarPrestamo(p_id, 8)
                            if ok:
                                _refrescar_historial()
                                open_succesful_dialog(page, "Préstamo ampliado por 8 días con éxito.")
                            else:
                                _open_error_dialog(page, f"Error al ampliar el préstamo: {msg}")
                    return _handler

                cards.append(
                    card_historial_prestamo(
                        titulo=p[4] or "Sin título",
                        autores=p[5] or "Sin autor",
                        fecha_prestamo=fecha_p,
                        fecha_devolucion=fecha_v,
                        descripcion=p[6] or "",
                        devuelto=dev_val,
                        estado_prestamo=est_pres,
                        on_ampliar=_ampliar_factory() if not dev_val and est_pres == 'Aprobada' else None,
                    )
                )

            content = ft.ListView(
                horizontal=True,
                height=440,
                width=970,
                spacing=0,
                padding=ft.Padding(0, 0, 0, 8),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                scroll=ft.ScrollMode.ALWAYS,
                build_controls_on_demand=False,
                controls=cards,
            )

        container = body_container_ref.current
        if container:
            container.content = content
            page.update()

    # Primera carga
    codigo_usuario = page.session.store.get("codigo_usuario")
    prestamos = obtenerHistorialPrestamosUsuario(codigo_usuario) if codigo_usuario else []

    if not prestamos:
        initial_content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.HISTORY, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "No tienes préstamos en tu historial",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_500,
                ),
            ],
        )
    else:
        cards = []
        for p in prestamos:
            id_pres = p[0]
            id_ej = p[1]
            fecha_p = p[2].strftime("%d/%m/%y") if hasattr(p[2], "strftime") else str(p[2])
            fecha_v = p[3].strftime("%d/%m/%y") if hasattr(p[3], "strftime") else str(p[3])
            dev_val = bool(p[7])
            est_pres = p[8] if len(p) > 8 else 'Aprobada'

            def _ampliar_factory(p_id=id_pres, ej_id=id_ej):
                def _handler(e):
                    from views.reusable.succesful import open_succesful_dialog
                    from views.user.prestar_dialog import _open_error_dialog

                    if estaEjemplarReservado(ej_id):
                        _open_error_dialog(
                            page,
                            "No se puede ampliar el préstamo porque este ejemplar ya tiene una reserva activa de otro usuario."
                        )
                    else:
                        ok, msg = ampliarPrestamo(p_id, 8)
                        if ok:
                            _refrescar_historial()
                            open_succesful_dialog(page, "Préstamo ampliado por 8 días con éxito.")
                        else:
                            _open_error_dialog(page, f"Error al ampliar el préstamo: {msg}")
                return _handler

            cards.append(
                card_historial_prestamo(
                    titulo=p[4] or "Sin título",
                    autores=p[5] or "Sin autor",
                    fecha_prestamo=fecha_p,
                    fecha_devolucion=fecha_v,
                    descripcion=p[6] or "",
                    devuelto=dev_val,
                    estado_prestamo=est_pres,
                    on_ampliar=_ampliar_factory() if not dev_val and est_pres == 'Aprobada' else None,
                )
            )

        initial_content = ft.ListView(
            horizontal=True,
            height=440,
            width=970,
            spacing=0,
            padding=ft.Padding(0, 0, 0, 8),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            scroll=ft.ScrollMode.ALWAYS,
            build_controls_on_demand=False,
            controls=cards,
        )

    return ft.Container(
        ref=body_container_ref,
        width=1000,
        height=460,
        margin=ft.Margin(0),
        padding=ft.Padding(8, 0, 8, 0),
        content=initial_content
    )


def historial_body_after_sidebar(page: ft.Page) -> ft.Column:
    return ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                margin=ft.Margin(20, 50, 0, 0),
                content=ft.Text(
                    value="Historial",
                    size=50,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_900,
                ),
            ),
            fila_historial_scroll(page),
        ],
    )
