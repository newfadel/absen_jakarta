import socket
from datetime import datetime
import time
from zk import ZK, const

def check_device_connection(ip, port=4370, timeout=5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.close()
        return True
    except Exception as e:
        print(f"Cannot connect to ZKTeco device at {ip}:{port}. Error: {str(e)}")
        return False

def connect_zkteco():
    try:
        conn = ZK('192.168.1.111', port=4370, timeout=15, password=1, force_udp=False, ommit_ping=False)
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
    # Check connection to ZKTeco device
    if not check_device_connection('192.168.1.111'):
        print("Error: Cannot proceed due to connection failure.")
        return

    # Get current machine time
    conn = connect_zkteco()
    if conn:
        try:
            zktime = conn.get_time()
            print(f"Current ZKTeco machine time: {zktime}")

            # Get current date and time
            current_time = datetime.now()
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

                # Disable device
                conn.disable_device()
                print("Device disabled for time update")

                # Set new time to machine
                conn.set_time(new_time)
                print(f"Time temporarily set to: {new_time}")

                # Verify the new time
                updated_time = conn.get_time()
                print(f"Updated ZKTeco machine time: {updated_time}")

                # Wait for 5 seconds
                print("Waiting for 5 seconds before reverting time...")
                time.sleep(5)

                # Revert to current time
                current_time = datetime.now()
                conn.set_time(current_time)
                print(f"Time reverted to: {current_time}")

                # Verify reverted time
                final_time = conn.get_time()
                print(f"Final ZKTeco machine time: {final_time}")

                # Enable device
                conn.enable_device()
                print("Device enabled")

            except ValueError as ve:
                print(f"Invalid day or time format: {str(ve)}")
                print("Ensure day is a number and time is in HH:MM format.")
            except Exception as e:
                print(f"Error during operation: {str(e)}")
            finally:
                conn.enable_device()  # Ensure device is enabled even on error
                conn.disconnect()
                print("Disconnected from ZKTeco device")
        except Exception as e:
            print(f"Error getting time: {str(e)}")
            conn.disconnect()
    else:
        print("Cannot proceed due to connection failure.")

if __name__ == "__main__":
    main()