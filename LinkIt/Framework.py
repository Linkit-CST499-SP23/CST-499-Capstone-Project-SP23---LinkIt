import csv
from datetime import datetime
from PluginApi import PluginApi
from collections import defaultdict

# Andrew:
# TO DO:
# - only take a sample of data. Currently entire file is read.
# - fix/improve process for determining best score (I have not touched this) 
# - complete documentation 
# - add additional try-catch at key points 
# - improve catalogue layout 
# - adjust console output and catalogue output for taking multiple csv's


def read_csv_file(filename):
    """
    Reads in a CSV file and returns a dict containing the specified column data and its name.
    """
    columns_dict = defaultdict(list)
    with open("LinkIt/csv/" + filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file) 
        for row in reader: 
            for (key,value) in row.items():
                columns_dict[key].append(value)
                                 
    return columns_dict

                     
def create_catalog(catalog_path, table_name, column_guesses, column_data):
    """
    Creates a catalog of analyzed CSV data, selecting the plugin with the highest confidence score.
    """
    # Populate catalog
    #need to make sure data does not get overwritten 
    column_names = list(column_guesses.keys())
    with open(catalog_path, 'a', newline='') as file:
        
        writer = csv.writer(file)
        for column_name in column_names:
            best_plugin = list(column_guesses[column_name].keys())[0] 
            best_confidence_score = column_guesses[column_name][best_plugin] 
        
            #Andrew: removed is_generic for now
            writer.writerow([table_name, column_name, best_plugin, best_confidence_score, 
                             column_data[column_name][1], column_data[column_name][2], column_data[column_name][3]]) 

        #for column_name in column_names:
        #    best_plugin = list(column_guesses[column_name].keys())[0] 
        #    best_confidence_score = column_guesses[column_name][best_plugin] 
        #
            #Andrew: removed is_generic for now
        #    writer.writerow([column_name, best_plugin, best_confidence_score, column_data[column_name]]) 

def analyze_data(dict_values):
    """
    Uses PluginApi to gather confidence scores for all columns of a table 
    """
    column_names = list(dict_values.keys())
    api = PluginApi()
    confidence_scores = {}
    # Andrew: run analyze_column from API for every column in csv file

    for column_name in column_names:
        print("Framework: Analyzing '" + column_name + "'...")
        single_conf_score = api.analyze_column(column_name, dict_values[column_name])
        confidence_scores.update({column_name: single_conf_score})
        print()

    # Andrew: return dict {column name: {plugin names, confidence scores}}
    return confidence_scores

def column_find_best_guess(confidence_scores):
    """
    docu here
    """
    #analyze data should return list of confidence scores & plugin names so it can be determined 
    #if they are generic or not, or scores can be tagged as generic or non gerneric
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

    best_guesses_dict = {}
    # Andrew: additional loop was necessary here
    # Andrew: for each column in the original table
    for disp_column in confidence_scores:
        plugin_names = list(confidence_scores[disp_column].keys())
        # Andrew: for each plugin that has given a confidence score for disp_column's type
        for plugin in plugin_names:
            # Andrew: the original logic, I just updated variable names
            current_score = confidence_scores[disp_column][plugin]
            if current_score > best_confidence_score:
                best_confidence_score = current_score
                is_generic = False
                if current_score >= nongeneric_threshold:
                    best_plugin = plugin  
                elif best_plugin is None or best_confidence_score >= 0.95:
                    best_plugin = plugin if current_score >= generic_threshold else "generic"

        # Andrew: adds the best plugin and its score to the column name list
        plugin_and_score = {best_plugin: best_confidence_score}
        best_guesses_dict.update({disp_column: plugin_and_score})

    # Andrew: return dict{column_name:{plugin_name:score}}
    return best_guesses_dict

def initialize_catalog():
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
    cat_name = 'catalog_' + dt_string
    cat_path = 'LinkIt/csv/' + cat_name + '.csv'
    open(cat_path, "x")
    with open(cat_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Table Name", "Column Name", "Data Category", "Confidence Score", 
                         "Data Sample 1", "Data Sample 2", "Data Sample 3"])
    return cat_path



def start_linkit():
    """
    Main program entry point. Prompts user for CSV files to analyze and runs the analysis.
    """
    filenames_str = input("Enter the CSV files to be analyzed separated by commas: ")
    filenames = filenames_str.split(",")

    catalog_path = initialize_catalog()

    for filename in filenames:
        try:
            #reading files
            columns_dict = read_csv_file(filename.strip())

            #console
            print("Framework: csv read...")

            #running plugin analysis 
            confidence_scores = analyze_data(columns_dict)

            #console
            print("Framework: confidence scores recieved...")

            # Andrew: made a seperate function for selecting the best plugin 
            best_guesses_dict = column_find_best_guess(confidence_scores)

            #console
            print("Framework: scores analyzed...")

            # populating output catalog with best guesses and sample data
            create_catalog(catalog_path, filename[:-4], best_guesses_dict, columns_dict)

            #console
            print("Framework: catalogue updated...")

        except FileNotFoundError:
            print("Framework: File not found:", filename.strip())


# Start Program Run
start_linkit()

