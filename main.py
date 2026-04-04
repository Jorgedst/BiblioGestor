import flet as ft
from views.login_Page import login_page
from views.register_Page import register_Page
from views.userDashboard_Page import dashBoardPage

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
        elif page.route == "/register":
            page.views.append(register_Page(page))
        elif page.route == "/userDashboard":
            page.views.append(dashBoardPage(page))

        page.update()
    page.on_route_change = route_change
    #Pa probal
    #page.route = "/register"
    route_change(None)


if __name__ == "__main__":
    ft.run(main)