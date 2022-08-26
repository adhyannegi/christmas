##########################################################################
#    Computer Project #6
#    Algorithm
#        Program that reads a CSV file
#        Puts data into master list of lists.
#        Some functions that manipulate the master list.
#        Main function that loops, promppting the user for choices.
##########################################################################

import csv
from operator import itemgetter

# Keywords used to find christmas songs in get_christmas_songs()
CHRISTMAS_WORDS = ['christmas', 'navidad', 'jingle', 'sleigh', 'snow',\
                   'wonderful time', 'santa', 'reindeer']

# Titles of the columns of the csv file. used in print_data()
TITLES = ['Song', 'Artist', 'Rank', 'Last Week', 'Peak Rank', 'Weeks On']

# ranking parameters -- listed here for easy manipulation
A,B,C,D = 1.5, -5, 5, 3

#The options that should be displayed
OPTIONS = "\nOptions:\n\t\
        a - display Christmas songs\n\t\
        b - display songs by peak rank\n\t\
        c - display songs by weeks on the charts\n\t\
        d - display scores by calculated rank\n\t\
        q - terminate the program \n"

#the prompt to ask the user for an option
PROMPT = "Enter one of the listed options: "

def get_option():
    '''
    Prompts the user for a valid option and returns it as a string.
    Parameters: None
    Returns: str
    '''
    ans = True
    while ans:
        val = input(PROMPT)
        val = val.lower()
        if val in ["a", "b", "c", "d", "q"]:    #checks if option is valid
            return val
            ans = False
        else:
            print('Invalid option!\nTry again')
            
    
def open_file():
    '''
    Prompts for a file name until a file is correctly opened.
    Parameters: None
    Returns: File Pointer
    Displays: Prompts and error messages.
    '''
    ans = True
    while ans:
        file_name = input("Enter a file name: ")
        try:
            f1 = open(file_name, "r")    #tries to open file
            return f1
            ans = False
        except FileNotFoundError:    #repeats loop if file did not open
            print('\nInvalid file name; please try again.\n')    

def read_file(fp):
    '''Reada data of file and adds data to master list.
    Parameters: File Pointer
    Returns: List of lists
    '''
    master_list=[]
    reader=csv.reader(fp)    
    next(reader,None)    #skips header line   
    for line in reader:
       for val in line:
           if val.isdigit()==True:
               num=line.index(val)
               line[num]=int(val)         
       master_list.append(line[:6])    #adds data to master list
    for i in master_list:    
        if type(i[0])!=str:    #for invalid values
            i[0]=str(i[0])
        if type(i[2])!=int:
            i[2]=-1
        if type(i[3])!=int:            
            i[3]=-1
        if type(i[4])!=int:
            i[4]=-1
        if type(i[5])!=int:
            i[5]=-1        
        
    return master_list


def print_data(song_list):
    '''
    This function is provided to you. Do not change it
    It Prints a list of song lists.
    '''
    if not song_list:
        print("\nSong list is empty -- nothing to print.")
        return
    # String that the data will be formatted to. allocates space
    # and alignment of text
    format_string = "{:>3d}. "+"{:<45.40s} {:<20.18s} "+"{:>11d} "*4
    
    # Prints an empty line and the header formatted as the entries will be
    print()
    print(" "*5 + ("{:<45.40s} {:<20.18s} " 
                   +"{:>11.9s} "*4+'\n'+'-'*120).format(*TITLES))

    # Prints the formatted contents of every entry
    for i, sublist in enumerate(song_list, 1):
        #print(i,sublist)
        print(format_string.format(i, *sublist).replace('-1', '- '))

def get_christmas_songs(master_list):
    '''Returns all songs that have a Christmas theme.
    Parameters: List of lists
    Returns: List of lists
    '''
    list1 = []
    for words in CHRISTMAS_WORDS:
        for line in master_list:
            if words in line[0].lower():    #checks if word is valid
                list1.append(line)
    list1.sort()
    return list1
            
def sort_by_peak(master_list):
    '''Sorts master list by peak rank.
    Parameters: List of lists
    Returns: List of lists'''
    for i in master_list:
        if i[4] == -1:
            master_list.remove(i)    #does not include invalid data.
    #Sorts master list based on peak rank value
    for i in range(len(master_list)-1):
        for j in range(len(master_list)-i-1):
            if master_list[j][4] > master_list[j+1][4]:       
                master_list[j],master_list[j+1]=master_list[j+1],master_list[j]       
    return master_list
    

def sort_by_weeks_on_list(master_list):
    '''Sorts master list by weeks on top 100.
    Parameters: List of lists
    Returns: List of lists'''
    for i in master_list:
        if i[5] == -1:
            master_list.remove(i)    #does not include invalid data.
    #Sorts master list based on weeks on top 100 value
    for i in range(len(master_list)-1):
        for j in range(len(master_list)-i-1):
            if master_list[j][5] < master_list[j+1][5]:      
                master_list[j],master_list[j+1]=master_list[j+1],master_list[j]    
    return master_list
        
def song_score(song):
    '''Calculates and returns soong score of a song.
    Parameters: Song (List)
    Returns: Float'''
    #Setting up curr_rank and peak_rank values
    if song[2] == -1:
        curr_rank = -100
    else:
        curr_rank = 100 - song[2]
    if song[4] == -1:
        peak_rank = -100
    else:
        peak_rank = 100 - song[4]
    
    rank_delta = song[2] - song[3]
    weeks_on_chart = song[5]
    #Calculating song score
    score = (A*peak_rank) + (B*rank_delta) + (C*weeks_on_chart) + (D*curr_rank)
    return score

def sort_by_score(master_list):
    '''Sorts master list by song score.
    Parameters: List of lists
    Returns: List of lists'''
    #Sorts master list based on song score value
    for i in range(len(master_list)-1):
        for j in range(len(master_list)-i-1):
            if song_score(master_list[j]) < song_score(master_list[j+1]):
                master_list[j],master_list[j+1]=master_list[j+1],master_list[j]        
            elif song_score(master_list[j]) == song_score(master_list[j+1]):
                if master_list[j][0] < master_list[j+1][0]:               
                    master_list[j],master_list[j+1]=master_list[j+1], master_list[j]         
    return master_list
        
    
def main():
    '''opens and reads a file and calls the other functions in a loop.'''
    
    print("\nBillboard Top 100\n")
    f1 = open_file()
    a = read_file(f1)
    count_master = 0
    for i in a:
        count_master += 1
    print_data(a)
    print(OPTIONS)
    b = get_option()
    while b != "q":
        if b == "a":
            count_christmas = 0
            c = get_christmas_songs(a)
            print_data(c)
            for i in c:
                count_christmas += 1
            if count_christmas == 0:
                print('None of the top 100 songs are Christmas songs.')
                print(OPTIONS)    
            else:
                percent = int((count_christmas*100)/count_master)
                print('\n{:d}% of the top 100 songs are Christmas songs.'\
                                                          .format(percent))
                print(OPTIONS)
        elif b == "b":
            d = sort_by_peak(a)
            print_data(d)
            print(OPTIONS)
        elif b == "c":
            e = sort_by_weeks_on_list(a)
            print_data(e)
            print(OPTIONS)
        elif b == "d":
            f = sort_by_score(a)
            print_data(f)
            print(OPTIONS)
        
        b = get_option()
    else:
        print("\nThanks for using this program!\nHave a good day!\n")
        
# Calls main() if this modules is called by name
if __name__ == "__main__":
    main()           
