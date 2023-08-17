import pandas as pd
import sys


def java_comparison_producer(build_number, comparison_run):
    """
    This function constructs the table with th test data taken from the extraction and compares it with a table that the user has chosen. It then returns the table in json format with all extracted information and the comparison table showing if test failures or errors appear in the current run which where not in the comparison run.
    """
    try:
        # read output-tests.csv file as dataframe
        df = pd.read_csv('output-tests.csv', header=None)
        # Give column names
        df.columns = ['Tests_run', 'Failures', 'Errors', 'Skipped', 'Test_name']
        # Erase all unnecessary characters in each column and transform them into type int64
        df['Tests_run'] = df['Tests_run'].str.split(':', n=1).str[1].astype('int64')
        df['Failures'] = df['Failures'].str.split(':', n=1).str[1].astype('int64')
        df['Errors'] = df['Errors'].str.split(':', n=1).str[1].astype('int64')
        df['Skipped'] = df['Skipped'].str.split(':', n=1).str[1].astype('int64')
        df['Test_name'] = df['Test_name'].str.split('-', n=1).str[1].str.replace('in','')
        # delete lines where no testname is given which corresponds to the total columns
        df = df.dropna(subset=['Test_name'])

        # Load the external dataframe which we want to compare
        # If We do not give a comparison run, we compare it with the same dataset which will not give any difference
        if comparison_run == "0":
            df_external = df
        # Otherwise we compare it with the dataset we give for comparison
        else:
            df_external = pd.read_json(f'{comparison_run}')

        # Distinguish cases where the dataframes do not have the same shape for informative reasons.
        if df.shape[0] == df_external.shape[0]:
            print("INFO: Same number of tests executed as in comparison run")

        elif df.shape[0] > df_external.shape[0]:
            print("INFO: More tests have been executed than in comparison run")
        
        else :
            print("WARNING: Less tests have been executed than in comparison run")

        # Merge dataframe with the imported one
        df_merge = df.merge(df_external, how='outer', on='Test_name', indicator=True)

        # See if there is there are more errors or failures in the current run
        df_comparison = df_merge[(df_merge["Failures_x"] > df_merge["Failures_y"]) | (df_merge["Errors_x"]> df_merge["Errors_y"])]
        
        print("Data transformation succeeded")

        # Produce csv file for comparison and entire dataframe taht we will need later on for the decision making. These are the required outputs of the function.
        return df_comparison.to_csv('comparison-java.csv', header=False), df.to_json(f'results-{build_number}.json')
        
    except:
        print("Data transformation failed")
        sys.exit(1)


if __name__ == "__main__":
    # The build number is the 1st argument after the filename
    build_number = sys.argv[1]
    # If we give a filename as 3rd argument, comparison will be that filename
    if len(sys.argv) == 3:
        comparison_run = sys.argv[2]
    # Otherwise the variable comparison-run will be empty
    else:
        comparison_run = "0"
    java_comparison_producer(build_number, comparison_run)