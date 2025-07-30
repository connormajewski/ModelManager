# Model Manager User Guide
## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Features](#features)
    - [Sorting](#sorting)
    - [Simple Search](#simple-search)
    - [Filtering](#filtering)
    - [Exporting Results](#exporting-results)
    - [Editing](#editing)
    - [Generate Ebay Listings](#generate-ebay-listings)
   
    
## Overview
ModelManager is a program, written in Python, for management of a scale model database. It includes a number of useful features that make keeping track of collections easy. These features include:
1. **Easy Sorting** - With just a couple of clicks, models can be sorted by a number of categories, including type, manufacturer, scale, price, and condition.
2. **Simple Search** - models can be searched by exact keywords, such as 'monte carlo', 'junkers', or any other set of characters.
3. **Filtering** - Results can be filtered by any of the above search categories, plus a few extra. Clicking on any of the filter buttons will sort the results in ascending order. Clicking again will sort in descending order.
4. **Exporting Results** - Once the results are displayed and filtered, they can be exported to an spreadsheet for later use. These spreadsheets included the results of the search, as well as the total estimated value, and number of models.
5. **Editing** - Models can be added, removed, or edited with just a few buttons using the **Edit Catalogue** button.
6. **Generate Ebay Listings** - Once results are loaded, clicking on any model loads the **Create Listing** window. This part of the program uses the Ebay API to automatically create live listings directly from the app. Simply add photos, dimensions, and weight of object, click **Create Listing**,and wait for confirmation. If there are no errors, a live Ebay listing for the item will now be on your account.


## Getting Started
### Installing Python
ModelManager currently runs on **Python 3.12.4**. If you do not have Python installed on your machine, you can download it from the [Python Website] (https://www.python.org/downloads/windows). Just look for **Python 3.12.4**, select the download, and follow the instructions. 

To check if Python has been successfully installed, open Command Prompt (<kbd>Win</kbd> + R, type '**cmd**', hit <kbd>Enter</kbd>), and type:

 '**python --version**'

If it works, you should see '**Python 3.12.4**' appear on the screen. If it does, then you are all set, and Command Prompt can be closed. If that does not work, try each of the following:

 '**python3 --version**'
  '**py --version**'

If neither of these work, try reinstalling, or check that installation completed without any issues.

### Connecting To Ebay API
- [ ] Need to add this section on first time Ebay API connection.
## Features
### Sorting

Sorting is done by setting the dropdown boxes on the left side of the window. Once set, select the **Search Catalogue** button in order to see the results.

<img width="1920" height="1080" alt="sorting" src="https://github.com/user-attachments/assets/f1877c39-293a-4649-a994-53dbe68f8d98" />
<img width="1920" height="1080" alt="sorting3" src="https://github.com/user-attachments/assets/d4a4b902-a295-428e-afbc-e259f99af5e9" />

### Simple Search

Using the **Keywords** textbox, models can be searched for by keywords matching their description. Again, select **Search Catalogue** to view results.

<img width="1920" height="1080" alt="search" src="https://github.com/user-attachments/assets/efc00c79-c619-4d0a-ab1d-a7602e6ee36a" />

### Filtering

Once results are loaded, they can be further filtered by using the filter buttons on the right hand side of the window. Pressing a filter button toggles between ascending and descending order, and only one filter can be applied at a time. The below photos show results filtered by value, ascending and descending.

<img width="1920" height="1080" alt="filter" src="https://github.com/user-attachments/assets/cd6d878a-1f51-4a8c-9f85-af26d5969034" />
<img width="1920" height="1080" alt="filter1" src="https://github.com/user-attachments/assets/98931db0-3b20-434a-ace2-828984fc2854" />

### Exporting Results

Results can be exported when needed for later use. Select **Export Results**, choose a file name and location, and save.

<img width="1920" height="1080" alt="export" src="https://github.com/user-attachments/assets/d65fc91a-4e95-4000-9512-dac69b11b233" />
<img width="1920" height="1080" alt="export1" src="https://github.com/user-attachments/assets/049f5a23-e148-427c-bd6c-773db69e802c" />

### Editing

Models can be updating, added, or removed by selecting **Edit Catalogue**. When updating or removing a model, its **ID** must be included. When adding a model, **ID** is not needed. In the photos below, the
price of model 102 is changed from $25.00 to $50.00. It is then deleted from the collection. If added back, it would no longer have the original ID.

<img width="1920" height="1103" alt="update" src="https://github.com/user-attachments/assets/54c63781-cc6d-46ce-a518-5c5db70d8c83" />
<img width="1920" height="1080" alt="update1" src="https://github.com/user-attachments/assets/6920a2e3-1a40-4a48-8e9e-4b74510f182c" />
<img width="1920" height="1080" alt="update2" src="https://github.com/user-attachments/assets/0d79a6b8-0462-4492-ad13-ae9297ac964d" />

### Generate Ebay Listings 

Once results are loaded, selecting any of the models that appear opens the Listing Window. Here, listing information can be added. 
*Note* - In order to create a listing, at least **one** photo must be selected, as well as item dimensions and weight. The photos below show a successfull listing for a model in the collection.

<img width="1920" height="1080" alt="ebay" src="https://github.com/user-attachments/assets/a429446e-3287-4a9a-a3d9-dcd314c94818" />
<img width="1920" height="1080" alt="ebay1" src="https://github.com/user-attachments/assets/2b63758f-3004-4977-92da-f79ffe662474" />
<img width="1920" height="1080" alt="ebay2" src="https://github.com/user-attachments/assets/7a919ab9-e072-47e4-9b87-349089ca6a86" />
<img width="1920" height="937" alt="ebay3" src="https://github.com/user-attachments/assets/f1f94382-d663-4566-835c-901dc10039e7" />
<img width="1920" height="832" alt="ebay4" src="https://github.com/user-attachments/assets/91c31247-1cbb-43ee-adfb-a29a63deb408" />




