"""
Name: Ashlee Shum
UPI: ashu443
Student ID: 971424393
Date: 10/10/24
Description: This is a connect 4 game where the user plays against the computer and is given a
unique disk. The user then has to try get as many of the same disks to be 4 times in a row,
either horizontally, diagonally or vertically. Each point is gained from how many 4 disks
in a row combinations there are, and the winner is determined by whoever has the most points.
The game board is visually printed out in the program, so the user can see what move to play
next or what the board currently looks like. The user can also decide what size they want the
board to be, whether it is 4 x 4 or 7 x 7.
"""
import math
import random
import tkinter as tk
from tkinter import messagebox


class GameBoard:
    def __init__(self, size=4):
        # initialising variables for game
        self.size = size
        self.num_disks = [0] * self.size
        self.items = [[0] * size for i in range(self.size)]
        self.points = [0] * 2

        # creating popup GUI
        self.window = tk.Tk()
        self.window.title("Connect Four")
        self.window.geometry("1100x550")
        self.run_program()
        self.window.mainloop()

        self.current_disk_type = 0


    def run_program(self):
        """
        Description: Runs the entire program, starting first with the instructions and introductory window
        """

        # formatting and making the home window aesthetically pleasing
        dash = tk.Label(self.window, text="----" * 38)
        dash.pack(pady=10)
        empty_line = tk.Label(self.window, text="")
        empty_line.pack()
        heading = tk.Label(self.window, text="Welcome to CONNECT 4  (⸝⸝´꒳`⸝⸝)", font=("Courier", 25))
        heading.pack()

        empty_line = tk.Label(self.window, text="")
        empty_line.pack()
        dash = tk.Label(self.window, text="----" * 38)
        dash.pack()

        instructions = tk.Label(
            self.window,
            justify="left",
            text="""
        Read below for the instructions for connect 4: 

        1) Choose what grid size you want (suggested: 4 by 4)
        2) Click the button of which column you want to put your token into, 
           and wait for the computer to play their turn.
        3) Keep playing the game until the entire board is full !

        "Note: Points are calculated based on how many four in a rows you have on a board. 
        Winner has the most points.""", font=("Courier", 15))
        instructions.pack(pady=10)

        grid_size_text = tk.Label(self.window, justify="left",
                                  text="Enter a digit from 4 to 10 (inclusive) to choose what size grid you want, then press submit:",
                                  font="Courier")
        grid_size_text.pack(pady=10)

        # creating an entry widget for grid size input
        self.entry_grid_size = tk.Entry(self.window, width=30)
        self.entry_grid_size.pack(pady=10)

        # creating a submit button
        button = tk.Button(self.window, text="Submit", font="Courier", command=self.grid_size)
        button.pack(pady=5)

        self.window.mainloop()

    def grid_size(self):
        """
        Description: Makes sure the user enters appropriate grid size, and if they do, then are directed to the game window.
                if not, then an error message occurs and prompts user to input a valid grid size.
        """

        # making error messages if the user enters an invalid integer
        try:
            # getting input from entry widget
            self.size = int(self.entry_grid_size.get())

            if 4 <= self.size <= 10:
                # re-initialising to users input
                self.num_disks = [0] * self.size
                self.items = [[0] * self.size for i in range(self.size)]

                # checking if the game is over, if not then open the connect 4 window
                if not self.game_over():
                    self.display_window()

            else:
                # error if user enters an integer not between 4 and 10
                messagebox.showerror("Invalid input", "Please enter a digit from 4 to 10 (inclusive).")
                self.entry_grid_size.delete(0, tk.END)

        except ValueError:
            # error if the user enters a string
            messagebox.showerror("Invalid input", "Please enter a valid integer.")
            self.entry_grid_size.delete(0, tk.END)


    def display_window(self):
        """
        Description: creates the window the user plays the game on
        """
        # creating the window to play connect 4 on
        self.play_window = tk.Toplevel(self.window)
        # adjusting window size based on what grid size users choose
        if self.size <= 5:
            self.play_window.geometry("400x400")
        elif 5 < self.size <= 8:
            self.play_window.geometry("600x600")
        elif 8 < self.size <= 10:
            self.play_window.geometry("800x700")
        self.play_window.title("Play the game !!")
        # go to the function to create the grid for connect 4
        self.create_grid()

        self.window.mainloop()

    def num_free_positions_in_column(self, column):
        """
        Description: returns how many free positions there are in a specific column
        """
        empty = 0
        for j in range(self.size):
            if self.items[column][j] == 0:
                empty += 1
        return empty

    def game_over(self):
        """
        Description: returns False if no positions are free on the gameboard.
        """
        for column in range(self.size):
            if self.num_free_positions_in_column(column) > 0:
                return False
        return True

    def create_grid(self):
        """
        Description: creates the connect 4 grid on tkinter pop up window depending on what size grid the user entered.
        """

        # initialising grid for connect 4 board
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.cell_size = 50
        self.canvas_width = self.size * self.cell_size
        self.canvas_height = self.size * self.cell_size

        self.canvas = tk.Canvas(self.play_window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # creating circular grid
        for r in range(self.size):
            for c in range(self.size):
                x = c * self.cell_size + self.cell_size // 2
                y = r * self.cell_size + self.cell_size // 2
                self.grid[r][c] = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")

        # creating a button for each column and aligning them
        button_frame = tk.Frame(self.play_window)
        button_frame.pack()

        for c in range(self.size):
            button = tk.Button(button_frame, text=f"{c + 1}", command=lambda col=c: self.player_turn(col),
                               width=2, font="Courier")
            button.grid(row=0, column=c, padx=2, pady=2)

        # creating the player points text to display underneath the grid and buttons
        score_frame = tk.Frame(self.play_window)
        score_frame.pack()

        self.player1_score_label = tk.Label(score_frame, text=f"Your score (pink): {self.points[0]}", font=("Courier", 12))
        self.player1_score_label.grid(row=0, column=0, padx=10)

        self.player2_score_label = tk.Label(score_frame, text=f"Computer score (purple): {self.points[1]}", font=("Courier", 12))
        self.player2_score_label.grid(row=1, column=0, padx=10)


    def num_new_points(self, column, row, player):
        """
        Description: returns the number of points you get from having 4 or more disks in a row.
        """
        count = 0

        # (column, row)
        directions = [
            (1, 0),  # horizontal right - column moves one to the right, row stays same
            (0, 1),  # vertical up - column stays the same, row moves up one
            (1, 1),  # diagonal up-right - column moves one to the right and row moves one up
            (-1, 1),  # diagonal up-left - column moves one to the left and up one
        ]

        for d_col, d_row in directions:
            total = 0  # how many disks we have encountered from the SAME PLAYER

            # checking horizontal and diagonal
            c, r = column, row
            # check that disk is same as player, and that the column and row are within given size of board
            while 0 <= c < self.size and 0 <= r < self.size and self.items[c][r] == player:
                total += 1

                # going to next column
                c += d_col
                r += d_row

            # first total matches excluding the newly added disk
            first_total = total - 1

            # check in the vertical and diagonal
            c, r = column - d_col, row - d_row
            while 0 <= c < self.size and 0 <= r < self.size and self.items[c][r] == player:
                total += 1
                c -= d_col
                r -= d_row

            # second total matches on other direction
            second_total = total - first_total - 1

            # if 4 disks in a row found
            if total >= 4:
                # if new disk is added to ends then just count as 1 match
                if first_total == 0 or second_total == 0:
                    count += 1
                else:
                    # this section covers when disk is added joining 2 sequences

                    # keep track of existing counted matches
                    first_total_count = 0
                    second_total_count = 0

                    # if first line of sequences >= 4 then it is already counted in previous adds
                    if first_total >= 4:
                        # formula to calculate how many points earned in a sequence of disks greater than 4
                        first_total_count = 1 + first_total - 4
                    # if second line of sequences >= 4 then it is already counted in previous adds
                    if second_total >= 4:
                        second_total_count = 1 + second_total - 4

                    # calculate total number of sequences minus the previously counted ones
                    count += 1 + (total - 4) - first_total_count - second_total_count

        return count

    def add_disk(self, column, player):
        """
        Description: adds a disk of the given player to the given column.
        """
        # add disk to selected column
        row = self.num_disks[column]
        self.items[column][row] = player
        self.num_disks[column] += 1
        self.points[player - 1] += self.num_new_points(column, row, player)


        # set disk color
        disk_color = "pink" if player == 1 else "purple"
        self.canvas.itemconfig(self.grid[self.size - row - 1][column], fill=disk_color)

        # display player points text
        self.player1_score_label.config(text=f"Your score (pink): {self.points[0]}")
        self.player2_score_label.config(text=f"Computer score (purple): {self.points[1]}")

        # checking if game is over, if it is then display the winner
        if self.game_over():
                self.show_winner()

    def player_turn(self, col):
        """
        Description: adds the players disk to their desired column
        """
        if self.num_free_positions_in_column(col) > 0:
            self.add_disk(col, player=1)  # player disk
            if not self.game_over():
                self.computer_turn()  # computer's turn

    def computer_turn(self):
        """
        Description: computer generates a column to add their disk to
        """
        free_slots = self.free_slots_as_close_to_middle_as_possible()
        if free_slots:
            # randomly selecting a column from the list of free slots available
            col = random.choice(free_slots)
            self.add_disk(col, player=2)

    def show_winner(self):
        """
        Description: displays a message declaring the winner of the game, then prompts the user if they want to play
        again or exit.
        """
        winner_window = tk.Toplevel(self.window)
        winner_window.title("Game Over")
        winning_msg = ""

        # winning messages
        if self.points[0] > self.points[1]:
            winning_msg = f"Player 1 wins ( ꩜ ᯅ ꩜;)⁭ ⁭!\nPlayer 1: {self.points[0]} points\nPlayer 2: {self.points[1]} points"
        elif self.points[0] < self.points[1]:
            winning_msg = f"Computer wins ( ꩜ ᯅ ꩜;)⁭ ⁭!\nPlayer 1: {self.points[0]} points\nPlayer 2: {self.points[1]} points"
        elif self.points[0] == self.points[1]:
            winning_msg = f"You tied !! ( ꩜ ᯅ ꩜;)⁭ ⁭!\nPlayer 1: {self.points[0]} points\nPlayer 2: {self.points[1]} points"

        # displaying winner message
        winner_message = tk.Label(winner_window, text=winning_msg, font="Courier")
        winner_message.pack(pady=20, padx = 10)
        restart_button = tk.Button(winner_window, text="Restart?", font="Courier", command=self.restart_game)
        restart_button.pack(pady=20, padx = 10)
        exit_button = tk.Button(winner_window, text="Exit", font="Courier", command = self.exit)
        exit_button.pack(pady=10)

    def exit(self):
        """
        Description: exits the game, closes windows
        """
        self.window.destroy()

    def restart_game(self):
        """
        Description: this function restarts the entire game and resets the points and grid size - runs from the beginning again.
        """
        self.window.destroy()
        GameBoard()

    def free_slots_as_close_to_middle_as_possible(self):
        """
        Description: returns a list of columns closest to the middle that have free slots available.
        """
        free_slots_list = []
        middle = math.floor((0 + self.size - 1) // 2)  # finding the middle column of the grid

        for offset in range(self.size):
            # calculating the next column closest to the middle
            left = middle - offset
            right = middle + offset
            # adding the disks closest to the middle depending on whether the grid is an even or odd number
            if self.size % 2 == 0:

                if self.size > right != left and self.num_free_positions_in_column(right) > 0:
                    free_slots_list.append(right)

                if left >= 0 and self.num_free_positions_in_column(left) > 0:
                    free_slots_list.append(left)

            else:
                if left >= 0 and self.num_free_positions_in_column(left) > 0:
                    free_slots_list.append(left)

                if self.size > right != left and self.num_free_positions_in_column(right) > 0:
                    free_slots_list.append(right)

        return free_slots_list

    def column_resulting_in_max_points(self, player):
        """
        Description: returns the column you would get max points, and the number of max points you can get.
        """
        # getting the list of all free slots in the board
        slots_free = self.free_slots_as_close_to_middle_as_possible()

        max_points = 0
        max_column = slots_free[0]

        for i in range(len(slots_free)):
            column = slots_free[i]
            row = self.num_disks[column]

            # temporarily adding the disk to check for the points
            self.items[column][row] = player
            points = self.num_new_points(column, row, player)

            # resetting the disk to 0 so we don't affect the game
            self.items[column][row] = 0

            if points > max_points:
                max_points = points
                max_column = column

        return max_column, max_points

if __name__ == "__main__":
    GameBoard()


