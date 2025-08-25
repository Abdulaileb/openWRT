import json


def count_logs_in_json(file_path):
    """
    Count the total number of logs in a JSON file with the given structure.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        int: Number of logs in the file
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Check if 'logs' key exists and is a list
        if 'logs' in data and isinstance(data['logs'], list):
            return len(data['logs'])
        else:
            print("Warning: 'logs' key not found or is not a list")
            return 0
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return 0
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' contains invalid JSON")
        return 0
    except Exception as e:
        print(f"Error reading file: {e}")
        return 0

# Example usage
if __name__ == "__main__":
    file_path = "generated_logs/mixed_batch_1.json"
    log_count = count_logs_in_json(file_path)
    print(f"Total number of logs: {log_count}")