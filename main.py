from frontend import App
from ebay import check_access_token_validity


if __name__ == '__main__':
    
    check_access_token_validity()
    
    app = App()
    app.mainloop()


