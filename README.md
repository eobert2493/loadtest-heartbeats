# Loadtest Heartbeats

This script generates heartbeat files for different POS types for load testing purposes. Follow the instructions below to set up the environment and run the script.

## Prerequisites

- Python

## Setup

### macOS and Linux

1. **Open Terminal**

2. **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd loadtest-heartbeats
    ```

3. **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    -or-
    py -m venv venv
    -or-
    python -m venv venv
    ```

4. **Activate the Virtual Environment**
    ```bash
    source venv/bin/activate
    ```

5. **Run the Script**
    ```bash
    python3 create_files.py
    -or-
    py create_files.py
    -or-
    python create_files.py
    ```

### Windows

1. **Open Command Prompt**

2. **Clone the Repository**
    ```cmd
    git clone <repository_url>
    cd loadtest-heartbeats
    ```

3. **Create a Virtual Environment**
    ```cmd
    py -m venv venv
    ```

4. **Activate the Virtual Environment**
    ```cmd
    venv\Scripts\activate
    ```

5. **Run the Script**
    ```cmd
    py create_files.py
    ```

## Script Details

### `create_files.py`

This script generates heartbeat files with staggered delays for different POS types based on the configuration parameters defined in the script. These files are used by the PTS load testing tool.

### Configuration Parameters

- **`num_heartbeats`**: Number of heartbeats to generate per file.
- **`time_increment_ms`**: Time increment in milliseconds between each heartbeat.
- **`num_copies`**: Number of copies to generate for each POS type.
- **`create_connection_delay`**: Delay increment for establishing connections in milliseconds.
- **`num_zip_files`**: This is a new configuration parameter. It determines the number of zip files to create.

### Default Values

- **`default_timestamp`**: Default timestamp for each heartbeat entry.
- **`default_protocol`**: Protocol used for the heartbeats.
- **`default_host`**: Default host for the heartbeats.
- **`port_map`**: Dictionary mapping POS types to their respective ports.
- **`default_tcp_header_type`**: Default TCP header type (if any).
- **`default_http_headers`**: Default HTTP headers (if any).
- **`default_st_flag`**: Default ST flag.
- **`default_participant_id`**: Default participant ID.
- **`default_site_id`**: Default site ID.
- **`output_dir`**: Directory where the output files will be stored.

### POS Types and Heartbeats

The script defines heartbeats for three POS types: `passport`, `verifone`, and `radiant`. Each type has a unique XML template.

### Example Usage

To run the script and generate the files, simply execute:

```bash
python create_files.py
```

# Updates

## Configuration Parameters (5/31)

- **`num_zip_files`**: This is a new configuration parameter. It determines the number of zip files to create.

## Default Values (5/31)

- **`zip_dir`**: This is a new default value. It specifies the directory where the zip files will be stored.

## POS Types and Heartbeats

The script defines heartbeats for three POS types: `passport`, `verifone`, and `radiant`. Each type has a unique XML template. The script now replaces "{participant_udk}:{site_udk}" in the heartbeat templates with the actual values of `default_participant_id` and `default_site_id`.

## Zip Files Generation

The script now creates a number of zip files as specified by `num_zip_files`, each containing an approximately equal number of files. The list of files is shuffled before dividing them into zip files to ensure that each zip file contains a mix of different types of files.

