"Frontend of database application."

from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
import customtkinter as ctk
from openpyxl import Workbook
import backend
from natsort import natsorted
from ebay import create_test_listing, clear_inventory

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, master, width, height):
        
        self.set_height = 30

        super().__init__(master)

        font = self.master.body_font

        valuesdict = {
            "Any": "Any",
            "$0-$10": [0.00,10.00],
            "$10-$25": [10.00,25.00],
            "$25-$50": [25.00,50.00],
            "$50-$100": [50.00,100.00],
            "$100-$500": [100.00,500.00],
            "$500-$1000": [500.00,1000.00]
            }

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.configure(width=width, height=height)    

        # Manufacturer Textbox

        manufacturer_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Manufacturer",
            font=font
        )

        manufacturer_menu_textbox.grid(
            row=1
        )

        manufacturer_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=self.set_height,  
            values = ["Any"] + sorted([model_type[0] for model_type in list(backend.distinct_column_values("manufacturer"))])
        )
        
        manufacturer_menu.set("Any")

        manufacturer_menu.grid(
            row=2,
        )

        # Scale Menu

        scale_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Scale",
            font=font
        )

        scale_menu_textbox.grid(
            row=4
        )

        scale_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=self.set_height,
            values = ["Any"] + natsorted([model_type[0] for model_type in list(backend.distinct_column_values("scale"))])
        )

        scale_menu.grid(
            row=5,
        )

        # Value Menu

        value_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Value",
            font=font
        )

        value_menu_textbox.grid(
            row=6
        )

        value_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=self.set_height,
            values=["Any", "$0-$10", "$10-$25", "$25-$50", "$50-$100", "$100-$500", "$500-$1000"]
        )

        value_menu.grid(
            row=7,
        )

        # Condition Menu

        condition_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Condition",
            font=font
        )

        condition_menu_textbox.grid(
            row=8,
        )

        condition_menu = ctk.CTkComboBox(
            self,
            width=width,
            values = natsorted([model_type[0] for model_type in list(backend.distinct_column_values("condition"))] + ["Any"])
        )

        condition_menu.set("Any")

        condition_menu.grid(
            row=9,
            
        )
        
         # Type Textbox

        type_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Type",
            font=font
        )

        type_menu_textbox.grid(
            row=10
        )

        type_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=self.set_height,
            values = ["Any"] + [model_type[0] for model_type in list(backend.distinct_column_values("model_type"))]
        )

        type_menu.grid(
            row=11,
        )
        
        # Location Textbox

        location_menu_textbox = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Location",
            font=font
        )

        location_menu_textbox.grid(
            row=12
        )

        location_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=self.set_height,  
            values =  ["Any"] + natsorted([model_type[0] for model_type in list(backend.distinct_column_values("location"))])
        )

        location_menu.grid(
            row=13,
            pady=(0,10)
        )
        
        # Description Entry
        
        description_menu = ctk.CTkLabel(
            self,
            height=self.set_height,
            width=width,
            text="Keywords",
            font=font
        )

        description_menu.grid(
            row=14,
            pady=(0,0)
        )
        
        description_menu_textbox = ctk.CTkEntry(
            self,
            height=self.set_height,
            width=width,
            placeholder_text="Keywords",
            font=font
        )

        description_menu_textbox.grid(
            row=15,
            pady=(10,10)
        )

        # Search Button

        self.search_button = ctk.CTkButton(
            self,
            text="Search Catalogue",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            command=lambda: self.search_request(
                manufacturer_menu.get(),
                scale_menu.get(),
                valuesdict[value_menu.get()],
                condition_menu.get(),
                type_menu.get(),
                location_menu.get(),
                description_menu_textbox.get()
                )
        )

        self.search_button.grid(
            row=16,
        )

        # Export Button

        self.export_button = ctk.CTkButton(
            self,
            text="Export Results",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            state="disabled",
            command=lambda: self.export_results()
        )

        self.export_button.grid(
            row=17,
            pady=(10,0)
        )

        # Edit Button

        self.edit_button = ctk.CTkButton(
            self,
            text="Edit Catalogue",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            command=lambda: self.edit_catalogue()
        )

        self.edit_button.grid(
            row=18,
            pady=(10,0)
        )
        
        # Results Textbox
        
        self.total_results_textbox = ctk.CTkLabel(self, text=f"{len(self.master.queryresults)} results", font=(None, 24))
        self.total_results_textbox.grid(
            row = 20,
            pady=(10,0),
        )
        
        self.estimate_results_textbox = ctk.CTkLabel(self, text=f"Estimated Value: \n$0.00", font=(None, 24))
        self.estimate_results_textbox.grid(
            row = 21,
            pady=(10,0),
        )
        
        

    def sum_cost(self):
        
        total = 0.00
        
        for result in self.master.queryresults:
            
            cost = result[10]
            
            total += cost

        return total

    def search_request(self, *args):

        "Construct search query to be passed to execute_query()."

        attributes=["manufacturer", "scale", "estimate", "condition", "model_type", "location", "keyword"]

        arguments={}

        for attribute in attributes:
            arguments[attribute] = None

        arguments["min"] = 0
        arguments["max"] = 1000

        for i in range(len(args)):
            if(len(args[i]) != 0 and args[i] != "Any"):

                arguments[attributes[i]] = args[i]

        search_query=(
            "SELECT * FROM models \nWHERE quantity BETWEEN "
            f"{arguments['min']} AND {arguments['max']}"
        )

        for key in arguments:
            if arguments[key] is not None:
                if key == "estimate":
                    search_query = (
                        search_query +
                        f"\nAND {key} BETWEEN {arguments[key][0]} AND {arguments[key][1]}"
                    )

                elif key == 'keyword':
                    search_query = (
                    
                        search_query + f"\nAND description LIKE '%{arguments[key]}%'\nOR make LIKE '%{arguments[key]}%'"
                    
                    )

                else:

                    if key != "min" and key != 'max':

                        search_query = search_query + f"\nAND {key}='{arguments[key]}'"

        print(search_query)

        results = backend.execute_query(search_query)

        self.master.queryresults = results

        self.master.main_window.display_query(self.master.queryresults)
        
        results_length = len(self.master.queryresults)
        
        self.total_results_textbox.configure(text=f"{results_length} {'result' if results_length == 1 else 'results'}")
        self.estimate_results_textbox.configure(text=f"Estimated Value: \n${self.sum_cost():.2f}")

        if results_length > 0:
            self.export_button.configure(state="enabled")
        else:
            self.export_button.configure(state="disabled")

    def export_results(self):

        query_value = self.sum_cost()

        saveFile = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[("Excel - *.xlsx", "*.xlsx")]
        )

        if saveFile is None:
            return

        work_book = Workbook()

        work_sheet = work_book.active

        work_sheet.append([
            'ID',
            'TYPE',
            'MANUFACTURER',
            'MAKE',
            'DESCRIPTION',
            'YEAR',
            'SCALE',
            'CONDITION',
            'QUANTITY',
            'LOCATION',
            'VALUE',
            '',
            'TOTAL VALUE'
        ])

        for result in self.master.queryresults:

            work_sheet.append(result)
            
        total_value_cell = 'L2'
        total_results_cell = 'L3'

        work_sheet[total_value_cell] = f"${query_value:.2f}"
        work_sheet[total_results_cell] = f"{len(self.master.queryresults)} results"

        work_book.save(saveFile)

    def edit_catalogue(self):

        edit_window = EditWindow(self)

        self.edit_button.configure(state='disabled')
        self.search_button.configure(state='disabled')
        self.export_button.configure(state='disabled')
        
    def open_map(self):
        
        map_window = MapWindow(self)

class EditWindow(ctk.CTkToplevel) :

    "Secondary window for editing database entries."

    def __init__(self,master):
        
        self.attribute_list_id_index = 0
        self.attribute_list_manufacturer_index = 1
        self.attribute_list_make_index = 2
        self.attribute_list_description_index = 3
        self.attribute_list_year_index = 4
        self.attribute_list_scale_index = 5
        self.attribute_list_quantity_index = 6
        self.attribute_list_location_index = 7
        self.attribute_list_estimated_index = 8

        super().__init__(master)

        self.attribute = ([
            "ID",
            "Manufacturer",
            "Make",
            "Description",
            "Year",
            "Scale",
            "Quantity",
            "Location",
            "Estimated Value"
        ])

        self.attribute_list = []

        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=18
        )

        width=300
        height=600

        self.title('Edit Catalogue')
        self.geometry(f'{width}x{height}')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.attributes('-topmost', True)

        self.resizable(False, False)

        for i in range(len(self.attribute)):

            self.attribute_textbox = ctk.CTkEntry(
                self,
                placeholder_text=f'{self.attribute[i]}',
                width=width,
                height=30,
            )

            self.attribute_textbox.grid(
                column=0,
                row=i,
                pady=(0,10)
            )

            self.attribute_list.append(self.attribute_textbox)
            
        self.model_type_textbox = ctk.CTkLabel(
        
            self,
            text="Model Type",
            height = 30
        
        )
        
        self.model_type_textbox.grid(
        
            column=0,
            row = 10
        
        )

        self.model_type_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["car", "plane", "helicopter", "rocket", "ship", "balloon", "army", "truck", "submarine", "figurine", "motorcycle", "slotcar", "miscellaneous", "tank"]
        )

        self.model_type_menu.grid(
            column=0,
            row=10,
        )

        self.condition_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["opened", "sealed"]
        )

        self.condition_menu.grid(
            column=0,
            row=11,
        )

        self.attribute_list.append(self.model_type_menu)
        self.attribute_list.append(self.condition_menu)

        self.add_button = ctk.CTkButton(
            self,
            text="Add Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command=lambda: self.add(              
            )
        )

        self.add_button.grid(
            column=0,
            row=12,
            pady=(10,0)
        )
        
        
        

        self.update_button = ctk.CTkButton(
            self,
            text="Update Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command=lambda: self.update(
            )
        )

        self.update_button.grid(
            column=0,
            row=13,
            pady=(10,0)
        )

        self.delete_button = ctk.CTkButton(
            self,
            text="Delete Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command = lambda: self.delete(self.attribute_list[0].get())
        )

        self.delete_button.grid(
            column=0,
            row=14,
            pady=(10,0)
        )

        self.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):

        "Toggle sidebar buttons and destroy window on close."

        self.master.edit_button.configure(state='enabled')
        self.master.search_button.configure(state='enabled')
        self.master.export_button.configure(state='enabled')

        self.destroy()
        
    # Wrapper function for backend.update_model, so that alert box can be created on success. Didn't want
    # to have to be calling frontend functions in backend if i didn't have to.
        
    def update(self):
        
        # Wanted to do an enum but currently on Python 3.12 not 3.4. Also didn't want a bunch
        # of magic numbers for attribute array so I did this. More readable, I think, at cost of more lines.
        

        
        status = backend.update_model(
                self.attribute_list[self.attribute_list_id_index].get(),
                self.model_type_menu.get(),
                self.attribute_list[self.attribute_list_manufacturer_index].get(),
                self.attribute_list[self.attribute_list_make_index].get(),
                self.attribute_list[self.attribute_list_description_index].get(),
                self.attribute_list[self.attribute_list_year_index].get(),
                self.attribute_list[self.attribute_list_scale_index].get(),
                self.condition_menu.get(),
                self.attribute_list[self.attribute_list_quantity_index].get(),
                self.attribute_list[self.attribute_list_location_index].get(),
                self.attribute_list[self.attribute_list_estimated_index].get(),
            )
            
        if status is not None:
            
            AlertWindow("Sucess", "Update Successful.")
            
        else:
            
            AlertWindow("Failure", "Update Failed.")

            
    def delete(
        self,
        model_id,
    ):
        
        status = backend.delete_model(
                model_id
            )
            
        if status is not None:
            
            AlertWindow("Success", "Deletion Successful.")
            
        else:
            
            AlertWindow("Failure", "Deletion Failed.")
            
            
    def add(self):
        
        status = backend.add_model(
                self.attribute_list[self.attribute_list_id_index].get(),
                self.model_type_menu.get(),
                self.attribute_list[self.attribute_list_manufacturer_index].get(),
                self.attribute_list[self.attribute_list_make_index].get(),
                self.attribute_list[self.attribute_list_description_index].get(),
                self.attribute_list[self.attribute_list_year_index].get(),
                self.attribute_list[self.attribute_list_scale_index].get(),
                self.condition_menu.get(),
                self.attribute_list[self.attribute_list_quantity_index].get(),
                self.attribute_list[self.attribute_list_location_index].get(),
                self.attribute_list[self.attribute_list_estimated_index].get(),
            )
            
        if status is not None:
            
            AlertWindow("Success", "Model Added Successful.")
            
        else:
            
            AlertWindow("Failure", "Model Failed To Be Added To Database.")
        
class AlertWindow():
    
    def __init__(self, title, label):
        
        alert = ctk.CTkToplevel()
        alert.geometry(f"300x150")
        alert.attributes("-topmost", True)
        alert.title(title)
        
        label = ctk.CTkLabel(alert, text=f"{label}", wraplength=275)
        label.pack(pady=20)
        
        ok_button = ctk.CTkButton(alert, text="OK", command=alert.destroy)
        ok_button.pack(pady=10)
        
        alert.grab_set()

class MainWindow(ctk.CTkScrollableFrame):

    "Window class to display and filter query results."

    def __init__(self, master, width, height):

        "Set needed variables as well as preloaded buttons and text."

        super().__init__(master)

        self.master = master
        
        self.page_number = 1
        
        self.maxresults = 22

        # This is displayed query results. This is GUI component, NOT actual database results.

        self.models = []
        
        self.filters = []

        self.configure(width=width, height=height)

        # Main Window text and buttons are loaded on init,
        # rather than reloaded each time display_query() is called.

        label = ctk.CTkLabel(
            self,
            text=f"{'ID' :>5} {'TYPE' :<16} {'MANUFACTURER'  :<16} {'DESCRIPTION' :<26} {'YEAR' :<6} {'SCALE' :<8} {'CONDITION' :<10} {'LOCATION' :<20} {'VALUE' :>8}", font=("Courier", 14, "bold"))

        label.grid(row=1, column=0, pady=(0,5), sticky="w")

        # This would make more sense as a dictionary.

        attrs = ["Id", "Type", "Manufacturer", "Scale", "Condition", "Location", "Value"]
        index = [0, 1, 2, 6, 7, 9, 10]
        # Loop to initialize and place filter buttons next to results.

        for i in range(len(attrs)):

            self.filter_button = ctk.CTkButton(
                self,
                text=attrs[i],
                width=100,
                fg_color="#4ab1ff",
                hover_color="#286b9e",
                command=lambda i=i : self.filter_results(
                    self.master.queryresults, i, index[i] 
                )
            )
            
            self.filter_button.toggle = 0

            self.filter_button.grid(
                column=11,
                row=i+1,
                pady=(10,0),
                padx=(20,0)
            )
            
            self.filters.append(self.filter_button)
            
            # Results Page Buttons
        
            self.page_button_frame = ctk.CTkFrame(self, width=100)
            self.page_button_frame.grid(row=8, column=11, pady=(10, 0))

            self.page_decrement = ctk.CTkButton(self.page_button_frame, text="<", font=(None, 18, "bold"), width=20)
            self.page_decrement.pack(side="left", padx=(20, 10))
            
            self.page_label = ctk.CTkLabel(self.page_button_frame, text="", font=(None, 14))
            self.page_label.pack(side="left", padx=(0,10))

            self.page_increment = ctk.CTkButton(self.page_button_frame, text=">", font=(None, 18, "bold"), width=20)
            self.page_increment.pack(side="right")
           
            
            self.page_decrement.bind("<Button-1>", lambda event, value=-1: self.set_page(value))
            self.page_increment.bind("<Button-1>", lambda event, value=1: self.set_page(value))

    def display_query(self, queryresults, page_number=1) -> list:

        "Given a returned query from execute_query(), display to MainWindow object."

        # Max number of models to be shown when displaying results.
        # Loading in all results to GUI slows down program considerably. If user wants to view all results, can export to file and view.

        self.page_number = page_number

        #maxresults = 22

        # Current display must be destroyed before results can be shown.

        if len(self.models) > 0:
            for i in range(len(self.models)):
                self.models[i].destroy()

        # Display results up to maxresults to reduce loading time.
        # Append to models[] to allow for destruction on next display_query() call.
        
        x = (page_number - 1) * self.maxresults + 1
        y = (page_number - 1) * self.maxresults + self.maxresults + 1
        
        print(f"{self.page_number}: {x} : {y} :: {y-x+1}")
        
        row_index = 2

        for j in range(x, y if y < len(queryresults) + 1 else len(queryresults) + 1):#len(queryresults)+1):
            
            i = j - 1

            label = ctk.CTkLabel(self, text=f"{str(queryresults[i][0]) + ':' : >5} {queryresults[i][1] : <16} {queryresults[i][2][:16] : <16} {queryresults[i][4][:24] :<26} {queryresults[i][5] if queryresults[i][5] is not None else '    ' : <6} {queryresults[i][6] : <8} {queryresults[i][7] : <10} {queryresults[i][9] : <20} {queryresults[i][10] : >8.2f}", font=("Courier", 14, "normal"))

            label.model_id = queryresults[i][0]

            self.models.append(label)
            
            label.bind("<Enter>", lambda event, temp_label=label: temp_label.configure(fg_color="#4ab1ff"))
            label.bind("<Leave>", lambda event, temp_label=label: temp_label.configure(font=("Courier", 14, "normal"), fg_color="transparent"))
            
            label.bind("<Button-1>", lambda event, model_id=label.model_id: self.create_listing_window(model_id))

            label.grid(row=row_index, column=0, pady=(0,5), sticky="w")
            
            row_index += 1
            
        self.page_label.configure(text=f"{self.page_number} / {int(len(queryresults) / self.maxresults + 1)}")

    # Function to filter and change ordering of App.queryresults.

    def filter_results(self, results, attr, index):

        "Reorder stored results from given input and button state."      

        toggle = self.filters[attr].toggle
        
        for button in self.filters:
            
            if button != self.filters[attr]:
                
                button.configure(fg_color="#4ab1ff")
        
            else:
                
                self.filters[attr].configure(fg_color="#286b9e")

        results = natsorted(results, key=lambda x: x[index])

        if toggle == 1:

            results = list(reversed(results)) 

        self.filters[attr].toggle ^= 1

        self.master.queryresults  = results

        self.display_query(self.master.queryresults, self.page_number)
        
        self.configure()
        
    def create_listing_window(self, model_id):
        
        search_query = f"SELECT * FROM models WHERE id is {model_id}"
        
        sell_window = SellWindow(self.master, backend.execute_query(search_query)[0])
        
    def set_page(self, value):
        
        if value > 0 and self.page_number < len(self.master.queryresults) / self.maxresults:
            
            self.page_number += value
            
            self.display_query(self.master.queryresults, self.page_number)
        
        elif value < 0 and self.page_number > 1:
            
            self.page_number += value
            
            self.display_query(self.master.queryresults, self.page_number)
        
        
        
        

class SellWindow(ctk.CTkToplevel):
    
    class Model():
        
        def __init__(self, model_title, model_sku, model_type, model_manufacturer, model_scale, model_condition, model_price, model_quantity):
            
            self.model_title = model_title
            self.model_sku = model_sku
            self.model_type = model_type
            self.model_manufacturer = model_manufacturer
            self.model_scale = model_scale
            self.model_condition = model_condition
            self.model_price = model_price
            self.model_quantity = model_quantity
            self.model_dimensions = ()
            self.model_weight = 0.00
    
    def __init__(self, master, model_attributes):
        
        super().__init__(master)
        
        print("\n\n\n")
        print(self.master)
        print("\n\n\n")
        
        
        width = 500
        height = 750
        
        self.image_urls = []

        "Construct layout for window as well as needed variables."
        
        model_id = model_attributes[0]
        model_type = model_attributes[1]
        model_manufacturer = model_attributes[2]
        model_make = model_attributes[3]
        model_desc = model_attributes[4]
        model_year = model_attributes[5]
        model_scale = model_attributes[6]
        model_condition = model_attributes[7]
        model_quantity = model_attributes[8]
        model_price = model_attributes[10]
        
        model_title = f"{model_manufacturer} {model_make if model_make is not None and model_make != "None" else ""} {model_desc} {model_year if model_year is not None else ""} kit. {model_scale} Model".title()
        
        model_sku = f"model_id_{model_id}"
        
        self.model_object = self.Model(model_title, model_sku, model_type, model_manufacturer, model_scale, model_condition, model_price, model_quantity)
        
        attributes = {"Brand" : model_manufacturer, "Scale" : model_scale, "Subject" : model_make, "Condition" : model_condition, "Price" : model_price}
                
        # Title, desription, brand, scale, type, imageURLS. Plus button to list or cancel.
        
        self.model_label = ctk.CTkLabel(
            self, 
            text=model_title, font=("Courier", 24, "bold"),
            wraplength=width - 50,
            justify="left",
            anchor="w"
            )
            
        self.model_label.grid(pady=10,padx=10,
            column=0,
            sticky="w")
        
        for key, value in attributes.items():
            
            if value is not None and value != "None":
            
                self.attribute_label = ctk.CTkLabel(
                    self,
                    text = f"{key} : {value}" if key !="Price" else f"{key} : ${value}",
                    wraplength = width - 50,
                    font = ("Courier", 18),
                    justify="left",
                    anchor="w"
                )
                
                #self.attribute_label.grid(pady=10, sticky="w", column=0, padx=10)
                self.attribute_label.grid(sticky="w", column=0, padx=10)
                
                
        dimensions_label = ctk.CTkLabel(self, text="Dimensions (in & lb)", font=("Courier", 24, "bold"))        
        dimensions_label.grid(sticky="w", column=0, padx=10, pady=(10,0))        
                
        w = 75       
                
        self.length_textbox = ctk.CTkEntry(
            self,
            height=30,
            width=w,
            placeholder_text="Length",
            font=("Courier", 12),
        )

        r = 7

        self.length_textbox.grid(
            #pady=(10,10)
            row=r,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )
        
        self.width_textbox = ctk.CTkEntry(
            self,
            height=30,
            width=w,
            placeholder_text="Width",
            font=("Courier", 12),
        )

        self.width_textbox.grid(
            #pady=(10,10)
            row=r,
            column=0,
            sticky="w",
            padx=95,
            pady=10
        )
        
        self.height_textbox = ctk.CTkEntry(
            self,
            height=30,
            width=w,
            placeholder_text="Height",
            font=("Courier", 12),
        )

        self.height_textbox.grid(
            #pady=(10,10)
            row=r,
            column=0,
            sticky="w",
            padx=180,
            pady=10
            
        )
        
        self.weight_textbox = ctk.CTkEntry(
            self,
            height=30,
            width=w,
            placeholder_text="Weight",
            font=("Courier", 12),
        )

        self.weight_textbox.grid(
            #pady=(10,10)
            row=r,
            column=0,
            sticky="w",
            padx=265,
            pady=10
        )
            
        self.select_images_button = ctk.CTkButton(
            self,
            text="Select Photos",
            width=width-50,
            fg_color="#4ab1ff",
            font=("Helvetica",18),
            
            command=lambda: self.select_photos()
        )

        self.select_images_button.grid(
            
            pady=(10),
            padx=20,
            sticky="w"
            
        )
        
        self.image_frame = ctk.CTkScrollableFrame(self,width=width-50, height=50)  # Frame to hold labels
        self.image_frame.grid(pady=10, sticky="w", padx=10)
        
        self.create_listing_button = ctk.CTkButton(
            self,
            text="Create Listing",
            width=width-50,
            fg_color="#4ab1ff",
            font=("Helvetica",18),
            
            command=lambda: self.call_create_test_listing(self.image_urls, self.model_object)
        )

        self.create_listing_button.grid(
            
            pady=(10),
            padx=20,
            sticky="w"
            
        )
        
        self.cancel_button = ctk.CTkButton(
            self,
            text="Cancel",
            width=width-50,
            fg_color="#4ab1ff",
            font=("Helvetica",18),
            
            command=lambda: self.destroy()
        )

        self.cancel_button.grid(
            
            pady=(10),
            padx=20,
            sticky="w"
            
        )
        
        self.title('Create Ebay Listing')
        self.geometry(f'{width}x{height}')

        self.attributes('-topmost', True)

        self.resizable(False, False)
        
    def select_photos(self):
        
        images = askopenfilenames(title="Choose images for listing", parent=self) # show an "Open" dialog box and return the path to the selected file

        self.image_urls = []
        
        image_counter = 1
        
        for image in images:
            
            self.image_urls.append(image)
            
            image_counter += 1
            
        print(self.image_urls)
        
        if self.image_urls:
            
            for widget in self.image_frame.winfo_children():
                widget.destroy()

            # Add a label for each selected image
            for path in self.image_urls:
                lbl = ctk.CTkLabel(self.image_frame, text=path, anchor="w", wraplength=450)
                lbl.pack(anchor="w", padx=10, pady=2)

    def call_create_test_listing(self, image_urls, model_object):
        
        """
            TODO:
            
            Maybe implement custom return values for create_test_listing to narrow down errors for user.    
            
            Possible Errors:
            
                - Listing already exists
                - No photos selected
                - Dimensions incorrect
                
        """
        
        model_object.model_dimensions = (float(self.length_textbox.get()), float(self.width_textbox.get()), float(self.height_textbox.get()))
        
        model_object.model_weight  = float(self.weight_textbox.get())
        
        response = create_test_listing(self.image_urls, model_object)
        
        print(f"\n\n\nTRESPONSE: {response}\n\n\n")
        
        if response is not None:
            
            alert = AlertWindow(title="Sucess", label="Listing was successfully added. Check Ebay account for full listing info.")
            
        else:
            
            alert = AlertWindow(title="Failure", label="Listing could not be created.")
        

class App(ctk.CTk):

    "Main App class. Program is contained within this class."

    def __init__(self):

        super().__init__()

        AppWidth=1920
        AppHeight=1080


        # Stores results of database query to be filtered/exported.

        self.queryresults = []

        #backend.create_table(backend.creation_query)

        ctk.set_appearance_mode('dark')
        self.title('Model Car Catalogue')
        self.geometry(f'{AppWidth}x{AppHeight}-0-0')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Appearance variables to be used by all children objects.

        self.title_font = ctk.CTkFont(
            family="Arial",
            size=40,
            weight='bold'
        )

        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=18
        )

        self.body_font = ctk.CTkFont(
            family="Helvetica",
            size=18
        )

        self.button_color = "#4ab1ff"
        self.button_hover_color = "#286b9e"

        # Sidebar object for querying.

        self.sidebar = Sidebar(self, 250, 600)
        self.sidebar.grid(
            column=0,
            row=0,
            padx=(10, 5),
            pady=10,
            sticky="ns"
        )

        # Main Window object to display results of query.

        self.main_window = MainWindow(
            self,
            AppWidth - self.sidebar.width,
            AppHeight - self.sidebar.height - 200
        )

        self.main_window.grid(
            column=1,
            row=0,
            padx=(5, 10),
            pady=10,
            sticky="nsew"
        )