import flet as ft
from Modules.customControls import CustomOperationContainer, CustomTextField, CustomFilledButton, CustomImageContainer
from config import getDB
import constants
from utils.pathUtils import getImagePath

class AboutUs(ft.Container):
  def __init__(self, page):
    super().__init__()
    self.page = page
    
    self.margin = ft.margin.symmetric(horizontal=5, vertical=15)
    self.padding = ft.padding.all(5)
    self.expand=True
    self.bgcolor = ft.Colors.TRANSPARENT
    self.border_radius = ft.border_radius.all(30)
    
    self.img = getImagePath("aboutUs2.jpg")
    
    self.imageComponent = ft.Container(
      content=ft.Image(
        src=self.img,
        fit=ft.ImageFit.CONTAIN,
        height=450,
        border_radius=ft.border_radius.all(20),
      ),
      shadow=ft.BoxShadow(
        color=constants.BLACK_GRAY,
        blur_radius=10,
        spread_radius=0,
        offset=ft.Offset(0, 5),  
      ),
      border_radius=ft.border_radius.all(20)
    )
    
    self.essence = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        self.getTitle("Nuestra Esencia"),
        self.getParagraph(constants.aboutUs["essence"])
      ]
    )
    
    self.mission = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        self.getTitle("Nuestra Misión"),
        self.getParagraph(constants.aboutUs["mission"])
      ]
    )
    
    self.vision = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      controls=[
        self.getTitle("Nuestra Visión"),
        self.getParagraph(constants.aboutUs["vision"])
      ]
    )
    
    self.content = ft.Row(
      expand=True,
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Column(
          expand=1,
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            self.imageComponent,
          ]
        ),
        ft.Column(
          expand=2,
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          spacing=30,
          controls=[
            self.essence,
            self.mission, 
            self.vision,
          ]
        )
      ]
    )
    
  def getTitle(self, text: str):
    return ft.Row(
      alignment=ft.MainAxisAlignment.CENTER,
      vertical_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text(
          value=text,
          size=32,
          color=constants.BLACK,
          weight=ft.FontWeight.W_700,
          text_align=ft.TextAlign.CENTER,
        )
      ]
    )
  
  def getParagraph(self, text: str):
    return ft.Text(
      value=text,
      size=18,
      color=constants.BLACK,
      text_align=ft.TextAlign.CENTER,
    )