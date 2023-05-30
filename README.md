# Checkers

## About
"Checkers" is a simple application that allows users to play checkers. It enables both 1v1 human vs. human gameplay and human vs. machine gameplay..

## Configuration
The application allows loading a configuration file with various settings and also enables changing most settings during gameplay. The configuration file is located in the directory ``/resources`` and is named ``config.json.``.


It should have the following structure:
```json
{
  "first_player": "Username 123",
  "second_player": "Username 2sss",
  "theme": "Dark",
  "language": "EN",
  "king_multiple_moves": false,
  "obligatory_best_beat": false,
  "reverse_beat": false,
  "opponent": "Computer",
  "difficulty": "Medium",
  "time": "1"
}
```
Where:
 - ``first_player`` - nickname of the first player
 - ``second_player`` - nickname of the second player
 - ``theme`` - application theme (possible values are ``Dark`` and `Light`)
 - ``language`` - application language (possible values are ``EN`` and ``PL``)
 - ``opponent`` -  opponent to play against (`Computer` or `Human`)
 - ``difficulty`` - difficulty for playing against the computer (possible values are `Easy`, `Medium`, or `Hard`)
 - ``time`` -  specified in minutes (possible values are `"0.5"`, `"1"`, `"3"`, `"5"`)

The remaining three options describe the game mode. They are detailed in the following paragraph.

## Gameplay modes
The application allows the user to configure various combinations of gameplay modes.

Gameplay modes:
 - `king_multiple_moves` -  when active, the king can move any number of squares.
 - `obligatory_best_beat` -  when active, a piece must make the best capturing move available.
 - `reverse_beat` -  when active, a piece must make the best capturing move available.

The provided modes can be set both in the configuration file and in the `Settings` section within the running application.

Any settings made within the application will automatically override the configuration file when exiting the application.

## Match history

The application provides the ability to track user actions on the board. To check the last match result, you need to go to the `History` section.

## Technologies
The following technologies were used to develop the application:
 - Python 3.10.11
 - pygame 2.4.0
 - python-i18n 0.3.9
 - python-dotenv 1.0.0
 - PyYAML 6.0

