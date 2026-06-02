"""
notificaciones.py
=================
Componente de Centro de Notificaciones para el dashboard del usuario.

Uso:
    from views.user.notificaciones import build_notificaciones_panel
    # dentro de una función de cuerpo principal:
    panel = build_notificaciones_panel(page)

El panel puede integrarse en la sidebar o en el cuerpo principal del
dashboard. Muestra todas las notificaciones del usuario en sesión,
permite marcar cada una como leída y tiene un botón "Marcar todo".
"""

import flet as ft
from database.queries import fetch_query, execute_query


# ─────────────────────────────────────────────────────────────────
# Helpers de BD (privados al módulo)
# ─────────────────────────────────────────────────────────────────

def _obtener_notificaciones(codigo_usuario: str) -> list:
    """
    Retorna todas las notificaciones del usuario ordenadas por fecha desc.
    Columnas: idNotificacion, mensaje, fechaEnvio, leido
    """
    query = """
        SELECT idNotificacion, mensaje, fechaEnvio, leido
        FROM   notificaciones
        WHERE  codigoUsuario = %s
        ORDER  BY fechaEnvio DESC
        LIMIT  50
    """
    ok, rows = fetch_query(query, (codigo_usuario,))
    return rows if ok else []


def _marcar_leida(id_notificacion: int) -> None:
    execute_query(
        "UPDATE notificaciones SET leido = 1 WHERE idNotificacion = %s",
        (id_notificacion,),
    )


def _marcar_todas_leidas(codigo_usuario: str) -> None:
    execute_query(
        "UPDATE notificaciones SET leido = 1 WHERE codigoUsuario = %s",
        (codigo_usuario,),
    )


# ─────────────────────────────────────────────────────────────────
# Icono de campana con badge (para insertar en sidebar/header)
# ─────────────────────────────────────────────────────────────────

def build_campana_notificaciones(page: ft.Page, on_abrir) -> ft.Control:
    """
    Devuelve un Stack con la campana y un badge numérico de no leídas.
    `on_abrir` es el callback que muestra el panel completo.
    """
    codigo = page.session.store.get("codigo_usuario") if hasattr(page, "session") else None
    if not codigo:
        return ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE, on_click=on_abrir)

    notifs = _obtener_notificaciones(codigo)
    no_leidas = sum(1 for n in notifs if n[3] == 0)

    badge_ctrl = ft.Badge(
        content=ft.Icon(ft.Icons.NOTIFICATIONS, size=24, color=ft.Colors.GREY_700),
        label=str(no_leidas) if no_leidas > 0 else None,
        bgcolor=ft.Colors.RED_600,
        label_color=ft.Colors.WHITE,
        small_size=10,
    )

    return ft.IconButton(
        content=badge_ctrl,
        tooltip="Notificaciones",
        on_click=on_abrir,
    )


# ─────────────────────────────────────────────────────────────────
# Panel completo de notificaciones
# ─────────────────────────────────────────────────────────────────

def build_notificaciones_panel(page: ft.Page) -> ft.Column:
    """
    Construye el panel completo de notificaciones del usuario en sesión.
    Devuelve un ft.Column listo para usarse como cuerpo en _mostrar_cuerpo().
    """
    codigo = page.session.store.get("codigo_usuario") if hasattr(page, "session") else None

    # ── Lista mutable de controles ───────────────────────────────
    lista_col = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, tight=True)
    contador_text = ft.Text("", size=12, color=ft.Colors.GREY_600)

    def _fmt_fecha(dt_obj):
        if hasattr(dt_obj, "strftime"):
            return dt_obj.strftime("%d/%m/%Y  %H:%M")
        return str(dt_obj) if dt_obj else "—"

    def _refrescar():
        notifs = _obtener_notificaciones(codigo) if codigo else []
        lista_col.controls.clear()

        no_leidas = sum(1 for n in notifs if n[3] == 0)
        contador_text.value = (
            f"{no_leidas} sin leer  •  {len(notifs)} en total"
            if notifs else "No tienes notificaciones."
        )

        if not notifs:
            lista_col.controls.append(
                ft.Container(
                    padding=ft.Padding(0, 40, 0, 40),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS_OFF_OUTLINED,
                                    size=48, color=ft.Colors.GREY_300),
                            ft.Text("Todo al día — sin notificaciones",
                                    size=14, color=ft.Colors.GREY_400),
                        ],
                    ),
                )
            )
            page.update()
            return

        for n in notifs:
            id_notif, mensaje, fecha_envio, leido = n

            # ── Fondo diferenciado para no leídas ────────────────
            is_leida = leido == 1
            bg_color = ft.Colors.WHITE if is_leida else ft.Colors.BLUE_50
            border_color = ft.Colors.GREY_200 if is_leida else ft.Colors.BLUE_200

            # ── Icono según tipo de mensaje ───────────────────────
            if "vence" in mensaje.lower() or "atención" in mensaje.lower() or "⚠️" in mensaje:
                icono = ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED,
                                color=ft.Colors.AMBER_700, size=20)
            elif "reserva" in mensaje.lower():
                icono = ft.Icon(ft.Icons.BOOKMARK_ADDED,
                                color=ft.Colors.BLUE_600, size=20)
            else:
                icono = ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED,
                                color=ft.Colors.GREY_600, size=20)

            # ── Botón marcar como leída ───────────────────────────
            def _make_leer(nid):
                def _h(e):
                    _marcar_leida(nid)
                    _refrescar()
                return _h

            fila = ft.Container(
                border=ft.Border.all(1, border_color),
                border_radius=10,
                padding=ft.Padding(12, 10, 12, 10),
                bgcolor=bg_color,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Row(
                            spacing=10,
                            expand=True,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Container(
                                    margin=ft.Margin(0, 2, 0, 0),
                                    content=icono,
                                ),
                                ft.Column(
                                    spacing=3, tight=True, expand=True,
                                    controls=[
                                        ft.Text(
                                            mensaje,
                                            size=13,
                                            color=ft.Colors.GREY_900 if not is_leida
                                                  else ft.Colors.GREY_700,
                                            weight=ft.FontWeight.W_500
                                                   if not is_leida
                                                   else ft.FontWeight.W_400,
                                            max_lines=4,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                        ft.Text(
                                            _fmt_fecha(fecha_envio),
                                            size=10,
                                            color=ft.Colors.GREY_500,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        # Badge "NUEVO" + botón marcar leída
                        ft.Column(
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            tight=True,
                            controls=[
                                ft.Container(
                                    padding=ft.Padding(6, 2, 6, 2),
                                    border_radius=4,
                                    bgcolor=ft.Colors.BLUE_600,
                                    visible=not is_leida,
                                    content=ft.Text("NUEVO", size=9,
                                                    weight=ft.FontWeight.W_700,
                                                    color=ft.Colors.WHITE),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE
                                         if not is_leida
                                         else ft.Icons.CHECK_CIRCLE,
                                    icon_size=18,
                                    icon_color=ft.Colors.BLUE_400
                                               if not is_leida
                                               else ft.Colors.GREY_400,
                                    tooltip="Marcar como leída",
                                    on_click=_make_leer(id_notif),
                                    visible=not is_leida,
                                    padding=0,
                                ),
                            ],
                        ),
                    ],
                ),
            )
            lista_col.controls.append(fila)

        page.update()

    def _marcar_todo(e):
        if codigo:
            _marcar_todas_leidas(codigo)
            _refrescar()

    # ── Carga inicial ────────────────────────────────────────────
    _refrescar()

    # ── Layout del panel ─────────────────────────────────────────
    return ft.Column(
        spacing=16,
        controls=[
            # Encabezado
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS, size=28,
                                    color=ft.Colors.GREY_800),
                            ft.Text(
                                "Centro de Notificaciones",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_900,
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            contador_text,
                            ft.FilledButton(
                                content="Marcar todo como leído",
                                icon=ft.Icons.DONE_ALL,
                                on_click=_marcar_todo,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREY_800,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    text_style=ft.TextStyle(
                                        size=12, weight=ft.FontWeight.W_600,
                                    ),
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                icon_size=20,
                                tooltip="Actualizar",
                                on_click=lambda e: _refrescar(),
                            ),
                        ],
                    ),
                ],
            ),

            # Lista con scroll
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=12,
                bgcolor=ft.Colors.GREY_50,
                height=460,
                content=lista_col,
            ),

            # Nota informativa al pie
            ft.Container(
                padding=ft.Padding(12, 8, 12, 8),
                border_radius=8,
                bgcolor=ft.Colors.BLUE_50,
                border=ft.Border.all(1, ft.Colors.BLUE_100),
                content=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=14,
                                color=ft.Colors.BLUE_600),
                        ft.Text(
                            "Las notificaciones de alertas de vencimiento se generan "
                            "automáticamente al iniciar sesión. Revisa regularmente "
                            "para no perder la fecha de devolución.",
                            size=11,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                ),
            ),
        ],
    )
