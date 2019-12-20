import csv
import datetime
import time
import math
import typing
from tkinter import *
from ast import literal_eval

#2D list for all running batches to be stored
#the list consists of the elements in the backup file
with open('runBatchBackup.txt', 'r') as f:
    running_batches = literal_eval('[' + f.read().replace('\n', ',') + ']')

#tanks list is static with all tanks from specifications
tanks = [["Albert", 1000, "FC", 0], ["Brigadier", 800, "FC", 0], ["Camilla", 1000, "FC", 0], ["Dylon", 800, "FC", 0], ["Emily", 1000, "FC", 0], ["Florence", 800, "FC", 0], ["Gertrude", 680, "C", 0], ["Harry", 680, "C", 0], ["R2D2", 800, "F", 0]]
""" 2D list to represent the tanks available:

    Key:
    [0] - tank name - str
    [1] - tank full capacity - int
    [2] - capability (F - Fermenter, C - Conditioner) - str
    [3] - filled - int
"""

class Interface(Frame):
    """ UI class.
        Contains the user interface elements as well as the functions created earlier as class methods which are
        assigned to buttons correspondingly.
    """
    
    def __init__(self, master):
        super().__init__(master)   
        
        #Create title
        self.master.title("BarnabyBrewhouse") 
        self.pack(fill=BOTH, expand=1)
        
        #Create background rectangles
        canvas = Canvas(self)
        canvas.create_rectangle(900, 120, 100, 10, 
            outline="#fb0", fill="#fb0")
        canvas.create_rectangle(500, 450, 100, 150, 
            outline="#fb0", fill="#fb0")        
        canvas.create_rectangle(900, 150, 520, 370, 
            outline="#fb0", fill="#fb0")       
        canvas.create_rectangle(900, 700, 520, 400, 
            outline="#fb0", fill="#fb0") 
        canvas.create_rectangle(500, 700, 100, 480, 
            outline="#fb0", fill="#fb0")         
        
        """ Create new_batch interface
        """
        
        canvas.create_text((190, 30), text="Create new batch", font=("Times", 15, "italic", "bold", "underline"))  
        
        #create interactive text
        self.changeme = Label(canvas, text="Please enter appropriate data.", font=("Times", 15, "bold"), bg="red")
        canvas.create_window(600,100,window=self.changeme) 
        
        #batch number field
        self.batch_number = Entry(canvas)
        canvas.create_text((170, 60), text="Batch number:", font=("Times", 15))
        canvas.create_window(290,60,window=self.batch_number)
        
        #litre quantity field
        self.quantity_litres = Entry(canvas)
        canvas.create_text((430, 60), text="Litre quantity:", font=("Times", 15))
        canvas.create_window(550,60,window=self.quantity_litres)       
        
        #beer type drop down list
        OPTIONS = ["Organic Red Helles","Organic Pilsner","Organic Dunkel"]
        self.beer_type_is = StringVar(canvas)
        self.beer_type_is.set(OPTIONS[0]) # default value
        self.beer_type = OptionMenu(canvas, self.beer_type_is, *OPTIONS)
        canvas.create_text((680, 60), text="Beer type:", font=("Times", 15))
        canvas.create_window(800,60,window=self.beer_type) 

        #submit data button  
        submitButton = Button(canvas, text="Submit", command=self.new_batch)
        canvas.create_window(170,100,window=submitButton)
        
        """ Create check_status for BATCHES interface
        """
        
        canvas.create_text((580, 420), text="Batch status", font=("Times", 15, "italic", "bold", "underline")) 
        
        #create update button
        updateBatchButton = Button(canvas, text="Update", command=self.check_status_batch)
        canvas.create_window(680,420,window=updateBatchButton)
        
        #create update text
        self.updatedBatch = Label(canvas, text="Please update the batches.", font=("Times", 11), bg="#fb0")
        canvas.create_window(710,580,window=self.updatedBatch)
      
        """ Create check_status for TANKS interface
        """
        
        canvas.create_text((160, 500), text="Tank status", font=("Times", 15, "italic", "bold", "underline")) 
        
        #create update button
        updateTankButton = Button(canvas, text="Update", command=self.check_status_tank)
        canvas.create_window(250,500,window=updateTankButton)
        
        #create update text
        self.updatedTank = Label(canvas, text="Please update the tanks.", font=("Times", 11), bg="#fb0")
        canvas.create_window(300,610,window=self.updatedTank)
      
        """ Create options menu.
            Includes stop_batch, start_stage and *record sales data
        """
        
        canvas.create_text((150, 170), text="Options", font=("Times", 15, "italic", "bold", "underline")) 
        
        #create stop process option
        self.stop_batch_number = Entry(canvas)
        canvas.create_text((170, 200), text="Stop process:", font=("Times", 15))
        canvas.create_text((170, 220), text="(Enter batch number)", font=("Times", 10))
        canvas.create_window(290,200,window=self.stop_batch_number)
        
        stopProcessButton = Button(canvas, text="Submit", command=self.stop_batch)
        canvas.create_window(400,200,window=stopProcessButton)
        
        #create start stage option
        self.start_batch_number = Entry(canvas)
        canvas.create_text((170, 250), text="Start stage:", font=("Times", 15))
        canvas.create_text((170, 270), text="(Enter batch number", font=("Times", 10))
        canvas.create_text((170, 280), text="and select tank)", font=("Times", 10))
        canvas.create_window(290,250,window=self.start_batch_number)
        
        TANKS = ["Albert", "Brigadier", "Camilla", "Dylon", "Emily", "Florence", "Gertrude", "Harry", "R2D2", "No tank"]
        self.put_in_tank = StringVar(canvas)
        self.put_in_tank.set(TANKS[0]) # default value
        self.put_in_tank_choose = OptionMenu(canvas, self.put_in_tank, *TANKS)
        canvas.create_window(290,280,window=self.put_in_tank_choose) 
        
        startProcessButton = Button(canvas, text="Submit", command=self.start_stage)
        canvas.create_window(400,265,window=startProcessButton)
        
        #create record sales option
        self.invoice_number = Entry(canvas)
        canvas.create_text((170, 320), text="Record sale:", font=("Times", 15))
        canvas.create_text((170, 340), text="(Enter invoice number)", font=("Times", 10))
        canvas.create_window(300,340,window=self.invoice_number)
        
        self.customer_name = Entry(canvas)
        canvas.create_text((170, 360), text="(Enter customer name)", font=("Times", 10))
        canvas.create_window(300,360,window=self.customer_name)
        
        self.batch_sold = Entry(canvas)
        canvas.create_text((170, 380), text="(Enter batch number)", font=("Times", 10))
        canvas.create_window(300,380,window=self.batch_sold)
        
        self.quantity_sold = Entry(canvas)
        canvas.create_text((170, 400), text="(Enter quantity sold)", font=("Times", 10))
        canvas.create_window(300,400,window=self.quantity_sold)
        
        recordButton = Button(canvas, text="Submit", command=self.record_batch)
        canvas.create_window(420,360,window=recordButton)
        
        #log text
        self.changemelog = Label(canvas, text="Please enter appropriate data.", font=("Times", 13, "bold"), bg="red")
        canvas.create_window(300,430,window=self.changemelog) 
      
        """ Create prediction window
        """
        
        canvas.create_text((570, 170), text="Planning", font=("Times", 15, "italic", "bold", "underline"))
        
        calculatePrediction = Button(canvas, text="Calculate", command=self.planning_algorithm)
        canvas.create_window(670, 170,window=calculatePrediction)
        
        #create update text
        self.updatedPrediction = Label(canvas, text="Please calculate.", font=("Times", 11), bg="#fb0")
        canvas.create_window(700, 280,window=self.updatedPrediction)
      
        """ Run canvas
        """
        
        canvas.pack(fill=BOTH, expand=1)
        
    def new_batch(self) -> None:
        """ Adds a new batch to the list with the given number and quantity.
            Automatically starts the hot brew stage.
            Volume has to be less than 1000 for the input to be valid.
        
            Key:
            [0] - batch_number - int
            [1] - start_time - int
            [2] - current stage - str
            [3] - quantity_litres - int
            [4] - status (True = in progress) - bool
            [5] - tank name batch is in - str
            [6] - beer_type - str
        """
        
        #get the input values
        self.batch_number_temp = self.batch_number.get()
        self.quantity_litres_temp = self.quantity_litres.get()
        self.beer_type_is_temp = self.beer_type_is.get()
        
        global running_batches
        
        #validate user input
        try:
            int(self.batch_number_temp)
            int(self.quantity_litres_temp)
        except ValueError:
            self.changeme.config(text="ERROR: Input not valid")
        else:
            
            #look for batch with same name
            i = 0
            batchFound = False
            while i < len(running_batches):
                if running_batches[i][0] == int(self.batch_number_temp):
                    batchFound = True
                    break
                i = i + 1
            
            if batchFound == False:
                if int(self.quantity_litres_temp) <= 1000 and int(self.quantity_litres_temp) > 0:
                    start_time = time.time()
                    running_batches.append([int(self.batch_number_temp), start_time, "Hot Brew", int(self.quantity_litres_temp), True, "No tank", self.beer_type_is_temp])
                    self.changeme.config(text="SUCCESS: Batch created")
                    
                else:
                    self.changeme.config(text="ERROR: Batch volume is not adequate.")
            else:
                self.changeme.config(text="ERROR: Batch already exists")
    
    def check_status_batch(self) -> None:
        """ Checks the status of all running batches.
            Outputs detail about each batch.
            It updates the backup file with the current batch situation.
            
            WARNING: After about 30 batches, the interface glitches due to space on screen.
        """     
        
        global running_batches
            
        end_time = time.time()
        output_text = ["Batch/Time/Stage/Volume/Process?/Tank/Type"]
        
        #add each batch data to the output_text list
        i = 0
        while i < len(running_batches):
            batchNumberTemp = running_batches[i][0]
            start_time = running_batches[i][1]
            time_lapsed = end_time - start_time
            timeTakenTemp = time_convert(time_lapsed)
            currentStageTemp = running_batches[i][2]
            quantityTemp = running_batches[i][3]
            statusTemp = running_batches[i][4]
            currentTankTemp = running_batches[i][5]
            beerTypeTemp = running_batches[i][6]
            output_text.append("{}, {}, {}, {}, {}, {}, {}".format(batchNumberTemp, timeTakenTemp, currentStageTemp, quantityTemp, statusTemp, currentTankTemp, beerTypeTemp))
            i = i + 1
        
        #update the text
        self.updatedBatch.config(text="\n".join(output_text))
        
        #update backup file
        with open('runBatchBackup.txt', 'w') as f:
            for item in running_batches:
                f.write("%s\n" % item)
                
    def check_status_tank(self) -> None:
        """ Checks the status of all tanks.
            Outputs detail about each tank.
        """     
        
        global tanks
            
        output_text = ["Name/Capability/Max Volume/Volume in use"]
        
        #add each tank data to the output_text    
        i = 0
        while i < len(tanks):
            tankNameTemp = tanks[i][0]
            tankCapabilityTemp = tanks[i][2]
            tankFullTemp = tanks[i][1]
            tankUsedTemp = tanks[i][3]
            output_text.append("{}, {}, {}, {}".format(tankNameTemp, tankCapabilityTemp, tankFullTemp, tankUsedTemp))
            i = i + 1
            
        #update the text
        self.updatedTank.config(text="\n".join(output_text))
        
    def stop_batch(self) -> None:
        """ End a current stage. Works for all 4 stages.
            The function outputs the stage that finished and the time it took for it to finish.
            Removes volume from the tank and shifts batch to the next stage (but not start it).
        """
        
        global running_batches
        
        self.stop_batch_number_temp = self.stop_batch_number.get()
        end_time = time.time()
        
        #validate input
        try:
            int(self.stop_batch_number_temp)
        except ValueError:
            self.changemelog.config(text="ERROR: Input not valid")
        else:
            
            #loop to see if the batch exists
            i = 0
            batchFound = "Nothing"
            while i < len(running_batches):
                if running_batches[i][0] == int(self.stop_batch_number_temp):
                    batchFound = i
                    break
                i = i + 1        
                
            if batchFound != "Nothing":
                if running_batches[batchFound][4] == True:
                    start_time = running_batches[batchFound][1]
                    time_lapsed = end_time - start_time
                    running_batches[batchFound][4] = False
                    
                    #Hot Brew stage is finished
                    if running_batches[batchFound][2] == "Hot Brew":
                        running_batches[batchFound][2] = "Fermentation"
                        
                        self.changemelog.config(text="UPDATE: Hot Brew finished. Time taken: {}".format(time_convert(time_lapsed)))
                     
                    #Fermentation stage is finished   
                    elif running_batches[batchFound][2] == "Fermentation":
            
                        i = 0
                        while i < len(tanks):
                            if tanks[i][0] == running_batches[batchFound][5] :
                                tankFound = i
                                break
                            i = i + 1
                        
                        tanks[tankFound][3] = tanks[tankFound][3] - running_batches[batchFound][3]
                        running_batches[batchFound][2] = "Conditioning"
                        running_batches[batchFound][5] = "No tank"
                        self.changemelog.config(text="UPDATE: Fermentation finished. Time taken: {}".format(time_convert(time_lapsed)))
                    
                    #Conditioning stage is finished    
                    elif running_batches[batchFound][2] == "Conditioning":
                      
                        i = 0
                        while i < len(tanks):
                            if tanks[i][0] == running_batches[batchFound][5] :
                                tankFound = i
                                break
                            i = i + 1
                        
                        tanks[tankFound][3] = tanks[tankFound][3] - running_batches[batchFound][3]
                        running_batches[batchFound][2] = "Bottling"
                        running_batches[batchFound][5] = "No tank" 
                        self.changemelog.config(text="UPDATE: Conditioning finished. Time taken: {}".format(time_convert(time_lapsed)))
                    
                    #Bottling stage is finished    
                    elif running_batches[batchFound][2] == "Bottling":
                    
                        bottlesProduced = math.floor(running_batches[batchFound][3] / 0.5)
                        self.changemelog.config(text="UPDATE: Batch finished. Time taken: {}. Bottles: {}".format(time_convert(time_lapsed), bottlesProduced))
                        
                        dataInventory = [running_batches[batchFound][0], running_batches[batchFound][6], bottlesProduced]
                        
                        #add data to inventory
                        with open("inventory_data.csv", "a", newline='') as fp:
                            wr = csv.writer(fp, dialect='excel')
                            wr.writerow(dataInventory)
                        
                        #remove the batch from the list
                        del(running_batches[batchFound])
                        
                else:
                    self.changemelog.config(text="ERROR: Batch not currently running")
            else: 
                self.changemelog.config(text="ERROR: Batch not found")

    def start_stage(self) -> None:
        """ Starts the stage the batch is in if it is not started already.
        
            tank_name should be "No tank" for the bottling process.
            tank_name can be "No tank" for the other processes too although is not recommended.
            
            Updates the batch with the relevant info and the tanks available capacity.
        """
        
        global running_batches
        global tanks
        
        self.start_batch_number_temp = self.start_batch_number.get()
        self.put_in_tank_temp = self.put_in_tank.get()
        
        
        #validate input
        try:
            int(self.start_batch_number_temp)
        except ValueError:
            self.changemelog.config(text="ERROR: Input not valid")
        else:
            
            i = 0
            batchFound = "Nothing"
            while i < len(running_batches):
                if running_batches[i][0] == int(self.start_batch_number_temp):
                    batchFound = i
                    break
                i = i + 1
                
            i = 0
            tankFound = "Nothing"
            while i < len(tanks):
                if tanks[i][0] == self.put_in_tank_temp:
                    tankFound = i
                    break
                i = i + 1
            
            #all conditions have to be met in order for the batch to start
            #see the else statements to find the conditions          
            if batchFound != "Nothing":
                if running_batches[batchFound][4] != True:
                    if self.put_in_tank_temp == "No tank" or tanks[tankFound][1] - tanks[tankFound][3] >= running_batches[batchFound][3]:
                        
                        correctContainer = False
                        if running_batches[batchFound][2] == "Fermentation":
                            if "F" in tanks[tankFound][2]:
                                correctContainer = True
                        elif running_batches[batchFound][2] == "Conditioning":
                            if "C" in tanks[tankFound][2]:
                                correctContainer = True
                                
                        if correctContainer == True or self.put_in_tank_temp == "No tank":
                            
                            if correctContainer == True:
                                tanks[tankFound][3] = tanks[tankFound][3] + running_batches[batchFound][3]
                                running_batches[batchFound][5] = tanks[tankFound][0]
                                
                            start_time = time.time()
                            running_batches[batchFound][1] = start_time
                            running_batches[batchFound][4] = True
                            self.changemelog.config(text="UPDATE: Process started successfully")
                            
                        else:
                            self.changemelog.config(text="ERROR: Non-appropriate capability")
                    else:
                        self.changemelog.config(text="ERROR: Tank volume not enough")
                else:
                    self.changemelog.config(text="ERROR: Batch already in a process")
            else:
                self.changemelog.config(text="ERROR: Batch not found")
    
    def record_batch(self) -> None:
        """ Records the data inputed by the user for a sale.
            Appends the current sales_data file with the new data.
            Changes the quantity of a batch in the inventory_data file accordingly.
        """
        
        self.invoice_number_temp = self.invoice_number.get()
        self.customer_name_temp = self.customer_name.get()
        self.batch_sold_temp = self.batch_sold.get()
        self.quantity_sold_temp = self.quantity_sold.get()
        
        
        with open('inventory_data.csv', 'r') as infile:
        # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
        
        batchNumber = data['GyleNumber']
        recipeRecord = data['Recipe']
        quantityRecorded = data['Quantity']
        
        #validate input
        try:
            int(self.batch_sold_temp)
            int(self.quantity_sold_temp)
        except ValueError:
            self.changemelog.config(text="ERROR: Input not valid")
        else:
            
            #check batch exists
            i = 0
            batchFound = "Nothing"
            while i < len(batchNumber):
                if batchNumber[i] == self.batch_sold_temp:
                    batchFound = i
                    break
                i = i + 1
            
            if batchFound != "Nothing":   
                #check if there is enough quantity to be taken out
                if int(quantityRecorded[batchFound]) >= int(self.quantity_sold_temp) and int(self.quantity_sold_temp) > 0:   
                    
                    newQuantity = int(quantityRecorded[batchFound]) - int(self.quantity_sold_temp)
                    recipeTemp = recipeRecord[batchFound]
                    changeData = [batchNumber[batchFound], recipeTemp, newQuantity]
                    
                    #read inventory
                    with open("inventory_data.csv", "r") as f:
                        data = list(csv.reader(f))
                    
                    #remove the line with the batch from inventory
                    with open('inventory_data.csv', 'w', newline='') as inp:
                        writer = csv.writer(inp)
                        firstLine = True
                        for row in data:
                            if firstLine == False:
                                if row[0] != self.batch_sold_temp:
                                    writer.writerow(row)
                            else:
                                firstLine = False
                                writer.writerow(row)
                    
                    #add the modified line in inventory    
                    if newQuantity != 0:
                        with open("inventory_data.csv", "a", newline='') as fp:
                            wr = csv.writer(fp, dialect='excel')
                            wr.writerow(changeData)
                        
                    today = datetime.datetime.today()
                    d1 = today.strftime("%d/%m/%Y")
                        
                    newSale = [self.invoice_number_temp, self.customer_name_temp, d1, recipeTemp, self.batch_sold_temp, self.quantity_sold_temp]
                    
                    #append the sales file with the new data
                    with open("sales_data.csv", "a",newline='') as fp:
                        wr = csv.writer(fp, dialect='excel')
                        wr.writerow(newSale)
                
                    self.changemelog.config(text="UPDATE: Sale added successfully")
                    
                else:
                    self.changemelog.config(text="ERROR: Quantity not enough")
            else:
                self.changemelog.config(text="ERROR: Batch not found")
                
    def planning_algorithm(self) -> None:
        """ Outputs the next type of beer to be produce, the litre quantity that should be put and in which tank it should be put.
            Next type of beer is approximated to be needed in the next 2 months.
        
            From the data in the spreadsheet, program assumes that the approximate quantity in the next year is 25000.
        
            The amount of beer needed works on a principle of "safe value" which is the value of 
            the 2 months in from of the current month added. If the "safe value" is reached for each type
            of beer then no beer of that type needs producing.
        """
        
        global tanks
        global running_batches
        
        # open the file in universal line ending mode 
        with open('sales_data.csv', 'r') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
        
        # extract the variables in list format
        quantityOrdered = data['QuantityOrdered']
        recipeNumber = data['Recipe']
        dateRequired = data['DateRequired']
        
        approxQuantity = 25000 
        
        #get the current month + 2 extra months to be used for the prediction
        today = datetime.datetime.today()
        chooseMonth1 = today.month + 1
        chooseMonth2 = today.month + 2
        if chooseMonth1 > 12:
            chooseMonth1 = chooseMonth1 - 12
        if chooseMonth2 > 12:
            chooseMonth2 = chooseMonth2 - 12
            
        a = predict_quantity(approxQuantity, get_average_growth_rate(get_growth_list(dateRequired, quantityOrdered)), get_beer_ratio(recipeNumber, quantityOrdered))
        
        #extract the "safe value" quantity from the prediction algorithm used in part 1.
        chooseMonth1 = chooseMonth1 - 1
        chooseMonth2 = chooseMonth2 - 1
        redHellesNeeded = a[0][chooseMonth1] + a[0][chooseMonth2]
        pilserNeeded = a[1][chooseMonth1] + a[1][chooseMonth2]
        dunkelNeeded = a[2][chooseMonth1] + a[2][chooseMonth2]
        
        with open('inventory_data.csv', 'r') as infile:
        # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
    
        # extract the variables in list format
        quantityRecorded = data['Quantity']
        recipeRecord = data['Recipe']
        
        i = 0
        totalRedHelles = 0
        totalPilsner = 0
        totalDunkel = 0
        quantityRecorded = [ int(x) for x in quantityRecorded ]
        
        #take into consideration inventory
        while i < len(quantityRecorded):
            if recipeRecord[i] == "Organic Red Helles":
                totalRedHelles = totalRedHelles + quantityRecorded[i]
            elif recipeRecord[i] == "Organic Pilsner":
                totalPilsner = totalPilsner + quantityRecorded[i]
            elif recipeRecord[i] == "Organic Dunkel":
                totalDunkel = totalDunkel + quantityRecorded[i]
            i = i + 1
        
        #take into consideration currently running batches
        i = 0
        while i < len(running_batches):
            if running_batches[i][6] == "Organic Red Helles":
                totalRedHelles = totalRedHelles + running_batches[i][3] * 2
            if running_batches[i][6] == "Organic Pilsner":
                totalPilsner = totalPilsner + running_batches[i][3] * 2
            if running_batches[i][6] == "Organic Dunkel":
                totalDunkel = totalDunkel + running_batches[i][3] * 2
            i = i + 1
            
        redHellesNeeded = redHellesNeeded - totalRedHelles
        pilserNeeded = pilserNeeded - totalPilsner
        dunkelNeeded = dunkelNeeded - totalDunkel
        
        #the biggest batch should be produced next
        if redHellesNeeded >= pilserNeeded:
            if redHellesNeeded >= dunkelNeeded:
                beerToProduce = redHellesNeeded
                beerToProduceType = "Organic Red Helles"
            else:
                beerToProduce = dunkelNeeded
                beerToProduceType = "Organic Dunkel"           
        else:
            if pilserNeeded >= dunkelNeeded:
                beerToProduce = pilserNeeded
                beerToProduceType = "Organic Pilsner"
            else:
                beerToProduce = dunkelNeeded
                beerToProduceType = "Organic Dunkel"
        
        #if all batches are 0, then there is no need for extra production
        if beerToProduce > 0:
            text1 = "The advised next batch is: {}.\n Litres that should be put in: {}".format(beerToProduceType, beerToProduce / 2)
        else:
            text1 = "There is currently no need for beer to be produced!"
        
        i = 0
        appropriateTank = "Nothing"
        while i < len(tanks):
            if tanks[i][1] - tanks[i][3] >= beerToProduce / 2:
                appropriateTank = tanks[i][0]
                break
            i = i + 1
        
        #take into consideration which tank the beer should be put in    
        if appropriateTank != "Nothing" and beerToProduce > 0:
            text2 = "Tank the beer could be brewed in: {}".format(appropriateTank)
        elif beerToProduce < 0:
            text2 = ""
        else:
            text2 = "There is no tank that's big enough for the whole batch!"
        
        percentageList = get_beer_ratio(recipeNumber, quantityOrdered)
        
        text3 = "\nFrom the sales data: \n Red Helles: {} % \n Pilsner: {} % \n Dunkel: {} %".format("%.2f" % (percentageList[0]*100), "%.2f" % (percentageList[1]*100), "%.2f" % (percentageList[2]*100))
        
        text4 = "Average monthly increase of beer sale: {} % \n".format(average_list(get_average_growth_rate(get_growth_list(dateRequired, quantityOrdered))))
        outputText = [text1,text2, text3,text4]
        
        self.updatedPrediction.config(text="\n".join(outputText))

def get_beer_ratio(recipe: list, number: list) -> list:
    """ Extract the quantity for each type of beer.
        Return the percentage of each type of beer out of total beer produced in the given period as a list.
    """
    
    i = 0
    totalRedHelles = 0
    totalPilsner = 0
    totalDunkel = 0
    number = [ int(x) for x in number ]
    
    #add up the quantity ordered for each type of beer
    while i < len(number) - 1:
        if recipe[i] == "Organic Red Helles":
            totalRedHelles = totalRedHelles + number[i]
        elif recipe[i] == "Organic Pilsner":
            totalPilsner = totalPilsner + number[i]
        elif recipe[i] == "Organic Dunkel":
            totalDunkel = totalDunkel + number[i]
        i = i + 1
        
    #gets percentage of each type of beer    
    total = totalDunkel + totalPilsner + totalRedHelles
    percRedHelles = (totalRedHelles/total)
    percPilsner = (totalPilsner/total)
    percDunkel = (totalDunkel/total)
    
    percBeerList = [percRedHelles, percPilsner, percDunkel]
    percBeerList = [ float(x) for x in percBeerList ]
    
    return percBeerList
    
def zerolistmaker(n: int) -> list:
    """ Create a list with n elements which are all 0's
    """
    
    listofzeros = [0] * n
    
    return listofzeros

def get_growth_list(date: list, number: list) -> list:
    """ For every month in the database, all the quantities for that month are added.
        Returns quantity of every month as a list in chronological order.
    """
    
    i = 0
    number = [ int(x) for x in number ]
    dateList = zerolistmaker(12)
    
    #for each element in the file, its date is tested and added to a list to get the total beer for each month
    while i < len(date) - 1:
        thisDate = datetime.datetime.strptime(date[i], "%d/%m/%Y")
    
        mo = 1
        while mo < 13:
            if thisDate.month == mo:
                dateList[mo - 1] = dateList[mo - 1] + number[i] 
            mo = mo + 1
                 
        i = i + 1
   
    return dateList   

def get_average_growth_rate(monthList: list) -> list:
    """ Calculate the average growth rate between every 2 successive elements in a list.
        Returns the list of average growth rate.
        
        Formula: Growth Rate = ( Last Month - First Month ) / First Month
    """
    
    growth_rate_list = []
    
    i = 0
    while i < len(monthList) - 1:
        growthRate = (monthList[i+1] - monthList[i]) / monthList[i]
        growth_rate_list.append(growthRate)
        i = i + 1
     
    return growth_rate_list

def average_list(averageList: list) -> str: 
    """ Calculates the average of all elements in a list.
        Returns the average as a percentage.
    """
        
    average_growth_rate = sum(averageList) / len(averageList) * 100
    average_growth_rate = "%.2f" % average_growth_rate
    
    return average_growth_rate

def predict_quantity(quantityAvailable: int, percGrowthRateList: list, percList: list) -> list:
    """ Prediction takes place by comparing the actual data in the file to a new given quantity by the user.
        As the database extends, the results and predictions will also change accordingly.
        For each type of beer, given the new stock, the growth rate formula is derived to make Last Month the subject to approximate the amount of beer needed in a specific month.
        Returns a 2D list with approximations of each type of beer for each month.
        
        Formula: Last Month = First Month * ( Growth Rate + 1 )
        [Derived from the growth rate formula]
    """
    # open the file in universal line ending mode 
    with open('sales_data.csv', 'r') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    
    # extract the variables in list format
    quantityOrdered = data['QuantityOrdered']
    dateRequired = data['DateRequired']
    
    a = get_growth_list(dateRequired, quantityOrdered)
    firstMonth = a[0] / sum(a) * quantityAvailable
    
    redHellesApprox = int(round(firstMonth * percList[0]))
    pilsnerApprox = int(round(firstMonth* percList[1]))
    dunkelApprox =int(round(firstMonth * percList[2]))
    
    #a list is created for each type of beer to hold the predictions
    redHellesPred = [redHellesApprox]
    pilsnerPred = [pilsnerApprox]
    dunkelPred = [dunkelApprox]
    
    #the new formula is used to calculate the predicted needed beer for each month
    i = 0
    while i < 11:
        redHellesChange = redHellesPred[i] * (percGrowthRateList[i] + 1)
        redHellesPred.append(int(round(redHellesChange)))
        
        pilsnerChange = pilsnerPred[i] * (percGrowthRateList[i] + 1)
        pilsnerPred.append(int(round(pilsnerChange)))
        
        dunkelChange = dunkelPred[i] * (percGrowthRateList[i] + 1)
        dunkelPred.append(int(round(dunkelChange)))
        
        i = i + 1   
    
    predictionList = [redHellesPred, pilsnerPred, dunkelPred]
    
    return predictionList

def time_convert(sec: int) -> str:
    """ Converts "sec" argument in a HH:MM:SS format.
        Returns a string of Time Lapsed.
    """
    
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    
    out = "{0}:{1}:{2}".format(int(hours),int(mins),"%.0f" % sec)
    
    return out
               
def planning_algorithm() -> None:
    """ Outputs the next type of beer to be produce, the litre quantity that should be put and in which tank it should be put.
        Next type of beer is approximated to be needed in the next 2 months.
    
        From the data in the spreadsheet, program assumes that the approximate quantity in the next year is 25000.
    
        The amount of beer needed works on a principle of "safe value" which is the value of 
        the 2 months in from of the current month added. If the "safe value" is reached for each type
        of beer then no beer of that type needs producing.
    """
    
    global tanks
    global running_batches
    
    approxQuantity = 25000 
    
    #get the current month + 2 extra months to be used for the prediction
    today = datetime.datetime.today()
    chooseMonth1 = today.month + 1
    chooseMonth2 = today.month + 2
    if chooseMonth1 > 12:
        chooseMonth1 = chooseMonth1 - 12
    if chooseMonth2 > 12:
        chooseMonth2 = chooseMonth2 - 12
        
    a = predict_quantity(approxQuantity, get_average_growth_rate(get_growth_list(dateRequired, quantityOrdered)), get_beer_ratio(recipeNumber, quantityOrdered))
    
    #extract the "safe value" quantity from the prediction algorithm used in part 1.
    chooseMonth1 = chooseMonth1 - 1
    chooseMonth2 = chooseMonth2 - 1
    redHellesNeeded = a[0][chooseMonth1] + a[0][chooseMonth2]
    pilserNeeded = a[1][chooseMonth1] + a[1][chooseMonth2]
    dunkelNeeded = a[2][chooseMonth1] + a[2][chooseMonth2]
    
    with open('inventory_data.csv', 'r') as infile:
    # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    # extract the variables in list format
    quantityRecorded = data['Quantity']
    recipeRecord = data['Recipe']
    
    i = 0
    totalRedHelles = 0
    totalPilsner = 0
    totalDunkel = 0
    quantityRecorded = [ int(x) for x in quantityRecorded ]
    
    #take into consideration inventory
    while i < len(quantityRecorded):
        if recipeRecord[i] == "Organic Red Helles":
            totalRedHelles = totalRedHelles + quantityRecorded[i]
        elif recipeRecord[i] == "Organic Pilsner":
            totalPilsner = totalPilsner + quantityRecorded[i]
        elif recipeRecord[i] == "Organic Dunkel":
            totalDunkel = totalDunkel + quantityRecorded[i]
        i = i + 1
    
    #take into consideration currently running batches
    i = 0
    while i < len(running_batches):
        if running_batches[i][6] == "Organic Red Helles":
            totalRedHelles = totalRedHelles + running_batches[i][3] * 2
        if running_batches[i][6] == "Organic Pilsner":
            totalPilsner = totalPilsner + running_batches[i][3] * 2
        if running_batches[i][6] == "Organic Dunkel":
            totalDunkel = totalDunkel + running_batches[i][3] * 2
        i = i + 1
        
    redHellesNeeded = redHellesNeeded - totalRedHelles
    pilserNeeded = pilserNeeded - totalPilsner
    dunkelNeeded = dunkelNeeded - totalDunkel
    
    #the biggest batch should be produced next
    if redHellesNeeded >= pilserNeeded:
        if redHellesNeeded >= dunkelNeeded:
            beerToProduce = redHellesNeeded
            beerToProduceType = "Organic Red Helles"
        else:
            beerToProduce = dunkelNeeded
            beerToProduceType = "Organic Dunkel"           
    else:
        if pilserNeeded >= dunkelNeeded:
            beerToProduce = pilserNeeded
            beerToProduceType = "Organic Pilsner"
        else:
            beerToProduce = dunkelNeeded
            beerToProduceType = "Organic Dunkel"
    
    #if all batches are 0, then there is no need for extra production
    if beerToProduce > 0:
        print("The advised next batch should be: {}, with liter quantity: {}".format(beerToProduceType, beerToProduce / 2))
    else:
        print("There is currently no need for beer to be produced!")
    
    i = 0
    appropriateTank = "Nothing"
    while i < len(tanks):
        if tanks[i][1] - tanks[i][3] >= beerToProduce / 2:
            appropriateTank = tanks[i][0]
            break
        i = i + 1
    
    #take into consideration which tank the beer should be put in    
    if appropriateTank != "Nothing" and beerToProduce > 0:
        print("Tank the beer could be put in is: {}".format(appropriateTank))
    elif beerToProduce < 0:
        print("")
    else:
        print("There is no tank that's big enough for the whole batch!")
         
    return

#main frame class to run the Interface 
class MainFrame():
    """ Class to run the tkinter object creating adequate window size.
    """
    
    def __init__(self):
        root = Tk()
        root.title('Fix.IT')
        root.geometry("1000x750")
        firstPage = Interface(root)
        root.mainloop() 

#run code
if __name__ == '__main__':
    MainFrame()
    

