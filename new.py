# coding: latin-1
import sys
import datetime


# Get the Month Day Year into string_date. 
# This is printed at the very bottom of the output.
now = datetime.datetime.now()
string_date = now.strftime("%b %d %Y")
#print(string_date)  



# array of afg classes.    One afg class per Austin area AFG
afglist=[]


def getzip(address):
    # get zip code from address.
    # for example, if address is
    #  14181 FM 306, Canyon Lake, TX, 78133, USA
    # address can be any length. So
    # chop off the last 12 chars at the end 
    # , 78133, USA
    # then return characters 2-7 of that
    last12=address[-12:]  # last 12 characters 
    zip = last12[2:7]
    # TO DO: check that zip is numerical before returning
    #     ELSE return ""
    if zip.isdigit():
         return (zip)
    else:     
         return ("99999")


def isnewrecord(the_line):
    if ( clean_line.endswith("AFG")  or clean_line.endswith("GFA") or \
       ( "Alateen" in the_line  and (len(clean_line) > 8) ) ):
        return True
    else:
        return False
    




def isinafglist(afglist, thename, zipcode):
#  Determines if thename and its zipcode  are already in the afglist array.
#  If it is, return the index of where it was found in the array,
#  It it wasn't, return -1
#   (Added zipcode as additional test ites because two groups in Austin area
#    have the same name of "Courage to chage AFG" )
    #print ("inside isinafglist")
    myindex = -1
    for item in afglist:
       myindex = myindex +1
       #print (item.name)
       #print ("Checking for " + thename + " against " + item.name )
       if ( (item.name == thename) and (item.zip == zipcode) ) :
          #print ("FOUND IT " + str(myindex) ) 
          return (myindex)
    return(-1)      
                    

class afg:
    # The constructor method initialized when a new object is made
    def __init__(self, name, loc, addr, special):
        self.name = name    # Instance attribute
        self.loc = loc  # Instance attribute
        self.addr = addr
        self.special = special # such as :room 161" or "under tree"
        self.zip = ""   # zipcode
        self.area = "??"  # general area where meeting is e.g., North, South, West, etc
        self.isaustin = 0
        self.sun = ""
        self.mon = ""
        self.tue = ""
        self.wed = ""
        self.thu = ""
        self.fri = ""
        self.sat = ""

    # A custom method defining object behavior
    def bark(self):
        return f"{self.name} says Woof!"
        
    def changename(self, newname):
        self.name = newname
        
    def chgsun(self, addit):
        self.sun = self.sun + addit      
        
    def chgmon(self, addit):
        self.mon = self.mon + addit
        
    def chgtue(self, addit):
        self.tue = self.tue + addit        
        
    def chgwed(self, addit):
        self.wed = self.wed + addit      
        
    def chgthu(self, addit):
        self.thu = self.thu + addit
        
    def chgfri(self, addit):
        self.fri = self.fri + addit        
        
    def chgsat(self, addit):
        self.sat = self.sat + addit      




# dictionary to translate zip code to its geneneral austin area
areas = {
    "78759": "N",
    "78758": "N",
    "78757": "C",
    "78756": "C",      # 78756 incorrectly specified for northland Alateen zip
    "78752": "C",
    "78750": "NW",
    "78749": "S",
    "78746": "W",
    "78745": "S",
    "78731": "W",
    "78729": "NW",
    "78723": "E",
    "78704": "S",
    "78701" : "C"
}

# dictionary to translate zip code to areas OUTSIDE of Austin area
outsideareas = {
    "78645": "LV",  # Lago Vista
    "78738": "LT",  # Lake Travis
    "78610": "BU",  # Buda
    "78641": "LE",  # Leander
    "78664": "RR",  # Round Rock
    "78681": "RR",  # Round Rock
    "78633": "GT",  # Georgetown
    "78626": "GT",  # Georgetown
    "78628": "GT",  # Georgetown
    "78660": "PF",  # Pflugerville
    "78620": "DS",  # Dripping Springs
    "78734": "LW",  # Lakeway
    "76504": "TE",  # Temple
    "99999": "ZM"   # ZOOM
}


#print spreadsheet header
#print ("GROUP,DSORT,DAY,TIME,LOCATION,ADDRESS")


# the number of AFG groups found so far
num_groups = 0

# after finding an AFG group, i is line count 
# of the input data within that AFG group.
i = 0

# Globals
csvline=""
s=""
DAY=""
TIME=""
LOC=""
ADDR=""
women=""
Allcaps = ""
zoom=""
chair=""
new=""
span=""
room=""
zipcode=""
haveaddr = 0
special =""  # used only if Hilltoppers or tree group


#with open("mdatashort.txt", "r") as file:
#with open("mdata.txt", "r") as file:
#with open("mdata50.txt", "r") as file:
with open("mdatanew.txt", "r") as file:


    for line in file:
    
       
        # remove the trailing newline character from each line
        clean_line = line.rstrip("\n")
        #clean_line = clean_line[:55]    # chop off line
        
        # Line ending in AFG or GFA means new group, or Alateen 
        if isnewrecord(clean_line):

             i = 0  
             women=""
             zoom=""
             chair=""
             new=""
             room=""
             span=""
             haveaddr = 0   # because of the line 5 or 7 ambiguity for address
                            # set haveaddr =1 when we have the address field 
             special = ""               
       
        i = i + 1     # i is the line number within that AFG's record
        # look at the lines after AfG was found up until WSO is found
        
        #print ("processing line number " + str(i))
        #print (line)
        #print


       
        if ( clean_line != ""):
        
              Allcaps =  clean_line.upper()
             
            
              #print ( "     " + str(i) + "    " + clean_line)
              #myflag=0  # myflag indicates Day of week 

              if ("ZOOM" in Allcaps and csvline != ""):
                      zoom=" Z"
                      #zoom="\n ZOOM available. See NOTE."            
                      
            
              # set the sort ordinal s for the day to  0=sun, 1=mon, etc.
              # get DAY and TIME
              if (i==3):   # line 3 is Day time e.g. "Thursday 6:00 PM"
                  # Get day of week
                  first_three = clean_line[:2]
                  upper_three = first_three.upper()
                  if (upper_three == "SU"):
                     s=0
                  if (upper_three == "DO"):  # Domingo
                     s=0                     
                  if (upper_three == "MO"):
                     s=1   
                  if (upper_three == "LU"):  #Lunes
                     s=1                     
                  if (upper_three == "TU"):
                     s=2
                  if (upper_three == "MA"):  # Martes
                     s=2                     
                  if (upper_three == "WE"):
                     s=3   
                  if (upper_three == "MI"):  # Miércoles
                     s=3                      
                  if (upper_three == "TH"):
                     s=4  
                  if (upper_three == "JU"):  # Jueves
                     s=4  
                  if (upper_three == "FR"):
                     s=5
                  if (upper_three == "VI"):  # Viernes
                     s=5
                  if (upper_three == "SA"): 
                     s=6 
                  if (upper_three == "SÁ"): # Sabado
                     s=6                     
                     
                  # "Thursday 6:00 PM"  split into DAY and TIME 
                  splitstuff = clean_line.split()
                  DAY=splitstuff[0]
                  if (len(splitstuff) > 1 ): 
                      if (splitstuff[2] == "PM"):
                          TIME=splitstuff[1]   # OMIT "PM" as most times are PM
                      else:    
                          #TIME=splitstuff[1] + splitstuff[2]  # keep "AM"
                          TIME=splitstuff[1] + "am"
                     
              
              # Location name (e.g., "Clifford St Church") is usually line 5 and
              # Address (e.g. "6438 West 5th St, Austin, TX 78759 USA") is usually line 7.
              # However, occasionally location name is omitted on a couple
              # of groups.  If so, the address is line 5 (and we ignore line 7).
              
              # handle special case where address is line 5
              if ( clean_line.endswith("USA") and (i==5) and (haveaddr == 0) ):
                   #print (clean_lin
                   ADDR = clean_line
                   LOC = ""
                   haveaddr = 1

              if  ( (i==5) and (haveaddr == 0) ):  # get location 
                   LOC = clean_line 

              if  ( (i==7) and (haveaddr == 0) ):  # get address
                   if clean_line.endswith("USA"):
                      ADDR = clean_line
                   else:
                      ADDR = ""

              if (i > 7): 
                  
                  if ("WOMEN" in Allcaps and csvline != ""):
                      women=" Wo"
                      #women="\n Women Only."                      
                      
                  if ((Allcaps == "MEN") and (csvline != "") ): 
                      women=" Mo"
                      #women="\n Men Only."
                      
                  if ("LGBTQIA" in Allcaps and csvline != ""):
                      women=" G"
                      #women="\n LGBTQIA+ welcoming."                    
                      
                  if ("BEGINNER" in Allcaps and csvline != ""):
                       new=" Nc"
                       #new="\n Newcomers"
                       
                  if ("ESPA" in Allcaps and csvline != ""):
                       span=" E"
                       #new="\n Spanish Language."   
                       
                  if ("ALATEEN" in Allcaps  and csvline != ""):
                       women=" At"
                       
                       
                  #if ("CHAIR" in Allcaps and csvline != ""):
                  #    #chair="\n We meet under the tree. Bring a chair." 
                  #    chair=" T"                      
                  #     
                  #if ("ROOM 161" in Allcaps and csvline != ""):
                  #     #room="\n Room 161." 
                  #     room= " Rm"
                  #if ("ROOM A" in Allcaps and csvline != ""):
                  #     #room="\n Room 161."
                  #     room= " Rm"
                                    
                 

        # Assemble all the fields collected and print the final line.                      
        if ( clean_line[:3] == "WSO" ):   #WSO ID mmmm  is at the very end of each group's info
            #csvline = csvline + "," + str(s) + "," + DAY + "," + TIME + ",\"" +  LOC + "\",\"" + ADDR + women + zoom +  chair + new + span + "\""
            #print (csvline)
            zipcode = getzip(ADDR)
            ADDR = ADDR[:-16]   # chop off ", TX, 78133, USA"
            
            if (csvline == "Hilltoppers AFG"):
                special = "  Room 161"
            if (csvline == "The Tree AFG") or (csvline == "The Tree2 AFG"):
                special = "  Meet under tree, bring a chair"  
                
            new_afg = afg(csvline,LOC,ADDR,special)
            new_afg.zip = zipcode
            
            
            # is this an austin location?
            if zipcode in areas:
                 new_afg.area = areas[zipcode]   # found  so set area based on zip code.  e.g.  area = N if zip = 78759
                 new_afg.isaustin = 1
            if zipcode in outsideareas:
                 new_afg.area = outsideareas[zipcode]   # found  so set area based on zip code.  e.g.  area = N if zip = 78759
                 new_afg.isaustin = 0    
                 
            
            
            attribs = women + zoom +  new + span
            daytime = TIME + attribs + "\n"  # apace at end for next time if any
            if (s == 0):
                  new_afg.chgsun(daytime)
            if (s == 1):
                  new_afg.chgmon(daytime)
            if (s == 2):
                  new_afg.chgtue(daytime)
            if (s == 3):
                  new_afg.chgwed(daytime) 
            if (s == 4):
                  new_afg.chgthu(daytime)
            if (s == 5):
                  new_afg.chgfri(daytime)
            if (s == 6):
                  new_afg.chgsat(daytime)
                  
                  
            testname=csvline
            rc=isinafglist(afglist, testname, zipcode)
            if (rc == -1):
                #print (testname + " NOT found")
                afglist.append(new_afg)
            else: 
                #print (testname + " found at " + str(rc) ) 
                if (s == 0):
                      afglist[rc].sun = afglist[rc].sun + " " + daytime
                if (s == 1):
                      afglist[rc].mon = afglist[rc].mon + " " + daytime
                if (s == 2):
                      afglist[rc].tue = afglist[rc].tue + " " + daytime
                if (s == 3):
                      afglist[rc].wed = afglist[rc].wed + " " + daytime 
                if (s == 4):
                      afglist[rc].thu = afglist[rc].thu + " " + daytime
                if (s == 5):
                      afglist[rc].fri = afglist[rc].fri + " " + daytime
                if (s == 6):
                      afglist[rc].sat = afglist[rc].sat + " " + daytime                

            
   
            
        # get the name of the AFG or Alateen group 
        if isnewrecord(clean_line):
            #print (clean_line)
            csvline = clean_line
            num_groups = num_groups +1

########################
# Begin Printout Section
########################

#print spreadsheet header.  
print ("AREA,                          AUSTIN AL-ANON GROUPS,SUN,MON,TUE,WED,THU,FRI,SAT")

#  Print out 

for item in afglist:
    if (item.isaustin == 1): 
        firstline = item.name.upper() + "   " + item.loc 
        firstline = firstline[:66]
        
        secondline = item.addr + " " + item.zip + " " + item.special
        secondline = secondline[:66]
        
        afginfo = "\"" + firstline + "\n  " + secondline + "\""
        
        
        #afginfo = "\"" + item.name.upper() + "   " + item.loc + "\n  " + item.addr + " " + item.zip + " " + item.special + "\""

        
        
        #print (firstline)
        #print (secondline)
        #print (afginfo)
        #sys.exit()

        afginfo = item.area + "," + afginfo
        sun= "\"" + item.sun + "\""
        mon= "\"" + item.mon + "\""
        tue= "\"" + item.tue + "\""
        wed= "\"" + item.wed + "\""  
        thu= "\"" + item.thu + "\""
        fri= "\"" + item.fri + "\""    
        sat= "\"" + item.sat + "\""    
    
        meetings = sun + "," + mon + "," + tue + "," + wed + "," + thu + "," + fri + "," + sat
        afginfo = afginfo + "," + meetings
        print (afginfo)
        
 

print (",AL-ANON GROUPS OUTSIDE OF AUSTIN,SUN,MON,TUE,WED,THU,FRI,SAT")

# print the information about meetings outside of Austin        
for item in afglist:        
    if (item.isaustin == 0): 
        firstline = item.name.upper() + "   " + item.loc 
        firstline = firstline[:66]
        
        secondline = item.addr + " " + item.zip + " " + item.special
        secondline = secondline[:66]
        
        afginfo = "\"" + firstline + "\n  " + secondline + "\""
        
        
        #afginfo = "\"" + item.name.upper() + "   " + item.loc + "\n  " + item.addr + " " + item.zip + " " + item.special + "\""

        
        
        #print (firstline)
        #print (secondline)
        #print (afginfo)
        #sys.exit()

        afginfo = item.area + "," + afginfo
        sun= "\"" + item.sun + "\""
        mon= "\"" + item.mon + "\""
        tue= "\"" + item.tue + "\""
        wed= "\"" + item.wed + "\""  
        thu= "\"" + item.thu + "\""
        fri= "\"" + item.fri + "\""    
        sat= "\"" + item.sat + "\""    
    
        meetings = sun + "," + mon + "," + tue + "," + wed + "," + thu + "," + fri + "," + sat
        afginfo = afginfo + "," + meetings
        print (afginfo)        
    

   





# Print trailer information            
#print ("\n,The number of Groups = " + str(num_groups))
print ("\n, list created " + string_date )
print ("\n,Shows meetings 25 miles of central Austin 78705.")

#print ("\n\n,  NOTE: This is not an official")
#print (",publication of Al-Anon or any of its groups.")
#print (",Some details were omitted for brevity. For com-")
#print (",plete meeting information see Al-Anon website")
#print (",https://al-anon.org/al-anon-meetings")

#print ("\n\n,A printable file (pdf) of this list is available on")
#print (",https://myalanon.github.io") 


#zz=len(afglist)
#print ("length =  " + str(zz) )


#for item in afglist:
#      print (item.name)
#      print (item.loc)
#      print (item.addr)
#      print  (item.zip)
#      print ("attribs: " + item.attribs)
#      print ("sun: " + item.sun)  
#      print ("mon: " + item.mon)      
#      print ("tue: " + item.tue) 
#      print ("wed: " + item.wed)  
#      print ("thu: " + item.thu)      
#      print ("fri: " + item.fri)   
#      print ("sat: " + item.sat)       
#      print ()
#
#print ()
#zz=len(afglist)
#print ("length =  " + str(zz) )


