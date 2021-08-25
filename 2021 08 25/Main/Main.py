
Test_Class_Card_Category: bool = False

debug: bool = False

test_SQL_entry_Multiplication = True

Number_of_Players = 4


empty_list = []
Create_Engine_Filename_Prefix = 'sqlite:///'


User_Settings_File_Location = "AppData/User_Preferences.txt"


mono_coloured = [1, 2, 4, 8, 16]
colourless = [0]
multicoloured = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]


Category = ["Monocoloured", "Colourless", "Multicoloured"]
Rarity = ["Common", "Uncommon"]


if(Test_Class_Card_Category):
    class Card_Category:
        def __init__(Self, Name: str, List_of_SQL_Queries, UI_Question: str):
            Self.Name = Name
            Self.List_of_SQL_Queries = List_of_SQL_Queries
            Self.UI_Question = UI_Question

    Monocoloured = Card_Category("Monocoloured", 0, "Wonderwall?")
    Multicoloured = Card_Category("Multicoloured", 0, "Wonderwall?")
    Colourless = Card_Category("Colourless", 0, "Wonderwall?")
    
    class Card_Rarity:
        def __init__(Self, Name: str, List_of_SQL_Queries):
            Self.Name = Name
            Self.List_of_SQL_Queries = List_of_SQL_Queries
            

class User_Preferences:
    def __init__(self, \
        Database_File_address: str, \
        Number_of_Players: int, \
        commonspercolour: int, \
        uncommonspercolour: int, \
        colourlesscommons: int, \
        colourlessuncommons: int, \
        multicolouredcommons: int, \
        multicoloureduncommons: int, \
        commonspername: int, \
        uncommonspername: int, \
        Multiply_Cards_By_Rarity: bool, \
        ):
        self.Database_File_address = Database_File_address
        self.Number_of_Players = Number_of_Players
        self.commonspercolour = commonspercolour
        self.uncommonspercolour = uncommonspercolour
        self.colourlesscommons = colourlesscommons
        self.colourlessuncommons = colourlessuncommons
        self.multicolouredcommons = multicolouredcommons
        self.multicoloureduncommons = multicoloureduncommons
        self.commonspername = commonspername
        self.uncommonspername = uncommonspername
        self.Multiply_Cards_By_Rarity = Multiply_Cards_By_Rarity
    def load(User_Settings_File_Location: str):
        f = open(User_Settings_File_Location, "r")
        import json
        x = json.load(f)
        f.close
        return User_Preferences(x[0],\
                                x[1],\
                                x[2],\
                                x[3],\
                                x[4],\
                                x[5],\
                                x[6],\
                                x[7],\
                                x[8],\
                                x[9],\
                                x[10])
    def Save(Self):
        if(debug):
            print([\
                Self.Database_File_address, \
                Self.Number_of_Players, \
                Self.commonspercolour, \
                Self.uncommonspercolour, \
                Self.colourlesscommons, \
                Self.colourlessuncommons, \
                Self.multicolouredcommons, \
                Self.multicoloureduncommons, \
                Self.commonspername, \
                Self.uncommonspername, \
                Self.Multiply_Cards_By_Rarity, \
                ])
        
        f = open(User_Settings_File_Location, "w")
        import json
        json.dump([\
            Self.Database_File_address, \
            Self.Number_of_Players, \
            Self.commonspercolour, \
            Self.uncommonspercolour, \
            Self.colourlesscommons, \
            Self.colourlessuncommons, \
            Self.multicolouredcommons, \
            Self.multicoloureduncommons, \
            Self.commonspername, \
            Self.uncommonspername, \
            Self.Multiply_Cards_By_Rarity, \
            ], f)
        f.close
        print("Preferences Successfully saved to " + User_Settings_File_Location)
    

def Generate_Card_Pool():
    global Multiply_Cards_By_Rarity

    print(Multiply_Cards_By_Rarity)
    print(Prefs.Multiply_Cards_By_Rarity)
    
    if(Multiply_Cards_By_Rarity):
        commonspername = Prefs.commonspername
        uncommonspername = Prefs.uncommonspername
    else:
        commonspername = 1
        uncommonspername = 1
    
    
    Create_Engine_Imput = Create_Engine_Filename_Prefix + Prefs.Database_File_address.replace('/', '\\')
        
    from sqlalchemy import create_engine
    engine = create_engine(Create_Engine_Imput)

    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

    from sqlalchemy import Column, Integer, String

    Base.metadata.create_all(engine)

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)

    sess = Session()


    class SQL_Entry(Base):
            __tablename__ = 'cardsieboi'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            rarity = Column(Integer)
            colour = Column(Integer)


    def outerloop(colourcode: int, raritycode: int, Rarity_Multiplication_Factor: int, Cards_Per_Player_In_This_Category: int, Number_of_Players: int):
        for Card_in_Category_Rarity in sess.query(SQL_Entry).filter_by(colour = colourcode).filter_by(rarity = raritycode):
            for Rarity_Multiplication_Counter in list(range(Rarity_Multiplication_Factor)):
                tempmap.append(Card_in_Category_Rarity.name)
        printloop(tempmap, Cards_Per_Player_In_This_Category, Number_of_Players)
        tempmap.clear()
    
    def printloop(thelist: list, nmax, Number_of_Players: int):
        for Player_Counter in range(Prefs.Number_of_Players):
            print("p" + str(Player_Counter))
            for Card_in_Category_Rarity_Counter in list(range(nmax)):
                thelist = innerprintloop(thelist)
            print("\n")

    def innerprintloop(thelist: list):
        print(thelist.pop(random.randrange(len(thelist))))
        return thelist

    def Muticolourouterloop(raritycode: int, Rarity_Multiplication_Factor: int, Cards_Per_Player_In_This_Category: int, Number_of_Players: int):
        for colourcode in multicoloured:
            for Card_in_Category_Rarity in sess.query(SQL_Entry).filter_by(colour = colourcode).filter_by(rarity = raritycode):
                for Rarity_Multiplication_Counter in list(range(Rarity_Multiplication_Factor)):
                    tempmap.append(Card_in_Category_Rarity.name)
        printloop(tempmap, Cards_Per_Player_In_This_Category, Number_of_Players)
        tempmap.clear()
    
    import random

    tempmap = empty_list

    for colourcode in mono_coloured:
        if(Prefs.commonspercolour):
            outerloop(colourcode, raritycode = 0, Rarity_Multiplication_Factor = Prefs.commonspername, Cards_Per_Player_In_This_Category = Prefs.commonspercolour, Number_of_Players = Prefs.Number_of_Players)
        if(Prefs.uncommonspercolour):
            outerloop(colourcode, raritycode = 1, Rarity_Multiplication_Factor = Prefs.uncommonspername, Cards_Per_Player_In_This_Category = Prefs.uncommonspercolour, Number_of_Players = Prefs.Number_of_Players)

    for colourcode in colourless:
        if(Prefs.colourlesscommons):
            outerloop(colourcode, raritycode = 0, Rarity_Multiplication_Factor = Prefs.commonspername, Cards_Per_Player_In_This_Category = Prefs.colourlesscommons, Number_of_Players = Prefs.Number_of_Players)
        if(Prefs.colourlessuncommons):
            outerloop(colourcode, raritycode = 1, Rarity_Multiplication_Factor = Prefs.uncommonspername, Cards_Per_Player_In_This_Category = Prefs.colourlessuncommons, Number_of_Players = Prefs.Number_of_Players)

    if(Prefs.multicolouredcommons):
        Muticolourouterloop(raritycode = 0, Rarity_Multiplication_Factor = Prefs.commonspername, Cards_Per_Player_In_This_Category = Prefs.multicolouredcommons, Number_of_Players = Prefs.Number_of_Players)
    if(Prefs.multicoloureduncommons):
        Muticolourouterloop(raritycode = 1, Rarity_Multiplication_Factor = Prefs.uncommonspername, Cards_Per_Player_In_This_Category = Prefs.multicoloureduncommons, Number_of_Players = Prefs.Number_of_Players)


def File_From_Address(Database_File_address: str):
    return(Database_File_address[len(Database_File_address)-Database_File_address[len(Database_File_address)::-1].find('/',0,len(Database_File_address)):len(Database_File_address)])

def locatedatabase():
    dummy = File_Ask_Box()

    while((dummy != "") and (dummy[len(dummy)-3: len(dummy)] != ".db")):
        dummy = File_Ask_Box()
    if(dummy != ""):
        var0.set(File_From_Address(dummy))
        Prefs.Database_File_address = dummy

def File_Ask_Box():
    from tkinter import filedialog
    return tkinter.filedialog.askopenfilename()

def howmany(colour_name, rarity_name):
    dummy = Integer_Ask_Box(colour_name, rarity_name)
    while((dummy == None) or ((type(dummy) == int) and (dummy <= 0))):
        dummy = Integer_Ask_Box(colour_name, rarity_name)
    return dummy

def Integer_Ask_Box(colour_name, rarity_name):
    from tkinter import simpledialog
    return tkinter.simpledialog.askinteger(colour_name + " " + rarity_name, "How many " + colour_name + " " + rarity_name + " would you like each player to have?")

def question(Category: str, Rarity: str):
    return "How many " + Category + " " + Rarity + " cards would you like per player?"

def SQL_Askbox(rarity_name):
    from tkinter import simpledialog
    return tkinter.simpledialog.askinteger(rarity_name, "How many " + rarity_name + " cards per SQL entry would you like in the card pool?")

def How_Many_SQL_Rarity(rarity_name):
    dummy = SQL_Askbox(rarity_name)
    while((dummy == None) or ((type(dummy) == int) and (dummy <= 0))):
        dummy = SQL_Askbox(rarity_name)
    return dummy

def Category_Rarity_UI_loop(variables, functions):
    variable_function_counter = 0
        
    for Category_Counter in range(len(Category)):
        Frame_Child = Frame(root)
        Frame_Child.pack(pady=Space_Between_Categories)
            
        for Rarity_Counter in range(len(Rarity)):
            Frame_Grandchild = Frame(Frame_Child)
            Frame_Grandchild.pack(pady=0)
            Display_Category_Rarity = Label(Frame_Grandchild, text = question(Category[Category_Counter], Rarity[Rarity_Counter]))
            Display_Category_Rarity.pack()

            Frame_Great_Grandchild = Frame(Frame_Grandchild)
            Frame_Great_Grandchild.pack()
            Display_Value = Label(Frame_Great_Grandchild, textvariable = variables[variable_function_counter])
            Display_Value.pack(side=LEFT)
            Button_Value = Button(Frame_Great_Grandchild, text = Change_Value_Button_Text, command=functions[variable_function_counter])
            Button_Value.pack()
                
            variable_function_counter = variable_function_counter + 1
 
def SQL_Multiplyer_Rarity_UI_loop(variables, functions):
    Frame_Child = Frame(root)
    Frame_Child.pack()

    Tickbox_Multiply_By_Rarity = tkinter.Checkbutton(Frame_Child, text="Multiplying card by Rarity?", variable=Prefs.Multiply_Cards_By_Rarity, onvalue=TRUE, offvalue=FALSE)
    Tickbox_Multiply_By_Rarity.pack(pady=10)
    if(Prefs.Multiply_Cards_By_Rarity):
        Tickbox_Multiply_By_Rarity.select()

    Frame_Grandchild = Frame(Frame_Child)
    Frame_Grandchild.pack()

    variable_function_counter = 0
        
    for Rarity_Counter in range(len(Rarity)):
        Display_Common_Multiplication = Label(Frame_Grandchild, text = "How many " + Rarity[Rarity_Counter] + " per SQL entry would you like?")
        Display_Common_Multiplication.pack()
            
        Frame_Great_Grandchild = Frame(Frame_Grandchild)
        Frame_Great_Grandchild.pack()
        Display_Value = Label(Frame_Great_Grandchild, textvariable = variables[variable_function_counter])
        Display_Value.pack(side=LEFT)
        Button_Value = Button(Frame_Great_Grandchild, text = Change_Value_Button_Text, command=functions[variable_function_counter])
        Button_Value.pack()

        variable_function_counter = variable_function_counter + 1

def Player_Askbox():
    from tkinter import simpledialog
    return tkinter.simpledialog.askinteger("Number of Players", "How many players?")

def How_Many_Players():
    dummy = Player_Askbox()
    while(dummy <= 0):
        dummy = Player_Askbox()
    return dummy


def cpc():
    Prefs.commonspercolour = howmany("Monocoloured", "Commons")
    var2.set(Prefs.commonspercolour)
def upc():
    Prefs.uncommonspercolour = howmany("Monocoloured", "Uncommons")
    var3.set(Prefs.uncommonspercolour)
def cllc():
    Prefs.colourlesscommons = howmany("Colourless", "Commons")
    var4.set(Prefs.colourlesscommons)
def cllu():
    Prefs.colourlessuncommons = howmany("Colourless", "Uncommons")
    var5.set(Prefs.colourlessuncommons)
def mltc():
    Prefs.multicolouredcommons = howmany("Multicoloured", "Commons")
    var6.set(Prefs.multicolouredcommons)
def mltu():
    Prefs.multicoloureduncommons = howmany("Multicoloured", "Uncommons")
    var7.set(Prefs.multicoloureduncommons)

def cpn():
    Prefs.commonspername = How_Many_SQL_Rarity("Commons")
    var8.set(Prefs.commonspername)
def upn():
    Prefs.uncommonspername = How_Many_SQL_Rarity("Uncommons")
    var9.set(Prefs.uncommonspername)


Prefs = User_Preferences.load(User_Settings_File_Location)

Multiply_Cards_By_Rarity: bool = Prefs.Multiply_Cards_By_Rarity

import tkinter
from tkinter import *

root = tkinter.Tk()
root.title("Sealed Pool Generator")
root.geometry("600x800")

Change_Value_Button_Text = "change"
Space_At_Top = 20
Space_Between_Super_Categories = 15
Space_Between_Categories = 5


var0 = StringVar()
var0.set(File_From_Address(Prefs.Database_File_address))


Frame_Child = Frame(root)
Frame_Child.pack(pady = Space_At_Top)
Ask_Label_Select_File = Label(Frame_Child, text = "Which SQL file would you like to use?")
Ask_Label_Select_File.pack()
Button_Select_Database = Button(Frame_Child, text = "Browse", command = locatedatabase)
Button_Select_Database.pack()
Display_File = Label(Frame_Child, textvariable = var0)
Display_File.pack()



var1 = StringVar()
var1.set(Prefs.Number_of_Players)

Frame_Grandchild = Frame(Frame_Child)
Frame_Grandchild.pack(pady = Space_Between_Categories)

def NoP():
    Prefs.Number_of_Players = How_Many_Players()
    var1.set(Prefs.Number_of_Players)

def Generate_How_Many_Players_Button():
    Header = Label(Frame_Grandchild, text = "How many players?")
    Header.pack()
            
    Frame_Great_Grandchild = Frame(Frame_Grandchild)
    Frame_Great_Grandchild.pack()
    Display_Value = Label(Frame_Great_Grandchild, textvariable = var1)
    Display_Value.pack(side=LEFT)
    Button_Value = Button(Frame_Great_Grandchild, text = Change_Value_Button_Text, command = NoP)
    Button_Value.pack()


Generate_How_Many_Players_Button()


var2 = StringVar()
var2.set(Prefs.commonspercolour)
var3 = StringVar()
var3.set(Prefs.uncommonspercolour)
var4 = StringVar()
var4.set(Prefs.colourlesscommons)
var5 = StringVar()
var5.set(Prefs.colourlessuncommons)
var6 = StringVar()
var6.set(Prefs.multicolouredcommons)
var7 = StringVar()
var7.set(Prefs.multicoloureduncommons)
    

Category_Rarity_UI_loop([var2, var3, var4, var5, var6, var7], [cpc, upc, cllc, cllu, mltc, mltu])


var8 = StringVar()
var8.set(Prefs.commonspername)
var9 = StringVar()
var9.set(Prefs.uncommonspername)


SQL_Multiplyer_Rarity_UI_loop([var8, var9], [cpn, upn])




Button_Run_Main = Button(root, text = "Run Programme", command = Generate_Card_Pool)
Button_Run_Main.pack(pady = Space_Between_Super_Categories)

Button_Save_Preferences = Button(root, text = "Save Preferences", command = Prefs.Save)
Button_Save_Preferences.pack(pady = Space_Between_Categories)

root.mainloop()


