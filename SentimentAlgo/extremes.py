"""
_Sentiment Analysis Algorithm -> Data Analysis_
@author:
    Jakob Balkovec

@date:
    July 3, 2023

@version:
    1.0

@license:
    This code is licensed under the MIT License.

@file:
    extremes.py
    
@desc This script reads a JSON file containing objects with polarity values and finds 
      the objects with the highest and lowest polarity.

@file_format {
          JSON file format -> JSON str:
          {
              "polarity": double,
              "id": str,
              "date": str,
              "user": "str",
              "text": "str",
              "classification": str
          }
        }
"""

"__imports__"
import json
import shutil
from tqdm import tqdm
from typing import List

"__constants__"
INPUT_JSON: str = "out/output.json"
OUT_FILE_: str = "data/extremes.json"
NUM_OBJECTS_: int = 5
LOW_TITLE_: str = "\n{lowest polarity object/s}\n"
HIGH_TITLE_: str = "\n{highest polarity object/s}\n"

DEBUG_: bool = False

"""__summary__
:desc: (function) Returns a tuple containing the objects with the highest and lowest polarity 
       from the given data_set (JSON file).

:param: file_path (str): The path to the JSON file.
:param: num_objects (int): The number of objects to retrieve.
:param: polarity_key (str, optional): The key to use for sorting the objects by polarity. Defaults to "polarity".

:return: tuple: A tuple containing the objects with the highest 
                polarity and the objects with the lowest polarity.
"""
def get_objects_with_extreme_polarity(file_path: str, num_objects: int, polarity_key: str = "polarity") -> tuple:
    with open(file_path) as f:
        data = json.load(f)

    sorted_objects = sorted(data, key=lambda x: x[polarity_key])
    highest_polarity_objects = sorted_objects[-num_objects:]
    lowest_polarity_objects = sorted_objects[:num_objects]

    return highest_polarity_objects, lowest_polarity_objects

"""__summary__
:desc: A function that retrieves the maximum value from a list of objects with extreme polarity.

:return: str: The maximum value.
"""
def get_max() -> str:
    max, _ = get_objects_with_extreme_polarity(INPUT_JSON, 1, "polarity")
    return max

""" __summary__
:desc: A function that retrieves the minimum value from a list of objects with extreme polarity.

:return: str: The maximum value.
"""
def get_min() -> str:
    _, min = get_objects_with_extreme_polarity(INPUT_JSON, 1, "polarity")
    return min
    

"""__summary__
:desc: (function) Print the JSON objects with a given title.

:param: objects (list): The list of JSON objects to be printed.
:param: title (str): The title to be displayed before printing the objects.

:return: None
"""
def print_json_objects(objects: List[str], title: str) -> None:
    break_terminal()
    print(f"\n{title}\n")
    print(json.dumps(objects[:-1], indent=4, ensure_ascii=False))

"""__summary__
:desc: (function) Breaks the terminal by printing a horizontal line if debugging is enabled.

:param: debug (bool): A boolean indicating whether debugging is enabled.

:return: None
"""
def break_terminal() -> None:
  if DEBUG_:
      terminal_width, _ = shutil.get_terminal_size()
      horizontal_line = '-' * terminal_width
      print(horizontal_line)
  else:
    pass

"""__summary__
:desc: (function) Write the highest and lowest polarity objects to a file.

:param: filepath (str): The path of the file to write to.
:param: highest_objects (list): A list of the highest polarity objects.
:param: lowest_objects (list): A list of the lowest polarity objects.

:return: None
"""
def write_to_file(filepath: str, highest_objects: List[str], lowest_objects: List[str]) -> None:
    extremes = {
        "highest_polarity_objects": highest_objects,
        "lowest_polarity_objects": lowest_objects
    }
    total_items = NUM_OBJECTS_
    with tqdm(total=total_items, desc="[writing data...]    ") as pbar:
        with open(filepath, "w") as file:
            json.dump(extremes, file, indent=4)
            pbar.update(total_items)

    print(f"[data written to file]:\t {filepath}\n\n")
    
"""__summary__
:desc: (function) Prints and writes the highest and lowest polarity objects
       in a JSON file to a JSON file.

:param: None

:return: None
"""
def find_extremes() -> None:
    highest_polarity_objects, lowest_polarity_objects = get_objects_with_extreme_polarity(INPUT_JSON, NUM_OBJECTS_)
    if DEBUG_:
      print_json_objects(highest_polarity_objects, HIGH_TITLE_)
      print_json_objects(lowest_polarity_objects, LOW_TITLE_)

    else:
      write_to_file(OUT_FILE_, highest_polarity_objects, lowest_polarity_objects)
      
    return None
  

def main() -> None:
    find_extremes()
    
if __name__ == "__main__":
    main()
