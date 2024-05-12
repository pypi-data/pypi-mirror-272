import numpy_financial as npf
import os
 
'''
    list_files_in_dir :: returns a list of files in a directory
    find_nth :: find the nth occurrence of a substring in a string
    twoDecimalPlaces :: returns a number as two decimal places
    gross_payment :: returns the gross loan payment
    net_payment :: returns the net loan repayment for mortgages in the netherlands
    calculate_loan_payments :: returns the amount to repay on a loan. 

''' 
def list_files_in_dir(directory):
    filelist = []


    for root, dirs, files in os.walk(directory):
        for filename in files:
            filelist.append(os.path.join(root, filename))
    return filelist




def find_nth(haystack: str, needle: str, n: int) -> int:
    '''
        This will find the nth occurrence of a substring in a string 
    '''
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def twoDecimalPlaces(answer):
    '''
        This simply formats the input as two decimal places.
    '''
    return("%.2f" % answer)

def gross_payment(rate, nper, pv):
    '''
        
    '''
    return float(twoDecimalPlaces(npf.pmt(rate/12, nper*12, pv)))

def net_payment(grosspayment):
    return float(twoDecimalPlaces(grosspayment * (1-0.22)))

def calculate_loan_payments(rate, nper, pv):
    gp = gross_payment(rate, nper, pv)
    np = net_payment(gp)
    print('Gross payment:', gp)
    print('Net payment:', np)