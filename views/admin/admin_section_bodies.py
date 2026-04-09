import flet as ft
import datetime


def build_admin_gestion_home(page: ft.Page) -> ft.Column:
    """Vista principal Gestión: paneles con datos reales de la BD."""
    from database.queries import (
        obtenerPrestamosActivos, obtenerPrestamosVencidos,
        obtenerUsuariosMasPrestamos, obtenerLibrosMasPrestados,
    )

    # ── Helpers ──────────────────────────────────────────────────
    def _fmt_fecha(dt_obj):
        if hasattr(dt_obj, "strftime"):
            return dt_obj.strftime("%d/%m/%Y")
        return str(dt_obj)

    def _fila_prestamo(p):
        """
        p: (idPrestamo, nombreUsuario, titulo, ejemplar, fechaPrestamo, fechaVencimiento)
        """
        return ft.Container(
            border=ft.Border.all(1, ft.Colors.GREY_200),
            border_radius=6,
            padding=ft.Padding(8, 6, 8, 6),
            bgcolor=ft.Colors.WHITE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=1, tight=True, expand=True,
                        controls=[
                            ft.Text(f"#{p[0]}  {p[2]}", size=12, weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(f"{p[1]}  •  Ej. #{p[3]}", size=10,
                                    color=ft.Colors.GREY_600, max_lines=1),
                        ],
                    ),
                    ft.Column(
                        spacing=1, tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text(_fmt_fecha(p[4]), size=10, color=ft.Colors.GREY_600),
                            ft.Text(_fmt_fecha(p[5]), size=10, weight=ft.FontWeight.W_600,
                                    color=ft.Colors.GREY_800),
                        ],
                    ),
                ],
            ),
        )

    def _empty_msg(texto):
        return ft.Container(
            padding=20, alignment=ft.Alignment.CENTER,
            content=ft.Text(texto, size=12, color=ft.Colors.GREY_500),
        )

    # ── 1) Préstamos activos ─────────────────────────────────────
    activos = obtenerPrestamosActivos()
    activos_controls = [_fila_prestamo(p) for p in activos] if activos else [_empty_msg("Sin préstamos activos")]

    # ── 2) Préstamos vencidos ────────────────────────────────────
    vencidos = obtenerPrestamosVencidos()
    vencidos_controls = [_fila_prestamo(p) for p in vencidos] if vencidos else [_empty_msg("Sin préstamos vencidos")]

    # ── 3) Usuarios con más préstamos ────────────────────────────
    top_users = obtenerUsuariosMasPrestamos()
    if top_users:
        top_users_controls = []
        for i, u in enumerate(top_users):
            bg = ft.Colors.AMBER_50 if i == 0 else ft.Colors.WHITE
            top_users_controls.append(
                ft.Container(
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                    border_radius=6,
                    padding=ft.Padding(10, 6, 10, 6),
                    bgcolor=bg,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(spacing=8, controls=[
                                ft.Container(
                                    width=24, height=24, border_radius=12,
                                    bgcolor=ft.Colors.GREY_300,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text(str(i + 1), size=11,
                                                    weight=ft.FontWeight.W_700,
                                                    color=ft.Colors.BLACK),
                                ),
                                ft.Text(u[1], size=12, weight=ft.FontWeight.W_600,
                                        color=ft.Colors.BLACK),
                            ]),
                            ft.Container(
                                padding=ft.Padding(8, 2, 8, 2),
                                border_radius=4,
                                bgcolor=ft.Colors.LIGHT_GREEN_600,
                                content=ft.Text(f"{u[2]} préstamos", size=10,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.WHITE),
                            ),
                        ],
                    ),
                )
            )
    else:
        top_users_controls = [_empty_msg("Sin datos de préstamos")]

    # ── 4) Libros más prestados (con filtro de fechas) ───────────
    libros_col = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO, tight=True)

    tf_desde = ft.TextField(
        hint_text="dd/mm/aaaa", width=120, height=40, dense=True, border_radius=8,
    )
    tf_hasta = ft.TextField(
        hint_text="dd/mm/aaaa", width=120, height=40, dense=True, border_radius=8,
    )

    def _parse_fecha(txt):
        txt = (txt or "").strip()
        if not txt:
            return None
        for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(txt, fmt)
            except ValueError:
                continue
        return None

    def _refrescar_libros(e=None):
        fecha_d = _parse_fecha(tf_desde.value)
        fecha_h = _parse_fecha(tf_hasta.value)
        data = obtenerLibrosMasPrestados(fecha_d, fecha_h)
        libros_col.controls.clear()

        if not data:
            libros_col.controls.append(_empty_msg("Sin datos en ese rango"))
            page.update()
            return

        for i, lb in enumerate(data):
            # lb: (isbn, titulo, autores, totalPrestamos)
            libros_col.controls.append(
                ft.Container(
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                    border_radius=6,
                    padding=ft.Padding(10, 6, 10, 6),
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(spacing=8, controls=[
                                ft.Container(
                                    width=24, height=24, border_radius=12,
                                    bgcolor=ft.Colors.GREY_300,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text(str(i + 1), size=11,
                                                    weight=ft.FontWeight.W_700,
                                                    color=ft.Colors.BLACK),
                                ),
                                ft.Column(spacing=0, tight=True, controls=[
                                    ft.Text(lb[1], size=12, weight=ft.FontWeight.W_600,
                                            color=ft.Colors.BLACK, max_lines=1,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(f"{lb[2]}  •  ISBN: {lb[0]}", size=10,
                                            color=ft.Colors.GREY_600, max_lines=1),
                                ]),
                            ]),
                            ft.Container(
                                padding=ft.Padding(8, 2, 8, 2),
                                border_radius=4,
                                bgcolor=ft.Colors.BLUE_600,
                                content=ft.Text(f"{lb[3]} préstamos", size=10,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.WHITE),
                            ),
                        ],
                    ),
                )
            )
        page.update()

    tf_desde.on_submit = _refrescar_libros
    tf_hasta.on_submit = _refrescar_libros

    _refrescar_libros()

    # ── Layout ───────────────────────────────────────────────────
    return ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(value="Gestión", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),

            # Fila: Activos + Vencidos
            ft.Row(
                spacing=12,
                controls=[
                    ft.Container(
                        expand=True,
                        height=200,
                        border=ft.Border.all(1, ft.Colors.GREY_400),
                        border_radius=10,
                        padding=ft.Padding(12, 12, 12, 12),
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=6, tight=True,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text("Préstamos (Activos)", size=14,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.BLACK),
                                        ft.Container(
                                            padding=ft.Padding(6, 2, 6, 2),
                                            border_radius=4,
                                            bgcolor=ft.Colors.GREEN_600,
                                            content=ft.Text(str(len(activos)), size=11,
                                                            weight=ft.FontWeight.W_700,
                                                            color=ft.Colors.WHITE),
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    expand=True,
                                    border_radius=8,
                                    bgcolor=ft.Colors.GREY_50,
                                    padding=4,
                                    content=ft.Column(
                                        spacing=4,
                                        scroll=ft.ScrollMode.AUTO,
                                        tight=True,
                                        controls=activos_controls,
                                    ),
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        height=200,
                        border=ft.Border.all(1, ft.Colors.GREY_400),
                        border_radius=10,
                        padding=ft.Padding(12, 12, 12, 12),
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=6, tight=True,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text("Préstamos (Vencidos)", size=14,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.BLACK),
                                        ft.Container(
                                            padding=ft.Padding(6, 2, 6, 2),
                                            border_radius=4,
                                            bgcolor=ft.Colors.RED_600,
                                            content=ft.Text(str(len(vencidos)), size=11,
                                                            weight=ft.FontWeight.W_700,
                                                            color=ft.Colors.WHITE),
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    expand=True,
                                    border_radius=8,
                                    bgcolor=ft.Colors.GREY_50,
                                    padding=4,
                                    content=ft.Column(
                                        spacing=4,
                                        scroll=ft.ScrollMode.AUTO,
                                        tight=True,
                                        controls=vencidos_controls,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),

            # Usuarios con más préstamos
            ft.Container(
                height=160,
                border=ft.Border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                padding=ft.Padding(12, 12, 12, 12),
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=6, tight=True,
                    controls=[
                        ft.Text("Usuarios con más préstamos", size=14,
                                weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                        ft.Container(
                            expand=True,
                            border_radius=8,
                            bgcolor=ft.Colors.GREY_50,
                            padding=4,
                            content=ft.Column(
                                spacing=4,
                                scroll=ft.ScrollMode.AUTO,
                                tight=True,
                                controls=top_users_controls,
                            ),
                        ),
                    ],
                ),
            ),

            # Libros más prestados con filtro de fechas
            ft.Container(
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value="Libros más prestados",
                                    size=18,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                                ft.Row(
                                    spacing=12,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Desde", size=12, color=ft.Colors.BLACK),
                                        tf_desde,
                                        ft.Text("Hasta", size=12, color=ft.Colors.BLACK),
                                        tf_hasta,
                                        ft.IconButton(
                                            icon=ft.Icons.SEARCH,
                                            icon_size=20,
                                            tooltip="Filtrar",
                                            on_click=_refrescar_libros,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(
                            height=250,
                            margin=ft.Margin(0, 0, 0, 30),
                            border=ft.Border.all(1, ft.Colors.GREY_400),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=libros_col,
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_libros(page: ft.Page) -> ft.Column:
    """Layout para gestionar libros con CRUD completo y panel de ejemplares."""
    from database.queries import (
        registrar_libro, registrar_ejemplar,
        existeISBN, existeEjemplar,
        obtenerLibros, obtenerEjemplaresPorISBN,
        actualizarLibro, actualizarEjemplar,
        eliminarLibro, eliminarEjemplar,
    )
    from views.reusable.succesful import open_succesful_dialog, open_confirm_dialog

    # ── Categorías comunes ───────────────────────────────────────
    _CATEGORIAS = [
        "Ciencia ficción", "Fantasía", "Romance", "Misterio", "Terror",
        "Historia", "Biografía", "Ciencia", "Tecnología", "Matemáticas",
        "Filosofía", "Psicología", "Arte", "Música", "Poesía",
        "Derecho", "Economía", "Medicina", "Ingeniería", "Educación",
        "Literatura clásica", "Novela", "Infantil", "Autoayuda", "Religión",
    ]

    _UBICACIONES = [
        "Sala","Estante",
    ]

    _ESTADOS = ["Disponible", "Prestado", "Perdido"]

    # ── Campos del formulario de libro ───────────────────────────
    tf_isbn = ft.TextField(
        label="ISBN",
        hint_text="Ej: 9783161484100",
        dense=True,
        border_radius=8,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    tf_titulo = ft.TextField(label="Título", dense=True, border_radius=8)
    tf_autores = ft.TextField(label="Autor(es)", dense=True, border_radius=8)
    tf_editorial = ft.TextField(label="Editorial", dense=True, border_radius=8)
    tf_anio = ft.TextField(
        label="Año",
        dense=True,
        border_radius=8,
        max_length=4,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    dd_categoria = ft.Dropdown(
        label="Categoría",
        dense=True,
        border_radius=8,
        options=[ft.DropdownOption(key=c, text=c) for c in _CATEGORIAS],
        menu_height=200,
    )
    tf_descripcion = ft.TextField(
        label="Descripción",
        multiline=True,
        min_lines=2,
        max_lines=4,
        dense=True,
        border_radius=8,
    )

    _libro_fields = [tf_isbn, tf_titulo, tf_autores, tf_editorial, tf_anio, tf_descripcion]

    # ── Campos del formulario de ejemplar ────────────────────────
    tf_id_ejemplar = ft.TextField(
        label="ID ejemplar #",
        dense=True,
        border_radius=8,
        width=170,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    tf_isbn_ejemplar = ft.TextField(
        label="Código ISBN del libro",
        hint_text="ISBN del libro relacionado",
        dense=True,
        border_radius=8,
        width=170,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    dd_ubicacion = ft.Dropdown(
        label="Ubicación",
        dense=True,
        border_radius=8,
        options=[ft.DropdownOption(key=u, text=u) for u in _UBICACIONES],
    )
    dd_estado = ft.Dropdown(
        label="Estado",
        dense=True,
        border_radius=8,
        options=[ft.DropdownOption(key=e, text=e) for e in _ESTADOS],
    )

    _ejemplar_fields = [tf_id_ejemplar, tf_isbn_ejemplar]

    # ── Contenedor mutable para la lista de libros ─────────────────
    lista_libros_column = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO, tight=True)

    # ── Helpers ──────────────────────────────────────────────────
    def _limpiar_errores(fields):
        for f in fields:
            f.error = None

    def _val(field):
        return (field.value or "").strip()

    # ══════════════════════════════════════════════════════════════
    # REFRESCAR LISTA DE LIBROS (en tiempo real)
    # ══════════════════════════════════════════════════════════════
    def _refrescar_lista():
        libros = obtenerLibros()
        lista_libros_column.controls.clear()

        if not libros:
            lista_libros_column.controls.append(
                ft.Container(
                    padding=20, alignment=ft.Alignment.CENTER,
                    content=ft.Text("No hay libros registrados", size=13, color=ft.Colors.GREY_500),
                )
            )
            page.update()
            return

        for libro in libros:
            isbn_l, titulo_l, autores_l = libro[0], libro[1], libro[2]
            anio_l = libro[4]

            def _make_click(iv):
                return lambda e: _abrir_panel_ejemplares(iv)

            def _make_edit(lb):
                return lambda e: _abrir_editar_libro(lb)

            def _make_delete(iv, tv):
                def _h(e):
                    open_confirm_dialog(
                        page, titulo="Eliminar libro",
                        mensaje=f"¿Eliminar \"{tv}\" (ISBN {iv})?\nSe eliminarán también sus ejemplares.",
                        on_confirm=lambda ev, _i=iv: _ejecutar_eliminar_libro(_i),
                    )
                return _h

            fila = ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=ft.Padding(10, 8, 10, 8),
                bgcolor=ft.Colors.WHITE,
                ink=True,
                on_click=_make_click(isbn_l),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=2, tight=True, expand=True,
                            controls=[
                                ft.Text(titulo_l, size=14, weight=ft.FontWeight.W_600,
                                        color=ft.Colors.BLACK, max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"{autores_l}  •  {anio_l}  •  ISBN: {isbn_l}", size=11,
                                        color=ft.Colors.GREY_600, max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                            ],
                        ),
                        ft.Row(spacing=0, controls=[
                            ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_size=18,
                                          tooltip="Editar", icon_color=ft.Colors.BLUE_600,
                                          on_click=_make_edit(libro)),
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=18,
                                          tooltip="Eliminar", icon_color=ft.Colors.RED_600,
                                          on_click=_make_delete(isbn_l, titulo_l)),
                        ]),
                    ],
                ),
            )
            lista_libros_column.controls.append(fila)
        page.update()

    # ══════════════════════════════════════════════════════════════
    # ELIMINAR LIBRO (+ sus ejemplares)
    # ══════════════════════════════════════════════════════════════
    def _ejecutar_eliminar_libro(isbn):
        for ej in obtenerEjemplaresPorISBN(isbn):
            eliminarEjemplar(ej[0])
        ok, _ = eliminarLibro(isbn)
        if ok:
            _refrescar_lista()
            open_succesful_dialog(page, "El libro y sus ejemplares han sido eliminados.")

    # ══════════════════════════════════════════════════════════════
    # EDITAR LIBRO (overlay)
    # ══════════════════════════════════════════════════════════════
    def _abrir_editar_libro(libro):
        ed_titulo = ft.TextField(label="Título", value=libro[1], dense=True, border_radius=8)
        ed_autores = ft.TextField(label="Autor(es)", value=libro[2], dense=True, border_radius=8)
        ed_editorial = ft.TextField(label="Editorial", value=libro[3], dense=True, border_radius=8)
        ed_anio = ft.TextField(label="Año", value=str(libro[4]), dense=True, border_radius=8,
                               max_length=4, input_filter=ft.NumbersOnlyInputFilter())
        ed_categoria = ft.Dropdown(
            label="Categoría", value=libro[5], dense=True, border_radius=8,
            options=[ft.DropdownOption(key=c, text=c) for c in _CATEGORIAS], menu_height=200,
        )
        ed_descripcion = ft.TextField(label="Descripción", value=libro[6] or "", dense=True,
                                      border_radius=8, multiline=True, min_lines=2, max_lines=4)
        _ed_fields = [ed_titulo, ed_autores, ed_editorial, ed_anio, ed_descripcion]

        def _close(e=None):
            ref = getattr(page, "_edit_libro_overlay", None)
            ov = getattr(page, "overlay", None)
            if ref and ov and ref in ov:
                ov.remove(ref)
            page._edit_libro_overlay = None
            page.update()

        def _guardar(e):
            _limpiar_errores(_ed_fields)
            ed_categoria.error = None
            has_err = False
            for f, m in [(ed_titulo, "Obligatorio"), (ed_autores, "Obligatorio"),
                         (ed_editorial, "Obligatorio"), (ed_anio, "Obligatorio"),
                         (ed_descripcion, "Obligatorio")]:
                if not (f.value or "").strip():
                    f.error = m; has_err = True
            if not ed_categoria.value:
                ed_categoria.error = "Selecciona una categoría"; has_err = True
            if (ed_anio.value or "").strip() and len(ed_anio.value.strip()) != 4:
                ed_anio.error = "Debe tener 4 dígitos"; has_err = True
            if has_err:
                page.update(); return
            ok, msg = actualizarLibro(
                libro[0], ed_titulo.value.strip(), ed_autores.value.strip(),
                ed_editorial.value.strip(), int(ed_anio.value.strip()),
                ed_categoria.value, ed_descripcion.value.strip(),
            )
            if ok:
                _close()
                _refrescar_lista()
                open_succesful_dialog(page, "El libro se ha actualizado correctamente.")
            else:
                ed_titulo.error = f"Error: {msg}"; page.update()

        modal = ft.Container(
            width=480, bgcolor=ft.Colors.WHITE, border_radius=14,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            padding=ft.Padding(20, 18, 20, 16),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=20,
                                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)),
            content=ft.Column(spacing=10, tight=True, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(f"Editar libro (ISBN {libro[0]})", size=16,
                            weight=ft.FontWeight.W_700, color=ft.Colors.BLACK),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_size=20, on_click=_close),
                ]),
                ed_titulo, ed_autores, ed_editorial, ed_anio, ed_categoria, ed_descripcion,
                ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                    ft.FilledButton(content="Guardar", on_click=_guardar,
                                   style=ft.ButtonStyle(bgcolor=ft.Colors.LIGHT_GREEN_600,
                                                        color=ft.Colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=10))),
                ]),
            ]),
        )
        _dim = 1280
        backdrop = ft.Container(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Container(
                margin=ft.Margin(0), bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                content=ft.Stack(width=_dim, height=_dim, alignment=ft.Alignment.CENTER, controls=[
                    ft.GestureDetector(content=ft.Container(width=_dim, height=_dim), on_tap=_close),
                    modal,
                ]),
            ),
        )
        _close()
        page._edit_libro_overlay = backdrop
        ov = getattr(page, "overlay", None)
        if ov is None:
            page.overlay = [backdrop]
        else:
            ov.append(backdrop)
        page.update()

    # ══════════════════════════════════════════════════════════════
    # PANEL DE EJEMPLARES (al hacer clic en un libro)
    # ══════════════════════════════════════════════════════════════
    def _abrir_panel_ejemplares(isbn):
        ejemplares = obtenerEjemplaresPorISBN(isbn)

        def _close_panel(e=None):
            ref = getattr(page, "_ejemplares_overlay", None)
            ov = getattr(page, "overlay", None)
            if ref and ov and ref in ov:
                ov.remove(ref)
            page._ejemplares_overlay = None
            page.update()

        def _reabrir(_e=None):
            _close_panel()
            _abrir_panel_ejemplares(isbn)

        def _editar_ejemplar(ej):
            ed_ubi = ft.Dropdown(label="Ubicación", value=ej[2], dense=True, border_radius=8,
                                 options=[ft.DropdownOption(key=u, text=u) for u in _UBICACIONES])
            ed_est = ft.Dropdown(label="Estado", value=ej[3], dense=True, border_radius=8,
                                 options=[ft.DropdownOption(key=s, text=s) for s in _ESTADOS])

            def _close_ed(e=None):
                ref = getattr(page, "_edit_ej_overlay", None)
                ov = getattr(page, "overlay", None)
                if ref and ov and ref in ov:
                    ov.remove(ref)
                page._edit_ej_overlay = None
                page.update()

            def _guardar_ej(e):
                ed_ubi.error = None; ed_est.error = None
                has_err = False
                if not ed_ubi.value:
                    ed_ubi.error = "Selecciona una ubicación"; has_err = True
                if not ed_est.value:
                    ed_est.error = "Selecciona un estado"; has_err = True
                if has_err:
                    page.update(); return
                ok, _ = actualizarEjemplar(ej[0], ed_ubi.value, ed_est.value)
                if ok:
                    _close_ed(); _reabrir()
                    open_succesful_dialog(page, "Ejemplar actualizado correctamente.")
                else:
                    ed_ubi.error = "Error al actualizar"; page.update()

            modal_ej = ft.Container(
                width=380, bgcolor=ft.Colors.WHITE, border_radius=14,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                padding=ft.Padding(20, 18, 20, 16),
                shadow=ft.BoxShadow(spread_radius=2, blur_radius=20,
                                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 4)),
                content=ft.Column(spacing=10, tight=True, controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Text(f"Editar ejemplar #{ej[0]}", size=16,
                                weight=ft.FontWeight.W_700, color=ft.Colors.BLACK),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_size=20, on_click=_close_ed),
                    ]),
                    ed_ubi, ed_est,
                    ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                        ft.FilledButton(content="Guardar", on_click=_guardar_ej,
                                       style=ft.ButtonStyle(bgcolor=ft.Colors.LIGHT_GREEN_600,
                                                            color=ft.Colors.WHITE,
                                                            shape=ft.RoundedRectangleBorder(radius=10))),
                    ]),
                ]),
            )
            _dim = 1280
            bd = ft.Container(
                expand=True, alignment=ft.Alignment.CENTER,
                content=ft.Container(
                    margin=ft.Margin(0), bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Stack(width=_dim, height=_dim, alignment=ft.Alignment.CENTER, controls=[
                        ft.GestureDetector(content=ft.Container(width=_dim, height=_dim), on_tap=_close_ed),
                        modal_ej,
                    ]),
                ),
            )
            _close_ed()
            page._edit_ej_overlay = bd
            ov = getattr(page, "overlay", None)
            if ov is None:
                page.overlay = [bd]
            else:
                ov.append(bd)
            page.update()

        def _eliminar_ejemplar_handler(id_ej):
            def _h(e):
                open_confirm_dialog(
                    page, titulo="Eliminar ejemplar",
                    mensaje=f"¿Eliminar el ejemplar #{id_ej}?",
                    on_confirm=lambda ev: _do_delete_ej(id_ej),
                )
            return _h

        def _do_delete_ej(id_ej):
            ok, _ = eliminarEjemplar(id_ej)
            if ok:
                _reabrir(); _refrescar_lista()
                open_succesful_dialog(page, "Ejemplar eliminado correctamente.")

        ej_rows = []
        if not ejemplares:
            ej_rows.append(ft.Container(
                padding=20, alignment=ft.Alignment.CENTER,
                content=ft.Text("No hay ejemplares registrados para este libro.",
                                size=13, color=ft.Colors.GREY_500),
            ))
        else:
            for ej in ejemplares:
                def _make_edit_ej(r):
                    return lambda e: _editar_ejemplar(r)
                ej_rows.append(ft.Container(
                    border=ft.Border.all(1, ft.Colors.GREY_200), border_radius=8,
                    padding=ft.Padding(10, 6, 10, 6), bgcolor=ft.Colors.WHITE,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(spacing=2, tight=True, expand=True, controls=[
                                ft.Text(f"Ejemplar #{ej[0]}", size=13,
                                        weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                                ft.Text(f"Ubicación: {ej[2]}  •  Estado: {ej[3]}",
                                        size=11, color=ft.Colors.GREY_600),
                            ]),
                            ft.Row(spacing=0, controls=[
                                ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, icon_size=16,
                                              tooltip="Editar", icon_color=ft.Colors.BLUE_600,
                                              on_click=_make_edit_ej(ej)),
                                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=16,
                                              tooltip="Eliminar", icon_color=ft.Colors.RED_600,
                                              on_click=_eliminar_ejemplar_handler(ej[0])),
                            ]),
                        ],
                    ),
                ))

        panel = ft.Container(
            width=520, bgcolor=ft.Colors.WHITE, border_radius=14,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            padding=ft.Padding(20, 18, 20, 16),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=20,
                                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)),
            content=ft.Column(spacing=10, tight=True, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(f"Ejemplares del libro (ISBN {isbn})", size=16,
                            weight=ft.FontWeight.W_700, color=ft.Colors.BLACK),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_size=20, on_click=_close_panel),
                ]),
                ft.Container(
                    height=300,
                    content=ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, controls=ej_rows),
                ),
            ]),
        )
        _dim = 1280
        backdrop = ft.Container(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Container(
                margin=ft.Margin(0), bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                content=ft.Stack(width=_dim, height=_dim, alignment=ft.Alignment.CENTER, controls=[
                    ft.GestureDetector(content=ft.Container(width=_dim, height=_dim), on_tap=_close_panel),
                    panel,
                ]),
            ),
        )
        _close_panel()
        page._ejemplares_overlay = backdrop
        ov = getattr(page, "overlay", None)
        if ov is None:
            page.overlay = [backdrop]
        else:
            ov.append(backdrop)
        page.update()

    # ══════════════════════════════════════════════════════════════
    # HANDLER – AGREGAR LIBRO
    # ══════════════════════════════════════════════════════════════
    def _on_agregar_libro(e):
        _limpiar_errores(_libro_fields)
        dd_categoria.error = None
        has_error = False

        if not _val(tf_isbn):
            tf_isbn.error = "El ISBN es obligatorio"
            has_error = True
        elif not _val(tf_isbn).isdigit():
            tf_isbn.error = "El ISBN debe contener solo números"
            has_error = True
        elif existeISBN(int(_val(tf_isbn))):
            tf_isbn.error = "Este ISBN ya está registrado"
            has_error = True

        if not _val(tf_titulo):
            tf_titulo.error = "El título es obligatorio"; has_error = True
        if not _val(tf_autores):
            tf_autores.error = "El autor es obligatorio"; has_error = True
        if not _val(tf_editorial):
            tf_editorial.error = "La editorial es obligatoria"; has_error = True
        if not _val(tf_anio):
            tf_anio.error = "El año es obligatorio"; has_error = True
        elif len(_val(tf_anio)) != 4:
            tf_anio.error = "El año debe tener 4 dígitos"; has_error = True
        if not dd_categoria.value:
            dd_categoria.error = "Selecciona una categoría"; has_error = True
        if not _val(tf_descripcion):
            tf_descripcion.error = "La descripción es obligatoria"; has_error = True

        if has_error:
            page.update(); return

        ok, msg = registrar_libro(
            int(_val(tf_isbn)), _val(tf_titulo), _val(tf_autores),
            _val(tf_editorial), int(_val(tf_anio)),
            dd_categoria.value, _val(tf_descripcion),
        )
        if ok:
            for f in _libro_fields:
                f.value = ""; f.error = None
            dd_categoria.value = None; dd_categoria.error = None
            _refrescar_lista()
            open_succesful_dialog(page, "El libro se ha registrado correctamente.")
        else:
            tf_isbn.error = f"Error: {msg}"; page.update()
            print(msg)

    # ══════════════════════════════════════════════════════════════
    # HANDLER – AGREGAR EJEMPLAR
    # ══════════════════════════════════════════════════════════════
    def _on_agregar_ejemplar(e):
        _limpiar_errores(_ejemplar_fields)
        dd_ubicacion.error = None; dd_estado.error = None
        has_error = False

        if not _val(tf_id_ejemplar):
            tf_id_ejemplar.error = "El ID del ejemplar es obligatorio"; has_error = True
        elif not _val(tf_id_ejemplar).isdigit():
            tf_id_ejemplar.error = "Debe ser numérico"; has_error = True
        elif existeEjemplar(int(_val(tf_id_ejemplar))):
            tf_id_ejemplar.error = "Este ID de ejemplar ya existe"; has_error = True

        if not _val(tf_isbn_ejemplar):
            tf_isbn_ejemplar.error = "El ISBN del libro es obligatorio"; has_error = True
        elif not _val(tf_isbn_ejemplar).isdigit():
            tf_isbn_ejemplar.error = "El ISBN debe contener solo números"; has_error = True
        elif not existeISBN(int(_val(tf_isbn_ejemplar))):
            tf_isbn_ejemplar.error = "No existe un libro con este ISBN"; has_error = True

        if not dd_ubicacion.value:
            dd_ubicacion.error = "Selecciona una ubicación"; has_error = True
        if not dd_estado.value:
            dd_estado.error = "Selecciona un estado"; has_error = True

        if has_error:
            page.update(); return

        ok, msg = registrar_ejemplar(
            int(_val(tf_id_ejemplar)), int(_val(tf_isbn_ejemplar)),
            dd_ubicacion.value, dd_estado.value,
        )
        if ok:
            tf_id_ejemplar.value = ""; tf_id_ejemplar.error = None
            tf_isbn_ejemplar.value = ""; tf_isbn_ejemplar.error = None
            dd_ubicacion.value = None; dd_ubicacion.error = None
            dd_estado.value = None; dd_estado.error = None
            open_succesful_dialog(page, "El ejemplar físico se ha registrado correctamente.")
        else:
            tf_id_ejemplar.error = f"Error: {msg}"; page.update()

    # ══════════════════════════════════════════════════════════════
    # CARGA INICIAL
    # ══════════════════════════════════════════════════════════════
    _refrescar_lista()

    # ══════════════════════════════════════════════════════════════
    # UI
    # ══════════════════════════════════════════════════════════════
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(value="Gestionar Libros", size=32,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Row(
                expand=True, spacing=16,
                controls=[
                    # ─── Columna de formulario ───────────────────
                    ft.Container(
                        expand=True,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=12, padding=16, bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=10, scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Text("Agregar Libro", size=16,
                                        weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                                ft.Row(
                                    spacing=16,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    controls=[
                                        ft.Column(spacing=10, expand=True, controls=[
                                            tf_isbn, tf_titulo, tf_autores, tf_editorial,
                                            tf_anio, dd_categoria, tf_descripcion,
                                            ft.Row(alignment=ft.MainAxisAlignment.START, controls=[
                                                ft.FilledButton(
                                                    content="Agregar Libro", icon=ft.Icons.ADD,
                                                    on_click=_on_agregar_libro,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.LIGHT_GREEN_600,
                                                        color=ft.Colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=10)),
                                                ),
                                            ]),
                                        ]),
                                        ft.Column(expand=True, spacing=8, controls=[
                                            ft.Text("Información para ejemplares físicos",
                                                    size=12, color=ft.Colors.BLACK,
                                                    weight=ft.FontWeight.W_600),
                                            tf_id_ejemplar, tf_isbn_ejemplar,
                                            dd_ubicacion, dd_estado,
                                            ft.Row(alignment=ft.MainAxisAlignment.START, controls=[
                                                ft.FilledButton(
                                                    content="Registrar Ejemplar", icon=ft.Icons.LIBRARY_ADD,
                                                    on_click=_on_agregar_ejemplar,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.BLUE_600,
                                                        color=ft.Colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=10)),
                                                ),
                                            ]),
                                        ]),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    # ─── Columna de lista de libros ──────────────
                    ft.Container(
                        expand=True,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=12, padding=16, bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text("Lista de libros", size=16,
                                        weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                                ft.Container(
                                    height=400,
                                    border=ft.Border.all(1, ft.Colors.GREY_300),
                                    border_radius=10, bgcolor=ft.Colors.GREY_50,
                                    padding=8,
                                    content=lista_libros_column,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


def build_admin_prestamos(page: ft.Page) -> ft.Column:
    """Layout de préstamos: lista con estados y botones Aprobar/Rechazar."""
    from database.queries import obtenerPrestamosRecientes, aprobarPrestamo, rechazarPrestamo
    from views.reusable.succesful import open_succesful_dialog, open_confirm_dialog

    lista_prestamos_col = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, tight=True)

    def _refrescar():
        prestamos = obtenerPrestamosRecientes()
        lista_prestamos_col.controls.clear()

        if not prestamos:
            lista_prestamos_col.controls.append(
                ft.Container(
                    padding=40, alignment=ft.Alignment.CENTER,
                    content=ft.Text("No hay préstamos registrados", size=14, color=ft.Colors.GREY_500),
                )
            )
            page.update()
            return

        for p in prestamos:
            # p: (idPrestamo, codigoUsuario, nombreUsuario, ejemplar, titulo,
            #     fechaPrestamo, fechaVencimiento, estadoPrestamo)
            id_prest = p[0]
            nombre_u = p[2]
            ejemplar = p[3]
            titulo = p[4]
            fecha_p = p[5].strftime("%d/%m/%Y") if hasattr(p[5], "strftime") else str(p[5])
            fecha_v = p[6].strftime("%d/%m/%Y") if hasattr(p[6], "strftime") else str(p[6])
            estado = p[7] if len(p) > 7 else "Aprobada"

            # Badge de estado
            badge_colors = {
                "En solicitud": ft.Colors.AMBER_700,
                "Aprobada": ft.Colors.GREEN_600,
                "Rechazada": ft.Colors.RED_600,
            }
            badge_color = badge_colors.get(estado, ft.Colors.GREY_600)

            botones_accion = []
            if estado == "En solicitud":
                def _make_aprobar(ip):
                    def _h(e):
                        open_confirm_dialog(
                            page,
                            titulo="Aprobar préstamo",
                            mensaje=f"¿Aprobar el préstamo #{ip}?",
                            on_confirm=lambda ev, _ip=ip: _do_aprobar(_ip),
                        )
                    return _h

                def _make_rechazar(ip):
                    def _h(e):
                        open_confirm_dialog(
                            page,
                            titulo="Rechazar préstamo",
                            mensaje=f"¿Rechazar el préstamo #{ip}?\nEl ejemplar será liberado.",
                            on_confirm=lambda ev, _ip=ip: _do_rechazar(_ip),
                        )
                    return _h

                def _do_aprobar(ip):
                    ok, _ = aprobarPrestamo(ip)
                    if ok:
                        _refrescar()
                        open_succesful_dialog(page, f"Préstamo #{ip} aprobado.")

                def _do_rechazar(ip):
                    ok, _ = rechazarPrestamo(ip)
                    if ok:
                        _refrescar()
                        open_succesful_dialog(page, f"Préstamo #{ip} rechazado. El ejemplar fue liberado.")

                botones_accion = [
                    ft.FilledButton(
                        content="Aprobar", width=100, height=32,
                        on_click=_make_aprobar(id_prest),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_600),
                        ),
                    ),
                    ft.FilledButton(
                        content="Rechazar", width=100, height=32,
                        on_click=_make_rechazar(id_prest),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_600),
                        ),
                    ),
                ]

            fila = ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=ft.Padding(12, 10, 12, 10),
                bgcolor=ft.Colors.WHITE,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=2, tight=True, expand=True,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Text(f"#{id_prest}", size=13, weight=ft.FontWeight.W_700,
                                                color=ft.Colors.BLACK),
                                        ft.Container(
                                            padding=ft.Padding(8, 2, 8, 2),
                                            border_radius=4,
                                            bgcolor=badge_color,
                                            content=ft.Text(estado, size=10, weight=ft.FontWeight.W_600,
                                                            color=ft.Colors.WHITE),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    f"{titulo}  •  Ejemplar #{ejemplar}",
                                    size=12, color=ft.Colors.GREY_800,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    f"Usuario: {nombre_u}  |  Préstamo: {fecha_p}  →  Vencimiento: {fecha_v}",
                                    size=11, color=ft.Colors.GREY_600,
                                ),
                            ],
                        ),
                        ft.Row(spacing=6, controls=botones_accion),
                    ],
                ),
            )
            lista_prestamos_col.controls.append(fila)
        page.update()

    _refrescar()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(
                value="Préstamos",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            ),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=16,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Lista de préstamos",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    icon_size=20,
                                    tooltip="Actualizar",
                                    on_click=lambda e: _refrescar(),
                                ),
                            ],
                        ),
                        ft.Container(
                            height=420,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=lista_prestamos_col,
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_devoluciones(page: ft.Page) -> ft.Column:
    """Lista de devoluciones con estados y diálogos de aprobación/rechazo."""
    from database.queries import (
        obtenerDevoluciones, aprobarDevolucion, rechazarDevolucion, calcularTarifaTardia,
    )
    from views.reusable.succesful import open_succesful_dialog

    lista_devoluciones_col = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, tight=True)

    # ── Diálogo de aprobación ────────────────────────────────────
    def _abrir_dialogo_aprobar(id_dev, titulo_libro, nombre_u, fecha_prestamo):
        tarifa = calcularTarifaTardia(fecha_prestamo)

        tf_observacion = ft.TextField(
            label="Observación (obligatoria)",
            multiline=True, min_lines=2, max_lines=4,
            dense=True, border_radius=8,
        )

        tarifa_display = ft.Container(
            padding=ft.Padding(12, 10, 12, 10),
            border_radius=10,
            bgcolor=ft.Colors.RED_50 if tarifa > 0 else ft.Colors.GREEN_50,
            border=ft.Border.all(
                1, ft.Colors.RED_300 if tarifa > 0 else ft.Colors.GREEN_300
            ),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        "Tarifa por entrega tardía" if tarifa > 0 else "Entrega a tiempo",
                        size=13, weight=ft.FontWeight.W_600,
                        color=ft.Colors.RED_800 if tarifa > 0 else ft.Colors.GREEN_800,
                    ),
                    ft.Text(
                        f"${tarifa:,.0f} COP" if tarifa > 0 else "$0 COP — Sin recargo",
                        size=22, weight=ft.FontWeight.W_700,
                        color=ft.Colors.RED_700 if tarifa > 0 else ft.Colors.GREEN_700,
                    ),
                    ft.Text(
                        f"Sanción de $10,000 por cada día de retraso después de 15 días.",
                        size=11, color=ft.Colors.GREY_600,
                    ) if tarifa > 0 else ft.Container(),
                ],
            ),
        )

        def _close(e=None):
            ref = getattr(page, "_aprobar_dev_overlay", None)
            ov = getattr(page, "overlay", None)
            if ref and ov and ref in ov:
                ov.remove(ref)
            page._aprobar_dev_overlay = None
            page.update()

        def _confirmar(e):
            obs = (tf_observacion.value or "").strip()
            if not obs:
                tf_observacion.error = "La observación es obligatoria"
                page.update()
                return
            ok, msg = aprobarDevolucion(id_dev, obs, tarifa)
            if ok:
                _close()
                _refrescar()
                open_succesful_dialog(page, f"Devolución #{id_dev} aprobada correctamente.")
            else:
                tf_observacion.error = f"Error: {msg}"
                page.update()

        modal = ft.Container(
            width=480, bgcolor=ft.Colors.WHITE, border_radius=14,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            padding=ft.Padding(24, 20, 24, 18),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=20,
                                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)),
            content=ft.Column(spacing=12, tight=True, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(f"Aprobar devolución #{id_dev}", size=16,
                            weight=ft.FontWeight.W_700, color=ft.Colors.BLACK),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_size=20, on_click=_close),
                ]),
                ft.Text(
                    f"Libro: {titulo_libro}\nUsuario: {nombre_u}",
                    size=13, color=ft.Colors.GREY_700,
                ),
                tarifa_display,
                tf_observacion,
                ft.Row(alignment=ft.MainAxisAlignment.END, spacing=8, controls=[
                    ft.OutlinedButton(
                        content="Cancelar", on_click=_close,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.FilledButton(
                        content="Aprobar devolución", on_click=_confirmar,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ]),
            ]),
        )
        _dim = 1280
        backdrop = ft.Container(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Container(
                margin=ft.Margin(0), bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                content=ft.Stack(width=_dim, height=_dim, alignment=ft.Alignment.CENTER, controls=[
                    ft.GestureDetector(content=ft.Container(width=_dim, height=_dim), on_tap=_close),
                    modal,
                ]),
            ),
        )
        _close()
        page._aprobar_dev_overlay = backdrop
        ov = getattr(page, "overlay", None)
        if ov is None:
            page.overlay = [backdrop]
        else:
            ov.append(backdrop)
        page.update()

    # ── Diálogo de rechazo ───────────────────────────────────────
    def _abrir_dialogo_rechazar(id_dev, titulo_libro, nombre_u):
        tf_observacion = ft.TextField(
            label="Observación (obligatoria)",
            multiline=True, min_lines=2, max_lines=4,
            dense=True, border_radius=8,
        )

        def _close(e=None):
            ref = getattr(page, "_rechazar_dev_overlay", None)
            ov = getattr(page, "overlay", None)
            if ref and ov and ref in ov:
                ov.remove(ref)
            page._rechazar_dev_overlay = None
            page.update()

        def _confirmar(e):
            obs = (tf_observacion.value or "").strip()
            if not obs:
                tf_observacion.error = "La observación es obligatoria"
                page.update()
                return
            ok, msg = rechazarDevolucion(id_dev, obs)
            if ok:
                _close()
                _refrescar()
                open_succesful_dialog(page, f"Devolución #{id_dev} rechazada.")
            else:
                tf_observacion.error = f"Error: {msg}"
                page.update()

        modal = ft.Container(
            width=440, bgcolor=ft.Colors.WHITE, border_radius=14,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            padding=ft.Padding(24, 20, 24, 18),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=20,
                                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                offset=ft.Offset(0, 4)),
            content=ft.Column(spacing=12, tight=True, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Text(f"Rechazar devolución #{id_dev}", size=16,
                            weight=ft.FontWeight.W_700, color=ft.Colors.BLACK),
                    ft.IconButton(icon=ft.Icons.CLOSE, icon_size=20, on_click=_close),
                ]),
                ft.Text(
                    f"Libro: {titulo_libro}\nUsuario: {nombre_u}",
                    size=13, color=ft.Colors.GREY_700,
                ),
                tf_observacion,
                ft.Row(alignment=ft.MainAxisAlignment.END, spacing=8, controls=[
                    ft.OutlinedButton(
                        content="Cancelar", on_click=_close,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                    ft.FilledButton(
                        content="Rechazar devolución", on_click=_confirmar,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_600,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    ),
                ]),
            ]),
        )
        _dim = 1280
        backdrop = ft.Container(
            expand=True, alignment=ft.Alignment.CENTER,
            content=ft.Container(
                margin=ft.Margin(0), bgcolor=ft.Colors.with_opacity(0.42, ft.Colors.BLACK),
                alignment=ft.Alignment.CENTER,
                content=ft.Stack(width=_dim, height=_dim, alignment=ft.Alignment.CENTER, controls=[
                    ft.GestureDetector(content=ft.Container(width=_dim, height=_dim), on_tap=_close),
                    modal,
                ]),
            ),
        )
        _close()
        page._rechazar_dev_overlay = backdrop
        ov = getattr(page, "overlay", None)
        if ov is None:
            page.overlay = [backdrop]
        else:
            ov.append(backdrop)
        page.update()

    # ── Refrescar lista ──────────────────────────────────────────
    def _fmt_fecha(dt_obj):
        if hasattr(dt_obj, "strftime"):
            return dt_obj.strftime("%d/%m/%Y")
        return str(dt_obj) if dt_obj else "—"

    def _refrescar():
        devoluciones = obtenerDevoluciones()
        lista_devoluciones_col.controls.clear()

        if not devoluciones:
            lista_devoluciones_col.controls.append(
                ft.Container(
                    padding=40, alignment=ft.Alignment.CENTER,
                    content=ft.Text("No hay devoluciones registradas", size=14, color=ft.Colors.GREY_500),
                )
            )
            page.update()
            return

        for d in devoluciones:
            # d: (idDevolucion, idPrestamo, observaciones, codigoUsuario,
            #     nombreUsuario, titulo, ejemplar, estadoDevolucion, tarifaCobro,
            #     fechaDevolucion, fechaPrestamo)
            id_dev = d[0]
            id_prest = d[1]
            observaciones = d[2] or ""
            nombre_u = d[4]
            titulo = d[5]
            ejemplar = d[6]
            estado = d[7] if len(d) > 7 else "Aprobada"
            tarifa = d[8] if len(d) > 8 else 0
            fecha_dev = d[9] if len(d) > 9 else None
            fecha_prest = d[10] if len(d) > 10 else None

            # Badge de estado
            badge_colors = {
                "En solicitud": ft.Colors.AMBER_700,
                "Aprobada": ft.Colors.GREEN_600,
                "Rechazada": ft.Colors.RED_600,
            }
            badge_color = badge_colors.get(estado, ft.Colors.GREY_600)

            # Info adicional para aprobadas/rechazadas
            info_extra = []
            if observaciones and estado != "En solicitud":
                info_extra.append(
                    ft.Text(
                        f"Obs: {observaciones}",
                        size=11, color=ft.Colors.GREY_600, italic=True,
                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                    )
                )
            if estado == "Aprobada" and tarifa and float(tarifa) > 0:
                info_extra.append(
                    ft.Container(
                        padding=ft.Padding(6, 2, 6, 2),
                        border_radius=4,
                        bgcolor=ft.Colors.RED_100,
                        content=ft.Text(
                            f"Tarifa: ${float(tarifa):,.0f} COP",
                            size=10, weight=ft.FontWeight.W_600,
                            color=ft.Colors.RED_700,
                        ),
                    )
                )

            # Botones según estado
            botones_accion = []
            if estado == "En solicitud":
                def _make_aprobar(idv, t, n, fp):
                    return lambda e: _abrir_dialogo_aprobar(idv, t, n, fp)

                def _make_rechazar(idv, t, n):
                    return lambda e: _abrir_dialogo_rechazar(idv, t, n)

                botones_accion = [
                    ft.FilledButton(
                        content="Aprobar", width=100, height=32,
                        on_click=_make_aprobar(id_dev, titulo, nombre_u, fecha_prest),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_600),
                        ),
                    ),
                    ft.FilledButton(
                        content="Rechazar", width=100, height=32,
                        on_click=_make_rechazar(id_dev, titulo, nombre_u),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_600),
                        ),
                    ),
                ]

            fila = ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=ft.Padding(12, 10, 12, 10),
                bgcolor=ft.Colors.WHITE,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=2, tight=True, expand=True,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Text(f"Dev. #{id_dev}", size=13, weight=ft.FontWeight.W_700,
                                                color=ft.Colors.BLACK),
                                        ft.Container(
                                            padding=ft.Padding(8, 2, 8, 2),
                                            border_radius=4,
                                            bgcolor=badge_color,
                                            content=ft.Text(estado, size=10, weight=ft.FontWeight.W_600,
                                                            color=ft.Colors.WHITE),
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    f"{titulo}  •  Ejemplar #{ejemplar}  •  Préstamo #{id_prest}",
                                    size=12, color=ft.Colors.GREY_800,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    f"Usuario: {nombre_u}  |  Solicitud: {_fmt_fecha(fecha_dev)}",
                                    size=11, color=ft.Colors.GREY_600,
                                ),
                                *info_extra,
                            ],
                        ),
                        ft.Row(spacing=6, controls=botones_accion),
                    ],
                ),
            )
            lista_devoluciones_col.controls.append(fila)
        page.update()

    _refrescar()

    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(
                value="Lista de devoluciones",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            ),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=16,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Lista de solicitudes",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    icon_size=20,
                                    tooltip="Actualizar",
                                    on_click=lambda e: _refrescar(),
                                ),
                            ],
                        ),
                        ft.Container(
                            height=420,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=lista_devoluciones_col,
                        ),
                    ],
                ),
            ),
        ],
    )


def _build_inventario_list(estado, data):
    """Genera las filas de la lista de inventario para un estado dado."""
    if not data:
        return [
            ft.Container(
                padding=40, alignment=ft.Alignment.CENTER,
                content=ft.Text(f"No hay ejemplares con estado '{estado}'", size=14,
                                color=ft.Colors.GREY_500),
            )
        ]

    badge_colors = {
        "Disponible": ft.Colors.GREEN_600,
        "Prestado": ft.Colors.ORANGE_600,
        "Perdido": ft.Colors.RED_600,
    }
    badge_color = badge_colors.get(estado, ft.Colors.GREY_600)

    rows = []
    for ej in data:
        # ej: (idEjemplar, codigoIsbn, ubicación, estado, titulo, autores)
        rows.append(
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=ft.Padding(10, 8, 10, 8),
                bgcolor=ft.Colors.WHITE,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=2, tight=True, expand=True,
                            controls=[
                                ft.Text(
                                    f"Ej. #{ej[0]}  —  {ej[4]}",
                                    size=13, weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    f"{ej[5]}  •  ISBN: {ej[1]}  •  Ubic: {ej[2]}",
                                    size=11, color=ft.Colors.GREY_600,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                        ),
                        ft.Container(
                            padding=ft.Padding(8, 2, 8, 2),
                            border_radius=4,
                            bgcolor=badge_color,
                            content=ft.Text(estado, size=10, weight=ft.FontWeight.W_600,
                                            color=ft.Colors.WHITE),
                        ),
                    ],
                ),
            )
        )
    return rows


def build_admin_disponibles(page: ft.Page) -> ft.Column:
    """Inventario Disponible: lista real desde la BD."""
    from database.queries import obtenerEjemplaresPorEstado

    data = obtenerEjemplaresPorEstado("Disponible")
    rows = _build_inventario_list("Disponible", data)

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        value="Inventario Disponible",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(
                        padding=ft.Padding(10, 4, 10, 4),
                        border_radius=6,
                        bgcolor=ft.Colors.GREEN_600,
                        content=ft.Text(f"{len(data)} ejemplares", size=12,
                                        weight=ft.FontWeight.W_700, color=ft.Colors.WHITE),
                    ),
                ],
            ),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=16,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text(
                            "Lista de ejemplares disponibles",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=ft.Column(
                                spacing=4,
                                scroll=ft.ScrollMode.AUTO,
                                tight=True,
                                controls=rows,
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_prestados(page: ft.Page) -> ft.Column:
    """Inventario Prestado: lista real desde la BD."""
    from database.queries import obtenerEjemplaresPorEstado

    data = obtenerEjemplaresPorEstado("Prestado")
    rows = _build_inventario_list("Prestado", data)

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        value="Inventario Prestado",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Container(
                        padding=ft.Padding(10, 4, 10, 4),
                        border_radius=6,
                        bgcolor=ft.Colors.ORANGE_600,
                        content=ft.Text(f"{len(data)} ejemplares", size=12,
                                        weight=ft.FontWeight.W_700, color=ft.Colors.WHITE),
                    ),
                ],
            ),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=16,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text(
                            "Lista de ejemplares prestados",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=ft.Column(
                                spacing=4,
                                scroll=ft.ScrollMode.AUTO,
                                tight=True,
                                controls=rows,
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_perdidos(page: ft.Page) -> ft.Column:
    """Inventario Perdido: lista real desde la BD con ícono de advertencia."""
    from database.queries import obtenerEjemplaresPorEstado

    data = obtenerEjemplaresPorEstado("Perdido")
    rows = _build_inventario_list("Perdido", data)

    return ft.Column(
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Text(
                                value="Inventario Perdido",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Icon(icon=ft.Icons.WARNING_AMBER_OUTLINED, size=30,
                                    color=ft.Colors.RED_600),
                        ],
                    ),
                    ft.Container(
                        padding=ft.Padding(10, 4, 10, 4),
                        border_radius=6,
                        bgcolor=ft.Colors.RED_600,
                        content=ft.Text(f"{len(data)} ejemplares", size=12,
                                        weight=ft.FontWeight.W_700, color=ft.Colors.WHITE),
                    ),
                ],
            ),
            ft.Container(
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                padding=16,
                bgcolor=ft.Colors.WHITE,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text(
                            "Lista de ejemplares perdidos",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_50,
                            padding=8,
                            content=ft.Column(
                                spacing=4,
                                scroll=ft.ScrollMode.AUTO,
                                tight=True,
                                controls=rows,
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )

