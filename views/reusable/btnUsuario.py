import flet as ft


def btnUsuario(page: ft.Page):
    async def ir_user_dashboard(e):
        await page.push_route("/")

    return ft.Container(
        alignment=ft.Alignment.TOP_RIGHT,
        content=ft.Button(
            on_click=ir_user_dashboard,
            width=120,
            margin=ft.Margin(0, 10, 0, 0),
            content="Usuario",
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: ft.Colors.WHITE},
                bgcolor={ft.ControlState.DEFAULT: ft.Colors.BLACK},
                shape=ft.ContinuousRectangleBorder(radius=10),
                mouse_cursor=ft.MouseCursor.CLICK,
                padding=ft.Padding(0),
                shadow_color=ft.Colors.TRANSPARENT,
                alignment=ft.Alignment.CENTER,
                text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            ),
        ),
    )
