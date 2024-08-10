class MyCustomError(Exception):
  pass

class DataNotFoundError(MyCustomError):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)