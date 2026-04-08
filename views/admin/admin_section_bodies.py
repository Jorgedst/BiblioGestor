import flet as ft


def _caja_placeholder(titulo: str, alto: int) -> ft.Container:
    inner_h = max(alto - 44, 48)
    return ft.Container(
        height=alto,
        border=ft.Border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=ft.Padding(12, 12, 12, 12),
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            spacing=8,
            tight=True,
            controls=[
                ft.Text(titulo, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK),
                ft.Container(
                    height=inner_h,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=8,
                ),
            ],
        ),
    )


def build_admin_gestion_home(page: ft.Page) -> ft.Column:
    """Vista principal Gestión: paneles resumen + filtros (diseño; datos con query después)."""
    return ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(value="Gestión", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Row(
                spacing=12,
                controls=[
                    ft.Container(
                        expand=True,
                        content=_caja_placeholder("Préstamos (Activos)", 200),
                    ),
                    ft.Container(
                        expand=True,
                        content=_caja_placeholder("Préstamos (Vencidos)", 200),
                    ),
                ],
            ),
            _caja_placeholder("Usuarios con más préstamos", 160),
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
                                    controls=[
                                        ft.Text("Desde", size=12, color=ft.Colors.BLACK),
                                        ft.TextField(
                                            hint_text="dd/mm/aaaa",
                                            width=120,
                                            height=40,
                                            dense=True,
                                            border_radius=8,
                                        ),
                                        ft.Text("Hasta", size=12, color=ft.Colors.BLACK),
                                        ft.TextField(
                                            hint_text="dd/mm/aaaa",
                                            width=120,
                                            height=40,
                                            dense=True,
                                            border_radius=8,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(
                            height = 280,
                            margin = ft.Margin(0,0,0,30),
                            content=ft.Container(
                                height=20,
                                border=ft.Border.all(1, ft.Colors.GREY_400),
                                border_radius=10,
                                bgcolor=ft.Colors.GREY_100,
                            ),
                        )
                    ],
                ),
            ),
        ],
    )


def build_admin_libros(page: ft.Page) -> ft.Column:
    """Layout para gestionar libros (formulario + tabla vacía)."""
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(
                value="Gestionar Libros",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            ),
            ft.Row(
                expand=True,
                spacing=16,
                controls=[
                    # Columna de formulario
                    ft.Container(
                        expand=True,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=12,
                        padding=16,
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "Agregar Libro",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                                ft.Row(
                                    spacing=16,
                                    controls=[
                                        # Datos principales del libro
                                        ft.Column(
                                            spacing=10,
                                            expand=True,
                                            controls=[
                                                ft.TextField(label="ISBN"),
                                                ft.TextField(label="Título"),
                                                ft.TextField(label="Autor/es"),
                                                ft.TextField(label="Editorial"),
                                                ft.TextField(label="Año"),
                                                ft.TextField(label="Categoría"),
                                                ft.TextField(
                                                    label="Descripción",
                                                    multiline=True,
                                                    min_lines=2,
                                                    max_lines=4,
                                                ),
                                            ],
                                        ),
                                        # Información para ejemplares físicos
                                        ft.Column(
                                            expand=True,
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    "Información para ejemplares físicos",
                                                    size=12,
                                                    color=ft.Colors.BLACK,
                                                ),
                                                ft.TextField(label="ID ejemplar #",
                                                width = 170),
                                                ft.Dropdown(label="Ubicación", options=[]),
                                                ft.Dropdown(label="Estado", options=[]),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    # Columna de tabla
                    ft.Container(
                        expand=True,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=12,
                        padding=16,
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "Lista de libros",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.BLACK,
                                ),
                                ft.Container(
                                    height=360,
                                    border=ft.Border.all(1, ft.Colors.GREY_300),
                                    border_radius=10,
                                    bgcolor=ft.Colors.GREY_100,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )


def build_admin_prestamos(page: ft.Page) -> ft.Column:
    """Layout de préstamos: tabla + botones Aprobar / Denegar."""
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
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.FilledButton(
                                            content="Aprobar",
                                            style=ft.ButtonStyle(
                                                bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN},
                                            ),
                                        ),
                                        ft.FilledButton(
                                            content="Denegar",
                                            style=ft.ButtonStyle(
                                                bgcolor={ft.ControlState.DEFAULT: ft.Colors.RED},
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_devoluciones(page: ft.Page) -> ft.Column:
    """Lista de devoluciones con diálogo de observaciones."""

    dialog = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            width=420,
            padding=20,
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    ft.Text(
                        "Observaciones",
                        size=20,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "Escribe aquí las observaciones de la devolución.",
                        size=12,
                        color=ft.Colors.BLACK,
                    ),
                    ft.TextField(
                        multiline=True,
                        min_lines=4,
                        max_lines=6,
                        border_radius=8,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=12,
                        controls=[
                            ft.TextButton("Cancelar"),
                            ft.FilledButton(
                                "Enviar",
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.DEFAULT: ft.Colors.GREEN},
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )

    def abrir_dialog(e: ft.ControlEvent) -> None:
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Conectar handlers de botones del diálogo
    def cerrar_dialog(e: ft.ControlEvent) -> None:
        dialog.open = False
        page.update()

    dialog.actions = []
    dialog.on_dismiss = None
    # Ajustar callbacks de botones creados arriba
    # (buscar por tipo en la columna de contenido)
    botones = dialog.content.content.controls[-1].controls  # Row de botones
    botones[0].on_click = cerrar_dialog
    botones[1].on_click = cerrar_dialog

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
                        ft.Text(
                            "Lista de solicitudes",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                            padding=12,
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                "Label   Label   Label   Label   Label",
                                                color=ft.Colors.BLACK,
                                            ),
                                            ft.FilledButton(
                                                "Aprobar",
                                                on_click=abrir_dialog,
                                                style=ft.ButtonStyle(
                                                    bgcolor={
                                                        ft.ControlState.DEFAULT: ft.Colors.GREEN
                                                    },
                                                ),
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                "Label   Label   Label   Label   Label",
                                                color=ft.Colors.BLACK,
                                            ),
                                            ft.FilledButton(
                                                "Aprobar",
                                                on_click=abrir_dialog,
                                                style=ft.ButtonStyle(
                                                    bgcolor={
                                                        ft.ControlState.DEFAULT: ft.Colors.GREEN
                                                    },
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_disponibles(page: ft.Page) -> ft.Column:
    """Inventario Disponible: tabla simple."""
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(
                value="Inventario Disponible",
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
                        ft.Text(
                            "Lista",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_prestados(page: ft.Page) -> ft.Column:
    """Inventario Prestado: tabla simple."""
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text(
                value="Inventario Prestado",
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
                        ft.Text(
                            "Lista",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                        ),
                    ],
                ),
            ),
        ],
    )


def build_admin_perdidos(page: ft.Page) -> ft.Column:
    """Inventario Perdido: tabla simple con ícono de advertencia."""
    return ft.Column(
        spacing=20,
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
                    ft.Icon(icon= ft.Icons.WARNING_AMBER_OUTLINED, size=30),
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
                            "Lista",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Container(
                            height=380,
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                        ),
                    ],
                ),
            ),
        ],
    )
