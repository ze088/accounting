#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

class Record:
    """Represent a record."""
    '''using class Record is a better way since it can represent "amount of a record" 
    rather than "the third item of a tuple".
    '''
    def __init__(self, category, item, amount): #constructor: initialize the attributes
        self._category = category
        self._item = item
        self._amount = amount
        
    def __repr__(self): #called by shell to get string instead of literal to display
        return f'{self.__class__.__name__}({self._category}, {self._item}, {self._amount})'
    
    @property
    def category(self):
        return self._category #do not call self._category() because of @property decorator
    
    @property
    def item(self):
        return self._item
    
    @property    
    def amount(self):
        return self._amount


class Records:
    """Maintain a list of all the records(saved type of 'Record's) and the initial amount of money."""
    
    def __init__(self): #Read the file 'records.txt' or prompt for initial amount of money. 
        try: 
            records = [] #declare a initial list data structure to store the records
            fh = open('records.txt') 

            try: # if 'records.txt' file exist and it is not empty or error content -> read and print 'Welcome back!'
                initial_money = fh.readline() #read  first line and declare *read(): return 'str' type
                assert initial_money != '', 'empty file!' #no line is in the file -> exception: AssertionError
                initial_money = int(initial_money) # read 'initial_money\n' need to convert it to integer -> exception: ValueError
                old = fh.readlines() #read the rest line
                fh.close() #finish read file then close it

                for i in old: #append the records list
                    records.append(Record(i.split()[0], i.split()[1], int(i.split()[2]))) # exception: IndexError or ValueError 
                print('Welcome back!') #when not first time open the program   
                
            except (AssertionError, IndexError, ValueError): #handle initial_money and records variable
                sys.stderr.write('Invalid format in records.txt. Deleting the contents.\n')
                try: #"new" declare the variables
                    initial_money = int(input('How much money do you have? ')) #literal for int() with base 10
                except ValueError: # if input is not the integer number then set 0 
                    sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                    initial_money = 0  

        except FileNotFoundError: # if not find 'records.txt' file then handle -> "new" declare the variables
            try:   
                initial_money = int(input('How much money do you have? '))
            except ValueError: 
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                initial_money = 0    
        
        #Initialize the attributes (self._records and self._initial_money) from the file or user input.
        self._initial_money = initial_money 
        self._records = records 
        
    def __repr__(self): #called by shell to get string instead of literal to display
        return f'{self.__class__.__name__}({self._initial_money}, {self._records})'
    
    
    def add(self, record, categories): #update the new recoed(s) to records list
        record = record.split(', ')
        try: 
            for i, v in enumerate(record): #the reason that record saved by tuple: tuple cannot be mutable 
                #check if the category is valid
                assert categories.is_category_valid(v.split()[0]) == True,'specified category must in list of categories' 
                #if the category is valid -> convert the string into a Record instance -> add the Record into self._records
                self._records.append(Record(v.split()[0], v.split()[1], int(v.split()[2]))) 
                
        except IndexError: #index out of range: the result of input.split() cannot be split into a list of two strings
            sys.stderr.write('The format of a record should be like this: breakfast -50.\n' + 'Fail to add a record.\n')
        except ValueError: #if second string after splitting cannot be converted to integer
            sys.stderr.write('Invalid value for money.\n' + 'Fail to add a record.\n')
        except AssertionError:
            sys.stderr.write('The specified category is not in the category list.\n'                             'You can check the category list by command "view categories".\n'                              'Fail to add a record.\n')
        return self._records
    
    
    def view(self):
        '''print all the records and report the balance'''
    
        one = 'Index'
        two = 'Category'
        three = 'Description'
        four = 'Amount'
        total = self._initial_money #declare the total money

        print(f'\nHere\'s your expense and income records:') 
        print(f'{one: ^7s} {two: ^14s} {three: ^15s} {four: ^11s}')
        print('-'*7 + ' ' + '-'*14 + ' ' + '-'*15 + ' ' + '-'*10)

        for index,val in enumerate(self._records): #inorder to delete function -> specify the records by index
            print(f'{index: ^7d} {val._category:<14s} {val._item:<15s} {val._amount:<10d}')
            total += val._amount #count the total money

        print('-'*7 + ' ' + '-'*14 + ' ' + '-'*15 + ' ' + '-'*10)
        print(f'Now you have {total:_^12} dollars.')
    
    def delete(self, index):
        '''prompt for a record to delete and delete it from the record list.'''
    
        try:
            index = int(index) #input specify record index number
            del self._records[index] #delete the specified record from self._records
        except ValueError: # input invalid format in respect record
            sys.stderr.write('Invalid format. Fail to delete a record.\n')   
        except IndexError: #specified record does not exist
            sys.stderr.write(f'There\'s no record with index \'{index}\'. Fail to delete a record.\n')
                    
        return self._records
    
    
    def find(self, target_categories): 
        '''Print out the filtered records and report the total amount of money of the listed records.'''
        
        #target_categories: non-nested list (returned from find_subcategories)
        #filter: x=records._records=Record(s) filter not in target_categories
        filter_records = filter(lambda x: x._category in target_categories, records._records)

        one = 'Index'
        two = 'Category'
        three = 'Description'
        four = 'Amount'
        amount = 0 #declare the initial amount

        print(f'\nHere\'s your expense and income records under category \"{category}\": \n')
        print(f'{one: ^7s} {two: ^14s} {three: ^15s} {four: ^11s}')
        print('-'*7 + ' ' + '-'*14 + ' ' + '-'*15 + ' ' + '-'*10)

        for index, val in enumerate(filter_records):
            print(f'{index: ^7d} {val._category:<14s} {val._item:<15s} {val._amount:<10d}')
            amount += val._amount #count the all amount of filtered records in Record.amount

        print('-'*7 + ' ' + '-'*14 + ' ' + '-'*15 + ' ' + '-'*10)
        print(f'The total amount above is {amount:_^12}.')
    
    
    def save(self):
        '''write the initial money and all the records to the file 'records.txt'.'''
    
        with open('records.txt','w') as fh: #open and write in the 'records.txt' file
            fh.write(f'{self._initial_money}\n')
            record = [] #declare the local varible 'record' in order to use 'writelines()'
            for i in self._records: 
                # +'\n' because of writline cannot auto add the newline
                record.append(i._category + " " + i._item + " " + str(i._amount) + '\n') 
            fh.writelines(record) #write record into the fh 

    
class Categories:
    """Maintain the category list and provide some methods."""
    
    def __init__(self): #Initialize self._categories as a nested list
        self._cate = ['expense', ['food', ['meal', 'snack', 'drink'],                               'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
      
    
    def view(self):
        # view the totlal categories. Handle the base case and recursive case
      
        def view_inner(categories, level=0): #define an inner function to do the recursion      
            if categories == None: #if L is empty (== None) -> do nothing
                return
            if type(categories) == list: #recursive case
                for child in categories:
                    view_inner(child, level + 1) #inner layer: level=level+1 but not change the initial 'level'
            else: #base case: print the categories with indentation
                print(f'{" " * level}-{categories}')

        return view_inner(self._cate)
    
    
    def is_category_valid(self, category):
        # check the specified category that is from add function valid in predefined list categories
        
        def is_category_valid_inner(category, categories):
            if type(categories) == list: #recursive case
                for child in categories:
                    p = is_category_valid_inner(category, child)
                    if p == True: # if p == False -> do nothing
                        return True
            return categories == category #base case: boolean
        
        return is_category_valid_inner(category, self._cate)

    
    def find_subcategories(self, category): 
    #returns a non-nested list containing the specified category and all the subcategories under it (if any)
    
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found) #yield if categories == category
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                    # When the target category is found,
                    # recursively call this generator on the subcategories with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index + 1], found=True) #yield if found == True
            else:
                if categories == category or found == True:
                    yield categories        
                    
        return find_subcategories_gen(category, self._cate)

    
if __name__ == '__main__':
    
    #instantiation the initial_money, records, categories objects
    categories = Categories()
    records = Records()
    
    while True:
        command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        
        if command == 'add':
            record = input('\nAdd an expense or income record with category, description, and amount'                           '(separate by spaces):\n cate1 desc1 amt1, cate2 desc2 amt2, cate3 desc3 amt3, ...\n')
            records.add(record, categories)
            
        elif command == 'view':
            records.view()
            
        elif command == 'delete':
            delete_record = input("Which record do you want to delete? ")
            records.delete(delete_record)
            
        elif command == 'view categories':
            categories.view()
            
        elif command == 'find':
            category = input('Which category do you want to find? ')
            target_categories = [i for i in categories.find_subcategories(category)] #find the subcategories under the specify catrgory
            records.find(target_categories) #find the records under the subcategories
            
        elif command == 'exit':
            records.save()
            break
            
        else:
            sys.stderr.write('Invalid command. Try again.\n')
            
            


# In[ ]:




