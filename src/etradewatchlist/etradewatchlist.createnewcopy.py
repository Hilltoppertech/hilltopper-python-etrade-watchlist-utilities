'''
Created on Jan 3, 2017

@author: HilltopperTech.com

# hilltopper-python-etrade-watchlist-utilities

**Description:**
- What does this project's python script do?:
    - This python script supports step #2 of the workflow described below to be used to create a new watchlist in Etrade based upon an old downloaded watchlist.
    - This python script reformats the old watchlist so that the output can be used to create a new watchlist with the same stock symbol tickers in Etrade.
- When to use this workflow:
    - When the Etrade account holder wants to create a new watchlist in order to evaluate the performance of an existing watchlist's stocks starting with the current date

**Overview of the entire workflow:**
- Perform these steps in order to create a new watchlist in Etrade based upon an old downloaded watchlist:
    - Step #1: (a manual process)
        - The Etrade account holder manually downloads 1 or more existing Etrade .csv watchlists into a single directory to be used as input to this python script
    - Step #2: (an automated process)
        - Execute this python script:
            - Read each downloaded Etrade watchlist file's stock ticker symbols
            - Write each set of input stock ticker symbols to a new output watchlist file & optionally set the output filename to include a datestamp
    - Step #3: (a manual process)
        - The Etrade account holder can use the output watchlist file content to:
            - Copy and paste the new output filename as the new new Etrade watchlist name (omit the trailing .csv and .txt suffixes)
            - Paste the output watchlist ticker symbols into the new watchlist
            - Utilize Etrade's 'pre-fill w/ default values' functionality to populate the purchase price as the current day's price
            - Save the new watchlist

**Python script usage:**
- Command line: <this python scriptname> <arg#1 name> <arg#1 value> <arg#2 name> <arg#2 value> <arg#3 name> <arg#3 value> ...
    - Arg #1: --arg_str_inputdirpath "<dir path w/ surrounding double quotes and w/ double forward slashes in the path>"
        - Description: required input directory path name string for accessing the set of input csv files. Type=string, case sensitive.
        - Example:  <this python scriptname> --arg_str_inputdirpath  "C://Etrade//WatchlistDownloads//20160701"
    - Arg #2: --arg_int_writenumberoftickersperrow 10
        - Description: required integer/number of tickers to be writen per output csv file line before a newline is written. Type=integer,{1-200}.
        - Example:  <this python scriptname> <arg#1 name> <arg#1 value> --arg_int_writenumberoftickersperrow 10
    - Arg #3: --arg_str_output_enable_filename_datestamping True
        - Description: required {True, False} string to specify if the output filename should include a current date YYYYMMDD timestamp. Type=string,{True,False}, case insensitive.
        - If the input filename DOES included a YYYYMMDD datestamp, then that value will be replaced w/ the current YYYYMMDD datestamp.
        - If the input filename DOES NOT include a YYYYMMDD datestamp, then the current YYYYMMDD datestamp will be added before the '.csv' in the filename.
        - Example:  <this python scriptname> <arg#1 name> <arg#1 value> <arg#2 name> <arg#2 value> --arg_str_output_enable_filename_datestamping True

**Python script design:**
- For each downloaded Etrade watchlist .csv file in the user provided input directory:
  - Step 1, input files:
    - Refer to the design notes for the input file filename & format requirements.
    - Read an input arg for the input directory path name where the set of input .csv files have been downloaded
    - Change to the input directory
    = Read the file list and create a list of all input .csv files in the user specified directory
  - Step 2, input .csv file processing:
    - Read each .csv file in the user provided input directory
    - Create a list of all the ticker symbols
      - Locate the Etrade provided token 'Symbol' in column 1
      - Read all ticker symbols in column 1 up to the next blank line or the Etrade provided token 'Generated'
  - Step 3, output directory & files:
    - Directory: create a new 'PythonreformattedoutputYYYYMMDD' subdirectory under the input directory for all the output files
    - Output files: Write 1 .txt file per input .csv file w/ a user specified number of ticker symbols written per line & each symbol separated by commas & no comma after the last symbol
    - Output filenames:
       - The output filename will always have the '.txt. suffix appended
       - Refer to the design notes for optional 'output filename datestamp' processing that can create an output filename based upon the input filename that WILL include the current date as YYYYMMDD.

**Python script design notes:**
- 'Output filename datestamping' functionality:
    - The objective is to create an output filename that can be copied/used in Etrade's watch create workflow as a new unique watchlist name.
        - When enabled, there are 2 scenarios:
            - The input filename's YYYYMMDD datestamp is replaced:
                - If the input/downloaded csv filename includes a YYYYMMDD datestamp, then the old datestamp will be replaced with the new current datestamp.
                - E.g.:
                    - Input/old watchlist & filename:   'Vanguard 20160128' 'Vanguard 20160128.csv'
                    - Output/new watchlist & filename:  'Vanguard 20170103' 'Vanguard 20170103.csv.txt'
            - If the input filename does not include a YYYYMMDD datestamp, then the output filename will include the input filename plus both 1) the new current datestamp inserted before '.csv' and 2) '.txt' appended
                - E.g.:
                - Input/old watchlist & filename:  'Vanguard' 'Vanguard.csv'
                - Output/new watchlist & filename: 'Vanguard20170103' 'Vanguard20170123.csv.txt'
        - When disabled:
            - The output filename will be the same as the input filename with '.txt' appended
                - E.g.:
                - Input/old watchlist & filename:  'Vanguard 20160128' 'Vanguard 20160128.csv'
                - Output/new watchlist & filename: 'Vanguard 20160128' 'Vanguard 20160128.csv.txt'
- Input file filename & format requirements:
    - Format requirements:
        - In Etrade, when downloading the original/input Etrade csv watchlist, specify a view such as 'Summary - Market View' that will print the ticker symbols in the 1st column of the .csv file
            - E.g.: sample input file content...
            - Watch List Name
            - Vanguard 20160128
            - View Summary - Market View
            - Symbol    Last Price $    Change $    Change %    Price When Added    Date Added    Change since Added %    Volume
            - CCYIX    38.02    0.11    0.29    36.48     01/28/2016    4.22    0
            - ...
            - VSCPX    178.28    -0.68    -0.38    137.25     01/28/2016    29.89    0
            - Generated at 01/03/2017 11:01:48 AM ET
    - Filename requirements:
        - In Etrade, after initiating the original/input Etrade csv watchlist download, verify that the filename type/suffix is '.csv'
'''

if __name__ == '__main__':
    pass

import csv
import glob
import os, os.path, errno
import re

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------
# Variables: command line arg related
# ---------------------------------------------------------------------------------------------------
commandline_args = None  # Set: commandline_args_setup(); Args subsequently parsed & set

# ---------------------------------------------------------------------------------------------------
# Variables: Input file, read related
# ---------------------------------------------------------------------------------------------------
input_filename = ''
input_csvfilename_list = []  # From directory name listing
input_filenumber = 0
input_file_row_list = []
ticker_list = []

# ---------------------------------------------------------------------------------------------------
# Variables: Output file, write related
# ---------------------------------------------------------------------------------------------------
output_dirpath = ''
output_dirpath_suffix = ''
output_filename = ''


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Functions: Command line related
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
def commandline_args_setup():
    import argparse

    commandline_args_token_list = ["--arg_str_inputdirpath", \
                                   "--arg_int_writenumberoftickersperrow", \
                                   "--arg_str_output_enable_filename_datestamping"]
    parser = argparse.ArgumentParser()
    parser.add_argument(commandline_args_token_list[0],
                        help="required input directory path name string for accessing the set of input csv files. Type=string, case sensitive.",
                        type=str)
    parser.add_argument(commandline_args_token_list[1],
                        help="required integer/number of tickers to be writen per output csv file line before a newline is written. Type=integer,{1-200}.",
                        type=int)
    parser.add_argument(commandline_args_token_list[2], help="required {True, False} string to specify if the output filename should include a current date YYYYMMDD timestamp. Type=string,{True,False},case insensitive.\
    - If the input filename DOES included a YYYYMMDD datestamp, then that value will be replaced w/ the current YYYYMMDD datestamp.\
    - If the input filename DOES NOT include a YYYYMMDD datestamp, then the current YYYYMMDD datestamp will be added before the '.csv' in the filename.",
                        type=str)
    commandline_args = parser.parse_args()

    error_exitrequired_flag = False

    # -----------------------------------------------------
    # Required input directory path name
    # -----------------------------------------------------
    if commandline_args.arg_str_inputdirpath:
        pass
    else:
        print('Error, exiting. Specify the required command line entry =', commandline_args_token_list[0],
              ' to specify the input directory path name for accessing the set of input csv files. Type=string, case sensitive')
        error_exitrequired_flag = True

    # -----------------------------------------------------
    # Required number of tickers to be writen per output csv file line before a newline is written
    # -----------------------------------------------------
    if commandline_args.arg_int_writenumberoftickersperrow:
        pass
    else:
        print('Error, exiting. Specify the required command line entry =', commandline_args_token_list[1],
              ' to specify the number of tickers to be writen per output csv file line before a newline is written. Type=integer.')
        error_exitrequired_flag = True

    # -----------------------------------------------------
    # Required string to specify enabling/disabling of output filename timestamping functionality
    # -----------------------------------------------------
    if commandline_args.arg_str_output_enable_filename_datestamping:
        pass
    else:
        print('Error, exiting. Specify the required command line entry =', commandline_args_token_list[2],
              ' to specify if the output filename should include a current date YYYYMMDD timestamp. Type=string,{True/False},case insensitive.')
        error_exitrequired_flag = True

    # Exit if an error occured. All of the associated error messages will have been printed.
    if (error_exitrequired_flag):
        exit(1)

    return (commandline_args)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Functions: Input file, read related
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------
# Function: input_chdir_geninput_csvfilename_list()
# Purpose: create a list of all the input filenames
# ---------------------------------------------------------------------------------------------------
def input_chdir_geninput_csvfilename_list():
    try:
        os.chdir(commandline_args.arg_str_inputdirpath)
    except OSError as exc:  # Python >2.5
        print(
            'Error, exiting: an os.chdir exception occurred when changing to directory = ({0}); os.chdir exception = {1}'.format(
                commandline_args.arg_str_inputdirpath, exc))
        raise
        exit(1)

    input_csvfilename_list = glob.glob('*.csv')
    if (len(input_csvfilename_list) == 0):
        print(
            'Error, exiting: the specified input directory did not include any .csv files. Input directory = {0}'.format(
                commandline_args.arg_str_inputdirpath))
        exit(1)

    return (input_csvfilename_list)


# ---------------------------------------------------------------------------------------------------
# Function: input_readallrows()
# Purpose: create a list of all the input file's rows
# ---------------------------------------------------------------------------------------------------
def input_readallrows():
    global input_filenumber

    # input file: read all rows
    input_filenumber = input_filenumber + 1
    print('Processing input csv file # {0}...'.format(input_filenumber))
    print('Step 1, input... reading input filename = {0}'.format(
        commandline_args.arg_str_inputdirpath + '//' + input_filename))

    input_file_row_list = []
    with open(input_filename, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if len(row) > 0:
                input_file_row_list.append(row[0])
    f.close()
    return (input_file_row_list)


# ---------------------------------------------------------------------------------------------------
# Function: input_parsetickers()
# Purpose: create a list of all the stock ticker symbols that were read
# ---------------------------------------------------------------------------------------------------
def input_parsetickers():
    # input file: create a list of all the stock ticker symbols that were read
    print('Step 2a, parsing for stock symbol tickers in column 1...')
    ticker_list = []
    ticker_rows_read_start = False
    ticker_totalnum_symbolrows_read_aftersymboltoken = 0
    for input_file_row in input_file_row_list:
        # Ticker lines: check if we read the last ticker line, i.e. we are done reading
        if ((ticker_rows_read_start) & ("generated" in input_file_row.lower())):
            ticker_rows_read_start = False
        # Ticker lines: check if we are at the line before the first ticker via the token "symbol"?
        if ("symbol" in input_file_row.lower()):
            ticker_rows_read_start = True
        # Ticker lines: allow 1 blank line after reading the token "symbol"
        elif ((len(input_file_row) == 0)) & (ticker_totalnum_symbolrows_read_aftersymboltoken == 0):
            pass
        # Ticker lines: read a ticker line's symbol, store in the ticker_list list
        elif (ticker_rows_read_start):
            ticker_list.append(input_file_row)
            ticker_totalnum_symbolrows_read_aftersymboltoken += 1

    if (len(ticker_list) == 0):
        print(
            'Error, the specified input file did not include any stock symbol tickers. Input directory and filename = {0}'.format(
                commandline_args.arg_str_inputdirpath + input_filename))
    else:
        print('Step 2b, parsed a total of {0} tickers. The ticker list = '.format(len(ticker_list)))
        print(*ticker_list, sep='\n')

    return (ticker_list)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Functions: Output file, write related
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------
# Function: output_openfilewrite_withcondmakedir(path)
# Purpose: create the specified directory & parent directories if they do not exist. No error if it already exists.
# ---------------------------------------------------------------------------------------------------
def output_openfilewrite_withcondmakedir(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(path)):
            pass
        else:
            raise
    return open(path, 'w')


# ---------------------------------------------------------------------------------------------------
# Function: output_dirpath_setup()
# Purpose: setup the output directory path name
# ---------------------------------------------------------------------------------------------------
def output_dirpath_setup():
    import datetime

    output_dirpath_suffix_timestamp = datetime.datetime.now().strftime('%Y%m%d')
    output_dirpath_suffix = 'Pythonreformattedoutput' + output_dirpath_suffix_timestamp

    output_dirpath = commandline_args.arg_str_inputdirpath + '//' + output_dirpath_suffix + '//'
    return (output_dirpath)


# ---------------------------------------------------------------------------------------------------
# Function: output_filename_setup()
# Purpose: setup the output file name
# ---------------------------------------------------------------------------------------------------
def output_filename_setup():
    import datetime

    output_filename = input_filename  # set the default filename value

    if commandline_args.arg_str_output_enable_filename_datestamping.lower() == 'true':  # set per input argument
        today = datetime.datetime.today()
        output_filename_new_yyyymmdd = today.strftime('%Y%m%d')

        # Try to find & replace the filename's original YYYYMMDD datestamp w/ the current YYYMMDD datestamp
        #  if '20YYMMDD' string not present/found, then we'll default to the input filename
        output_filename_regex_split_pattern = re.compile(r'(.*)(20)([0-9]{6})(.*)',
                                                         re.IGNORECASE)  # specify preceding 'r' for raw to avoid need to precede w/ backslashes; Specify '?' for non-greedy to get 1st occur only
        output_filename_text_match = output_filename_regex_split_pattern.search(
            output_filename)  # search returns a match object or none
        if (output_filename_text_match):
            if 0:
                print('output_filename_text_match = ' + str(output_filename_text_match))
                print('output_filename_text_match.group(0) = ' + output_filename_text_match.group(0))  # Entire string
                print('output_filename_text_match.group(1) = ' + output_filename_text_match.group(1))  # Filename prefix
                print('output_filename_text_match.group(2) = ' + output_filename_text_match.group(
                    2))  # Filename date part 1 as '20'
                print('output_filename_text_match.group(3) = ' + output_filename_text_match.group(
                    3))  # Filename date part 2 as 'YYMMDD
                print('output_filename_text_match.group(3) = ' + output_filename_text_match.group(4))  # Filename suffix

            # replace the filename'd original YYYYMMDD datestamp, i.e.: date part 1 & part 2
            output_filename = output_filename_text_match.group(1) + \
                              output_filename_new_yyyymmdd + \
                              output_filename_text_match.group(4)
        else:
            # Unable to find & replace the input filename's original YYYYMMDD datestamp.
            # Insert the current YYYMMDD datestamp before the '.csv'
            output_filename_token_index = output_filename.find('.csv')
            if (output_filename_token_index > 0):
                output_filename_part1 = output_filename[:output_filename_token_index - 1]
                output_filename_part2 = output_filename[output_filename_token_index:]
                if 0:  # debugging
                    print('output_filename_part1 =' + output_filename_part1)
                    print('output_filename_part2 =' + output_filename_part2)
                output_filename = output_filename_part1 + output_filename_new_yyyymmdd + output_filename_part2
            else:
                output_filename = output_filename + output_filename_new_yyyymmdd  # No .csv case: unexpected to happen

    output_filename = output_filename + '.txt'  # append '.txt' for easy browsing of commas

    return (output_filename)


# ---------------------------------------------------------------------------------------------------
# Function: output_writecsvfilerows()
# Purpose:
# ---------------------------------------------------------------------------------------------------
def output_writecsvfilerows():
    import datetime

    # output_file_rows_list: all stock ticker symbols that were read, separated with commas
    output_file_row = None
    output_file_rows_list = []
    writenumberoftickersperrow_idx = 0
    for ticker in ticker_list:
        if output_file_row is None:
            output_file_row = ticker
        else:
            output_file_row = output_file_row + ',' + ticker
        writenumberoftickersperrow_idx += 1
        if writenumberoftickersperrow_idx >= commandline_args.arg_int_writenumberoftickersperrow:
            output_file_row += ',' + '\n'  # append a comma & the newline
            output_file_rows_list.append(output_file_row)
            output_file_row = None
            writenumberoftickersperrow_idx = 0
    if writenumberoftickersperrow_idx > 0:  # write the balance/last row
        output_file_rows_list.append(output_file_row)

    # output dirpath setup
    output_dirpath = output_dirpath_setup()  # returns output_dirpath
    # output filename setup
    output_filename = output_filename_setup()  # returns output_filename

    # write the file's row(s)
    with output_openfilewrite_withcondmakedir(output_dirpath + output_filename) as f:
        for row in output_file_rows_list:
            f.write(row)
    f.close()

    print('Step 3, output... writing output filename = {0}'.format(output_dirpath + output_filename))

    return


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Mainline
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Process the command line args:
#   1) commandline_args.arg_str_inputdirpath: the input directory path for the csv files to be read from the command line args/
#   2) commandline_args.arg_int_writenumberoftickersperrow: the output file's # tickers per row
#   3) commandline_args.arg_str_output_enable_filename_datestamping: enable output filename current datestamping
commandline_args = commandline_args_setup()
input_csvfilename_list = input_chdir_geninput_csvfilename_list()
for input_filename in input_csvfilename_list:
    print(
        '----------------------------------------------------------------------------------------------------------------------------------------')
    input_file_row_list = input_readallrows()
    if (len(input_file_row_list) > 0):
        ticker_list = input_parsetickers()
    if (len(ticker_list) > 0):
        output_writecsvfilerows()
    print(
        '----------------------------------------------------------------------------------------------------------------------------------------')
