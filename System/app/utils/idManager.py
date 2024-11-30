def getId(item):
  if hasattr(item, "idProduct"):
    return item.idProduct
  elif hasattr(item, "idCombo"):
    return item.idCombo
  else:
    raise ValueError("El objeto no tiene un identificador válido")