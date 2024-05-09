import numpy as np
import pandas as pd
import struct
import os
from nptdms import TdmsFile, TdmsWriter, ChannelObject, RootObject


def read_dat_file(dat_file_path):
    """
    Reads a .dat file to extract metadata and configure channel information.

    Parameters:
        dat_file_path (str): The path to the .dat file.

    Returns:
        tuple: A tuple containing a dictionary with channel configurations and the path to the data file.
    """
    channels = {}
    current_channel = None
    data_file_path = None

    try:
        with open(dat_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#BEGINCHANNELHEADER'):
                    current_channel = {}
                elif line.startswith('#ENDCHANNELHEADER'):
                    if current_channel:
                        channels[current_channel['name']] = current_channel
                        if data_file_path is None:
                            data_file_path = current_channel.get('data_file')
                        current_channel = None
                elif current_channel is not None:
                    if ',' in line:
                        key, value = line.split(',', 1)
                        key, value = key.strip(), value.strip()
                        if key == '200':
                            current_channel['name'] = value
                        elif key == '202':
                            current_channel['unit'] = value
                        elif key == '214':
                            current_channel['dtype'] = value
                        elif key == '220':
                            current_channel['num_values'] = int(value)
                        elif key == '221':
                            current_channel['offset'] = int(value)
                        elif key == '222':
                            current_channel['block_offset'] = int(value)
                        elif key == '211':
                            current_channel['data_file'] = os.path.join(os.path.dirname(dat_file_path), value)
    except Exception as e:
        print(f"Failed to read or parse {dat_file_path}: {e}")
        return {}, None

    return channels, data_file_path


def read_data_file(data_file_path, channels):
    """
    Reads the data from a specified binary file and constructs a DataFrame based on the channel metadata.

    Parameters:
        data_file_path (str): Path to the binary data file.
        channels (dict): Dictionary containing channel definitions and metadata.

    Returns:
        pd.DataFrame: DataFrame populated with the structured data from the binary file.
    """
    data_types = {
        'REAL32': ('f', 4),
        'INT16': ('h', 2),
        'REAL64': ('d', 8)
    }

    try:
        total_channels = len(channels)
        data = np.empty((0, total_channels))

        with open(data_file_path, 'rb') as file:
            dtype_format = ''.join([data_types[info['dtype']][0] for info in channels.values()])
            record_size = sum([data_types[info['dtype']][1] for info in channels.values()])
            while True:
                record = file.read(record_size)
                if not record:
                    break
                unpacked_data = struct.unpack(dtype_format, record)
                data = np.vstack([data, unpacked_data])

        df = pd.DataFrame(data, columns=[ch['name'] for ch in channels.values()])

    except FileNotFoundError:
        print(f"Data file {data_file_path} not found.")
        return pd.DataFrame()
    except struct.error as e:
        print(f"Error unpacking data from {data_file_path}: {e}")
        return pd.DataFrame()

    return df


def dat_to_df(dat_file_path):
    """
    Converts data from a .dat and associated binary file to a DataFrame.

    Parameters:
        dat_file_path (str): The path to the .dat file.

    Returns:
        pd.DataFrame: DataFrame containing the structured data or an empty DataFrame on failure.
    """
    try:
        dataframe = pd.DataFrame()
        channels, data_file_path = read_dat_file(dat_file_path)
        if data_file_path:
            dataframe = read_data_file(data_file_path, channels)
        return dataframe
    except Exception as e:
        print(f"An error occurred while converting data to DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def dat_to_parquet(dat_file_path, parquet_file_name):
    """
    Converts data from a .dat file to a Parquet file.

    Parameters:
        dat_file_path (str): The path to the .dat file.
        parquet_file_name (str): The path where the Parquet file will be saved.
    """
    try:
        dataframe = dat_to_df(dat_file_path)
        if not dataframe.empty:
            dataframe.to_parquet(parquet_file_name)
            print(f"Data saved to {parquet_file_name}")
        else:
            print("No data available to save to Parquet.")
    except Exception as e:
        print(f"Failed to save data to Parquet: {e}")


def dat_to_csv(dat_file_path, csv_file_name):
    """
    Converts data from a .dat file to a CSV file.

    Parameters:
        dat_file_path (str): The path to the .dat file.
        csv_file_name (str): The path where the CSV file will be saved.
    """
    try:
        dataframe = dat_to_df(dat_file_path)
        if not dataframe.empty:
            dataframe.to_csv(csv_file_name, sep=';', index=False)
            print(f"Data saved to {csv_file_name}")
        else:
            print("No data available to save to CSV.")
    except Exception as e:
        print(f"Failed to save data to CSV: {e}")

def merge_dat_with_tdms(tdms_path, dat_path, fill_missing='nan'):
    """
    Merges data from TDMS and DAT files into a single DataFrame.

    Parameters:
        tdms_path (str): The file path to the TDMS file.
        dat_path (str): The file path to the DAT file.
        fill_missing (str): Specifies how to handle missing values: 'drop' or 'nan'.

    Returns:
        tuple: Contains merged DataFrame, TDMS channel units, DAT channel units, and the root name.
    """
    try:
        tdms_file = TdmsFile.read(tdms_path)
        tdms_df = tdms_file.as_dataframe()

        # Adjust column names by removing quotes and paths
        tdms_df.columns = [col.split('/')[-1].replace("'", "").strip() for col in tdms_df.columns]
        tdms_channel_units = {channel.path.split('/')[-1].replace("'", "").strip(): channel.properties.get('unit_string', 'unknown')
                              for group in tdms_file.groups() for channel in group.channels()}

        channels, _ = read_dat_file(dat_path)
        dat_df = dat_to_df(dat_path)

        root_name = 'Measurement'
        for group in tdms_file.groups():
            root_name = group.name

        # Store units and names for .dat channels
        dat_channel_units = {channel['name']: channel.get('unit', 'unknown') for channel in channels.values()}

        merged_df = pd.merge(tdms_df, dat_df, on='UnixTime', how='left')

        if fill_missing == 'drop':
            merged_df.dropna(inplace=True)
        elif fill_missing == 'nan':
            merged_df.fillna(value=np.nan, inplace=True)

        return merged_df, tdms_channel_units, dat_channel_units, root_name
    except Exception as e:
        print(f"Error merging TDMS and DAT files: {e}")
        return pd.DataFrame(), {}, {}, 'Measurement'

def save_to_tdms(df, tdms_channel_units, dat_channel_units, tdms_path_read, root_name, output_directory):
    """
    Saves the merged DataFrame to a new TDMS file with metadata.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        tdms_channel_units (dict): Dictionary of units from TDMS channels.
        dat_channel_units (dict): Dictionary of units from DAT channels.
        tdms_path_read (str): The original TDMS file path.
        root_name (str): The root name for the TDMS file.
        output_directory (str): Directory to save the new TDMS file.
    """
    try:
        os.makedirs(output_directory, exist_ok=True)
        tdms_path_write = os.path.join(output_directory, os.path.basename(tdms_path_read))
        root_object = RootObject(properties={"name": root_name})

        with TdmsWriter(tdms_path_write) as tdms_writer:
            tdms_writer.write_segment([root_object])
            for column in df.columns:
                properties = {'name': column}
                if column in tdms_channel_units:
                    properties['unit_string'] = tdms_channel_units[column]
                elif column in dat_channel_units:
                    properties['unit_string'] = dat_channel_units[column]

                channel = ChannelObject(root_name, column, df[column].values, properties=properties)
                tdms_writer.write_segment([root_object, channel])
            print(f"Data successfully saved to TDMS file: {tdms_path_write}")
    except Exception as e:
        print(f"Error saving data to TDMS file: {e}")


def create_merged_tdms(tdms_path, dat_path, output_directory, fill_missing='drop'):
    """
    Creates a merged TDMS file from TDMS and DAT sources.

    Parameters:
        tdms_path (str): The file path to the TDMS file.
        dat_path (str): The file path to the DAT file.
        output_directory (str): The directory to save the merged TDMS file.
        fill_missing (str): Specifies how to handle missing values in the merge.
    """
    result_df, tdms_channel_units, dat_channel_units, root_name = merge_dat_with_tdms(
        tdms_path, dat_path, fill_missing=fill_missing)
    save_to_tdms(result_df, tdms_channel_units, dat_channel_units, tdms_path, root_name, output_directory)


def tdms_to_parquet(tdms_path, parquet_file_name):
    try:
        tdms_file = TdmsFile.read(tdms_path)
        dataframe = tdms_file.as_dataframe()
        if not dataframe.empty:
            dataframe.to_parquet(parquet_file_name)
            print(f"Data saved to {parquet_file_name}")
        else:
            print("No data available to save to Parquet.")
    except Exception as e:
        print(f"Failed to save data to Parquet: {e}")


def tdms_metadata_to_csv(tdms_path):
    """
    Extracts and saves metadata from a TDMS file to a CSV file.

    Parameters:
        tdms_path (str): The path to the TDMS file.

    The function reads the specified TDMS file, extracts metadata from all channels across all groups,
    and saves this information into a CSV file named after the original TDMS file with a '_metadata' suffix.
    """
    try:
        # Read the TDMS file
        tdms_file = TdmsFile.read(tdms_path)

        # Extract metadata from each channel
        metadata = []
        for group in tdms_file.groups():
            for channel in group.channels():
                channel_metadata = {
                    "Group": group.name,
                    "Channel": channel.name,
                    "Unit": channel.properties.get("unit_string", "No unit available")
                }
                metadata.append(channel_metadata)

        # Convert the metadata into a DataFrame
        metadata_df = pd.DataFrame(metadata)

        # Determine the output file path
        output_file_path = os.path.splitext(tdms_path)[0] + "_metadata.csv"

        # Save the DataFrame to CSV
        metadata_df.to_csv(output_file_path, sep=';', index=False)
        print(f"Metadata saved successfully to: {output_file_path}")
    except Exception as e:
        print(f"An error occurred while extracting metadata from the TDMS file: {e}")