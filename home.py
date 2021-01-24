from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import re
import tkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.scrolledtext
import json
from datetime import date
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import csv
from csv import writer

def createOrder():
    homeFrame.place_forget()
    CreateOrderFrame.pack()


def viewOrders():
    print("View Orders Pressed")
    homeFrame.place_forget()
    ordersFrame.pack()

def returnHome():
    print("Return home")
    CreateOrderFrame.pack_forget()
    ordersFrame.pack_forget()
    homeFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

def SaveOrdertoDB():
    ordernum.set(enterordernum.get())
    shippingname.set(ShipNameEntry.get())
    billingname.set(enterbillname.get())
    billingemail.set(enterbillemail.get())
    shippingaddress.set(addressentry.get())
    city.set(cityentry.get())
    email.set(emailentry.get())
    phonenum.set(phonenumentry.get())

    prods = []
    for item in AllEntries:
        prods.append(str(item.get()))

    quanties = []
    for quant in AllQuantities:
        quanties.append(str(quant.get()))


    OrderDict["OrderNumber"] = ordernum.get()
    OrderDict["BillingName"] = enterbillname.get()
    OrderDict["BillingEmail"] = billingemail.get()

    OrderDict["ShippingName"] =shippingname.get()
    OrderDict["Address"] = shippingaddress.get()
    OrderDict["City"] = city.get()
    OrderDict["ShippingEmail"] = email.get()
    OrderDict["PhoneNumber"] =phonenum.get()
    OrderDict['Date'] = str(date.today())
    OrderDict["Product"] = prods
    OrderDict["Quantities"] = quanties



    AllOrders = {}

    with open('data.json', 'r') as fp:
        AllOrders = json.load(fp)

    if ordernum.get() not in AllOrders.keys():
        AllOrders[ordernum.get()] = OrderDict

    with open('data.json', 'w') as fp:
        json.dump(AllOrders, fp)

    print("Order Dict")
    print(OrderDict)
    print("ALL ORDERS")
    print(AllOrders)

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    total = 0
    layer  = 340
    name = ""
    for prod, quant in zip(prods, quanties):
        for product in ProductObjList:
            if(product.name == prod):
                total = total + (int(quant) * float(product.price))
                name = product.name
                print(total)
        can.drawString(115, layer, name)
        can.drawString(380, layer, quant)
        can.drawString(415, layer, "$" + str(int(quant) * float(product.price)) + "0")
        layer = layer +15



    tax = total * .05
    shipping = "$11.50"
    subtotal = total



    can.drawString(450, 759, ordernum.get())
    ###Draw Billing Info
    can.drawString(125, 550, billingemail.get())
    can.drawString(125, 565, enterbillname.get())

    ###Draw Shipping Info
    can.drawString(310, 580, shippingname.get())
    can.drawString(310, 565, shippingname.get())
    can.drawString(310, 550, city.get())
    can.drawString(310, 535, "New Zealand")
    can.drawString(310, 520, phonenum.get())
    can.drawString(310, 505, email.get())

    ###Draw Subtotal total Shipping
    can.drawString(400, 190, "$" + str(total) + "0")
    can.drawString(400, 150, "$" + str(tax) + "0")
    can.drawString(400, 165, str(shipping))
    #can.drawString(400, 180, couponammount)
    can.drawString(400, 110, str(total + tax + 11.5))

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("testpdf.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(ordernum.get() + ".pdf", "wb")
    output.write(outputStream)
    outputStream.close()


def importText():
   text = textPad.get(1.0, END)

   OrderInfo = text.splitlines()

   billingname.set(OrderInfo[12])

   numeric_filter = filter(str.isdigit, OrderInfo[1])
   numeric_string = "".join(numeric_filter)
   ordernum.set(numeric_string)

   billingemail.set(OrderInfo[14])
   shippingname.set(OrderInfo[18])
   shippingaddress.set(OrderInfo[20])
   city.set(OrderInfo[21])
   phonenum.set(OrderInfo[23])
   email.set(OrderInfo[22])



def FinalizeOrder():
    print("All the names stuff needs to go here")
    print("And be saved to database")

def ProductDelete():
    print(AllDelete)
    print(AllQuantities)
    print(AllEntries)
    print(count)
    n = (len(AllEntries)-1)
    AllEntries[n].grid_forget()
    AllQuantities[n].grid_forget()
    AllDelete[n].grid_forget()
    AllPrices[n].grid_forget()
    del AllEntries[n]
    del AllQuantities[n]
    del AllDelete[n]
    del AllPrices[n]


def AddToOrder():
    AddToOrderButton.forget()
    AddToOrderButton.grid(row =0, column=2)
    entrytext = tk.StringVar()
    entrytext.set(ProductSelect.get())

    entryquantity = tk.StringVar()
    entryquantity.set(QuantitySelect.get())

    pricetext = tk.StringVar()

    for prod in ProductObjList:
        if(prod.name == ProductSelect.get()):
            pricetext.set(str("${0:.2f}".format(float(prod.price) * int((QuantitySelect.get())))))
            print(prod.name)

    global count
    DeleteButton = tkinter.Button(ProductInputFrame, text="Delete", highlightbackground='#3E4149', command=ProductDelete)
    quantityEnt = Entry(ProductInputFrame, width = 3, textvariable= entryquantity)
    productEnt = Entry(ProductInputFrame, textvariable = entrytext)
    PriceEntry = Entry(ProductInputFrame, width=7, textvariable = pricetext)

    productEnt.grid(row = count, column =0)
    quantityEnt.grid(row = count, column =1)
    DeleteButton.grid(row = count, column = 3)
    PriceEntry.grid(row = count, column =2)
    AllEntries.append(productEnt)
    AllQuantities.append(quantityEnt)
    AllDelete.append(DeleteButton)
    AllPrices.append(PriceEntry)
    count = count + 1

def DisplayOrders():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    DictKeys = []
    for item in data.keys():
        DictKeys.append(item)
    print(DictKeys)
    print("Printing all orders")

    #### Read all order info from dictionary and display

    x=0
    print(data)
    for OrderNumber in DictKeys:
        print(OrderNumber)
        print(data[OrderNumber]['ShippingName'])
        viewOrderName = tk.StringVar()
        viewDate = tk.StringVar()
        ViewDateSent = tk.StringVar()
        ViewProducts = tk.StringVar()
        ViewOrderNumber = tk.StringVar()
        LabelVar = IntVar()
        if(data[OrderNumber]['ShippingLabel'] == 1):
            LabelVar.set(1)

        ViewOrderNumber.set(data[OrderNumber]['OrderNumber'])
        viewOrderName.set(data[OrderNumber]['ShippingName'])
        viewDate.set(data[OrderNumber]['Date'])
        ViewDateSent.set(data[OrderNumber]['ShippingDate'])

        ViewOrderNameEntry = Entry(OrdersInfoLabelsFrame, text = viewOrderName)
        ViewDateEntry = Entry(OrdersInfoLabelsFrame, width=10, text = viewDate)
        ViewDateSentEntry = Entry(OrdersInfoLabelsFrame, width=10, text = ViewDateSent)
        ViewOrderNumberEntry = Entry(OrdersInfoLabelsFrame, width = 10, text = ViewOrderNumber)
        LabelCheckButton = Checkbutton (OrdersInfoLabelsFrame, variable = LabelVar)

        ViewOrderNameEntry.grid(row=x+1, column=2)
        ViewDateEntry.grid(row=x+1,column=0)
        ViewDateSentEntry.grid(row=x+1, column=1)
        ViewOrderNumberEntry.grid(row=x+1, column=5)
        LabelCheckButton.grid(row=x+1, column=4)

        orderstr = ""
        for item in data[OrderNumber]['Product']:
            orderstr = orderstr + (item + "  \n")

        nlines = orderstr.count('\n')
        ViewProducts.set(orderstr)
        ViewProductsEntry = Text(OrdersInfoLabelsFrame,relief=RIDGE, width = 30, height = nlines, borderwidth = 3)
        ViewProductsEntry.insert(INSERT, ViewProducts.get())
        ViewProductsEntry.grid(row=x+1,column=3)

        ShippingDateList.append(ViewDateSentEntry)
        NameList.append(ViewOrderNameEntry)
        OrderDateList.append(ViewDateEntry)
        LabelList.append(LabelCheckButton)
        LabelVars.append(LabelVar)
        ProductList.append(ViewProductsEntry)
        orderNumberList.append(ViewOrderNumberEntry)
        x = x+1

def UpdateOrders():
    print("Update Orders")
    for item in ShippingDateList:
        print(item.get())

    with open('data.json', 'r') as fp:
        data = json.load(fp)

    total = len(ShippingDateList)
    for num in range(0,total):
        print(ShippingDateList[num].get())
        data[orderNumberList[num].get()]['ShippingDate'] = ShippingDateList[num].get()
        data[orderNumberList[num].get()]['ShippingLabel'] = LabelVars[num].get()
        print(data)

    with open('data.json', 'w') as fp:
        json.dump(data, fp)


def DisplayUnsentOrders():
    with open('unsentOrders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date Ordered", "Name", "Product"])

    with open('data.json', 'r') as fp:
        data = json.load(fp)
    DictKeys = []
    for item in data.keys():
        DictKeys.append(item)
    print(DictKeys)
    print("Printing all orders")


        #### Read all order info from dictionary and display
    for num in range(0, len(orderNumberList)):
        ShippingDateList[num].grid_forget()
        NameList[num].grid_forget()
        OrderDateList[num].grid_forget()
        LabelList[num].grid_forget()
        ProductList[num].grid_forget()
        orderNumberList[num].grid_forget()
    x=0
    print(data)
    for OrderNumber in DictKeys:
        print(OrderNumber)
        print(data[OrderNumber]['ShippingName'])


        if data[OrderNumber]['ShippingDate'] == '':


            viewOrderName = tk.StringVar()
            viewDate = tk.StringVar()
            ViewDateSent = tk.StringVar()
            ViewProducts = tk.StringVar()
            ViewOrderNumber = tk.StringVar()
            LabelVar = IntVar()
            if(data[OrderNumber]['ShippingLabel'] == 1):
                LabelVar.set(1)

            ViewOrderNumber.set(data[OrderNumber]['OrderNumber'])
            viewOrderName.set(data[OrderNumber]['ShippingName'])
            viewDate.set(data[OrderNumber]['Date'])
            ViewDateSent.set(data[OrderNumber]['ShippingDate'])


            ViewOrderNameEntry = Entry(OrdersInfoLabelsFrame, text = viewOrderName)
            ViewDateEntry = Entry(OrdersInfoLabelsFrame, width=10, text = viewDate)
            ViewDateSentEntry = Entry(OrdersInfoLabelsFrame, width=10, text = ViewDateSent)
            ViewOrderNumberEntry = Entry(OrdersInfoLabelsFrame, width = 10, text = ViewOrderNumber)
            LabelCheckButton = Checkbutton (OrdersInfoLabelsFrame, variable = LabelVar)

            ViewOrderNameEntry.grid(row=x+1, column=2)
            ViewDateEntry.grid(row=x+1,column=0)
            ViewDateSentEntry.grid(row=x+1, column=1)
            ViewOrderNumberEntry.grid(row=x+1, column=5)
            LabelCheckButton.grid(row=x+1, column=4)

            orderstr = ""
            for item in data[OrderNumber]['Product']:
                orderstr = orderstr + (item + "  \n")

            with open('unsentOrders.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                row = [data[OrderNumber]['Date'], data[OrderNumber]['ShippingName'], orderstr]
                writer.writerow(row)



            nlines = orderstr.count('\n')
            ViewProducts.set(orderstr)
            ViewProductsEntry = Text(OrdersInfoLabelsFrame,relief=RIDGE, width = 30, height = nlines, borderwidth = 3)
            ViewProductsEntry.insert(INSERT, ViewProducts.get())
            ViewProductsEntry.grid(row=x+1,column=3)

            ShippingDateList.append(ViewDateSentEntry)
            NameList.append(ViewOrderNameEntry)
            OrderDateList.append(ViewDateEntry)
            LabelList.append(LabelCheckButton)
            LabelVars.append(LabelVar)
            ProductList.append(ViewProductsEntry)
            orderNumberList.append(ViewOrderNumberEntry)
            x = x+1

def PrintUnsentOrders():
    print('print unsent')

def ShowManageProductsFrame():
    print("view products and create products")
    homeFrame.place_forget()
    ManageProductsFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    n=1
    with open('productlist.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:

            productName = tk.StringVar()
            productName.set(row[0])
            productPrice = tk.StringVar()
            productPrice.set(row[1])

            ManageProductsEntry = Entry(ShowProductsFrame, textvariable = productName)
            ManageProductPriceEntry = Entry(ShowProductsFrame, textvariable = productPrice)
            ManageProductsEntry.grid(row=n, column=0)
            ManageProductPriceEntry.grid(row=n, column=1)

            ManageProductsList.append(ManageProductsEntry)
            ManageProductsPriceList.append(ManageProductPriceEntry)
            n = n+1

    UpdateProductListButton = tkinter.Button(ShowProductsFrame, text="Update All Products", highlightbackground='#3E4149', command=UpdateAllProducts)
    UpdateProductListButton.grid(row=n, column =1)

def UpdateAllProducts():
    print('Update all products')
    with open('productlist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for name, price in zip(ManageProductsList, ManageProductsPriceList):
            print(name.get(), price.get())
            if(name.get() != ''):
                writer.writerow([name.get(), price.get()])

def AddProductToProductList():
    print("fuckit")
    print(ProductNameEntry.get())
    print(productPriceEntry.get())
    with open('productlist.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        row = [ProductNameEntry.get(), productPriceEntry.get()]
        writer.writerow(row)


def ManageProductsToHome():
    ManageProductsFrame.place_forget()
    homeFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    for name, price in zip(ManageProductsList, ManageProductsPriceList):
        del name
        del price


root = tkinter.Tk(className='Welcome to the window')
root.geometry("1000x1000")



###HOME FRAME
homeFrame = Frame(root)
homeFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
CreateOrderButton = tkinter.Button(homeFrame, text ="Create New Order", command = createOrder)
ViewOrdersButton = tkinter.Button(homeFrame, text ="View Orders", command = viewOrders)
ManageOrdersButton = tkinter.Button(homeFrame, text="Manage Products", command = ShowManageProductsFrame)
CreateOrderButton.grid(row=0)
ViewOrdersButton.grid(row=1)
ManageOrdersButton.grid(row=2)

##MANAGE PRODUCTS FRAME
ManageProductsFrame = Frame(root)

CreateProductsFrame = Frame(ManageProductsFrame, borderwidth =5, padx=5, pady=5, background='yellow')
CreateProductsFrame.grid(row=1)
BottomButtonsFrame = Frame(ManageProductsFrame, borderwidth=5, background='red', padx=5, pady=5)
BottomButtonsFrame.grid(row=2)

ShowProductsFrame = Frame(ManageProductsFrame, borderwidth=5, padx=5, pady=5, background='green')
ShowProductsFrame.grid(row=0)
productListNameLabel = Label(ShowProductsFrame, borderwidth =2, relief="solid", text="Product", font=('Helvetica', 18, 'bold'))
ProductListPriceLabel = Label(ShowProductsFrame, borderwidth =2, relief="solid", text="Price", font=('Helvetica', 18, 'bold'))

productListNameLabel.grid(sticky = W, row=0, column=0)
ProductListPriceLabel.grid(sticky = W, row=0, column=1)

ProductNameLabel = Label(CreateProductsFrame, text="Enter Product Name", font=('Helvetica', 18, 'bold'))
ProductPriceLabel = Label(CreateProductsFrame, text="Enter Product Price", font=('Helvetica', 18, 'bold'))
ProductNameLabel.grid(sticky = W, row=0)
ProductPriceLabel.grid(sticky = W, row=0, column=1)

productName = tk.StringVar()
productPrice = tk.StringVar()

ProductNameEntry = tkinter.Entry(CreateProductsFrame, textvariable = productName)
ProductNameEntry.grid(row=1)
productPriceEntry = tkinter.Entry(CreateProductsFrame, textvariable= productPrice)
productPriceEntry.grid(row=1, column=1)

AddProductToProductListButton = tkinter.Button(CreateProductsFrame, text="Save Product", command=AddProductToProductList)
ManageProductsHomeButton = tkinter.Button(BottomButtonsFrame, text="Home", command=ManageProductsToHome)
AddProductToProductListButton.grid(row=2, column=1)
ManageProductsHomeButton.pack()

ManageProductsList = []
ManageProductsPriceList = []



#### CREATE ORDER FRAME
CreateOrderFrame = Frame(root, width = 900, height = 900, background = 'green')
TopFrame = Frame(CreateOrderFrame)
TopFrame.grid(row=0)
BottomFrame = Frame(CreateOrderFrame)
BottomFrame.grid(row=1)

InputOrderFrame = Frame(TopFrame, borderwidth=5, background = 'blue')
InputOrderFrame.grid(row =0, column=0)

CustomerInfoFrame = Frame(TopFrame, background = 'pink')
CustomerInfoFrame.grid(row = 0, column=1)


homeButton = tkinter.Button(BottomFrame, text="Home", command = returnHome)
homeButton.pack(side = LEFT)
InputInstruct = Label(InputOrderFrame,text="Paste Order Info Here").grid(row=0)
textPad = ScrolledText(InputOrderFrame, width= 50, height = 30)
textPad.grid(row=1, column = 0)


EditOrderInfoFrame = Frame(CustomerInfoFrame, background = 'yellow')
EditOrderInfoFrame.grid(row = 1, column = 1)

ProductInputFrame = Frame(CustomerInfoFrame, width=5, height=5, background = 'red')
ProductInputFrame.grid(row = 2, column = 1)

importTextButton = tkinter.Button(InputOrderFrame, text ="Import Text", command = importText).grid(row=3)
billingname = tk.StringVar()
ordernum = tk.StringVar()
billingemail = tk.StringVar()
shippingname = tk.StringVar()
shippingaddress = tk.StringVar()
city = tk.StringVar()
email = tk.StringVar()
phonenum = tk.StringVar()

orderlabel = Label(EditOrderInfoFrame, text="Order No", font=('Helvetica', 18, 'bold')).grid(sticky = W, row=0)
enterordernum = tkinter.Entry(EditOrderInfoFrame, textvariable = ordernum)
enterordernum.grid(row=0,column=1)
blank1 = Label(EditOrderInfoFrame,text="").grid(row=1)

billLabel = Label(EditOrderInfoFrame, text="Billing Info", font=('Helvetica', 18, 'bold')).grid(sticky = W, row=2)
billname = Label(EditOrderInfoFrame, text="Billing Name").grid(sticky = W, row=3)
enterbillname = tkinter.Entry(EditOrderInfoFrame, textvariable=billingname)
enterbillname.grid(row=3, column=1)
billemail = Label(EditOrderInfoFrame, text="Billing email").grid(sticky = W, row=4)
enterbillemail = tkinter.Entry(EditOrderInfoFrame, textvariable=billingemail)
enterbillemail.grid(row=4, column= 1)

blank = Label(EditOrderInfoFrame,text="").grid(row=5)

shipLabel = Label(EditOrderInfoFrame, text="Shipping Info", font=('Helvetica', 18, 'bold')).grid(row=6)

tkinter.Label(EditOrderInfoFrame, text="Name").grid(sticky = W, row=7)
tkinter.Label(EditOrderInfoFrame, text="Address").grid(sticky = W, row=8)
tkinter.Label(EditOrderInfoFrame, text="City").grid(sticky = W, row=9)
tkinter.Label(EditOrderInfoFrame, text="Phone number").grid(sticky = W, row=10)
tkinter.Label(EditOrderInfoFrame, text="Email").grid(sticky = W, row=11)
tkinter.Label(EditOrderInfoFrame, text="").grid(sticky = W, row=12)

ShipNameEntry = tkinter.Entry(EditOrderInfoFrame,textvariable=shippingname)
ShipNameEntry.grid(row=7, column=1)
addressentry = tkinter.Entry(EditOrderInfoFrame, textvariable=shippingaddress)
addressentry.grid(row=8, column=1)
cityentry = tkinter.Entry(EditOrderInfoFrame, textvariable=city)
cityentry.grid(row=9, column=1)
emailentry = tkinter.Entry(EditOrderInfoFrame, textvariable=email)
emailentry.grid(row=11, column=1)
phonenumentry = tkinter.Entry(EditOrderInfoFrame, textvariable=phonenum)
phonenumentry.grid(row=10, column=1)


OrderDict = {
    "OrderNumber": "",
    "BillingName": "",
    "BillingEmail": "",
    "ShippingName": "",
    "Address": "",
    "City": "",
    "ShippingEmail": "",
    "PhoneNumber": "",
    "Date": "",
    "ShippingDate":"",
    "ShippingLabel":"" ,
    "Product": "",
    "Quantities": ""
}


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
ProductObjList = []
with open('productlist.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        product = Product(row[0], row[1])
        ProductObjList.append(product)



ProductList =[]
for prod in ProductObjList:
    ProductList.append(prod.name)


Quantity = []
for num in range(0,11):
    Quantity.append(str(num))

ProductSelect = tk.StringVar(ProductInputFrame)
ProductSelect.set("Select a product")

ProductDropDown = tk.OptionMenu(ProductInputFrame, ProductSelect, *ProductList)
ProductDropDown.config(width = 20)
ProductDropDown.grid(row=0, column=0)

QuantitySelect = tk.StringVar(ProductInputFrame)
QuantitySelect.set(Quantity[0])
QuantityDropDown = tk.OptionMenu(ProductInputFrame, QuantitySelect, *Quantity).grid(row=0, column=1)

AllEntries = []
AllEntryText = []
AllQuantities =[]
AllPrices = []
AllDelete = []

count=1
AddToOrderButton = tkinter.Button(ProductInputFrame, text ="Add to Order", highlightbackground='#3E4149', command = AddToOrder)
AddToOrderButton.grid(row =0, column=2)


SaveOrdertoDBbutton = tkinter.Button(BottomFrame, text ="Save Order To DB/Packing Slip", command = SaveOrdertoDB)
SaveOrdertoDBbutton.pack(side = RIGHT)



#### VIEW ORDERS Frame
ordersFrame = Frame(root, background = 'blue')

UpdatePrintOrdersFrame = Frame(ordersFrame, background='green')
UpdatePrintOrdersFrame.grid(row=2)
###Update all order info Button
UpdateOrdersButton = tkinter.Button(UpdatePrintOrdersFrame, padx=5, pady=5, text='Update Orders', command=UpdateOrders)
UpdateOrdersButton.grid(row = 0,column=0)
PrintUnsentOrdersButton = tkinter.Button(UpdatePrintOrdersFrame, padx=5,pady=5, text='Print Unsent Orders', command=PrintUnsentOrders)
PrintUnsentOrdersButton.grid(row=0,column=1)

### FRAME FOR VIEW ORDERS AND BUTTONS
ViewOrdersButtonFrame = Frame(ordersFrame, padx=10, pady=10, background = 'pink')
ViewOrdersButtonFrame.grid(row = 0)
homebutt = tkinter.Button(ViewOrdersButtonFrame, text = "Home", command = returnHome)
homebutt.grid(row=0,column=0)
DisplayOrdersButton = (tkinter.Button(ViewOrdersButtonFrame, text = "Display All Orders", padx=20, command = DisplayOrders))
DisplayOrdersButton.grid(row=0,column=1)
DisplayUnsentOrdersButton = tkinter.Button(ViewOrdersButtonFrame, text = "Diplay Unsent Orders", command = DisplayUnsentOrders)
DisplayUnsentOrdersButton.grid(row=0,column=2)

### FRAME FOR LABELS OF ORDER IE ORDER NUM, NAME, PRODUCT...
OrdersInfoLabelsFrame = Frame(ordersFrame, padx=10,pady=10, background = 'red')
OrdersInfoLabelsFrame.grid(row = 1)

nameLabel= Label(OrdersInfoLabelsFrame, text="Name", borderwidth =2, relief="raised")
nameLabel.grid(row=0,column=2)
orderDateLabel = Label(OrdersInfoLabelsFrame, text="Order Date", borderwidth =2, relief="raised")
orderDateLabel.grid(row=0,column=0)
shippingDateLabel = Label(OrdersInfoLabelsFrame, text="Shipping Date", borderwidth =2, relief="raised")
shippingDateLabel.grid(row=0,column=1)
productLabel = Label(OrdersInfoLabelsFrame, text="Products", borderwidth =2, relief="raised")
productLabel.grid(row=0,column=3)
courierPrinted = Label(OrdersInfoLabelsFrame, text="Label printed", borderwidth =2, relief="raised")
courierPrinted.grid(row=0,column=4)
orderNumberLabel = Label(OrdersInfoLabelsFrame, text="Order Number", borderwidth =2, relief="raised")
orderNumberLabel.grid(row=0,column=5)

OrderDateList = []
ShippingDateList = []
NameList = []
ProductList = []
LabelList = []
LabelVars = []
orderNumberList = []


root.mainloop()
