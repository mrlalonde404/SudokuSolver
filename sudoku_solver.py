import os
import time

# the sudoku grid, rows and columns
grid = []
grid_rows = []
grid_cols = []

# the counts of each value in the entire grid
counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

# number of starter hints
starter_hints = 0

# frames per second to see the animation
fps = 4

# box row and column index limits
boxes = [
		[0, 2, 0, 2], [0, 2, 3, 5], [0, 2, 6, 8], 
		[3, 5, 0, 2], [3, 5, 3, 5], [3, 5, 6, 8],
		[6, 8, 0, 2], [6, 8, 3, 5], [6, 8, 6, 8]
		]

# all available values in every cell, 9 empty lists in 1 list, then append the available cell's values in the appropriate innermost list
all_cells_available = [ [] for _ in range(9) ]


def refresh(clear=True):
	# clear the command line output from the screen
	if clear:
		os.system("clear")

	# output the sudoku grid
	show_grid_rows()


def show_grid_rows():
	for i in range(len(grid_rows)):
		# print the the lines where the box boundaries should be shown
		if i % 3 == 0:
			print("++-----------++-----------++-----------++")
		else:
			# print the lines separating each row
			print("||---|---|---||---|---|---||---|---|---||")

		if i % 3 == 0 and i != 0:
			print("++-----------++-----------++-----------++")

		# build the lines for the numbers to be spaced out 
		s1 = ""
		s2 = ""
		for j in range(len(grid_rows[i])):
			if j == 0:
				s1 += "||   |"
				if grid_rows[i][j] == 0:
					s2 += "|| ? |"
				else:
					s2 += f"|| {grid_rows[i][j]} |"
			else:
				s1 += "   |"

				if grid_rows[i][j] == 0:
					s2 += " ? |"
				else:
					s2 += f" {grid_rows[i][j]} |"
				if j % 3 == 2:
						s1 += "|"
						s2 += "|"
		# print the lines with the numbers on it
		print(s1)
		print(s2)
		print(s1)

	# print the last box line
	print("++-----------++-----------++-----------++")


def print_grid_cols():
	for i in range(len(grid_cols)):
		print(grid_cols[i])	


# makes the sudoku grid from the file at file_name
def make_grid(file_name):
	# use the global grid to modify
	global grid
	global grid_rows
	global grid_cols
	global counts
	global starter_hints

	# open the input grid file and get the text to make the sudoku grid rows
	file = open(file_name, "r")
	lines = file.readlines()

	for i in range(len(lines)):
		# skip the first line
		if i == 0:
			continue

		if lines[i] == "\n":
			continue

		# make the new line by splitting by the commas and removing the new line
		new_line = lines[i].strip("\n").split(",")

		# make the new list  by converting the numbers to integers
		row = []

		for el in new_line:
			# get the value as an integer
			val = int(el)

			# increment the count for this value
			if val != 0:
				counts[val] += 1

			# add the value to the row
			row.append(val)
			grid.append(val)

		# append the row of integers into the grid_rows
		grid_rows.append(row)

	# get the number of starter hints
	starter_hints = sum(counts.values())

	# make the grid_cols from the grid_rows
	i = 0
	while i < 9:
		col = []
		for j in range(len(grid_rows[i])):
			col.append(grid_rows[j][i])
		grid_cols.append(col)
		i += 1


def check_if_solved():
	# get the toal number of all filled cells in the grid
	count = sum(counts.values())

	# if the total count of cells filled is 81, then the entire 9x9 grid cell has been completely filled in
	if count >= 81:
		return True
	else: 
		return False


def solve_sudoku():
	# print the board and possibile moves at least 1 time
	refresh(clear=True)
	print_all_available_values(show_filled_in=False)

	# if the sudoku has not been solved, keep filling in squares 
	while not check_if_solved():
		for row in range(9):
			for col in range(9):
				# only look at cells that haven't been filled in yet
				if grid[get_grid_index(row, col)] == 0:
					# get the available numbers in the row
					available_row = get_available_in_row(row)

					# get the available numbers in the column
					available_col = get_available_in_column(col)

					# get the available numbers in the box where the cell at row, col is
					available_box = get_available_in_box(row, col)

					# get the available values that could fill in this spot
					cell_available = all_cells_available[row][col]

					# look at the row to see if it can fill in the last spot
					if len(available_row) == 1:
						mark_cell(row, col, available_row[0])
						print("Filled last cell in row.")
					
					# look at the column to see if it can fill in the last spot
					if len(available_col) == 1:
						mark_cell(row, col, available_col[0])
						print("Filled last cell in column.")
					
					# look at the box to see if it can fill in the last spot
					if len(available_box) == 1:
						mark_cell(row, col, available_box[0])
						print("Filled last cell in box.")
						
					# if the spot only has one available move, fill in that number
					if len(cell_available) == 1:
						mark_cell(row, col, cell_available[0])
						print("Only 1 available value in cell.")
						
					else:
						print(f"row: {row}, col: {col}")
						# more than 1 available value
						for val in cell_available:
							#print(f"value: {val}")

							# -- hidden singles start --
							if not check_row_for_same_available_val(row, col, val):
								mark_cell(row, col, val)
								print(f"This was the only cell in row {row} that had {val} available.")

							if not check_col_for_same_available_val(row, col, val):
								mark_cell(row, col, val)
								print(f"This was the only cell in column {col} that had {val} available.")

							if not check_box_for_same_available_val(row, col, val):
								mark_cell(row, col, val)
								print(f"This was the only cell in box {get_box_index(row, col)} that had {val} available.")
							# -- hidden singles end -- 

					# if fps is given a value then use sleep so that the animation of the cell being filled can be seen						
					if fps:
						time.sleep(1.0/fps)

		# after going through all the cells, see if you can remove some available values to speed up the solving
		remove_possibilities()


def remove_possibilities():
	print("Remove possibilities:")
	# candidate lines
	# loop through every box and get their lists of candidates for each box
	all_candidates = []
	for box in range(9):
		# get the limits for the box
		limits = boxes[box]
		
		# get the candidates that appear 2 times in the same box
		candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		for val in range(1, 10):
			count = 0
			for row in range(limits[0], limits[1]+1):
				for col in range(limits[2], limits[3]+1):
					if val in all_cells_available[row][col]:
						count += 1
			# if the candidate does not show up exactly twice in the same box, remove it from the candidate list
			if count != 2:
				candidates.remove(val)
		# add the list of candidates to the list that will hold every box's candidates
		all_candidates.append(candidates)
		print(f"box: {box}, candidates: {candidates}")

	# go through the candidates for every box
	for box in range(len(all_candidates)):
		# get the limits for the box
		limits = boxes[box]

		if len(all_candidates[box]) > 0:
			# loop through every candidate and see if it has a candidate of the same value in the same row or column
			for can in all_candidates[box]:
				# check row for 2 of the same candidate
				for row in range(limits[0], limits[1]+1):
					count = 0
					cols = []
					for col in range(limits[2], limits[3]+1):
						if can in all_cells_available[row][col]:
							# increment the counter when the value is found in the row
							count += 1
							# add the column index in the event that there are 2 of the same candidate in the same row
							cols.append(col)

					# if the candidate was seen twice in the same row, remove it from the rest of the cells in this row not in cols
					if count == 2:
						for col in range(9):
							# only keep the candidate values in the cols that it was seen in this box, remove everywhere else
							if col not in cols:
								# if the candidate is in this cell, remove it
								if can in all_cells_available[row][col]:
									all_cells_available[row][col].remove(can)
									print(f"Removed: {can}, from, row: {row}, col: {col}")

				# check column for 2 of the same candidate
				for col in range(limits[2], limits[3]+1):
					count = 0
					rows = []
					for row in range(limits[0], limits[1]+1):
						if can in all_cells_available[row][col]:
							# increment the counter when the value is found in the column
							count += 1
							# add the row index in the event that there are 2 of the same candidate in the same column
							rows.append(row)

					# if the candidate was seen twice in the same column, remove it from the rest of the cells in this column not in rows
					if count == 2:
						for row in range(9):
							# only keep the candidate values in the rows that it was seen in this box, remove everywhere else
							if row not in rows:
								# if the candidate is in this cell, remove it
								if can in all_cells_available[row][col]:
									all_cells_available[row][col].remove(can)
									print(f"Removed: {can}, from, row: {row}, col: {col}")
	
	# -- naked pair start --
	# look through rows
	for row in range(9):
		pair = []
		for col in range(9):
			# if the pair hasn't filled yet in this row
			if len(pair) == 0 and len(all_cells_available[row][col]) == 2:
				pair = all_cells_available[row][col]
			# a pair was obtained, see if you can remove possibilities in the rest of this row
			if len(pair) == 2:
				pass

	# look through columns
	for col in range(9):
		for row in range(9):
			pass
	# -- naked pair end --

	# -- hidden pair start --
	# -- hidden pair end --

	# -- pointing pair start --
	# -- pointing pair end --
    
def get_all_cells_available_values():
	global all_cells_available
	for row in range(9):
		for col in range(9):
			all_cells_available[row].append(get_cell_available_values(row, col))


# use the row index and column index
def get_cell_available_values(row, col, available_row=None, available_col=None, available_box=None):
	if grid[get_grid_index(row, col)] == 0:
		# if list of values for available_row, available_col, and available_box are given then use those instead of computing the same values again
		if available_row is None and available_col is None and available_box is None:
			# get the available numbers in the row
			available_row = get_available_in_row(row)

			# get the available numbers in the column
			available_col = get_available_in_column(col)

			# get the available numbers in the box where the cell at row, col is
			available_box = get_available_in_box(row, col)

		# return the available values that are in the row, column, and box
		available = []

		for val in range(1, 10):
			if val in available_row and val in available_col and val in available_box:
				available.append(val)

		# return the available values
		return available
	else:
		return []


# use the row index
def get_available_in_row(row):
	# start with all 9 values
	available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	
	# get the grid row from the row index
	grid_row = grid_rows[row]

	# remove values that are in the grid row from the available values
	for i in range(len(grid_row)):
		if grid_row[i] in available:
			available.remove(grid_row[i])

	# return the available values
	return available


# use the column index
def get_available_in_column(col):
	# start with all 9 values
	available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	
	# get the grid column from the row index
	grid_col = grid_cols[col]

	# remove values that are in the grid column from the available values
	for i in range(len(grid_col)):
		if grid_col[i] in available:
			available.remove(grid_col[i])

	# return the available values
	return available


def get_available_in_box(row, col):
	# start with all 9 values
	available = [1, 2, 3, 4, 5, 6, 7, 8, 9]

	# get the box index from the row and column
	box_ind = get_box_index(row, col)
	
	# get the box from the box index
	box = get_values_in_box(box_ind)

	# remove values that are in the grid box from the available values
	for i in range(len(box)):
		if box[i] in available:
			available.remove(box[i])

	# return the available values
	return available


# use the row and column indexes to get what box the cell at (row, col) is
def get_box_index(row, col):
	if 0 <= row < 3:
		if col < 3:
			box = 0
		elif 3 <= col < 6:
			box = 1
		elif 6 <= col < 9:
			box = 2
	if 3 <= row < 6:
		if col < 3:
			box = 3
		elif 3 <= col < 6:
			box = 4
		elif 6 <= col < 9:
			box = 5
	if 6 <= row < 9:
		if col < 3:
			box = 6
		elif 3 <= col < 6:
			box = 7
		elif 6 <= col < 9:
			box = 8
	return box


# use the box index to get the list of values in that box
# box with values:
# 1 2 3
# 4 5 6
# 7 8 9
# will return [1, 2, 3, 4, 5, 6, 7, 8, 9]
def get_values_in_box(box):
	# the values in the box with the box index
	values = []

	# get the row and column limits
	limits = boxes[box]

	# get the values from the row min to the row max and the column min to the column max
	for row in range(limits[0], limits[1]+1):
		for col in range(limits[2], limits[3]+1):
			# add the value at the grid index (for row,col)
			values.append(grid[get_grid_index(row, col)])

	# return the box's values
	return values


# use the row and column indexes to get the index in the [0,80] index list for the grid
def get_grid_index(row, col):
	if row == 0:
		return col
	else:
		return (row * 9) + col


# look if the same available value appears in the same row
def check_row_for_same_available_val(row, col, val):
	for c in range(9):
		if c != col:
			if val in all_cells_available[row][c]:
				# returns true if their is a matching value
				return True
	return False


# look if the same available value appears in the same row
def check_col_for_same_available_val(row, col, val):
	for r in range(9):
		if r != row:
			if val in all_cells_available[r][col]:
				# returns true if their is a matching value
				return True
	return False	


# look if the same available value appears in the same box
def check_box_for_same_available_val(row, col, val):
	# get the box and the box's limits from the row and column
	box_ind = get_box_index(row, col)
	limits = boxes[box_ind]

	# print("Inside check box function:")
	for r in range(limits[0], limits[1] + 1):
		for c in range(limits[2], limits[3] + 1):
			if (r == row and c != col) or (r != row and c == col) or (r != row and c != col):
				if val in all_cells_available[r][c]:
					# print(f"Found same value at row: {r}, col: {c}")
					# returns true if their is a matching value
					return True
	return False	


# remove the value from the available values for cells in the same row 
def remove_available_value_row(row, val):
	global all_cells_available
	for col in range(9):
		if val in all_cells_available[row][col]:
			all_cells_available[row][col].remove(val)
			print(f"removed {val} from row: {row}, col: {col}")


# remove the value from the available values for cells in the same column
def remove_available_value_col(col, val):
	global all_cells_available
	for row in range(9):
		if val in all_cells_available[row][col]:
				all_cells_available[row][col].remove(val)
				print(f"removed {val} from row: {row}, col: {col}")


# remove the value from the available values for cells in the same box
def remove_available_value_box(box, val):
	global all_cells_available
	# get the rox, column indexes for this box
	limits = boxes[box]

	# remove val from the the available values for this box from the row min to the row max and the column min to the column max
	for row in range(limits[0], limits[1]+1):
		for col in range(limits[2], limits[3]+1):
			if val in all_cells_available[row][col]:
				all_cells_available[row][col].remove(val)
				print(f"removed {val} from row: {row}, col: {col}")			


# after a spot is filled in remove that value from possible moves in any other cell in row, column, box
def mark_cell(row, col, val):
	global grid
	global grid_rows
	global grid_cols
	global counts

	# if the cell is zero, it can be filled in
	if grid[get_grid_index(row, col)] == 0:
		# mark the cell in the grid row
		grid_rows[row][col] = val

		# mark the cell in the gric column
		grid_cols[col][row] = val

		# mark the cell in the grid list with the value
		ind = get_grid_index(row, col)

		#print(f"index: {ind}")
		grid[ind] = val

		# increment the count for the value
		counts[val] += 1

		# remove the available moves in the cell we just marked
		all_cells_available[row][col].clear()

		# remove the value from the available values for cells in the same row, column and box
		remove_available_value_row(row, val)
		remove_available_value_col(col, val)
		# get the box and remove available values
		box_ind = get_box_index(row, col)
		remove_available_value_box(box_ind, val)

		# refresh the screen to show the change
		refresh(clear=True)
		print(f"MARKED: row: {row}, col: {col}. This spot marked with: {val}")
		print_all_available_values(show_filled_in=False)


def get_cell_info(row, col):
	row_available = get_available_in_row(row)
	col_available = get_available_in_column(col)
	box_available = get_available_in_box(row,col)
	cell_available = all_cells_available[row][col]

	print(f"row: {row}, col: {col}")
	print(f"row available: {row_available}")
	print(f"column available: {col_available}")
	print(f"box available: {box_available}")
	print(f"cell available: {cell_available}")


def print_all_available_values(show_filled_in=True):
	print("Every cell's available moves:")
	print(f"Value counts: {counts}")
	for box in range(9):
		# get the row and column limits
		limits = boxes[box]

		print(f"box: {box}")
		# print the available values for this box from the row min to the row max and the column min to the column max
		for row in range(limits[0], limits[1]+1):
			for col in range(limits[2], limits[3]+1):
				if len(all_cells_available[row][col]) != 0:
					print(f"  - row: {row}, col: {col}, available: {all_cells_available[row][col]}")
				else:
					if show_filled_in:
						print(f"  - row: {row}, col: {col}. This spot marked with: {grid[get_grid_index(row, col)]}")


def main():
	# start time
	start_time = time.time()

	# make the grid
	make_grid("input_grid.txt")

	# get every possible value in every cell
	get_all_cells_available_values()

	# solve the sudoku
	solve_sudoku()

	elapsed_time = time.time() - start_time
	print(f"Solved in: {elapsed_time} sec. Puzzle started with {starter_hints} hints.")

if __name__ == "__main__":
	main()