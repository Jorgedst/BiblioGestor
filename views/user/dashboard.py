import flet as ft
from database.queries import obtenerUsuarioInfo
from views.reusable.btnesCategoria import botonesCategoria
from views.user.prestar_dialog import open_prestar_dialog

# Verde principal alineado con botones de categoría / acciones
_PRESTAR_GREEN = ft.Colors.LIGHT_GREEN_600
_CARD_WIDTH = 200
_PORTADA_HEIGHT = 140


def obtenerIconoUsuario(nombreUsuario: str):
    diceBearIcono = f"https://api.dicebear.com/9.x/lorelei/png?backgroundType=gradientLinear&earrings[]&earringsProbability=0&hairAccessoriesProbability=0&mouth=happy01,happy02,happy03,happy04,happy05,happy06,happy07,happy08,happy09,happy10,happy11,happy12,happy13,happy14,happy15,happy16,happy17,happy18&backgroundColor=CDF7CD,7CB342&seed={nombreUsuario}"
    return diceBearIcono


def card_box_libro(
    titulo: str,
    autores: str,
    editorial: str,
    anio: str,
    descripcion: str,
    imagen_src: str | None = None,
    on_prestar=None,) -> ft.Container:
    """
    Tarjeta de libro para la lista horizontal.
    Parámetros listos para enlazar con la query más adelante.
    """
    portada = (
        ft.Container(
            height=_PORTADA_HEIGHT,
            border_radius=8,
            bgcolor= ft.Colors.GREY_300,
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.MENU_BOOK,
                size=48,
                color=ft.Colors.GREY_800,
            ),
        )
    )

    return ft.Container(
        width=_CARD_WIDTH,
        margin=ft.Margin(0, 0, 8, 0),
        padding=ft.Padding(12, 12, 12, 10),
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=12,
        content=ft.Column(
            spacing=6,
            tight=True,
            controls=[
                ft.Text(
                    titulo,
                    size=14,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.GREY_900,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    autores,
                    size=11,
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.GREY_600,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                portada,
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Text(
                            editorial,
                            size=11,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_800,
                            expand=True,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            anio,
                            size=11,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(
                            icon=ft.Icons.BOOK,
                            content="Prestar",
                            width=88,
                            height=34,
                            style=ft.ButtonStyle(
                                mouse_cursor=ft.MouseCursor.CLICK,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                },
                                bgcolor={
                                    ft.ControlState.DEFAULT: _PRESTAR_GREEN,
                                    ft.ControlState.HOVERED: ft.Colors.LIGHT_GREEN_900,
                                },
                                shape=ft.ContinuousRectangleBorder(radius=8),
                                text_style=ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                ),
                                padding=ft.Padding(8, 4, 8, 4),
                            ),
                            on_click=on_prestar,
                        ),
                    ],
                ),
            ],
        ),
    )


def _libros_ejemplo() -> list[dict]:
    """Datos de diseño; sustituir por resultados de búsqueda cuando exista la query."""
    return [
        {
            "titulo": "Título libro",
            "autores": "Autor(es)",
            "editorial": "Alfaguara",
            "anio": "1999",
            "descripcion": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.",
        },
        {
            "titulo": "Cien años de soledad",
            "autores": "Gabriel García Márquez",
            "editorial": "Sudamericana",
            "anio": "1967",
            "descripcion": "Novela fundacional del boom latinoamericano y obra cumbre del realismo mágico.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
        {
            "titulo": "El ingenioso hidalgo",
            "autores": "Miguel de Cervantes",
            "editorial": "Francisco de Robles",
            "anio": "1605",
            "descripcion": "Clásico de la literatura española y precursor de la novela moderna.",
        },
    ]


def fila_libros_scrollable(page: ft.Page) -> ft.Container:
    """Fila horizontal con scroll; aquí se conectará la búsqueda."""
    libros = _libros_ejemplo()

    def _prestar_factory(libro: dict):
        def _handler(e):
            open_prestar_dialog(page, libro)

        return _handler

    cards = [
        card_box_libro(
            titulo=L["titulo"],
            autores=L["autores"],
            editorial=L["editorial"],
            anio=L["anio"],
            descripcion=L["descripcion"],
            on_prestar=_prestar_factory(L),
        )
        for L in libros
    ]

    return ft.Container(
        width=1000,
        height=270,
        margin=ft.Margin(16, 0, 0, 0),
        content=ft.Row(
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
            controls=cards,
        ),
    )


def build_dashboard_main_body(page: ft.Page) -> ft.Column:

    codigoSesionUsuario = page.session.store.get("codigo_usuario")
    infoUsuario = obtenerUsuarioInfo(codigoSesionUsuario)
    nombreUsuario = infoUsuario[0][2] if infoUsuario else "Usuario"
    return ft.Column(
        spacing=0,
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            margin=ft.Margin(0, 0, 0, 10),
                            border_radius=100,
                            content=ft.Image(
                                src=obtenerIconoUsuario(nombreUsuario),
                                width=180,
                                height=180,
                                margin=0,
                                fit=ft.BoxFit.COVER,
                            ),
                        ),
                        ft.Text(
                            value=f"¡Hola {nombreUsuario}!",
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_900,
                        ),
                    ]
                )
            ),
            ft.Container(
                width=1000,
                height=120,
                content=ft.Column(
                    spacing=5,
                    margin=ft.Margin(15, 0, 0, 0),
                    controls=[
                        ft.Text(
                            margin=ft.Margin(8, 0, 0, 0),
                            value="Buscar libro",
                            size=15,
                            weight=ft.FontWeight.W_400,
                            color=ft.Colors.GREY_900,
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.SearchBar(
                                        bar_trailing=[
                                            ft.IconButton(
                                                icon=ft.Icons.SEARCH,
                                                icon_color=ft.Colors.GREY_600,
                                            )
                                        ],
                                        height=40,
                                        bar_elevation=2,
                                        bar_overlay_color=ft.Colors.GREY_200,
                                        bar_hint_text="Busca un libro",
                                        bar_bgcolor=ft.Colors.WHITE,
                                        bar_text_style=ft.TextStyle(
                                            color=ft.Colors.BLACK
                                        ),
                                        bar_hint_text_style=ft.TextStyle(
                                            color=ft.Colors.GREY_400
                                        ),
                                    ),
                                    ft.Container(
                                        content=ft.Row(
                                            margin=ft.Margin(15, 0, 0, 0),
                                            controls=[
                                                ft.Text(
                                                    value="Mostrar Solo\nDisponibles",
                                                    size=12,
                                                    weight=ft.FontWeight.W_400,
                                                    color=ft.Colors.GREY_900,
                                                ),
                                                ft.CupertinoSwitch(
                                                    value=False,
                                                    active_track_color=ft.Colors.BLACK,
                                                ),
                                            ],
                                        )
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            width=1000,
                            height=30,
                            content=ft.Row(
                                spacing=3,
                                controls=[
                                    botonesCategoria("Todos"),
                                    botonesCategoria("67"),
                                    botonesCategoria("mibombo"),
                                    botonesCategoria("Son"),
                                    botonesCategoria("Sybau"),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
            fila_libros_scrollable(page),
        ],
    )
