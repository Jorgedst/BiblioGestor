import flet as ft
import threading


def open_succesful_dialog(page: ft.Page, mensaje: str = "La operación se realizó correctamente."):
    """
    Overlay modal de éxito con ícono ✓, mensaje y cierre automático (3 s).
    """

    def _close_overlay(e=None):
        overlay_ref = getattr(page, "_succesful_overlay", None)
        overlay = getattr(page, "overlay", None)
        if overlay_ref and overlay is not None and overlay_ref in overlay:
            overlay.remove(overlay_ref)
        page._succesful_overlay = None
        page.update()

    def _auto_close():
        _close_overlay()

    # ── Contenido del modal ──────────────────────────────────────
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
                # Círculo verde con check
                ft.Container(
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=ft.Colors.LIGHT_GREEN_50,
                    border=ft.Border.all(3, ft.Colors.LIGHT_GREEN_400),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icon=ft.Icons.CHECK_ROUNDED,
                        size=48,
                        color=ft.Colors.LIGHT_GREEN_600,
                    ),
                ),
                ft.Text(
                    value="¡Operación exitosa!",
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
                        bgcolor=ft.Colors.LIGHT_GREEN_600,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
            ],
        ),
    )

    # ── Fondo oscuro semitransparente ────────────────────────────
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

    # Limpiar overlay anterior si existe
    _close_overlay()
    page._succesful_overlay = backdrop
    overlay = getattr(page, "overlay", None)
    if overlay is None:
        page.overlay = [backdrop]
    else:
        overlay.append(backdrop)
    page.update()

    # Cierre automático tras 3 segundos
    threading.Timer(3.0, _auto_close).start()


def open_confirm_dialog(page: ft.Page, titulo: str, mensaje: str, on_confirm):
    """
    Dialog de confirmación con dos botones: Cancelar / Confirmar.
    `on_confirm` se ejecuta al presionar "Confirmar".
    """

    def _close_overlay(e=None):
        overlay_ref = getattr(page, "_confirm_overlay", None)
        overlay = getattr(page, "overlay", None)
        if overlay_ref and overlay is not None and overlay_ref in overlay:
            overlay.remove(overlay_ref)
        page._confirm_overlay = None
        page.update()

    def _on_confirm_click(e):
        _close_overlay()
        if on_confirm:
            on_confirm(e)

    modal_content = ft.Container(
        width=400,
        bgcolor=ft.Colors.WHITE,
        border_radius=18,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        padding=ft.Padding(28, 28, 28, 22),
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
                # Ícono de advertencia
                ft.Container(
                    width=70,
                    height=70,
                    border_radius=35,
                    bgcolor=ft.Colors.RED_50,
                    border=ft.Border.all(3, ft.Colors.RED_300),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icon=ft.Icons.WARNING_AMBER_ROUNDED,
                        size=40,
                        color=ft.Colors.RED_600,
                    ),
                ),
                ft.Text(
                    value=titulo,
                    size=20,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    value=mensaje,
                    size=13,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=4),
                ft.Row(
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.OutlinedButton(
                            content="Cancelar",
                            width=130,
                            on_click=_close_overlay,
                            style=ft.ButtonStyle(
                                color=ft.Colors.GREY_700,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                side=ft.BorderSide(1, ft.Colors.GREY_400),
                            ),
                        ),
                        ft.FilledButton(
                            content="Confirmar",
                            width=130,
                            on_click=_on_confirm_click,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                    ],
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
    page._confirm_overlay = backdrop
    overlay = getattr(page, "overlay", None)
    if overlay is None:
        page.overlay = [backdrop]
    else:
        overlay.append(backdrop)
    page.update()
