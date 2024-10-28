class MyCustomError(Exception):
  pass

class DataNotFoundError(MyCustomError):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
    
class DataAlreadyExists(MyCustomError):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
    
class InvalidData(MyCustomError):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
    
class ErrorOperation(MyCustomError):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)