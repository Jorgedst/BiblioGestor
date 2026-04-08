import flet as ft
from views.reusable.userSideBar import userSideBar
from views.reusable.soyAdminBtn import soyAdminBtn

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


def _prestamos_ejemplo() -> list[dict]:
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
            "titulo": "Rayuela",
            "autores": "Julio Cortázar",
            "fecha_prestamo": "05/03/26",
            "fecha_devolucion": "20/03/26",
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
            "titulo": "Rayuela",
            "autores": "Julio Cortázar",
            "fecha_prestamo": "05/03/26",
            "fecha_devolucion": "20/03/26",
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


def fila_cards_devolver_scroll(page: ft.Page) -> ft.Container:
    prestamos = _prestamos_ejemplo()

    def _on_devolver_factory(_item: dict):
        def _h(e):
            pass

        return _h

    cards = [
        card_box_devolver(
            titulo=p["titulo"],
            autores=p["autores"],
            fecha_prestamo=p["fecha_prestamo"],
            fecha_devolucion=p["fecha_devolucion"],
            descripcion=p["descripcion"],
            on_devolver=_on_devolver_factory(p),
        )
        for p in prestamos
    ]

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


def devolverLibro(page: ft.Page):
    return ft.View(
        route="/devolverLibro",
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
                                    devolver_libro_body_after_sidebar(page),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
