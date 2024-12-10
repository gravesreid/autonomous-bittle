import serial
import time

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyAMA0',  # Use the correct serial port for your setup
    baudrate=115200,      # Baud rate
    timeout=1             # Timeout for read operations
)


def main():
    time.sleep(2)  # Give some time for the connection to establish
    print("Starting Serial communication. Press 'exit' to quit.")

    try:
        while True:
            print("Press 'c', 'h', 'n', or 't' to send commands.")
            key = input("Enter a key: ")
            if len(key) > 1:
                user_input = key
            elif key == 'c':
                user_input = "kwkF"
            elif key == 'h':
                user_input = "kwkL"
            elif key == 'n':
                user_input = "kwkR"
            elif key == 't':
                user_input = "kbk"
            elif key == 's':
                user_input = "krest"
            elif key == 'q':  # Press 'q' to exit
                print("Exiting...")
                break
            else:
                user_input = "krest"
                continue

            # Send the user input to the ESP32
            ser.write((user_input + '\n').encode('utf-8'))
            print(f"Sent: {user_input}")

            # Wait for a response from the ESP32
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f"Received: {response}")
            else:
                print("No response received")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()


