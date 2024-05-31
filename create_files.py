import os
import zipfile
import random

participant_udk = "OrbisTest"
site_udk = "700"
num_heartbeats = 1000
time_increment_ms = 60000
num_copies = 400
create_connection_delay = 100
num_zip_files = 1

# Define heartbeats for each POS type
heartbeat_templates = {
    "passport": """<GetLoyaltyOnlineStatusRequest><RequestHeader><POSLoyaltyInterfaceVersion>1.0</POSLoyaltyInterfaceVersion><VendorName>Excentus</VendorName><VendorModelVersion>1.0.0.0</VendorModelVersion><POSSequenceID>67438028001</POSSequenceID><StoreLocationID>{participant_udk}:{site_udk}</StoreLocationID><LoyaltyOfflineFlag value="no" /></RequestHeader></GetLoyaltyOnlineStatusRequest>""",
    "verifone": """<ns3:GetLoyaltyOnlineStatusRequest xmlns:ns2="http://www.naxml.org/POSBO/Vocabulary/2003-10-16" xmlns:ns3="http://www.pcats.org/schema/naxml/loyalty/v01" xmlns:ns4="http://www.pcats.org/schema/core/v01"><ns3:RequestHeader><ns3:POSLoyaltyInterfaceVersion>1.0</ns3:POSLoyaltyInterfaceVersion><ns2:VendorName>Excentus</ns2:VendorName><ns2:VendorModelVersion>1.0.0.0</ns2:VendorModelVersion><ns3:POSSequenceID>8a9b5f5a-a662-e568-faf5-ddd4aacc2c7a</ns3:POSSequenceID><ns3:StoreLocationID>{participant_udk}:{site_udk}</ns3:StoreLocationID><ns3:LoyaltyOfflineFlag value="no" /></ns3:RequestHeader></ns3:GetLoyaltyOnlineStatusRequest>""",
    "radiant": """<LoyaltyMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><SiteID>{participant_udk}:{site_udk}</SiteID><ClientSequenceID>703455984001</ClientSequenceID><POSSequenceID>703455984</POSSequenceID><BusinessPeriod>2024-05-21</BusinessPeriod><ClientID type="POS">1</ClientID><MessageTime>2024-05-21T16:13:08-05:00</MessageTime><TransactionStartTime>2024-05-21T16:13:08-05:00</TransactionStartTime><ClientVersion>2.1</ClientVersion><POSTranID>455984</POSTranID></Header><Operation><Method>STATUS</Method><Status>PENDING</Status></Operation></LoyaltyMessage>"""
}

# Default values
default_timestamp = "2024-03-29 08:00:00,000"
default_protocol = "tcp"
default_host = "staging-rise-connect.excentus.com"
port_map = {
    "passport": 9101,
    "radiant": 9102,
    "verifone": 9100
}
default_tcp_header_type = ""
default_http_headers = ""
default_st_flag = "false"
default_participant_id = participant_udk
default_site_id = site_udk
output_dir = "site_files"

# Create output directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate files with staggered delays
file_counter = 0
for copy_number in range(1, num_copies + 1):
    for pos_type, heartbeat in heartbeat_templates.items():
        filename = f"{output_dir}/{pos_type}_site_{copy_number}.txt"
        delay_for_file_start = file_counter * create_connection_delay
        file_counter += 1
        with open(filename, "w", newline='\n') as f:
            f.write("timestamp|time_since_start|protocol|host|port|tcp_header_type|http_headers|st_flag|participant_id|site_id|xml\n")
            for heartbeat_number in range(num_heartbeats):
                time_since_start = heartbeat_number * time_increment_ms
                # Format the heartbeat string with the actual values of participant_udk and site_udk
                formatted_heartbeat = heartbeat.format(participant_udk=default_participant_id, site_udk=default_site_id)
                f.write(f"{default_timestamp}|{time_since_start + delay_for_file_start}|{default_protocol}|{default_host}|{port_map[pos_type]}|{pos_type}|{default_http_headers}|{default_st_flag}|{default_participant_id}|{default_site_id}|{formatted_heartbeat}\n")

print("Files generated successfully.")

# After generating all the files, create zip files
files = os.listdir(output_dir)

# Shuffle the list of files to ensure a mix of different types of files in each zip
random.shuffle(files)

files_per_zip = len(files) // num_zip_files

# Create zip_files directory if not exists
zip_dir = "zip_files"
if not os.path.exists(zip_dir):
    os.makedirs(zip_dir)

for i in range(num_zip_files):
    start = i * files_per_zip
    end = start + files_per_zip if i != num_zip_files - 1 else None  # Take all remaining files in the last zip
    with zipfile.ZipFile(f'{zip_dir}/zipfile{i+1}.zip', 'w') as zipf:
        for filename in files[start:end]:
            zipf.write(os.path.join(output_dir, filename), arcname=filename)
