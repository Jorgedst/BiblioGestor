import datetime

import flet as ft

# Máximo de días de préstamo
_DIAS_PRESTAMO = 15


def open_prestar_dialog(page: ft.Page, libro: dict):
    """
    Modal en page.overlay: confirmar préstamo.
    """
    today = datetime.date.today()
    fecha_devolucion = today + datetime.timedelta(days=_DIAS_PRESTAMO)

    portada_child = ft.Icon(ft.Icons.MENU_BOOK, size=64, color=ft.Colors.LIGHT_GREEN_600)

    book_card = ft.Container(
        width=400,
        border_radius=14,
        bgcolor=ft.Colors.GREY_50,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        padding=ft.Padding(16, 14, 16, 14),
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Container(
                    height=220,
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    bgcolor=ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    content=portada_child,
                ),
                ft.Text(
                    value=libro.get("titulo", "Título libro"),
                    size=18,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    value=libro.get("autores", "Autor(es)"),
                    size=13,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_700,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Text(
                            libro.get("editorial", ""),
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_800,
                            expand=True,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            str(libro.get("anio", "")),
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                ),
                ft.Text(
                    value=libro.get("descripcion", ""),
                    size=11,
                    color=ft.Colors.GREY_700,
                    max_lines=6,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
        ),
    )

    detalle_column = ft.Container(
        width=420,
        padding=ft.Padding(8, 0, 0, 0),
        content=ft.Column(
            spacing=10,
            tight=True,
            controls=[
                ft.Text(
                    value="Fecha de devolución",
                    size=16,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                ),
                ft.Text(
                    value=f"Plazo del préstamo: {_DIAS_PRESTAMO} días desde hoy.",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                value="Debes devolver el libro antes del:",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(
                                value=fecha_devolucion.strftime("%d/%m/%Y"),
                                size=20,
                                weight=ft.FontWeight.W_700,
                                color=ft.Colors.LIGHT_GREEN_900,
                            ),
                        ],
                    ),
                ),
                ft.Text(
                    value="Sanción por retraso: $10.000 por día.",
                    size=12,
                    color=ft.Colors.GREY_600,
                ),
            ],
        ),
    )

    def _close_overlay(e=None):
        overlay_ref = getattr(page, "_prestamo_overlay", None)
        overlay = getattr(page, "overlay", None)
        if overlay_ref and overlay is not None and overlay_ref in overlay:
            overlay.remove(overlay_ref)
        page._prestamo_overlay = None
        page.update()

    modal_content = ft.Container(
        width=900,
        bgcolor=ft.Colors.WHITE,
        border_radius=14,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        padding=ft.Padding(18, 14, 18, 14),
        content=ft.Column(
            spacing=14,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            value="Confirma los datos del préstamo",
                            size=18,
                            weight=ft.FontWeight.W_700,
                            color=ft.Colors.GREY_900,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=20,
                            tooltip="Cerrar",
                            on_click=_close_overlay,
                            style = ft.ButtonStyle(
                                mouse_cursor= ft.MouseCursor.CLICK,
                            )
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=8,
                    controls=[book_card, detalle_column],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.FilledButton(
                            content="Prestar",
                            width=120,
                            on_click=_close_overlay,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.LIGHT_GREEN_600,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    # Panel semitransparente acotado (márgenes): no cubre toda la ventana.
    _dim_w = 1280
    _dim_h = 1280
    dim_panel = ft.Container(
        margin=ft.Margin(0),
        bgcolor=ft.Colors.with_opacity(0.38, ft.Colors.BLACK),
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
    page._prestamo_overlay = backdrop
    overlay = getattr(page, "overlay", None)
    if overlay is None:
        page.overlay = [backdrop]
    else:
        overlay.append(backdrop)
    page.update()
