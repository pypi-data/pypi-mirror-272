class RegistryEditor():
  WINDOWS = True
  try:
    import winreg
  except Exception:
    WINDOWS = False

  class Hives():
    import os
    import platform
    if platform.system() ==  'Windows':
      import winreg
    else:
      import unixreg as winreg #type:ignore
    HKCU = winreg.HKEY_CURRENT_USER #type:ignore
    HKLM = winreg.HKEY_LOCAL_MACHINE #type:ignore
    HKCR = winreg.HKEY_CLASSES_ROOT #type:ignore
    HKU = winreg.HKEY_USERS #type:ignore
    HKCC = winreg.HKEY_CURRENT_CONFIG #type:ignore

  class RegistryPath():
    def __init__(self, hive, folders_list):
      self.hive = hive
      self.folders_list = folders_list
      self.path = ""

    def build(self):
      self.path =""
      x = 0
      for folder in self.folders_list:
        slash = r"\\"
        if x == len(self.folders_list) - 1:
          slash = ""
        self.path = self.path + folder + slash
        x = x + 1
      return self.path

  @staticmethod
  def set(key_path_class, value_name, value, ALL_ACCESS=False):
    import platform
    if platform.system() ==  'Windows':
      import winreg
    else:
      import unixreg as winreg #type:ignore
    if type(value) is int: #type:ignore
      value_type = winreg.REG_DWORD #type:ignore
    else:
      value_type = winreg.REG_SZ #type:ignore
      try:
        value = str(value)
      except Exception:
        raise Exception('Invalid value') #type:ignore
    try:
      value_name = str(value_name)
    except ValueError:
      raise ValueError(f"Invalid value name, must be a string.") #type:ignore
    open_mode = winreg.KEY_WRITE #type:ignore
    if ALL_ACCESS:
      open_mode = winreg.KEY_ALL_ACCESS #type:ignore

    try:
      key = winreg.OpenKey(key_path_class.hive, key_path_class.path,0, open_mode) #type:ignore
    except FileNotFoundError:
        try:
          key = winreg.CreateKey(key_path_class.hive, key_path_class.path) #type:ignore
        except Exception as err:
          raise Exception(f"Error Creating Registry Key: {err}") #type:ignore
    except Exception as e:
      raise Exception(f"Error Opening Registry Key: {e}") #type:ignore

    try:
      winreg.SetValueEx(key, value_name, 0, value_type, value) #type:ignore
      winreg.CloseKey(key) #type:ignore
    except OSError:
      raise OSError("Please run this program as administrator.") #type:ignore
    except Exception as e:
      raise Exception(f"Error setting {str(value_name)} value: {e}") #type:ignore
    else:
      return value



