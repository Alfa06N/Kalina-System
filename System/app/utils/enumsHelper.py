from DataBase.models import MethodEnum

def getMethodEnum(methodStr: str):
  for method in MethodEnum:
    if method.value == methodStr:
      return method