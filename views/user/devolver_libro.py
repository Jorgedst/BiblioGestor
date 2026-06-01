import flet as ft
from database.queries import (
    obtenerPrestamosUsuario,
    obtenerSiguienteIdDevolucion,
    registrarDevolucion,
    yaExisteDevolucion,
)
from views.reusable.succesful import open_succesful_dialog

# Estilo mockup: verde acción y fondo tipo lavanda en la tarjeta
_DEVOLVER_GREEN = ft.Colors.LIGHT_GREEN_600
_CARD_BG = ft.Colors.WHITE
_CARD_WIDTH = 300
_CARD_HEIGHT = 390
_PORTADA_H = 100


def card_box_devolver(
    titulo: str,
    autores: str,
    fecha_prestamo: str,
    fecha_devolucion: str,
    descripcion: str,
    imagen_src: str | None = None,
    on_devolver=None,
) -> ft.Container:
    """Tarjeta de libro en préstamo (pantalla devolver). Listo para enlazar con la query."""
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

    return ft.Container(
        width=_CARD_WIDTH,
        height = _CARD_HEIGHT,
        margin=ft.Margin(0, 0, 12, 0),
        padding=ft.Padding(14, 14, 14, 12),
        bgcolor=_CARD_BG,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=14,
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Text(
                    titulo,
                    size=16,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
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
                    value=f"Fecha devolución: {fecha_devolucion}",
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
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.FilledButton(
                            content="Devolver",
                            icon=ft.Icons.ASSIGNMENT_RETURN,
                            style=ft.ButtonStyle(
                                bgcolor=_DEVOLVER_GREEN,
                                color=ft.Colors.WHITE,
                                shape=ft.ContinuousRectangleBorder(radius=20),
                                padding=ft.Padding(16, 8, 16, 8),
                            ),
                            on_click=on_devolver,
                        ),
                    ],
                ),
            ],
        ),
    )


def _open_error_dialog(page: ft.Page, mensaje: str):
    """Overlay de error."""

    def _close_overlay(e=None):
        overlay_ref = getattr(page, "_error_dev_overlay", None)
        overlay = getattr(page, "overlay", None)
        if overlay_ref and overlay is not None and overlay_ref in overlay:
            overlay.remove(overlay_ref)
        page._error_dev_overlay = None
        page.update()

    modal_content = ft.Container(
        width=420,
        bgcolor=ft.Colors.WHITE,
        border_radius=18,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        padding=ft.Padding(30, 32, 30, 28),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Column(
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            controls=[
                ft.Container(
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=ft.Colors.ORANGE_50,
                    border=ft.Border.all(3, ft.Colors.ORANGE_300),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icon=ft.Icons.INFO_OUTLINE,
                        size=48,
                        color=ft.Colors.ORANGE_600,
                    ),
                ),
                ft.Text(
                    value="Aviso",
                    size=22,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    value=mensaje,
                    size=14,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                ft.FilledButton(
                    content="Aceptar",
                    width=140,
                    on_click=_close_overlay,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.ORANGE_600,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
            ],
        ),
    )

    _dim_w = 1280
    _dim_h = 1280
    dim_panel = ft.Container(
        margin=ft.Margin(0),
        bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
        alignment=ft.Alignment.CENTER,
        content=ft.Stack(
            width=_dim_w,
            height=_dim_h,
            alignment=ft.Alignment.CENTER,
            controls=[
                ft.GestureDetector(
                    content=ft.Container(width=_dim_w, height=_dim_h),
                    on_tap=_close_overlay,
                ),
                modal_content,
            ],
        ),
    )

    backdrop = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=dim_panel,
    )

    _close_overlay()
    page._error_dev_overlay = backdrop
    overlay = getattr(page, "overlay", None)
    if overlay is None:
        page.overlay = [backdrop]
    else:
        overlay.append(backdrop)
    page.update()


def fila_cards_devolver_scroll(page: ft.Page) -> ft.Container:
    codigo_usuario = page.session.store.get("codigo_usuario")
    prestamos = obtenerPrestamosUsuario(codigo_usuario) if codigo_usuario else []

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
                    ft.Icon(ft.Icons.LIBRARY_BOOKS_OUTLINED, size=48, color=ft.Colors.GREY_400),
                    ft.Text(
                        "No tienes libros prestados actualmente",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_500,
                    ),
                ],
            ),
        )

    def _on_devolver_factory(prestamo_row):
        """
        prestamo_row: (idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento,
                       titulo, autores, descripción)
        """
        def _h(e):
            id_prestamo = prestamo_row[0]

            # Verificar si ya hay una devolución pendiente
            if yaExisteDevolucion(id_prestamo):
                _open_error_dialog(
                    page,
                    "Ya existe una solicitud de devolución pendiente para este libro.\n"
                    "Espera a que un administrador la procese.",
                )
                return

            id_devolucion = obtenerSiguienteIdDevolucion()
            ok, msg = registrarDevolucion(id_devolucion, id_prestamo)
            if ok:
                open_succesful_dialog(
                    page,
                    f"Solicitud de devolución de \"{prestamo_row[4]}\" enviada correctamente, "
                    "solicita a un administrador que acepte la devolución.",
                )
            else:
                _open_error_dialog(page, f"Error al registrar la devolución: {msg}")

        return _h

    cards = []
    for p in prestamos:
        # p: (idPrestamo, ejemplar, fechaPrestamo, fechaVencimiento, titulo, autores, descripción)
        fecha_p = p[2].strftime("%d/%m/%y") if hasattr(p[2], "strftime") else str(p[2])
        fecha_v = p[3].strftime("%d/%m/%y") if hasattr(p[3], "strftime") else str(p[3])
        cards.append(
            card_box_devolver(
                titulo=p[4] or "Sin título",
                autores=p[5] or "Sin autor",
                fecha_prestamo=fecha_p,
                fecha_devolucion=fecha_v,
                descripcion=p[6] or "",
                on_devolver=_on_devolver_factory(p),
            )
        )

    # ListView horizontal + ALWAYS: la barra se mantiene visible (AUTO a veces no se ve).
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


def devolver_libro_body_after_sidebar(page: ft.Page) -> ft.Column:
    return ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                margin=ft.Margin(20, 50, 0, 0),
                content=ft.Text(
                    value="Libros disponibles para devolver",
                    size=50,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_900,
                ),
            ),
            fila_cards_devolver_scroll(page),
        ],
    )
