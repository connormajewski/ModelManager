from frontend import App, AlertWindow
import customtkinter as ctk
from ebay import check_access_token_validity, clear_inventory, refresh_access_token


if __name__ == '__main__':
    
    is_token_invalid = check_access_token_validity()
    
    if is_token_invalid:
        
        root = ctk.CTk()
        root.withdraw()
        
        refresh_access_token()
        
        alert = AlertWindow(title="Restart Needed.", label="Ebay API key is no longer valid. Please restart.", on_exit=exit)
        
        alert.mainloop()
    
    else:
        
        clear_inventory()
    
        app = App()
        app.mainloop()


