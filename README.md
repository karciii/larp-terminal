# EVIL CORP Terminal System

## Description
EVIL CORP Terminal System is a hacking-lookalike terminal designed for LARP gaming and other activities. It features various animations, an encyclopedia, a journaling system, a login system, and more. The project is written in Python and uses the `colorama` library for terminal text coloring.


## Installation
1. Clone the repository:
    ```sh
    git clone <REPOSITORY_URL>
    ```
2. Navigate to the project directory:
    ```sh
    cd <PROJECT_NAME>
    ```
3. Install required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To run the terminal system, execute:
```sh
python ./main.py
```


## Animations
Animations can be enabled or disabled by setting the IS_ENABLED variable in `animations.py` to `True` or `False`.

## Files and Modules
- `animations.py`: Contains animation functions like `matrix_rain`, `glitch_line`, `data_wave_effect`, `flickering_status_line`, `generate_footer`, `frame_effect`, and `boot_sequence`.
- `encyclopedia.py`: Handles the in-game encyclopedia, including loading and saving data.
- `journal.py`: Handles the player's journal system, including adding and viewing entries.
- `login.py`: Handles user authentication, including loading and saving user data and logging operations.
- `tr.py`: Main terminal module containing functions like `show_help`, `exit_tr`, `journal_menu`, `login`, and others.

## Contributing
If you'd like to contribute to this project, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.