import flet as ft
from views.login_Page import login_page


def main(page: ft.Page):
    page.window.title = "BiblioGestor"
    page.window.width = 1290
    page.window.height = 680
    page.window.resizable = False
    page.window.maximizable = False
    page.window.alignment = ft.Alignment.CENTER
    page.fonts = {
        "Inter": "Inter-VariableFont_opsz,wght.ttf"
    }
    page.theme = ft.Theme(font_family="Inter")

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/":
            page.views.append(login_page(page))
        page.update()
        
    page.on_route_change = route_change
    page.route = "/"
    route_change(None)


if __name__ == "__main__":
    ft.run(main)