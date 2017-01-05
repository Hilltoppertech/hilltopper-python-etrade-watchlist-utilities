# hilltopper-python-etrade

Description:
- What does this python script do?:
    - This python script supports step #2 of the workflow described below to be used to create a new watchlist in Etrade based upon an old downloaded watchlist.
    - This python script reformats the old watchlist so that the output can be used to create a new watchlist with the same stock symbol tickers in Etrade.
- When to use this workflow:
    - When the Etrade account holder wants to create a new watchlist in order to evaluate the performance of an existing watchlist's stocks starting with the current date

Overview of the entire workflow:
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

Python script usage:
- Command line: <this python scriptname> <arg#1 name> <arg#1 value> <arg#2 name> <arg#2 value> <arg#3 name> <arg#3 value> ...
   - Arg #1: --arg_str_inputdirpath "<dir path w/ surrounding double quotes and w/ double forward slashes in the path>"
    - Description: required input directory path name string for accessing the set of input csv files. Type=string, case sensitive.
    - Example:  <this python scriptname> --arg_str_inputdirpath  "C://Downloads//Financial//Etrade//PortfolioDownloads//20160703"
   - Arg #2: --arg_int_writenumberoftickersperrow 10
    - Description: required integer/number of tickers to be writen per output csv file line before a newline is written. Type=integer,{1-200}.
    - Example:  <this python scriptname> <arg#1 name> <arg#1 value> --arg_int_writenumberoftickersperrow 10
   - Arg #3: --arg_str_output_enable_filename_datestamping True
    - Description: required {True, False} string to specify if the output filename should include a current date YYYYMMDD timestamp. Type=string,{True,False}, case insensitive.
        - If the input filename DOES included a YYYYMMDD datestamp, then that value will be replaced w/ the current YYYYMMDD datestamp.
        - If the input filename DOES NOT include a YYYYMMDD datestamp, then the current YYYYMMDD datestamp will be added before the '.csv' in the filename.
    - Example:  <this python scriptname> <arg#1 name> <arg#1 value> <arg#2 name> <arg#2 value> --arg_str_output_enable_filename_datestamping True

Python script design:
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

Python script design notes:
    - 'Output filename datestamping' functionality:
        - The objective is to create an output filename that can be copied/used as the new watchlist name in Etrade.
          Optionally, in Etrade one can manually update the input/old watchlist content to match the output/new watchlist content.
        - When enabled, there are 2 scenarios:
            1) The input filename's YYYYMMDD datestamp is replaced:
              If the input/downloaded csv filename includes a YYYYMMDD datestamp, then the old datestamp will be replaced with the new current datestamp.
              E.g.:
                Input/old watchlist & filename:   'Vanguard 20160128' 'Vanguard 20160128.csv'
                Output/new watchlist & filename:  'Vanguard 20170103' 'Vanguard 20170103.csv.txt'
            2) If the input filename does not include a YYYYMMDD datestamp, then the output filename will be the same as the input filename with both 1) the new current datestamp inserted before '.csv' and 2) '.txt. appended
              E.g.:
                Input/old watchlist & filename:  'Vanguard 20160128' 'Vanguard 20160128.csv'
                Output/new watchlist & filename: 'Vanguard 20160128' 'Vanguard 20160128.csv.txt'
        - When disabled:
            - The output filename will be the same as the input filename with '.txt. appended
    - Input file filename & format requirements:
        1) Format requirements:
            - In Etrade, when downloading the original/input Etrade csv watchlist, specify a view such as 'Summary - Market View' that will print the ticker symbols in the 1st column of the .csv file
              E.g.: sample input file content...
                Watch List Name
                Vanguard 20160128
                View Summary - Market View
                Symbol    Last Price $    Change $    Change %    Price When Added    Date Added    Change since Added %    Volume
                CCYIX    38.02    0.11    0.29    36.48     01/28/2016    4.22    0
                ...
                VSCPX    178.28    -0.68    -0.38    137.25     01/28/2016    29.89    0
                Generated at 01/03/2017 11:01:48 AM ET
        2) Filename requirements:
            A) In Etrade, after initiating the original/input Etrade csv watchlist download, verify that the filename type/suffix is '.csv'
            B) To utilize the 'output filename datestamping' functionality to create an output filename that can be copied/used as the new watchlist name:
                - In Etrade, when downloading the original/input Etrade csv watchlist, include a YYYYMMDD datestamp in the filename.
