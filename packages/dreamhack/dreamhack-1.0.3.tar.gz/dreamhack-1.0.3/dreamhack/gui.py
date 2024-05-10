class gui():
  def get_tkinter_root(): #type:ignore
    import tkinter
    return tkinter.Tk()

  def tk_geometry(root, width, height): #type:ignore
    try:
      return root.geometry(f'{width}x{height}') #type:ignore
    except Exception:
      raise Exception('Invalid Root.') #type:ignore

# ----------------------------------CUSTOMTKINTER---------------------------------------
  def get_customtkinter_root(): #type:ignore
    import customtkinter #type:ignore
    return customtkinter.CTk()

  def ctk_geometry(root, width, height): #type:ignore
    try:
      return root.geometry(f'{width}x{height}') #type:ignore
    except Exception:
      raise Exception('Invalid Root.') #type:ignore