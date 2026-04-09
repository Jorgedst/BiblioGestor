import flet as ft
from database.queries import obtenerHistorialPrestamosUsuario

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
) -> ft.Container:
    """Tarjeta de registro del historial (solo lectura)."""
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
    else:
        badge_color = ft.Colors.GREEN_600
        badge_text = "Activo"

    return ft.Container(
        width=_CARD_WIDTH,
        height=_CARD_HEIGHT,
        margin=ft.Margin(0, 0, 12, 0),
        padding=ft.Padding(14, 14, 14, 12),
        bgcolor=_CARD_BG,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=14,
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            titulo,
                            size=16,
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
                                badge_text, size=10,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.WHITE,
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    autores,
                    size=13,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_900,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                portada,
                ft.Text(
                    value=f"Fecha préstamo: {fecha_prestamo}",
                    size=12,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text(
                    value=f"Fecha vencimiento: {fecha_devolucion}",
                    size=12,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text(
                    descripcion,
                    size=11,
                    color=ft.Colors.GREY_800,
                    max_lines=5,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
        ),
    )


def fila_historial_scroll(page: ft.Page) -> ft.Container:
    """Zona scroll horizontal con datos reales del historial."""
    codigo_usuario = page.session.store.get("codigo_usuario")
    prestamos = obtenerHistorialPrestamosUsuario(codigo_usuario) if codigo_usuario else []

    if not prestamos:
        return ft.Container(
            width=1000,
            height=460,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
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
            ),
        )

    cards = []
    for p in prestamos:
        # p: (idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento,
        #     titulo, autores, descripción, devuelto)
        fecha_p = p[2].strftime("%d/%m/%y") if hasattr(p[2], "strftime") else str(p[2])
        fecha_v = p[3].strftime("%d/%m/%y") if hasattr(p[3], "strftime") else str(p[3])
        cards.append(
            card_historial_prestamo(
                titulo=p[4] or "Sin título",
                autores=p[5] or "Sin autor",
                fecha_prestamo=fecha_p,
                fecha_devolucion=fecha_v,
                descripcion=p[6] or "",
                devuelto=bool(p[7]),
            )
        )

    return ft.Container(
        width=1000,
        height=460,
        margin=ft.Margin(0),
        padding=ft.Padding(8, 0, 8, 0),
        content=ft.ListView(
            horizontal=True,
            height=440,
            width=970,
            spacing=0,
            padding=ft.Padding(0, 0, 0, 8),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            scroll=ft.ScrollMode.ALWAYS,
            build_controls_on_demand=False,
            controls=cards,
        ),
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
