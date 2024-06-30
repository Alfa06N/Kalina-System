import flet as ft

def main(page: ft.Page):
  # Create SVG control
  path = "ks-logo_only-cup_sin-color.svg"
  svgControl = ft.Image(resource=path, width=100, height=100)

  # Create column
  # column = ft.Column(controls=[svgControl], alignment="center")
  page.add(svgControl)
  # You've hit your usage limit. Please try again later.

ft.app(target=main)