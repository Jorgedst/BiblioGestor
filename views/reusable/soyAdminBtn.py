import flet as ft

def soyAdminBtn(page: ft.Page):
    async def irLoginAdmin(e):
        await page.push_route("/loginAdmin")
        
    return ft.Container(
        alignment=ft.Alignment.TOP_RIGHT,
        content=ft.Button(
            on_click= irLoginAdmin,
            width=150,
            margin=ft.Margin(0, 10, 0, 0),
            content="Soy Administrador",
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                },
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                },
                shape=ft.ContinuousRectangleBorder(
                    radius=10),
                mouse_cursor=ft.MouseCursor.CLICK,
                padding=ft.Padding(0),
                shadow_color=ft.Colors.TRANSPARENT,
                alignment=ft.Alignment.CENTER,
                text_style=ft.TextStyle(
                    weight=ft.FontWeight.W_400
                )
            )
        )
    )
