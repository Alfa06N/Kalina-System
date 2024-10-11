import flet as ft
import constants
from Modules.customControls import CustomAnimatedContainerSwitcher, CustomNavigationOptions, CustomAnimatedContainer, CustomFloatingActionButton, CustomGridView
from Modules.clients_module import ClientForm

class Clients(ft.Stack):
  def __init__(self, page):
    super().__init__()
    self.expand = True
    self.page = page
    
    self.clientsContainer = CustomAnimatedContainerSwitcher(
      shadow=ft.BoxShadow(
        spread_radius=1,
        blur_radius=5,
        color=constants.BLACK_INK,
      ),
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="There's nothing to show you here in clients.",
            color=constants.BLACK,
            size=32,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
          )
        ]
      ),
      height=None,
      width=None,
      expand=True,
      col={"sm": 12, "md": 9, "lg": 4, "xl": 5}
    )
    
    self.infoContainer = CustomAnimatedContainerSwitcher(
      content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          self.textForEmptyContainer(message="Selecciona un cliente para ver más información.")
        ]  
      ),
      expand=True,
      col={"sm": 12, "md": 12, "lg": 8, "xl": 7}
    )
    
    self.addClientButton = CustomFloatingActionButton(
      on_click=self.addClientForm,
    )
    
    self.controls = [
      ft.ResponsiveRow(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=10,
        controls=[
          self.clientsContainer,
          self.infoContainer,
        ]
      ),
      ft.Container(
        content=self.addClientButton,
        right=10,
        bottom=10,
      )
    ]
  
  def textForEmptyContainer(self, message):
    return ft.Text(
      value=message,
      size=32,
      color=constants.BLACK,
      weight=ft.FontWeight.W_700,
      text_align=ft.TextAlign.CENTER,
    )
  
  def addClientForm(self, e):
    if not self.infoContainer.height >= 500:
      self.infoContainer.changeStyle(
        height=500, width=700, shadow=ft.BoxShadow(
          blur_radius=5,
          spread_radius=1,
          color=constants.BLACK_INK,
        )
      )
    
    self.infoContainer.setNewContent(
      newContent=ClientForm(
        page=self.page,
        mainContainer=self,
      )
    )
  
  def resetInfoContainer(self):
    try:
      if not self.infoContainer.height == 150:
        self.infoContainer.changeStyle(height=150, width=300, shadow=None)
      self.infoContainer.setNewContent(
        newContent=ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.textForEmptyContainer(message="Selecciona un cliente para ver más información.")
          ]  
        )
      )
    except Exception as err:
      raise
  
  def resetAll(self):
    try:
      self.resetInfoContainer()
      # Here goes more logic for clientsContainer
    except:
      raise