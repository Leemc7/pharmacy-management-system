# -*- coding: utf-8 -*-
"""
This program is a pharmacy organizing system, it contains different options to manage products, customers and purchases.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np  
from datetime import datetime
import os

'''
This class represents Product 
'''
class Product:
    #Initializes the product with the given name, price, and barcode.
    def __init__(self, name, price, barcode):
        if price <= 0 or barcode <= 0: #The price/barcode must be a positive value. 
            raise ValueError("Price\Barcode cannot be negative or zero")
        self.name = name
        self.price = price
        self.barcode = barcode

    #Returns a user-friendly string representation of the product.
    def __str__(self):
        return f"Product: Name - {self.name}, Price - {self.price}, Barcode - {self.barcode}"

    #Returns a formal string representation of the product for debugging.
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, barcode='{self.barcode}')"
    
    #Allows searching for products by name. Returns a boolean indicating if the product name matches the query.
    def __getitem__(self, query):
        return query.lower() in self.name.lower()
    
    #Converts the product instance into a dictionary representation.
    def to_dict(self):
        return {
            'barcode': self.barcode,
            'name': self.name
        }

#Container, This class will help us manage the products, providing functionality to sort and display them.
class ProductManager:
    
    #Initializes the ProductManager with a list of products
    def __init__(self, products):
        self.products = products

    #Sorts the products based on the specified attribute ('price' or 'name').
    def sort_products(self, key, reverse=False):
        if key not in ['price', 'name']:
            raise ValueError("Invalid sort key. Choose 'price' or 'name'.")
        self.products.sort(key=lambda x: getattr(x, key), reverse=reverse)

    #Returns a string representation of all products in the list.
    def display_products(self):
        return '\n'.join(str(product) for product in self.products)
    

'''
Inherit classes of product
'''

#Represents a cosmetic product, inheriting from the Product class and adding a specific attribute for skin type.
class Cosmetics(Product):
    
    #Initializes a new Cosmetics instance.
    def __init__(self, name, price, barcode, skin_type):
        if not isinstance(skin_type, str) or not skin_type.isalpha(): #If the skin type is not a valid alphabetic string, an exception is raised, and the product is not added. 
            raise ValueError("Skin type must be an alphabetic string, product not added!")
        super().__init__(name, price, barcode)
        self.skin_type = skin_type

    #Returns a user-friendly string representation of the cosmetic product. 
    def __str__(self):
        return f"Cosmetic: {super().__str__()}, Skin Type - {self.skin_type}"

    #Returns a formal string representation of the cosmetic product for debugging purposes. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, skin_type='{self.skin_type}')"


#Represents a makeup product, inheriting from the Cosmetics class and adding a specific attribute for color. 
class Makeup(Cosmetics):
    
    #Initializes a new Makeup instance. 
    def __init__(self, name, price, barcode, skin_type, color):
        super().__init__(name, price, barcode, skin_type)
        self.color = color

    #Returns a user-friendly string representation of the makeup product. 
    def __str__(self):
        return f"Makeup: {super().__str__()}, Color - {self.color}"

    #Returns a formal string representation of the makeup product for debugging purposes. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, skin_type='{self.skin_type}', color='{self.color}')"


#Represents a skincare product, inheriting from the Cosmetics class and adding a specific attribute for ingredients. 
class SkincareProduct(Cosmetics):
    
    #Initializes a new SkincareProduct instance.
    def __init__(self, name, price, barcode, skin_type, ingredients):
        super().__init__(name, price, barcode, skin_type)
        self.ingredients = ingredients

    #Returns a user-friendly string representation of the skincare product. 
    def __str__(self):
        return f"Skincare Product: {super().__str__()}, Ingredients - {', '.join(self.ingredients)}"

    #Returns a formal string representation of the skincare product for debugging purposes. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, skin_type='{self.skin_type}', ingredients={self.ingredients})"


#Represents a medicine product, inheriting from the Product class and adding specific attributes for prescription requirements and expiry date. 
class Medicine(Product):
    
    #Initializes a new Medicine instance. 
    def __init__(self, name, price, barcode, prescription_required, expiry_date):
        super().__init__(name, price, barcode)
        self.prescription_required = prescription_required
        if not self._is_future_date(expiry_date): #Validate expiry_date as a future date
            raise ValueError("Expiry date must be a valid future date in 'YYYY-MM-DD' format")
        self.expiry_date = expiry_date

    #Validates that the provided date string represents a future date. It returns True if the date is in the future, False otherwise. 
    def _is_future_date(self, date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d') #Assuming expiry_date is in 'YYYY-MM-DD' format
            return date.date() > datetime.now().date()
        except ValueError:
            return False

    #Returns a user-friendly string representation of the medicine product. 
    def __str__(self):
        prescription = "Required" if self.prescription_required else "Not Required"
        return f"Medicine: {super().__str__()}"

    #Returns a formal string representation of the medicine product for debugging purposes. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, prescription_required={self.prescription_required})"


#Represents a medicine product that requires a prescription, inheriting from the Medicine class and adding a specific attribute for dosage. 
class WithPrescription(Medicine):
    
    #Initializes a new WithPrescription instance. 
    def __init__(self, name, price, barcode, prescription_required, expiry_date, dosage):
        super().__init__(name, price, barcode, prescription_required, expiry_date)
        self.dosage = dosage

    #Returns a user-friendly string representation of the medicine product. 
    def __str__(self):
        prescription = "Required" if self.prescription_required else "Not Required"
        return f"WithPrescription: {super().__str__()}, Prescription - {prescription}, Expiry Date - {self.expiry_date}, Dosage - {self.dosage}"

    #Returns a formal string representation of the prescription medicine product for debugging purposes. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, barcode='{self.barcode}', prescription_required={self.prescription_required}, expiry_date='{self.expiry_date}', dosage={self.dosage})"


#represents a medicine product that does not requires a prescription, inheriting from the Medicine class and adding a specific attribute for dosage. 
class Without_Prescription(Medicine):
    
    #Initializes a Without_Prescription instance. 
    def __init__(self, name, price, barcode, prescription_required, expiry_date, dosage):
        super().__init__(name, price, barcode, prescription_required, expiry_date)
        self.dosage = dosage
    
    #Returns a string representation of the Without_Prescription object. 
    def __str__(self):
        prescription = "Required" if self.prescription_required else "Not Required"
        return f"Without_Prescription: {super().__str__()}, Prescription - {prescription}, Expiry Date - {self.expiry_date}, Dosage - {self.dosage}"

    #Returns a string representation of the medicine suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, barcode='{self.barcode}', prescription_required={self.prescription_required}, expiry_date='{self.expiry_date}', dosage={self.dosage})"
   
    
# Represents a supplement product, inheriting from the Product class and adding specific attributes for active ingredients. 
class Supplement (Product):
    
    #Initializes a new instance of the Supplement class. 
    def __init__(self, name, price, barcode, active_ingredients):
        super().__init__(name, price, barcode)
        self.active_ingredients = active_ingredients
    
    #Returns a string representation of the supplement including active ingredients. 
    def __str__(self):
        return f"Supplement: {super().__str__()}, Active Ingredients - {', '.join(self.active_ingredients)}"

    #Returns a string representation of the supplement suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, active_ingredients={self.active_ingredients})"


#Represents a vitamin supplement with a specific type of vitamin, inheriting from the Supplement class and adding specific attributes for vitamin type. 
class Vitamin(Supplement):
    
    #Initializes a new instance of the Vitamin class. 
    def __init__(self, name, price, barcode, active_ingredients, vitamin_type):
        super().__init__(name, price, barcode, active_ingredients)
        self.vitamin_type = vitamin_type

    #Returns a string representation of the vitamin including its type. 
    def __str__(self):
        return f"Vitamin: {super().__str__()}, Vitamin Type - {self.vitamin_type}"

    #Returns a string representation of the vitamin suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, active_ingredients={self.active_ingredients}, vitamin_type='{self.vitamin_type}')"


#Represents a mineral supplement with a specific type of mineral, inheriting from the Supplement class and adding specific attributes for mineral type.
class Mineral(Supplement):
    
    #Initializes a new instance of the Mineral class. 
    def __init__(self, name, price, barcode, active_ingredients, mineral_type):
        super().__init__(name, price, barcode, active_ingredients)
        self.mineral_type = mineral_type

    #Returns a string representation of the mineral including its type. 
    def __str__(self):
        return f"Mineral: {super().__str__()}, Mineral Type - {self.mineral_type}"

    #Returns a string representation of the mineral suitable for debugging and logging.
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, active_ingredients={self.active_ingredients}, mineral_type='{self.mineral_type}')"


'''
New classes that are not Inherit classes of Product 
'''

#Represents a manufacturer with a name and country of origin. 
class Manufacturer:
    
    #Initializes a new instance of the Manufacturer class. 
    def __init__(self, name, country):
        self.name = name
        self.country = country

    #Returns a string representation of the manufacturer. 
    def __str__(self):
        return f"Manufacturer: Name - {self.name}, Country - {self.country}"

    #Returns a string representation of the manufacturer suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', country='{self.country}')"


#Represents a pharmaceutical company with a specific research focus, inheriting from the Manufacturer class and adding specific attributes for research focus. 
class PharmaceuticalCompany(Manufacturer):
    
    #Initializes a new instance of the PharmaceuticalCompany class. 
    def __init__(self, name, country, research_focus):
        super().__init__(name, country)
        self.research_focus = research_focus

    #Returns a string representation of the pharmaceutical company, including its research focus. 
    def __str__(self):
        return f"Pharmaceutical Company: {super().__str__()}, Research Focus - {self.research_focus}"

    #Returns a string representation of the pharmaceutical company suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', country='{self.country}', research_focus='{self.research_focus}')"


#Represents a health food company with specific certifications, inheriting from the Manufacturer class and adding specific attributes for certifications. 
class HealthFoodCompany(Manufacturer):
    
    #Initializes a new instance of the HealthFoodCompany class. 
    def __init__(self, name, country, certifications):
        super().__init__(name, country)
        self.certifications = certifications

    #Returns a string representation of the health food company, including its certifications. 
    def __str__(self):
        return f"Health Food Company: {super().__str__()}, Certifications - {', '.join(self.certifications)}"

    #Returns a string representation of the health food company suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', country='{self.country}', certifications={self.certifications})"


#Represents a cosmetics company with a specific target audience, inheriting from the Manufacturer class and adding specific attributes for target audience. 
class CosmeticsCompany(Manufacturer):
    
    #Initializes a new instance of the CosmeticsCompany class. 
    def __init__(self, name, country, target_audience):
        super().__init__(name, country)
        self.target_audience = target_audience

    #Returns a string representation of the cosmetics company, including its target audience. 
    def __str__(self):
        return f"Cosmetics Company: {super().__str__()}, Target Audience - {self.target_audience}"

    #Returns a string representation of the cosmetics company suitable for debugging and logging. 
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', country='{self.country}', target_audience='{self.target_audience}')"


#Represents a customer with personal details and a unique customer ID. 
class Customer:
    
    #Initializes a new instance of the Customer class. 
    def __init__(self, name, phone, address, customer_id):
        self.name = name
        self.phone = phone
        self.address = address
        self.customer_id = customer_id

    #Returns a string representation of the customer, including their name, phone number, address, and customer ID. 
    def __str__(self):
        return f"{self.name} | Phone: +972{self.phone} | Address: {self.address} | Customer ID: {self.customer_id}"

    #Returns a detailed string representation of the Customer instance. 
    def __repr__(self):
        return (f"Customer(name={self.name!r}, phone={self.phone!r}, "
                f"address={self.address!r}, customer_id={self.customer_id!r})")


#A utility class to generate unique customer IDs in a sequential order.
class CustomerIDGenerator:
    
    #Initializes a new instance of the CustomerIDGenerator class with the current_id set to 0. 
    def __init__(self):
        self.current_id = 0

    #Increments the current ID by 1 and returns the new unique customer ID. 
    def get_next_id(self):
        self.current_id += 1
        return self.current_id


#Represents a purchase made by a customer, including details about the product, quantity, and date of purchase. 
class Purchase:
    
    #Initializes a new instance of the Purchase class. 
    def __init__(self, customer_id, product, quantity, purchase_date):
        self.customer_id = customer_id
        self.product = product
        self.quantity = quantity
        self.purchase_date = datetime.now().strftime('%Y-%m-%d')
    
    #Converts the purchase details into a dictionary format. 
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'purchase_date': self.purchase_date
        }
    
    #Returns a string representation of the purchase, including customer ID, product details, quantity, date, and total price. 
    def __str__(self):
        return f"Customer: {self.customer_id} | Product: {self.product.barcode} | Product: {self.product.name} | Quantity: {self.quantity} | Date: {self.purchase_date} | Total price: {self.quantity*self.product.price}"

    #Returns a detailed string representation of the Purchase instance.
    def __repr__(self):
        return (f"Purchase(customer_id={self.customer_id!r}, product={self.product!r}, "
                f"quantity={self.quantity!r}, purchase_date={self.purchase_date!r})")

'''
Functions that will help with the menu
'''

#Manages a list of products, allowing for sorting and display of product details. 
class ProductManager:
    
    #Initializes a new instance of the ProductManager class. 
    def __init__(self, products):
        self.products = products

    #Sorts the list of products based on the specified key. 
    def sort_products(self, key, reverse=False):
        if key not in ['price', 'name']:
            raise ValueError("Invalid sort key. Choose 'price' or 'name'.")
        self.products.sort(key=lambda x: getattr(x, key), reverse=reverse)

    #Returns a string representation of all products in the list. 
    def display_products(self):
        if not self.products:
            return "No products available."
        return '\n'.join(str(product) for product in self.products)
 
       
#This function is for option 4 in the menu - create a Histogram showing the distribution of products by type (Cosmetics, Medicine, Supplement) in the inventory.
def generate_product_distribution_histogram(inventory):
    product_counts = {"Cosmetics": 0, "Medicine": 0, "Supplement": 0}

    for product in inventory:
        if isinstance(product, Cosmetics):
            product_counts["Cosmetics"] += 1
        elif isinstance(product, Medicine):
            product_counts["Medicine"] += 1
        elif isinstance(product, Supplement):
            product_counts["Supplement"] += 1
        else:
            print(f"Unknown product type encountered: {type(product)}")

    #Convert dictionary to pandas DataFrame
    product_counts_df = pd.DataFrame.from_dict(product_counts, orient='index', columns=['Count'])

    print("\nProduct Counts:")
    print(product_counts_df)  #Debug print to check data

    #Create a bar chart
    sns.barplot(x=product_counts_df.index, y=product_counts_df['Count'].astype(int))
    plt.xlabel('Product Type')
    plt.ylabel('Product Count')
    plt.title('Product Distribution by Type')
    plt.show()

#This function is for option 4 in the menu - create a Pie showing the distribution of products by type (Cosmetics, Medicine, Supplement) in the inventory.
def generate_product_distribution_pie(inventory):
    """
    This function generates a pie chart showing the distribution of products
    by type (Cosmetics, Medicine, Supplement) in the inventory.
    """
    product_counts = {"Cosmetics": 0, "Medicine": 0, "Supplement": 0}

    for product in inventory:
        if isinstance(product, Cosmetics):
            product_counts["Cosmetics"] += 1
        elif isinstance(product, Medicine):
            product_counts["Medicine"] += 1
        elif isinstance(product, Supplement):
            product_counts["Supplement"] += 1
        else:
            print(f"Unknown product type encountered: {type(product)}")

    #Convert potential inf values to NaN before plotting
    product_counts_df = pd.DataFrame.from_dict(product_counts, orient='index', columns=['Count']).replace([np.inf, -np.inf], np.nan)

    print("\nProduct Counts:")
    print(product_counts_df)  # Debug print to check data

    #Check for NaN values in 'Count' column
    if product_counts_df['Count'].isnull().any():
        print("Warning: NaN values found in product counts. Pie chart cannot be plotted.")
    else:
        #Check if all counts are zero
        if all(count == 0 for count in product_counts_df['Count']):
            print("\nNo data to display. Pie chart cannot be plotted.")
        else:
            #Create a pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(product_counts_df['Count'], labels=product_counts_df.index, autopct='%1.1f%%', startangle=140)
            plt.title('Product Distribution by Type')
            plt.axis('equal')  #Equal aspect ratio ensures that pie is drawn as a circle.
            plt.show()


#This function is for option 7 in the menu - remove product in the inventory by barcode  
def remove_product(self):
    try:
        barcode = int(input("\nEnter product barcode to remove: "))
        product_to_remove = None
        for product in self.inventory:
            if product.barcode == barcode:
                product_to_remove = product
                break

        if product_to_remove:
            self.inventory.remove(product_to_remove)  #Use the 'remove' method to remove the product
            print("Product removed successfully.")
        else: #The barcode dosen't exists 
            print("Product not found.")
    except ValueError: #The user didn't enter a number 
        print("Error: Please enter a valid integer for the barcode.")


#This function is for option 8 in the menu - update product in the inventory by barcode 
def update_product(self):
    try:
        barcode = input("\nEnter product barcode to update: ")
        product_to_update = None
        for product in self.inventory:
            if str(product.barcode) == barcode:  #Convert product barcode to string for comparison
                product_to_update = product
                break

        if product_to_update:
            #Update product attributes based on user input
            update_choice = input("What do you want to update? (name, price, attributes): ").lower()
            if update_choice == "name": #Update name 
                new_name = input("Enter new product name: ")
                product_to_update.name = new_name
                print("Product name updated successfully.")
            elif update_choice == "price": #Update price 
                while True:
                    try:
                        new_price = float(input("Enter new price: "))
                        break
                    except ValueError:
                        print("\nError: You didn't enter a number. Please try again.\n")
                product_to_update.price = new_price
                print("Product price updated successfully.")
            elif update_choice == "attributes": #Update attributes 
                #Update attributes based on product type
                if isinstance(product_to_update, Cosmetics):
                    #Update cosmetics 
                    if isinstance(product_to_update, Makeup):
                        new_color = input("Enter new color: ")
                        product_to_update.color = new_color
                        print("Makeup color updated successfully.")
                    elif isinstance(product_to_update, SkincareProduct):
                        new_ingredients = input("Enter new ingredients (comma-separated): ").split(",")
                        product_to_update.ingredients = new_ingredients
                        print("Skincare product ingredients updated successfully.")
                #Update medicine 
                elif isinstance(product_to_update, Medicine):
                    if isinstance(product_to_update, WithPrescription):
                        new_dosage = input("Enter new dosage: ")
                        product_to_update.dosage = new_dosage
                        print("Prescription medicine details updated successfully.")
                    elif isinstance(product_to_update, Without_Prescription):
                        new_dosage = input("Enter new dosage: ")
                        product_to_update.dosage = new_dosage
                        print("Non-prescription medicine details updated successfully.")
                #Update supplement 
                elif isinstance(product_to_update, Supplement):
                    if isinstance(product_to_update, Vitamin):
                        new_vitamin_type = input("Enter new vitamin type: ")
                        product_to_update.vitamin_type = new_vitamin_type
                        print("Vitamin type updated successfully.")
                    elif isinstance(product_to_update, Mineral):
                        new_mineral_type = input("Enter new mineral type: ")
                        product_to_update.mineral_type = new_mineral_type
                        print("Mineral type updated successfully.")
                else:
                    print("Invalid product type.")
            else:
                print("Invalid update choice.")
        else:
            print(f"Product with barcode {barcode} not found.")  # Debug print
    except Exception as e:
        print(f"Error updating product: {e}")


#This 4 functions are for option 9 in the menu - save all data on a file, convert objects to files 
def cosmetics_to_json(cosmetics):
  #Convert Cosmetics attributes to JSON-compatible representation
  return {
      "Cosmetics: "
      "Barcode-": cosmetics.barcode,
      "Name-": cosmetics.name,
      "Price-": cosmetics.price,
      "Skin_type-": cosmetics.skin_type,
  }

def medicine_to_json(medicine):
  #Convert Medicine attributes to JSON-compatible representation
  return {
      "Medicine: "
      "Barcode-": medicine.barcode,
      "Name-": medicine.name,
      "Price-": medicine.price,
      "Prescription_required-": medicine.prescription_required,
      "expiry date-": medicine.expiry_date
  }

def supplement_to_json(supplement):
  #Convert Supplement attributes to JSON-compatible representation
  return {
      "Supplement: "
      "Barcode-": supplement.barcode,
      "Name-": supplement.name,
      "Price-": supplement.price,
      "Active_ingredients-": supplement.active_ingredients,
  }

def product_to_json(product):
  # This function handles converting all product types
  if isinstance(product, Cosmetics):
    return cosmetics_to_json(product)
  elif isinstance(product, Medicine):
    return medicine_to_json(product)
  elif isinstance(product, Supplement):
    return supplement_to_json(product)
  else:
    raise TypeError(f"Unsupported product type: {type(product)}")


'''
This class represents a Container class to hold objects of different types
'''

class Inventory:
    def __init__(self):
        self.inventory = []
        self.customers = []
        self.purchases = []
        self.products = []
        self.product_manager = ProductManager(self.products)  #Initialize with ProductManager
        self.id_generator = CustomerIDGenerator()  #Initialize CustomerIDGenerator here

    #Search for products in inventory by barcode and returnes a list of products with matching barcode, beacuse barcode is unique it will return one item to each barcode. 
    def __getitem__(self, barcode):
        matching_products = []
        for product in self.inventory:
            if product.barcode == barcode:
                matching_products.append(product)
        return matching_products
    
    #Creates a list of products 
    def list_products(self):
        return [str(item["product"]) for item in self.products]

    #Sort the list by expiration
    def list_products_by_expiration(self):
        sorted_products = sorted(self.products, key=lambda x: x["product"].expiration_date)
        return [str(item["product"]) for item in sorted_products]

    #Search for products in inventory by barcode and sets new values 
    def __setitem__(self, index, value):
        self.inventory[index] = value

    #Search for products in inventory by barcode and deletes 
    def __delitem__(self, index):
       del self.inventory[index]

    #Adds new products by menu. 
    def add_product(self):
      try:
          while True:
              print("\nWelcome to the pharmecy organization system.\nThis system collects all the data of the products that are in the pharmecy.\n")
              print("\n=====Your option menu:=====")
              print("\n1. Cosmetics")
              print("2. Medicine")
              print("3. Supplement")

              choice2 = input("\nEnter your choice: ")

              #Add product 
              if choice2 == "1":
                  product_type = "cosmetics"
                  break 
              
              elif choice2 == "2":
                  product_type = "medicine"
                  break 
              
              elif choice2 == "3":
                  product_type = "supplement"
                  break 
              
              else: 
                  print("Invalid choice!")

          name = input("Enter product name: ")
          while True:
              try:
                  price = float(input("Enter product price: "))
                  break
              except ValueError:
                  print("\nError: You didn't enter a number. Please try again.\n")

          while True:
              try:
                  barcode = int(input("Enter product barcode: "))
                  break
              except ValueError:
                  print("\nError: You didn't enter a number. Please try again.\n")

          #uses the function "check_barcode_exists" for the deletion of duplicate barcodes 
          if self.check_barcode_exists(barcode):
              raise ValueError("Barcode already exists")

          #Handle different product types
          if product_type == "cosmetics":
              skin_type = input("Enter skin type: ")
              cosmetic_type = input("Choose cosmetic type (makeup, skincare): ").lower()
              if cosmetic_type == "makeup":
                  color = input("Enter the product color: ")
                  product = Makeup(name, price, barcode, skin_type, color)
              elif cosmetic_type == "skincare":
                  ingredients = input("Enter ingredients (comma-separated): ").split(",")
                  product = SkincareProduct(name, price, barcode, skin_type, ingredients)
              else:
                  raise ValueError("Invalid cosmetic type")
           
          elif product_type == "medicine":
              expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
              while True:
                  prescription_required = input("Is prescription required (yes/no): ").lower()
                  if prescription_required in ("yes"):
                      dosage = input("Enter dosage: ")
                      product = WithPrescription(name, price, barcode, prescription_required, expiry_date, dosage)
                      break
                  elif prescription_required in ("no"):
                      dosage = input("Enter dosage: ")
                      product = WithPrescription(name, price, barcode, prescription_required, expiry_date, dosage)
                      break
                  else:
                      print("\nError: Please enter 'yes' or 'no'.\n")

          else:  #Supplement
              active_ingredients = input("Enter active ingredients (comma-separated): ").split(",")
              supplement_type = input("Enter supplement type (vitamins, minerals): ").lower()
              if supplement_type == "vitamins":
                  vitamin_type = input("Enter vitamin type: ")
                  product = Vitamin(name, price, barcode, active_ingredients, vitamin_type)
              elif supplement_type == "minerals":
                  mineral_type = input("Enter mineral type: ")
                  product = Mineral(name, price, barcode, active_ingredients, mineral_type)
              else:
                  raise ValueError("Invalid supplement type")

          #Add manufacturer details
          manufacturer_name = input("Enter manufacturer name: ")
          country = input("Enter manufacturer country: ")
          while True:
              manufacturer_type = input("Choose manufacturer type (PharmaceuticalCompany, HealthFoodCompany, CosmeticsCompany): ").lower()
              if manufacturer_type in ("pharmaceuticalcompany", "healthfoodcompany", "cosmeticscompany"):
                  break
              else:
                  print("\nError: Invalid manufacturer type. Please try again.\n")

          #Create manufacturer based on type
          if manufacturer_type == "pharmaceuticalcompany":
              research_focus = input("Enter research focus: ")
              manufacturer = PharmaceuticalCompany(manufacturer_name, country, research_focus)
          elif manufacturer_type == "healthfoodcompany":
              certifications = input("Enter certifications (comma-separated): ").split(",")
              manufacturer = HealthFoodCompany(manufacturer_name, country, certifications)
          else:  #CosmeticsCompany
              target_audience = input("Enter target audience: ")
              manufacturer = CosmeticsCompany(manufacturer_name, country, target_audience)

          product.manufacturer = manufacturer  #Assign the manufacturer object, not just the name

          #Add product to inventory and product manager
          self.inventory.append(product)
          print("\nProduct added successfully!")
          self.product_manager.products.append(product)

      except ValueError as e:
          print(f"Error: {e}")


    #Check if the barcode entered already exists, This algorithm helps prevent duplicates of barcodes, the barcodes are unique
    def check_barcode_exists(self, barcode):
        for product in self.inventory:
            if product.barcode == barcode:
                return True
        return False

    #Prints the inventory, products
    def print_products(self):
        if not self.inventory:
            print("Inventory is empty!")
        else:
            for product in self.inventory:
                print(product)
    
    #Prints the inventory, customers
    def print_customers(self):
        if not self.customers:
            print("No customers found!")
        else:
            print("Customer List:")
            for customer in self.customers:
                print(customer)
    
    #Counts products by type 
    def count_by_type(self, product_type):

        # Convert input product_type to title case to match class names
        product_type = product_type.title()
    
        # Check if the product type is valid
        valid_product_types = ["Cosmetics", "Medicine", "Supplement"]
        if product_type not in valid_product_types:
            print(f"Invalid product type: {product_type}")
            return
    
        # Define a function to check if a product is of the specified type
        def is_product_of_type(product):
            return isinstance(product, globals().get(product_type))
    
        # Use filter to select products of the specified type
        filtered_products = filter(is_product_of_type, self.inventory)
    
        # Count the number of filtered products
        count = len(list(filtered_products))
    
        print(f"Number of {product_type} products:", count)


    #Sort the products by barcode.
    def sort_products(self, key='price', reverse=False):
        if key == 'price':
            self.products.sort(key=lambda p: p.price, reverse=reverse)
        elif key == 'name':
            self.products.sort(key=lambda p: p.name, reverse=reverse)
        else:
            print("Invalid sort key. Use 'price' or 'name'.")
            
    #Container, manages customer data, product inventory, and purchase records for a pharmacy system. 
    class CustomerManager:
        
       #Initializes a new instance of the CustomerManager class. 
       def __init__(self):
          self.customers = []
          self.inventory = []  #Assuming you have a list of products
          self.purchases = []
          self.id_generator = CustomerIDGenerator()

    #Prompts the user to input details for a new customer and adds the customer to the customer list. 
    def add_customer(self):
        try:
            name = input("Enter customer name: ")
            while True:
                try:
                    phone = int(input("Enter customer phone number (with the 0 at the begining, must be 10 letters long): "))
                    if len(str(phone)) == 9: #Check for 10 digits, for Isreali numbers 
                        break
                except ValueError:
                    print("You didn't enter a valid phone number.")
            address = input("Enter customer address: ")
            customer_id = self.id_generator.get_next_id() #Generate a unique customer ID 
            customer = Customer(name, phone, address, customer_id) #Create a new Customer object 
            self.customers.append(customer) #Add the new customer to the list
            print("\nCustomer added successfully!")
            print (customer)
            
        except Exception as e:
            print(f"Error adding customer: {e}")


    #Add purchase to the system 
    def add_purchase(self):
        try:
            #Get and verify customer ID
            customer_id = input("Enter customer ID: ")
            try:
                customer_id = int(customer_id)  #Convert to int
            except ValueError:
                print("Invalid customer ID format. It should be a number.")
                return

            customer = next((c for c in self.customers if c.customer_id == customer_id), None)
            if not customer:
                print("Customer not found.")
                print("Available customer IDs:", [c.customer_id for c in self.customers])
                return

            #Get and verify product barcode
            barcode = input("Enter product barcode: ")
            try:
                barcode = int(barcode)
            except ValueError:
                print("Invalid barcode format. It should be a number.")
                return

            product = next((p for p in self.inventory if p.barcode == barcode), None)
            if not product:
                print("Product not found.")
                print("Available product barcodes:", [p.barcode for p in self.inventory])
                return

            #Get and verify quantity
            while True:
                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                    else:
                        break
                except ValueError:
                    print("You didn't enter a valid number. Please try again.")

            #Record the purchase date
            purchase_date = datetime.now().strftime('%Y-%m-%d')

            #Create and add the purchase object
            purchase = Purchase(customer, product, quantity, purchase_date)
            self.purchases.append(purchase)
            print("\nPurchase added successfully!")

        except Exception as e:
            print(f"Error adding purchase: {e}")
            
            
    #List all purchases
    def list_purchases(self):
        if not self.purchases:
            print("No purchases found.")
        else:
            for purchase in self.purchases:
                print(purchase)

    
    #Saves the products data to a file.
    def save_inventory_to_file(self, filename):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, f"{filename}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                for product in self.inventory:
                    f.write(f"{product}\n")
            print(f"Inventory saved successfully to {file_path}")
        except Exception as e:
            print(f"Error saving inventory: {e}")

    #Saves the purchases data to a file.
    def save_purcheses_to_file(self, filename):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop, f"{filename}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                for purchase in self.purchases:
                    f.write(f"{purchase}\n")
            print(f"Purchases saved successfully to {file_path}")
        except Exception as e:
            print(f"Error saving purchases: {e}")
    
    #This function is for option 3 in the menu, it prints the names of all the objects in the system using map 
    def print_name(self, obj):
       print(obj.name)

    def print_all_names(self):
       print("\nProduct Names:")
       if not self.inventory:
          print("No products in the system.")
       else:
          # Use map to print all product names
          list(map(self.print_name, self.inventory))
       print("\nCustomer Names:")
       if not self.customers:
          print("No customers in the system.")
       else:
          # Use map to print all customer names
          list(map(self.print_name, self.customers))
       
     # Method to view all manufacturers in the system
    def view_all_manufacturers(self):
        if not self.inventory:
            print("No products in the inventory, so there are no manufacturers in the system.")
            return
        manufacturers = map(lambda product: product.manufacturer, self.inventory)
        print("\n==== Manufacturer Details ====")
        for manufacturer in manufacturers:
            print(manufacturer) 
            
            
    #The main menu 
    def main_menu(self):
        while True:
            print("\nWelcome to the pharmecy organization system.\nThis system collects all the data of the products that are in the pharmecy.\n")
            print("\n=====Your option menu=====")
            print("\n1. Add Product")
            print("2. Print Inventory")
            print("3. Print the names of all products and customers")
            print("4. Print all manufacturers")
            print("5. Create a Histogram")
            print("6. Create a Pie")
            print("7. Count Products by Type")
            print("8. Search Product")
            print("9. Remove product")
            print("10. Update product")
            print("11. Add Customer")
            print("12. Add Purchase")
            print("13. List All Purchases")
            print("14. Sort Products by price or name")
            print("15. Save all the product data on a file")
            print("16. Save all the purchases data on a file")
            print("17. Exit")

            choice = input("\nEnter your choice: ")

            #Add product 
            if choice == "1":
                self.add_product()
            
            #Print the inventory, only product and customer objects beacuse purcheses is depends on them it will not be in this option. 
            elif choice == "2":
                
                print("Please enter which objects you want to print:")
                print("1.products")
                print("2.customers")
                
                choice = input("\nEnter your choice (1/2): ").strip()
                if choice == "1":
                    self.print_products() #Prints the product class objects 
                elif choice == "2":
                    self.print_customers() #Prints the customer class objects 
                else:
                    print("You didn't enter a valid choice!")
            
            #Prints the names of all of the objects 
            elif choice == "3":
                self.print_all_names()
            
            #Prints all the manufacturers that are on the system 
            elif choice == "4":
                self.view_all_manufacturers()
                
            #Create a Histogram 
            elif choice == "5":
                generate_product_distribution_histogram(self.inventory)
            
            #Create a Pie 
            elif choice=="6":
                generate_product_distribution_pie(self.inventory)
            
            #Count products by type and print 
            elif choice == "7":

                 print("\n===== Product Type Menu =====")
                 print("1. Cosmetics")
                 print("2. Medicine")
                 print("3. Supplement")
    
                 choice = input("\nEnter your choice (1/2/3): ").strip()
    
                 product_type_map = {
                     "1": "cosmetics",
                     "2": "medicine",
                     "3": "supplement"
                  }
    
                 if choice in product_type_map:
                    product_type = product_type_map[choice]
                    self.count_by_type(product_type)
                 else:
                     print("Invalid choice! Please enter 1, 2, or 3.")

            #Search product and print details 
            elif choice == "8":
                try:
                    barcode = int(input("\nEnter product barcode to search: "))
                    results = self.__getitem__(barcode)
                    if results:
                        for product in results:
                            print(product)
                    else:
                        print("No products found.")
                except ValueError:
                    print("Error: Please enter a valid integer for the barcode.")
            
            #Remove product (find product and remove from inventory)
            elif choice == "9" :
                remove_product(self) 
            
            #Update product (find product and update attributes)
            elif choice == "10":
                update_product(self)
            
            #Add a customer 
            elif choice == "11":
                self.add_customer()
            
            #Add a purchase
            elif choice == "12":
                self.add_purchase()
            
            #list all the putchases 
            elif choice == "13":
                self.list_purchases()
            
            #Sort products by price or name 
            elif choice == "14":
                if not self.product_manager.products: #Check if there are products to sort 
                    print("No products to sort.")
                    continue

                sort_key = input("Sort by 'price' or 'name': ").strip().lower() #Prompt the user for the sorting key 
                if sort_key not in ['price', 'name']:
                    print("Invalid sort key. Please choose 'price' or 'name'.")
                    continue

                order = input("Ascending (a) or Descending (d): ").strip().lower() #Prompt the user for the sorting order 
                if order not in ['a', 'd']:
                    print("Invalid order. Please choose 'a' for ascending or 'd' for descending.")
                    continue

                reverse = True if order == 'd' else False #Determine the reverse flag based on user input 

                try:
                    self.product_manager.sort_products(key=sort_key, reverse=reverse) #Perform the sorting 
                    print("Sorted Products:\n" + self.product_manager.display_products()) #Display the sorted products 
                except Exception as e: #Handle any exceptions during the sorting process 
                    print(f"Error sorting products: {e}")
            
            #Saves products list to file 
            elif choice == "15":
                filename = input("\nEnter filename to save products list: ")
                self.save_inventory_to_file(filename)
            
            #Saves purchases list to file 
            elif choice == "16":
                filename = input("\nEnter filename to save purchases list: ")
                self.save_purcheses_to_file(filename)
                
            #Stop the loop of the menu 
            elif choice == "17":
                print("Exiting...")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 17.")

#This runs the main menu 
if __name__ == "__main__":
  inventory = Inventory()
  inventory.main_menu()