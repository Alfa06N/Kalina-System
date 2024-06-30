import flet as ft 

def main(page: ft.Page):
  page.title = "Custom Themed App"

  # Customized theme 
  customTheme = ft.Theme(
    color_scheme=ft.ColorScheme(
      primary="#6BAAB9",      # Azul
      on_primary="#FFFDFF",   # Blanco
      background="#353440",   # Negro
      surface="#E19E45",      # Naranja
      error="#402B19",        # Marrón oscuro
      on_background="#FFFDFF",
      on_surface="#FFFDFF",
      on_error="#FFFDFF",
    ) 
  )

  # Apply theme to the page
  page.theme = customTheme

  greeting = ft.Text("Que tal??", color="#FFFDFF")
  
  button = ft.ElevatedButton(
    "Click Me!",
    on_click=lambda e: print("Button clicked!"),
    style=ft.ButtonStyle(
      color="#FFFDFF",
      bgcolor="#6BAAB9",
      
    )
  )

  page.add(ft.Column([greeting, button], alignment=ft.MainAxisAlignment.CENTER, expand=True))

ft.app(target=main)