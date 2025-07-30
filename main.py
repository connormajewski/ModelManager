from frontend import App
from ebay import check_access_token_validity, clear_inventory


if __name__ == '__main__':
    
    check_access_token_validity()
    clear_inventory()
    
    app = App()
    app.mainloop()


