def load():
    
    # Import
    import pandas as pd

    # Path
    path = "data/"

    # Read and store content of an excel file 
    read_file = pd.read_excel(path+"spices.xlsx")

    # Write the dataframe object into csv file
    read_file.to_csv (path+"spices.csv", index = None, header=True)

    # Load in dataset of spices as a dataframe
    df_spices=pd.read_csv(path+'spices.csv', header =[0], delimiter=',', encoding="utf-8")

    # Select ones to include
    df_spices = df_spices.loc[(df_spices['include'] == "in")]

    # List the list of ids
    list_of_spices = df_spices['id'].tolist()
    print("List of spices:", list_of_spices, "\n", len(list_of_spices), "spices in total.")
    return