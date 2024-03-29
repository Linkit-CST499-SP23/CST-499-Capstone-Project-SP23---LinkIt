import csv
from datetime import datetime
from PluginApi import PluginApi
from collections import defaultdict
 

def read_csv_file(filename):
    """
    Reads in a CSV file and returns a defaultdict containing the collumn data from the file
            
    Parameters
    ----------
    filename : string
        the name of the file to be openned and scanned into a defaultdict 

    output: defaultdict{string:list}
    """

    columns_dict = defaultdict(list)

    # Andrew: open file with user given path
    with open("LinkIt/csv/" + filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Andrew: enter all column data into list value, key = column's name
        for row in reader: 
            for (key,value) in row.items():
                columns_dict[key].append(value)

    # Andrew: columns_dict{column_name:column_entries[]}                             
    return columns_dict


def initialize_catalog():
    """
    Creates a catalog file using the current date and time for naming (e.g. catalog_may-02-2023_12-10-42.csv)

    output: string
    """

    # Andrew: get current date and time, make file name
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
    cat_name = 'catalog_' + dt_string
    cat_path = 'LinkIt/csv/' + cat_name + '.csv'

    # Andrew: create file
    open(cat_path, "x")
    with open(cat_path, 'a', newline='') as file:
        writer = csv.writer(file)
        # Andrew: write column headers
        writer.writerow(["Table Name", "Column Name", "Data Category", "Confidence Score", 
                         "Data Sample 1", "Data Sample 2", "Data Sample 3"])

    return cat_path


def analyze_data(dict_values):
    """
    Uses PluginApi to gather confidence scores for all columns of a table 

    Parameters
    ----------
    dict_values : defaultdict {string:list}
        the file data to be analyzed; {column_name:column_entries[]}

    output: dict {dict{string:int}}
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

    # Andrew: confidence_scores{column name: {plugin names, confidence scores}}
    return confidence_scores


def create_catalog(catalog_path, table_name, column_guesses, column_data):
    """
    Populates the catalog file with analyzed data and program best-guesses for semantic meaning

    Parameters
    ----------
    catalog_path : string
        the filepath of the catalog into which the output data will be written
    table_name : string
        the name of the file that has been analyzed, and whose data is now being entered into the catalog
    column_guesses : dict{string:dict{string:int}} 
        the program's best guesses for the semantic meaning of the data sotred in the file; 
        semantically, {column_name:{plugin_name:score}}
    column_data : defaultdict{string:list}
        the file data of [table_name]; semantically, {column_name:column_entries[]}
        
    """

    column_names = list(column_guesses.keys())
    with open(catalog_path, 'a', newline='') as file:
        
        writer = csv.writer(file)
        for column_name in column_names:
            # Andrew: gather relevant data
            best_plugin = list(column_guesses[column_name].keys())[0] 
            best_confidence_score = column_guesses[column_name][best_plugin] 
            # Alex: getting fallback plugin name
            fallback_datatype =  column_guesses[column_name]["fallback"]

            # Andrew: trimming plugin name down for readability 
            if best_plugin.endswith("plugin") or best_plugin.endswith("Plugin"):
                best_plugin = best_plugin[:-6]
            if best_plugin.endswith("_"):
                best_plugin = best_plugin[:-1]
            if fallback_datatype.endswith("plugin") or fallback_datatype.endswith("Plugin"):
                fallback_datatype = fallback_datatype[:-6]
            
            # Andrew: write data row
            # Alex: removed sample data in output since it was not in design but can be added back
            # Alex: wrapped confidence score in float() so that output catalog had standardized output 
            writer.writerow([table_name, column_name, best_plugin, float(round(best_confidence_score, 2)), 
                             fallback_datatype, column_data[column_name][1], column_data[column_name][2]]) 


def column_find_best_guess(confidence_scores):
    """
        Returns the best guess for each column in a table, along with the corresponding plugin name and confidence score.

        Parameters
        ----------
        confidence_scores : dict
            A dictionary containing the confidence scores for each column in the table. The keys of the dictionary should be the
            column names, and the values should be dictionaries containing the plugin names and corresponding confidence scores
            for each plugin that has given a confidence score for the column.

        Returns
        -------
        dict
            A dictionary containing the best guess for each column in the table, along with the corresponding plugin name and
            confidence score. The keys of the dictionary are the column names, and the values are dictionaries containing the
            best plugin name and corresponding confidence score.

        Notes
        -----
        The function determines the best guess for each column based on the following criteria:

        - If a non-generic plugin has a confidence score of at least 60%, it is selected as the best guess.
        - If a generic plugin has a confidence score of 95% or higher, it is selected as the best guess.

        The function assumes that each plugin is either generic or non-generic based on the presence of the word "generic" in the
        plugin name, regardless of capitalization. The function returns a dictionary of the best guess for each column, along with
        the corresponding plugin name and confidence score.

        Examples
        --------
    
        >>> confidence_scores = {{'first_name': {'GenericTextPlugin': 1, 'NamePlugin': .7, 'CreditCardExpirationDatePlugin': .0},
                                 {'date': {'NamePlugin': .0, 'SocialMediaPlugin': .0,'GenericTextPlugin': .9}}
       

        In this example, the function takes a dictionary of confidence scores for two columns ('first_name' and 'date') and three
        plugins ('GenericTextPlugin', 'NamePlugin', and 'CreditCardExpirationDatePlugin'). For 'first_name', 'NamePlugin' has the highest confidence score of 0.7 and is nongeneric, which
        is above the non-generic threshold of 0.6, so it is selected as the best guess for that column. For 'date', 'GenericTextPlugin'
        has the highest confidence score of 0.9, which is also above the generic threshold, so it is selected as the best
        guess for that column. 
        """

    generic_threshold = 95
    nongeneric_threshold = 60
    best_plugin = None
    best_confidence_score = -1
    best_guesses_dict = {}


    # Andrew: for each column in the original table
    for disp_column in confidence_scores:
        plugin_names = list(confidence_scores[disp_column].keys())

        # Alex: creating variables for confidence score comparison for each plugins, outside loop because they need to be reset for each column
        best_confidence_score_generic = -1
        best_confidence_score_nongeneric = -1
        best_plugin_nongeneric = None
        best_plugin_generic = None
        fallback_plugin = None
        is_generic = False

        # Andrew: for each plugin that has given a confidence score for disp_column's type
        for plugin in plugin_names:
             
            # Andrew: the original logic, I just updated variable names
            current_score = confidence_scores[disp_column][plugin]

             # Alex: DEBUG PRINT STATMENTS 
            ''' 
            print ("IN LOOP ")
            print("COLNAME: " + disp_column)
            print("PLUGIN: " + plugin)
            print(" CURRENT SCORE: " + str(current_score))
        
            '''
           
            # Alex: Checks if plugin is generic
            if "generic" in plugin.lower():
                is_generic = True
            else:
                 is_generic = False

            # Alex: comparing scores for each plugin and finding highest for generic and nongeneric

            # Alex: logic gives best nongeneric confidence score
            if current_score > best_confidence_score_nongeneric and not is_generic:

                best_confidence_score_nongeneric = current_score
                best_plugin_nongeneric = plugin
                

            # Alex: logic gives best generic confidence score
            if current_score > best_confidence_score_generic and is_generic:
                best_confidence_score_generic = current_score
                best_plugin_generic = plugin

            # Alex: DEBUG PRINT STATMENTS 
            ''' 
            print(" BEST NONGEN SCORE: " + str(best_confidence_score_nongeneric))
            print(" BEST NONGEN PLUGIN: " + str(best_plugin_nongeneric))
            print(" BEST GEN SCORE: " + str(best_confidence_score_generic))
            print(" BEST GEN PLUGIN: " + str(best_plugin_generic))
            '''

        # Alex: comparing highest plugin scores for each column and determining best 

        # Alex: compares highest nongeneric and generic plugin scores, nongeneric wins if it is higher and above threshhold of 60 percent confidence
        if  best_confidence_score_nongeneric > nongeneric_threshold:
            best_confidence_score = best_confidence_score_nongeneric
            best_plugin = best_plugin_nongeneric

        # Alex: compares highest nongeneric and generic plugin scores, generic wins if it is higher and above threshhold of 95 percent confidence
        elif best_confidence_score_generic > generic_threshold:
             best_confidence_score = best_confidence_score_generic
             best_plugin = best_plugin_generic
        
        # Alex: incase no plugin is above set threshold generic score is returned
        elif best_confidence_score_generic > best_confidence_score_nongeneric:
             best_confidence_score = best_confidence_score_generic
             best_plugin = best_plugin_generic

        # Alex: DEBUG PRINT STATMENT # print("CURRENT COLUMN: " + disp_column + " BEST PLUGIN: " + str(best_plugin) + " BEST SCORE: " + str(best_confidence_score))
        
        # Alex: assigning the best generic plugin to fallback
        fallback_plugin = best_plugin_generic 

        # Andrew: trims and adds the best plugin and its score to the column name list
        # Alex: adds fallback var to dict
        plugin_and_score_and_fallback = {best_plugin: best_confidence_score,"fallback": fallback_plugin}
    
        best_guesses_dict.update({disp_column: plugin_and_score_and_fallback})

        

    # Andrew: best_guesses_dict{column_name:{plugin_name:score}}
    return best_guesses_dict

def initialize_catalog():
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
    cat_name = 'catalog_' + dt_string
    cat_path = 'LinkIt/csv/' + cat_name + '.csv'
    open(cat_path, "x")
    with open(cat_path, 'a', newline='') as file:
        writer = csv.writer(file)
        # Alex removed sample data and added fallback
        # writer.writerow(["Table Name", "Column Name", "Data Category","Confidence Score","Fallback"])

        # Andrew: re-added some sample data and reformatted ordering
        writer.writerow(["Table Name", "Column Name", "Data Category", "Confidence Score","Fallback",  
                          "Data Sample 1", "Data Sample 2"])
    return cat_path



def start_linkit():
    """
    Main program entry point. Prompts user for CSV files to analyze and runs the analysis.
    """

    # Andrew: Loop for checking valid file inputs
    proceed = False
    while not proceed:
        try:
            filenames_str = input("Enter the CSV files to be analyzed separated by commas: ")
            filenames = filenames_str.split(",")

            for filename in filenames:
                file = open("LinkIt/csv/" + filename.strip(), 'r')
                file.close()

            proceed = True
            catalog_path = initialize_catalog()

        except FileNotFoundError:
            print("Framework: File not found: ", filename.strip())
    
    # Andrew: Main loop
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

