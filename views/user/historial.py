import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn

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
    imagen_src: str | None = None,
) -> ft.Container:
    """Tarjeta de registro del historial (solo lectura). Listo para enlazar con la query."""
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
            ],
        ),
    )


def _registros_ejemplo() -> list[dict]:
    """Datos de diseño; sustituir por filas de la query."""
    lorem = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )
    return [
        {
            "titulo": "Título libro",
            "autores": "Autor(es)",
            "fecha_prestamo": "12/02/26",
            "fecha_devolucion": "20/02/26",
            "descripcion": lorem,
        },
        {
            "titulo": "Cien años de soledad",
            "autores": "Gabriel García Márquez",
            "fecha_prestamo": "01/03/26",
            "fecha_devolucion": "16/03/26",
            "descripcion": lorem,
        },
        {
            "titulo": "Rayuela",
            "autores": "Julio Cortázar",
            "fecha_prestamo": "05/03/26",
            "fecha_devolucion": "20/03/26",
            "descripcion": lorem,
        },
        {
            "titulo": "Pedro Páramo",
            "autores": "Juan Rulfo",
            "fecha_prestamo": "08/03/26",
            "fecha_devolucion": "23/03/26",
            "descripcion": lorem,
        },
        {
            "titulo": "Ficciones",
            "autores": "Jorge Luis Borges",
            "fecha_prestamo": "10/03/26",
            "fecha_devolucion": "25/03/26",
            "descripcion": lorem,
        },
    ]


def fila_historial_scroll() -> ft.Container:
    """Misma zona scroll horizontal que devolver_libro (altura y ListView)."""
    registros = _registros_ejemplo()
    cards = [
        card_historial_prestamo(
            titulo=r["titulo"],
            autores=r["autores"],
            fecha_prestamo=r["fecha_prestamo"],
            fecha_devolucion=r["fecha_devolucion"],
            descripcion=r["descripcion"],
        )
        for r in registros
    ]
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
            fila_historial_scroll(),
        ],
    )


def historial(page: ft.Page):
    return ft.View(
        route="/historial",
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
                        userSideBar(page),
                        ft.VerticalDivider(),
                        ft.Container(
                            width=1000,
                            height=700,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    soyAdminBtn(page),
                                    historial_body_after_sidebar(page),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
