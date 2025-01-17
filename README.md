In this project, I developed a Connect 4 game that features customizable grid sizes and a computer-generated opponent to provide a dynamic user experience. The user can choose the grid size, specify the column to place their token, and decide whether to replay or exit the game once it concludes. The game ends once the board is full.

I used several programming tools and practices to build and refine the game;

Python language:
- Python was the core programming language for implementing the game logic and handling user interactions. I utilized its features to create efficient algorithms for checking win conditions, switching turns between players, and implementing AI for the computer opponent.

Tkinter for GUI development:
- I used the Tkinter library to design and create the graphical user interface (GUI). For the grid creation, I used Tkinter's canvas widget to render the gameboard with circular empty rows and columns that update based on the size. The different tokens for the players are represented by different colours. Interactive buttons were implemented by using Tkinter's messagebox module, which enhanced the user experience. Getting the grids to display in the centre was difficult at first, but once I adjusted the Tkinter canvas dimensions it was good to go.

User input and Game control:
- I added functions that consistently check the win conditions - horizontal, vertical and diagonal so that the scores can be updated accordingly. I also made sure that every new move, the GUI is updated to reflect the last state.

Commenting and Code Documentation:
- Each function includes a docstring at the beginning describing what the function does. With trickier lines of code within the functions, I used in-line commenting to document and explain what is going on there so it's more efficient and readable, maintaining the code.
