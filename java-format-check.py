import pandas as pd
import sys

# First check if the user gave the "0" argument which means that there will be no comparison
if sys.argv[1] != "0":
    # define file
    comparison_file = sys.argv[1]
    # Check if file is of a valid json and if it is the case load the dataframe
    try:
        dataframe = pd.read_json(comparison_file)
        print("json file is readable")
    except:
        print("file does not exist, is not of json format or incompatible with pandas json reader")
        sys.exit(1)

    # the requested schema
    schema = {
        'Tests_run':int,
        'Failures': int,
        'Errors': int,
        'Skipped': int,
        'Test_name': object}
    
    # Check if the loaded dataframe has the same schema
    # First check if it has the same columns
    if dataframe.columns.tolist() == ['Tests_run', 'Failures', 'Errors', 'Skipped', 'Test_name']:
        print("Right columns")
        # Now let's check if the column types are the same
        if dataframe.dtypes.to_dict() == schema:
            print(dataframe.dtypes)
        else:
            print('Wrong schema')
    else:
        print("Wrong columns")
        sys.exit(1)
    
else:
    print("no comparison needed")
    