#Tiffany Nguyen     ID:1947724

import csv  #working with csv files
import datetime     #this will allow accessing time for later use

#initialize class for every output
class Item:
    def __init__(self, ID=000000, man_name='none', item_type='none', item_price='none', service_date='never', damage='no'):
        self.ID = ID
        self.man_name = man_name
        self.item_type = item_type
        self.item_price = item_price
        self.service_date = service_date
        self.damage = damage
# sorting methods
def sort_by_id(item):
    return item.ID
def sort_by_price(item):
    return item.item_price
def sort_by_service_date(item):
    return item.service_date
def sort_by_man_name(item):
    return item.man_name


# dictionary using ID as key
item_dict = {}  # Read data from files
# storing item types
item_type_list = []


# getting manufacturer list
with open('ManufacturerList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        # checking for damage
        damage = 'no'

        if line[3] != '':
            damage = 'yes'

        id = line[0]
        man_name = line[1]
        item_type = line[2]
        
        item_type_list.append(item_type)
        # update dict using id as key
        item_dict[id] = {}
        item_dict[id]['id'] = id
        item_dict[id]['man_name'] = man_name
        item_dict[id]['item_type'] = item_type
        item_dict[id]['damage'] = damage

# getting service dates
with open('ServiceDatesList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        id = line[0]
        date = line[1]
        # updating the s dictionary value
        item_dict[id]['service_date'] = date
# geting prices
with open('PriceList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        id = line[0]
        price = line[1]
        # updating the dictionary value
        item_dict[id]['item_price'] = float(price)

# convert the dictionary values
item_models = []
for item in item_dict.values():
    item_models.append(Item(
        ID=item['id'],
        man_name=item['man_name'],
        item_type=item['item_type'],
        item_price=item['item_price'],
        service_date=item['service_date'],
        damage=item['damage'],
    ))

# full inv section
item_models.sort(key=sort_by_man_name)

with open('FullInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')

    for item in item_models:
        writer.writerow(
            [item.ID, item.man_name, item.item_type, item.item_price, item.service_date,
             item.damage])
        
# item type lists
for item_type in item_type_list:

    items_in_type = []

    for item in item_models:
        if item.item_type == item_type:
            items_in_type.append(item)

    # sorting by ID
    items_in_type.sort(key=sort_by_id)

    # file name
    type_file = item_type.replace(" ", "") + "Inventory.csv"
    with open(type_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')

        for item in items_in_type:
            writer.writerow(
                [item.ID, item.man_name, item.item_price, item.service_date, item.damage])



past_date = []
for item in item_models:
	# checking date
    date = item.service_date.split("/")
    service_date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
    if service_date < datetime.date.today():
        past_date.append(item)

# sorting by date
past_date.sort(key=sort_by_service_date, reverse=True)

with open('PastServiceDateInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')

    for item in past_date:
        writer.writerow([item.ID, item.man_name, item.item_price, item.service_date, item.damage])


# damaged items
damaged_items = []
for item in item_models:
    if item.damage == 'yes':
        damaged_items.append(item)


damaged_items.sort(key=sort_by_price, reverse=True)

with open('DamagedInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')

    for item in damaged_items:
        writer.writerow([item.ID, item.man_name, item.item_type, item.item_price, item.service_date])

#Part 2
#store the data in a dictionary

data = {"id" : [1167234, 2347800, 2390112, 9034210, 7346234, 1009453, 3001265],

"manufacturer":["Apple", "Apple", "Dell", "Dell", "Lenovo", "Lenovo", "Samsung"],

"type" : ["phone", "laptop", "laptop", "tower", "laptop", "tower", "phone"],

"price": [534, 999, 799, 345, 239, 599, 1200],

"date": [2/1/2022, 7/3/2020, 7/2/2020, 5/27/2020, 9/1/2021, 10/1/2021, 12/1/2023],

"condition": [' ', ' ', ' ', ' ', ' ', 'damaged', ' ', ' ']}

#create while loop to ask user input
#continue prompt user input until q
while True:
    user_input = input("Enter item or q to quit: ")
    if user_input == "q":
        break
    item = ""
    types = ""
    for i in data["manufacturer"]:
        if i in user_input:
            item = i
    for i in data["type"]:
        if i in user_input:
            types = i
    if(item == "" or types == ""):                             #checking for bad input otherwise procceed to print message of item
        print("No such item in inventory")
    else:
        details = ["", "", "", 0]
        for i in range(len(data["id"])):
            if(data["manufacturer"][i] == item and data["type"][i] == types):
                if(details[3] < data["price"][i]):
                    details[0] = data["id"][i]
                    details[1] = data["manufacturer"][i]
                    details[2] = data["type"][i]
                    details[3] = data["price"][i]
        print("Your item is " + str(details[0]) + " " + str(details[1]) + " " + str(details[2]) + " " + str(details[3]))

    #create a list of other recommended items base on user manufacturer input
    consider = []
    for i in range(len(data["id"])):
        if(data["type"][i] == types and data["manufacturer"][i] != item):
            consider.append([data["id"][i], data["manufacturer"][i], data["type"][i], data["price"][i]])
    if(len(consider) != 0):
        print("You may, also, consider:")
        for i in range(len(consider)):
            print(str(consider[i][0]) + " " + consider[i][1] + " " + consider[i][2] + " " + str(consider[i][3]))