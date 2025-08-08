# AI Tic Tac Toe Bot
# Description:

This is our group's AI Tic Tac Toe Bot (Using Minimax/Alpha Beta Pruning/Expectiminimax). 

Note 1: add your own .env file with your own "GEMINI_API_KEY=" statement.
Note 2: Creating a decision tree creates a png in the project folder named visualized_decision_tree.png

# HOW TO RUN

Run main.py. This file displays the UI version. If you want to run the terminal/debug version instead, run main_debug.py.

# Dependencies:

This project uses:
- Pygame for the UI
- Google Gemini
- Graphviz for decision tree visualization.

To download these dependencies, run these commands in your terminal:
pip install pygame
pip install graphviz
pip install python-dotenv
pip install google-genai

In addition, Graphviz also requires you to download the Graphviz software, and to add it to your system PATH

To run the visualization code, you must install:

1. **Graphviz Software, Version 13.1.0** (for rendering)
    - Download from https://graphviz.org/download/, download version 13.1.0, using the exe listed
    - During installation, make sure to add Graphviz's `/bin` folder to your system PATH. There is an option to do so in the installer. If you miss this option during installation, you'll have to manually add it.

    Once the Graphviz software has been added to your system PATH, make sure you restart your IDE/Code Editor/Terminal, so it will update to display
