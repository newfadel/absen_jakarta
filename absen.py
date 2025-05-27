import socket
import re
from datetime import datetime
from zk import ZK, const

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return None

def is_same_subnet(ip):
    return ip and ip.startswith('192.168.1.')

def connect_zkteco():
    try:
        conn = ZK('192.168.1.115', port=4370, timeout=15, password=1, force_udp=False, ommit_ping=False)
        connection = conn.connect()
        if connection:
            print("Successfully connected to ZKTeco device")
            return conn
        else:
            print("Failed to connect to ZKTeco device")
            return None
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return None

def main():
    # Check local IPx
    local_ip = get_local_ip()
    if not is_same_subnet(local_ip):
        print(f"Error: Your IP ({local_ip}) is not in the 192.168.1.* subnet. Cannot proceed.")
        return

    # Get current machine time
    conn = connect_zkteco()
    if conn:
        try:
            zktime = conn.get_time()
            print(f"Current ZKTeco machine time: {zktime}")
        except Exception as e:
            print(f"Error getting time: {str(e)}")
            return

        # Get current date and time
        current_time = datetime.today()
        current_month = current_time.month
        current_year = current_time.year

        # Get user input for day and time
        try:
            day_input = input("Enter day (DD, e.g., 27): ")
            time_input = input("Enter time (HH:MM, e.g., 14:30): ")

            # Validate day input
            day = int(day_input)
            if not (1 <= day <= 31):
                print("Error: Day must be between 1 and 31.")
                return

            # Combine current year, month with user-provided day and time
            new_time = datetime.strptime(
                f"{current_year}-{current_month:02d}-{day:02d} {time_input}",
                "%Y-%m-%d %H:%M"
            )

            # Set new time to machine
            conn.set_time(new_time)
            print(f"Time successfully set to: {new_time}")

            # Verify the new time
            updated_time = conn.get_time()
            print(f"Updated ZKTeco machine time: {updated_time}")

        except ValueError as ve:
            print(f"Invalid day or time format: {str(ve)}")
            print("Ensure day is a number and time is in HH:MM format.")
        except Exception as e:
            print(f"Error setting time: {str(e)}")
        finally:
            conn.disconnect()
    else:
        print("Cannot proceed due to connection failure.")

if __name__ == "__main__":
    main()

