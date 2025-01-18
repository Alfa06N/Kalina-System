import flet as ft
import constants

class PaymentSearchBar(ft.SearchBar):
  def __init__(self, page, controls:list=[], on_submit=None):
    super().__init__()