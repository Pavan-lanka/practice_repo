import os
import glob
import psycopg2
from sshtunnel import SSHTunnelForwarder

SSH_HOST = '52.66.31.186'
SSH_PORT = 22
SSH_USER = 'ubuntu'
# SSH_KEY_PATH = '/home/pavan_azista/Documents/web_appInstance/HHCL-Ubuntu-key.pem'

SSH_KEY_PATH = os.path.expanduser('~/Documents/web_appInstance/HHCL-Ubuntu-key.pem')
gcp_dir = os.path.expanduser('/mnt/nas_analytics/Annotation/AFR_GCP/GCP_files')
oat_dir = os.path.expanduser('/mnt/data_products/afr/processed_data/oat')

POSTGRES_HOST = '127.0.0.1'
POSTGRES_DB = 'web_application_production'
POSTGRES_USER = 'april'
POSTGRES_PASSWORD = 'u&e!!!s4g3es28iTv3oqvkBod'
POSTGRES_PORT = 5432

# Directories to check
# oat_dir = os.path.expanduser('/mnt/data_products/afr/processed_data/oat')

table_name = 'images_data'
id_column = 'id'
oat_flag_column = 'oat_flag'
gcp_flag_column = 'gcp_flag'


# def check_id_in_directory(directory, ids, check_type):
#     """
#     Check the existence of files or directories for given IDs based on the type of check.

#     Args:
#         directory (str): The base directory to check.
#         ids (list): List of IDs to check for.
#         check_type (str): The type of check ("oat" or "gcp").

#     Returns:
#         dict: A dictionary with IDs as keys and flag values indicating existence.
#     """
#     result = {}
#     for id_ in ids:
#         base_id = id_
#         if '_' in id_:
#             base_id = id_.split('_')[0]
        
#         if check_type == "oat":
#             # Check for a .csv file with the ID name
#             path = os.path.join(directory, f"{base_id}.csv")
#             result[id_] = 1 if os.path.isfile(path) else 0
#         elif check_type == "gcp":
#             # Check for a directory with the ID name
#             path = os.path.join(directory, base_id)
#             result[id_] = 1 if os.path.exists(path) else 0
#         else:
#             raise ValueError("Invalid check_type. Must be 'oat' or 'gcp'.")
        
#         print(f"Checking {path}: {os.path.exists(path)}")
    
#     return result
def check_id_in_directory(directory, ids):
    """
    Check for the existence of .csv files matching given IDs in the specified directory.

    Args:
        directory (str): The base directory to check.
        ids (list): List of IDs to check for.

    Returns:
        dict: A dictionary with IDs as keys and flag values indicating existence.
    """
    result = {}
    for id_ in ids:
        base_id = id_
        if '_' in id_:
            base_id = id_.split('_')[0]
        
        # Use glob to match any .csv file starting with base_id
        pattern = os.path.join(directory, f"{base_id}*.csv")
        matching_files = glob.glob(pattern)
        
        # Set result to 1 if any matching files are found, else 0
        result[id_] = 1 if matching_files else 0
        
    # print(f"Checking {pattern}: {'Found' if matching_files else 'Not found'}")
    
    return result


def fetch_ids_from_database():
    ids = []
    try:
        # Create an SSH tunnel for secure connection
        with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_pkey=SSH_KEY_PATH,
            remote_bind_address=(POSTGRES_HOST, POSTGRES_PORT)
        ) as tunnel:
            if not tunnel.is_active:
                raise Exception("SSH tunnel could not be established.")

            # Use the local bind port provided by the SSH tunnel
            local_port = tunnel.local_bind_port            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host='127.0.0.1',  # Local bind address for the SSH tunnel
                port=local_port  # Port forwarded via SSH tunnel
            )
            cursor = conn.cursor()

            # Fetch all IDs from the table
            query = f"SELECT {id_column} FROM {table_name}"
            cursor.execute(query)
            ids = [row[0] for row in cursor.fetchall()]  # Retrieve all IDs as a list

            cursor.close()
            conn.close()
    except Exception as e:
        print(f"An error occurred while fetching IDs: {e}")
    return ids


def update_database_with_flags(ids, oat_flags, gcp_flags):
    try:
        # Create an SSH tunnel for secure connection
        with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_pkey=SSH_KEY_PATH,
            remote_bind_address=(POSTGRES_HOST, POSTGRES_PORT)
        ) as tunnel:
            if not tunnel.is_active:
                raise Exception("SSH tunnel could not be established.")

            # Use the local bind port provided by the SSH tunnel
            local_port = tunnel.local_bind_port                
            conn = psycopg2.connect(
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host='127.0.0.1',  # Local bind address for the SSH tunnel
                port=local_port  # Port forwarded via SSH tunnel
            )
            cursor = conn.cursor()

            for id_, oat_flag, gcp_flag in zip(ids, oat_flags, gcp_flags):
                query = f"""
                UPDATE {table_name}
                SET {oat_flag_column} = %s, {gcp_flag_column} = %s
                WHERE {id_column} = %s
                """
                cursor.execute(query, (int(oat_flag), int(gcp_flag), id_))

            conn.commit()
            cursor.close()
            conn.close()
        print("Database updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def ensure_columns_exist():
    try:
        # Create an SSH tunnel for secure connection
        with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_pkey=SSH_KEY_PATH,
            remote_bind_address=(POSTGRES_HOST, POSTGRES_PORT)
        ) as tunnel:
            if not tunnel.is_active:
                raise Exception("SSH tunnel could not be established.")

            # Use the local bind port provided by the SSH tunnel
            local_port = tunnel.local_bind_port    
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host='127.0.0.1',  # Local bind address for the SSH tunnel
                port=local_port  # Port forwarded via SSH tunnel
            )
            cursor = conn.cursor()

            # Check and create oat_flag column
            cursor.execute(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}' AND column_name = '{oat_flag_column}'
                    ) THEN
                        ALTER TABLE {table_name} ADD COLUMN {oat_flag_column} INT DEFAULT 0;
                    END IF;
                END
                $$;
            """)

            # Check and create gcp_flag column
            cursor.execute(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}' AND column_name = '{gcp_flag_column}'
                    ) THEN
                        ALTER TABLE {table_name} ADD COLUMN {gcp_flag_column} INT DEFAULT 0;
                    END IF;
                END
                $$;
            """)

            conn.commit()
            cursor.close()
            conn.close()
        print("Columns ensured successfully.")
    except Exception as e:
        print(f"An error occurred while ensuring columns: {e}")


if __name__ == "__main__":
    ensure_columns_exist()
    
    # Fetch IDs from the database
    ids = fetch_ids_from_database()
    print(f"Fetched IDs: {ids}")

    # Check the directories and files for oat and gcp flags
    oat_flags = check_id_in_directory(oat_dir, ids)
    gcp_flags = check_id_in_directory(gcp_dir, ids)

    # Prepare the flag lists for database update
    oat_flag_list = [oat_flags[id_] for id_ in ids]
    gcp_flag_list = [gcp_flags[id_] for id_ in ids]

    # Update the database with the flags
    update_database_with_flags(ids, oat_flag_list, gcp_flag_list)
