import pygame
from pygame import *

# finals
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

# colors
BG_COLOR = (59, 88, 107)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
START_SPOT_COLOR = (219, 72, 72)
END_SPOT_COLOR = (64, 219, 100)
OBSTACLE_SPOT_COLOR = (145, 138, 237)
SEARCH_SPOT_COLOR = (220, 128, 224)
BT_COLOR = (0, 0, 0)

# printing instructions
print("\nHey bro/sis, here is the way I set this thing up:")
print("Basically, the grid is 35 x 30 squares, but since we as programmers start our counts from 0, \n"
      "treat it like its a 34 x 29 grid :)")
print("After the inputs, the pygame window will open and you will have 15 seconds to set up obstacles \n"
      "using your mouse. Click on any grid square to set up an obstacle.")
print("Then, the magic will begin, enjoy!")

print()

# getting inputs of x and y positions of starting and ending spots
start_spot_pos_x = int(input("Enter x position of the start spot: "))
start_spot_pos_y = int(input("Enter y position of the start spot: "))
end_spot_pos_x = int(input("Enter x position of the goal spot: "))
end_spot_pos_y = int(input("Enter y position of the goal spot: "))


# initializing pygame
pygame.init()

# setting the screen
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(BG_COLOR)
pygame.display.set_caption("Breadth-First Search Visualizer")
icon = pygame.image.load("maze_icon.png")
pygame.display.set_icon(icon)


class Spot:
    def __init__(self, pos_x=0, pos_y=0, color=RED):
        # validating whether the coordinates of the spots will fit in the grid
        if pos_x <= SCREEN_WIDTH - 20:
            self.pos_x = pos_x
        else:
            self.pos_x = 0
        if pos_y <= SCREEN_HEIGHT - 20:
            self.pos_y = pos_y
        else:
            self.pos_y = 0

        self.color = color

    def draw(self):
        """this method will draw the spot on the grid"""
        pygame.draw.rect(display, self.color, [self.pos_x, self.pos_y, 20, 20])

    def get_coord(self):
        return self.pos_x, self.pos_y


# drawing grid
def draw_grid():
    rows = [r for r in range(0, 35 * 20, 20)]  # list of all the row coordinates to draw grid
    cols = [c for c in range(0, 30 * 20, 20)]  # list of all the col coordinates to draw grid

    for row in rows:
        for col in cols:
            pygame.draw.rect(display, WHITE, [row, col, 20, 20], 1)


# explore grid
def explore_grid(current_spot_pos, frontier_list, visited_list, obstacle_list):
    """
    in this function,
    - We check all the valid places to go; we add all those spots to the frontier list, one-by-one.
    - We keep track of all the spots we have visited so that we don't check them again.
    - All the places we go, we record what spot we came from (later used for back tracking).
    - Once we find a valid place, and go there, we take pop it off of the frontier list
      (from the front of the list since that would be where the most current place we go to, will be).
    """
    if len(frontier) != 0:
        right_of_curr_coord = (current_spot_pos[0] + 20, current_spot_pos[1])
        left_of_curr_coord = (current_spot_pos[0] - 20, current_spot_pos[1])
        top_of_curr_coord = (current_spot_pos[0], current_spot_pos[1] - 20)
        bottom_of_curr_coord = (current_spot_pos[0], current_spot_pos[1] + 20)

        Spot(pos_x=current_spot_pos[0], pos_y=current_spot_pos[1], color=SEARCH_SPOT_COLOR).draw()

        if (left_of_curr_coord not in visited_list) and (left_of_curr_coord not in obstacle_list) \
                and (left_of_curr_coord[0] >= 0) and (left_of_curr_coord[0] <= 680) and (left_of_curr_coord[1] >= 0) \
                and (left_of_curr_coord[1] <= 580):

            # adding the key (the next position) and value (the current/prev. position) into the solutions dictionary
            solutions[left_of_curr_coord[0], left_of_curr_coord[1]] = current_spot_pos[0], current_spot_pos[1]

            frontier.append(left_of_curr_coord)
            visited_list.append(left_of_curr_coord)
        if (right_of_curr_coord not in visited_list) and (right_of_curr_coord not in obstacle_list) \
                and (right_of_curr_coord[0] >= 0) and (right_of_curr_coord[0] <= 680) and (right_of_curr_coord[1] >= 0)\
                and (right_of_curr_coord[1] <= 580):

            # adding the key (the next position) and value (the current position) into the solutions dictionary
            solutions[right_of_curr_coord[0], right_of_curr_coord[1]] = current_spot_pos[0], current_spot_pos[1]

            frontier.append(right_of_curr_coord)
            visited_list.append(right_of_curr_coord)
        if (top_of_curr_coord not in visited_list) and (top_of_curr_coord not in obstacle_list) \
                and (top_of_curr_coord[0] >= 0) and (top_of_curr_coord[0] <= 680) and (top_of_curr_coord[1] >= 0) \
                and (top_of_curr_coord[1] <= 580):

            # adding the key (the next position) and value (the current/prev. position) into the solutions dictionary
            solutions[top_of_curr_coord[0], top_of_curr_coord[1]] = current_spot_pos[0], current_spot_pos[1]

            frontier.append(top_of_curr_coord)
            visited_list.append(top_of_curr_coord)
        if (bottom_of_curr_coord not in visited_list) and (bottom_of_curr_coord not in obstacle_list) \
            and (bottom_of_curr_coord[0] >= 0) and (bottom_of_curr_coord[0] <= 680) and (bottom_of_curr_coord[1] >= 0) \
                and (bottom_of_curr_coord[1] <= 580):

            # adding the key (the next position) and value (the current/prev. position) into the solutions dictionary
            solutions[bottom_of_curr_coord[0], bottom_of_curr_coord[1]] = current_spot_pos[0], current_spot_pos[1]

            frontier.append(bottom_of_curr_coord)
            visited_list.append(bottom_of_curr_coord)

        frontier_list.pop(0)


def back_track(curr_x, curr_y):
    """
    in this function, we draw a path to that starts from the end spot, and goes to the start spot.
    remember that the value coordinate of the solutions key is the spot that was explored immediately before.
    """
    if (curr_x, curr_y) != current_search_spot_pos:
        Spot(pos_x=solutions[curr_x, curr_y][0], pos_y=solutions[curr_x, curr_y][1], color=BT_COLOR).draw()
        final_solutions.append(solutions[curr_x, curr_y])

# We need 2 spots in the beginning, one start spot and one end spot
start_spot = Spot(start_spot_pos_x * 20, start_spot_pos_y * 20, color=START_SPOT_COLOR)
end_spot = Spot(end_spot_pos_x * 20, end_spot_pos_y * 20, color=END_SPOT_COLOR)

# spot coord of search spots
current_search_spot_pos = (start_spot.pos_x, start_spot.pos_y)

# visited spots
visited_spots = [current_search_spot_pos]

# obstacle spots
obstacle_spots = []

# frontier spots
frontier = [current_search_spot_pos]  # place starting position into frontier

# solution dictionary
solutions = {current_search_spot_pos: current_search_spot_pos, }

# final solution coordinate list - to track how long is the shortest path
final_solutions = []

# setting up a boolean to only print the length of the shortest path ONCE
back_track_done = False
once = False

# back tracking x and y positions (equal to end spot positions, initially)
bt_x = end_spot.get_coord()[0]
bt_y = end_spot.get_coord()[1]

# run loop for pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("\nThe shortest path found was %i units long :)" % len(final_solutions))

    draw_grid()
    start_spot.draw()
    end_spot.draw()

    if pygame.mouse.get_pressed()[0]:
        if ((event.pos[0] // 20) * 20, (event.pos[1] // 20) * 20) not in obstacle_spots:
            """we want to keep track of all the obstacle coordinates so that the search list does not contain 
            coordinates that are obstacles."""
            obstacle_spots.append(((event.pos[0] // 20) * 20, (event.pos[1] // 20) * 20))
        # obstacle spot instance
        obstacle_spot = Spot(obstacle_spots[-1][0], obstacle_spots[-1][1], color=OBSTACLE_SPOT_COLOR)
        obstacle_spot.draw()

    if pygame.time.get_ticks() > 15000:  # gives you 15 seconds to set up whatever obstacles you want
        try:
            explore_grid(current_spot_pos=frontier[0], frontier_list=frontier, visited_list=visited_spots,
                         obstacle_list=obstacle_spots)
        except IndexError:
            """this will occur once the frontier list becomes empty (after all the grid spots have 
            been searched"""
            try:
                back_track(curr_x=bt_x, curr_y=bt_y)
                bt_x, bt_y = solutions[bt_x, bt_y]
            except KeyError:
                """this will occur when the solutions dictionary cannot find the value for a key 
                which will be when the visited list does not contain the end spot value--so that's
                when you set the obstacles in a way which makes it impossible to get to the end spot"""
                print("\nHaha very funny, you made it impossible :'(")
                running = False

    # updating pygame
    pygame.display.update()


