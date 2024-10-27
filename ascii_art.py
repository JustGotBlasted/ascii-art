from PIL import Image
import requests
from io import BytesIO
from pathlib import Path

def warn(s):
    print(f"\033[31m{s}\033[0m") # Prints red characters

def ask(question, extra=""):
    return input(f"\033[36m{question}\033[33m{extra}\033[0m") # Prints blue characters for the question, then yellow for extra text

def main():
    result_path = Path("results/")
    result_path.mkdir(parents=True, exist_ok=True)

    while True:
        request = None
        image = None
        step = (6, 15)
        with_colors = False

        while True:
            try:
                data_from_input = ask("Where is your data from?\n", "(d) disk | (o) online\n")

                if data_from_input == 'o':
                    user_input = ask("Enter online image address to convert: ")
                    request = requests.get(user_input)
                    image = Image.open(BytesIO(request.content))
                elif data_from_input == 'd':
                    user_input = ask("Enter image file path to convert: ")
                    image = Image.open(user_input)
                else:
                    warn("Error has occurred: Invalid Input")
                    continue
                
                size_input = ask("Which pixels to check?\n", "ex. 6x15 checks for every 6th pixel horizontally and 15th pixel vertically\nLower values make the ascii larger; higher values make the ascii smaller\nDefault: 6x15 | Format: wxh\n")
                
                input_split = size_input.split("x")
                if len(input_split) == 2 and input_split[0].isnumeric() and int(input_split[0]) > 0 and input_split[1].isnumeric() and int(input_split[1]) > 0:
                    xstep = int(input_split[0])
                    ystep = int(input_split[1])
                    step = (xstep, ystep)
                elif input_split != "":
                    warn("Error with parsing scale; using default 6x15")

                color_input = ask("Add colors?\n", "Default: (n) no | (y) yes\n")
    
                if color_input == 'n':
                    with_colors = False
                elif color_input == 'y':
                    with_colors = True
                elif color_input != ' ':
                    warn("Error with parsing scale; using default no colors")

                break

            except Exception as e:
                warn(f"Error has occurred: {e}")

        print("\033[35mCreating...\033[0m")
        width, height = image.size
        ascii_art = ""

        image = image.convert("RGB")

        for y in range(0, height, step[1]):
            for x in range(0, width, step[0]):
                r, g, b = image.getpixel((x, y))
                brightness = r * 299/1000 + g * 587/1000 + b * 114/1000

                if with_colors:
                    ascii_art += f"\033[38;2;{r};{g};{b}m" # Assigns colors to character
                
                if brightness < 15:
                    ascii_art += " "
                elif brightness < 50:
                    ascii_art += "."
                elif brightness < 90:
                    ascii_art += "*"
                elif brightness < 140:
                    ascii_art += "/"
                elif brightness < 200:
                    ascii_art += "&"
                else:
                    ascii_art += "@"

            ascii_art += "\n"
        
        ascii_art += "\033[0m" # Resets terminal character color

        print(ascii_art)

if __name__ == "__main__":
    main()

