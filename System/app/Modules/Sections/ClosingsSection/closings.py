import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomFloatingActionButton

class Closings(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.page = page
    self.expand = True
    
    self.closingsContainer = ft.Container(
      col={"sm": 12, "md": 6, "xl": 4},
      margin=ft.margin.symmetric(horizontal=20, vertical=20),
      expand=True,
      alignment=ft.alignment.top_left,
      border_radius=ft.border_radius.all(30),
      bgcolor=constants.WHITE,
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.START,
        expand=True,
      )
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        controls=[
          self.textForEmptyContainer("Selecciona un cierre para ver mas información")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
      ),
      col={"sm": 12, "md": 6, "xl": 8},
    )
    
    self.closingsView = ft.ResponsiveRow(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      run_spacing=10,
      controls=[
        self.closingsContainer,
        self.infoContainer,
      ]
    )
    
    self.addUserButton = CustomFloatingActionButton(
      on_click=None,
      
    )
    
    self.controls = [
      self.closingsView,
      ft.Container(
        content=self.addUserButton,
        right=10,
        bottom=10
      )
    ]
  
  def textForEmptyContainer(self, value):
    return ft.Text(
      value=value,
      color=constants.BLACK,
      size=32,
      weight=ft.FontWeight.BOLD,
      text_align=ft.TextAlign.CENTER,
    )