import csv
import importlib


# need API analyze_column method to be updated so it takes column name and returns it 
# or can return string "generic or nongeneric"
# or if plugin names have that in title we can use strings to determine not sure

# need to make sure data written to catalog does not overwrite other data
# need to make sure each csv column is getting passed to analyze data


def read_csv_file(filename):
    """
    Reads in a CSV file and returns a list containing the specified column data and its name.
    """
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        # Andrew: reader is a dict, [fieldname (default 1st row's values)]:[row data. without a loop of some kind, most efficient to just return
        # the dict and sort it out

        #headers = reader.fieldnames
        #column_name = headers[0]  # Assumes the column to extract is the first column
        #column_data = [row[column_name] for row in reader]
        #return column_name, column_data #not sure if this returns one or multiple columns
        return reader




                       #or could take a dictionary containg these 
def create_catalog(confidence_scores, column_name, column_data, plugin_name):
    """
    Creates a catalog of analyzed CSV data, selecting the plugin with the highest confidence score.
    """
    #analyze data should return list of confidence scores & plugin names so it can be determined if they are generic or not, or scores can be tagged as generic or non gerneric
    #need to create values to determine which plugin and confidence score will be selected
    #if nongeneric is 80% or higher it should automattically win
    #if generic is 95% or higher it should win
    #if they are equal non generic wins
    # if nongenric is below 60% gernic wins

    generic_threshold = 0.6
    nongeneric_threshold = 0.8

    best_plugin = None
    best_confidence_score = -1
    is_generic = True

    for score in confidence_scores:
        if score > best_confidence_score:
            best_confidence_score = score
            is_generic = False
            if score >= nongeneric_threshold:
                best_plugin = plugin_name
            elif best_plugin is None or best_confidence_score >= 0.95:
                best_plugin = plugin_name if score >= generic_threshold else "generic"

    # Populate catalog
    #need to make sure data does not get overwritten 
    with open('catalog.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([column_name, column_data, best_plugin, is_generic, best_confidence_score])


def analyze_data(column_name,column_data):
    
    #run analyze_column from API for every column in csv file

    #return dictionary of colunm names, plugin names, confidence scores, and column data

    #send data to create catalog


def start_linkit():
    """
    Main program entry point. Prompts user for CSV files to analyze and runs the analysis.
    """
    filenames_str = input("Enter the CSV files to be analyzed separated by commas: ")
    filenames = filenames_str.split(",")

    for filename in filenames:
        try:
            #reading files
            column_name, column_data = read_csv_file(filename.strip())
            #running data analysis 
            analyzed_csv_data = analyze_data(column_name, column_data)
            #populating output catalog
            create_catalog(*analyzed_csv_data, plugin_name="example_plugin")

        except FileNotFoundError:
            print("File not found:", filename.strip())


# Start Program Run
start_linkit()

