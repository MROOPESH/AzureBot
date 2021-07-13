import os, uuid, sys
from azure.storage.filedatalake import DataLakeFileClient
from io import BytesIO
import pandas as pd

class QueryDatalake:
    
    def __init__(self, connection_string: str, file_system_name: str, file_path: str):
        
        # coonect to datalake storage...
        self.file = DataLakeFileClient.from_connection_string(connection_string, 
                                                        file_system_name = file_system_name, file_path = file_path)
        
        # downlaod the contents of the file from storage
        self.download = self.file.download_file()
        # readall the contents to data variable...
        self.data = self.download.readall()
        
    


    def query_datalake(self, empid: int, query: str):
        # loading the bytes data into pandas dataframe...
        df = pd.read_csv(BytesIO(self.data))
        # df = pd.read_csv("C:\\Users\\rmaganti\\Downloads\\export.csv")
        query_output = ""
        df = df[df['job_tos_is1'] == 1]
        # query = int(query)
        if empid not in list(df['prsnel_id']):
            return "Sorry!!!. Employee ID not found. Please check and Re-enter."

        if query == "Current status":
            if df[df['prsnel_id'] == empid]['emplmt_status_desc'].values[0] in ('Terminated', 'Retired'):
                query_output = "The employee is {0} on {1}".format(df[df['prsnel_id'] == empid]['emplmt_status_desc'].values[0],
                                                                    df[df['prsnel_id'] == empid]['event_end_dt'].values[0])
            else:
                query_output = "The employee status is {0}".format(df[df['prsnel_id'] == empid]['emplmt_status_desc'].values[0])

        elif query == "Location of Employee":
            query_output = "The employee location is {0}".format(df[df['prsnel_id'] == empid]['location_group_desc'].values[0])

        elif query == "Department":
            query_output = "The employee department is {0}".format(df[df['prsnel_id'] == empid]['department_unit_desc'].values[0])
        
        """
        for i in range(len(df[df['prsnel_id']== query])):
            
            if df[df['prsnel_id']== query]['emplmt_status_desc'].values[i] == 'Active':
                query_output += "The employee is {0} from {1} to {2}.".format(df[df['prsnel_id']== query]['emplmt_status_desc'].values[i],
                                                            df[df['prsnel_id']== query]['event_start_dt'].values[i],
                                                            df[df['prsnel_id']== query]['event_end_dt'].values[i])
                
            else:
                query_output += "The employee is {0} on {1}.".format(df[df['prsnel_id']== query]['emplmt_status_desc'].values[i],                            
                                                            df[df['prsnel_id']== query]['event_end_dt'].values[i])
        """


            
        # return df.iloc[int(query)].to_string()
        return query_output


   


