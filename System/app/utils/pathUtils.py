from pathlib import Path

def getProjectRoot() -> Path:
  return Path(__file__).resolve().parent.parent

def getImagePath(imageName: str) -> Path:
  return getProjectRoot() / "images" / imageName