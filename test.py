# Read the contents of the top_headlines.txt file
file_path = "top_headlines.txt"

try:
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")