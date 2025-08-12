import sys

def main():
    # Get the argument passed to the script
    if len(sys.argv) > 1:
        argument = sys.argv[1]  # First command-line argument
        print(f"Received argument: {argument}")
    else:
        print("No arguments provided")

if __name__ == "__main__":
    main()
