import csv
import importlib
from PluginApi import PluginApi
from collections import defaultdict

# Andrew:
# BUGS/ISSUES
# - Some plugins are not loading (possibly becasue of syntax issues within the plugin)
# -- Not loading: Phone Number, Credit Card Number
# -- Loading: Credit CVV, Credit Exp Date, Generic Number, Generic Text 
# - Using Sample Data, getting a lot of 0.0 confidence scores (other than Generics, which are consistently 0-49%) 
# which feels wrong. The data does seem to be going through correctly to the plugins though, so I'm not sure whats up
#
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

                     
def create_catalog(column_guesses, column_data):
    """
    Creates a catalog of analyzed CSV data, selecting the plugin with the highest confidence score.
    """
    # Populate catalog
    # need to make sure data does not get overwritten 
    column_names = list(column_guesses.keys())
    with open('LinkIt/csv/OutputCatalog.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for column_name in column_names:
            best_plugin = list(column_guesses[column_name].keys())[0] 
            best_confidence_score = column_guesses[column_name][best_plugin] 

            #Andrew: removed is_generic for now
            writer.writerow([column_name, best_plugin, best_confidence_score]) 

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

    # Andrew: return dict {column name: {plugin names, confidence scores}}
    return confidence_scores

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

        - If a non-generic plugin has a confidence score of at least 60% and is higher than the generic, it is selected as the best guess.
        - If a generic plugin has a confidence score of 95% or higher and is greatr than the nongeneric, it is selected as the best guess.
        - If the highest confidence score for a column is below the non-generic threshold of 60%, a generic plugin is selected due to this no nongeneric confidence score lower than .60 will be returned
    

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

    generic_threshold = 0.95
    nongeneric_threshold = 0.6

    best_plugin = None
    best_plugin_nongeneric = None
    best_plugin_generic = None
    best_confidence_score_generic = 0
    best_confidence_score_nongeneric = 0
    best_confidence_score = 0
    is_generic = False

    best_guesses_dict = {}
    # Andrew: additional loop was necessary here
    # Andrew: for each column in the original table
    for disp_column in confidence_scores:
        plugin_names = list(confidence_scores[disp_column].keys())
        # Andrew: for each plugin that has given a confidence score for disp_column's type
        print (confidence_scores)
        for plugin in plugin_names:
            # Andrew: the original logic, I just updated variable names
            current_score = confidence_scores[disp_column][plugin]

            # Alex: Checks if plugin is generic
            if "generic" in plugin.lower():
                is_generic = True

            # Alex: logic gives best nongeneric confidence score
            if current_score > best_confidence_score_nongeneric and not is_generic:
                best_confidence_score_nongeneric = current_score
                best_plugin_nongeneric = plugin

            # Alex: logic gives best generic confidence score
            if current_score > best_confidence_score_generic and is_generic:
                best_confidence_score_generic = current_score
                best_plugin_generic = plugin

            # Alex: compares highest nongeneric and generic plugin scores, nongeneric wins if it is higher and above threshhold of 60 percent confidence
            if  best_confidence_score_nongeneric > best_confidence_score_generic and best_confidence_score_nongeneric > nongeneric_threshold:
                best_confidence_score = best_confidence_score_nongeneric
                best_plugin = best_plugin_nongeneric

            # Alex: compares highest nongeneric and generic plugin scores, generic wins if it is higher and above threshhold of 95 percent confidence
            if  best_confidence_score_generic > best_confidence_score_nongeneric and best_confidence_score_generic > generic_threshold:
                best_confidence_score = best_confidence_score_generic
                best_plugin = best_plugin_generic
            
            # Alex: incase no plugin is above set threshold generic score is returned
            elif best_confidence_score_generic > best_confidence_score_nongeneric:
                 best_confidence_score = best_confidence_score_generic
                 best_plugin = best_plugin_generic

             
        # Andrew: adds the best plugin and its score to the column name list
        print (confidence_scores)
        print("IN BEST GUESS")
        print("CURRENT COLUMN: " + disp_column + " BEST PLUGIN: " + best_plugin + " BEST SCORE: " + str(best_confidence_score) + " PLUGIN NAME: " + plugin)
        plugin_and_score = {best_plugin: best_confidence_score}
        best_guesses_dict.update({disp_column: plugin_and_score})

    # Andrew: return dict{column_name:{plugin_name:score}}
    return best_guesses_dict




def start_linkit():
    """
    Main program entry point. Prompts user for CSV files to analyze and runs the analysis.
    """
    filenames_str = input("Enter the CSV files to be analyzed separated by commas: ")
    filenames = filenames_str.split(",")

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
            create_catalog(best_guesses_dict, columns_dict)

            #console
            print("Framework: catalogue created...")

        except FileNotFoundError:
            print("Framework: File not found:", filename.strip())


# Start Program Run
start_linkit()

