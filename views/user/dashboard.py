import flet as ft
from database.queries import obtenerUsuarioInfo, obtenerCategorias, obtenerLibrosFiltrados
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


def build_dashboard_main_body(page: ft.Page) -> ft.Column:

    codigoSesionUsuario = page.session.store.get("codigo_usuario")
    infoUsuario = obtenerUsuarioInfo(codigoSesionUsuario)
    nombreUsuario = infoUsuario[0][2] if infoUsuario else "Usuario"

    # ── Estado de los filtros ────────────────────────────────────
    categoria_seleccionada = {"valor": ""}       # "" = Todos
    solo_disponibles = {"valor": False}
    texto_busqueda = {"valor": ""}

    # ── Refs a contenedores dinámicos ────────────────────────────
    fila_libros_ref = ft.Ref[ft.Row]()
    fila_categorias_ref = ft.Ref[ft.Row]()

    # ── Construir tarjetas de libros desde la BD ─────────────────
    def _construir_cards() -> list[ft.Control]:
        libros_raw = obtenerLibrosFiltrados(
            texto_busqueda=texto_busqueda["valor"],
            categoria=categoria_seleccionada["valor"],
            solo_disponibles=solo_disponibles["valor"],
        )

        if not libros_raw:
            return [
                ft.Container(
                    width=960,
                    height=250,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=ft.Colors.GREY_400),
                            ft.Text(
                                "No se encontraron libros",
                                size=16,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREY_500,
                            ),
                        ],
                    ),
                )
            ]

        def _prestar_factory(libro_dict: dict):
            def _handler(e):
                open_prestar_dialog(page, libro_dict)
            return _handler

        cards = []
        for row in libros_raw:
            libro_dict = {
                "isbn": row[0],
                "titulo": row[1],
                "autores": row[2],
                "editorial": row[3],
                "anio": str(row[4]) if row[4] else "",
                "categoria": row[5] if row[5] else "",
                "descripcion": row[6] if row[6] else "",
            }
            cards.append(
                card_box_libro(
                    titulo=libro_dict["titulo"],
                    autores=libro_dict["autores"],
                    editorial=libro_dict["editorial"],
                    anio=libro_dict["anio"],
                    descripcion=libro_dict["descripcion"],
                    on_prestar=_prestar_factory(libro_dict),
                )
            )
        return cards

    # ── Construir fila de botones de categoría ───────────────────
    def _construir_btns_categoria() -> list[ft.Control]:
        categorias_db = obtenerCategorias()
        todas = ["Todos"] + categorias_db

        btns = []
        for cat in todas:
            valor_filtro = "" if cat == "Todos" else cat
            es_sel = (categoria_seleccionada["valor"] == valor_filtro)

            def _on_cat_click(e, v=valor_filtro):
                # Toggle: si ya está seleccionada, deseleccionar (mostrar todos)
                if categoria_seleccionada["valor"] == v and v != "":
                    categoria_seleccionada["valor"] = ""
                else:
                    categoria_seleccionada["valor"] = v
                _actualizar_todo()

            btns.append(botonesCategoria(cat, seleccionado=es_sel, on_click=_on_cat_click))
        return btns

    # ── Actualizar UI completa ───────────────────────────────────
    def _actualizar_todo():
        row_libros = fila_libros_ref.current
        if row_libros:
            row_libros.controls = _construir_cards()

        row_cats = fila_categorias_ref.current
        if row_cats:
            row_cats.controls = _construir_btns_categoria()

        page.update()

    # ── Handlers ─────────────────────────────────────────────────
    def _on_search_change(e):
        texto_busqueda["valor"] = e.data if e.data else ""
        _actualizar_todo()

    def _on_switch_change(e):
        solo_disponibles["valor"] = e.control.value
        _actualizar_todo()

    # ── Layout ───────────────────────────────────────────────────
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
                                        bar_hint_text="Busca por título, autor o ISBN",
                                        bar_bgcolor=ft.Colors.WHITE,
                                        bar_text_style=ft.TextStyle(
                                            color=ft.Colors.BLACK
                                        ),
                                        bar_hint_text_style=ft.TextStyle(
                                            color=ft.Colors.GREY_400
                                        ),
                                        on_change=_on_search_change,
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
                                                    on_change=_on_switch_change,
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
                                ref=fila_categorias_ref,
                                spacing=3,
                                scroll=ft.ScrollMode.AUTO,
                                controls=_construir_btns_categoria(),
                            ),
                        ),
                    ],
                ),
            ),
            # Fila de libros
            ft.Container(
                width=1000,
                height=270,
                margin=ft.Margin(16, 0, 0, 0),
                content=ft.Row(
                    ref=fila_libros_ref,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                    controls=_construir_cards(),
                ),
            ),
        ],
    )
