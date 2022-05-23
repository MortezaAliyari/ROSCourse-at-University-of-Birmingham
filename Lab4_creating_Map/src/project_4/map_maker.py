from project_4.geometry import *
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PointStamped
from math import sin, cos, degrees
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ------------------------------------------------------------------------------
# MapMaker class
# ------------------------------------------------------------------------------
class MapMaker:
  def __init__(self, origin_x, origin_y, resolution, size_x, size_y, transformer):
    self.origin_x = origin_x
    self.origin_y = origin_y
    self.resolution = resolution
    self.size_x = size_x
    self.size_y = size_y
    self.transformer = transformer
    
    self.grid = OccupancyGrid()
    self.grid.header.frame_id = 'odom'
    self.grid.info.resolution = resolution
    self.grid.info.width = size_x
    self.grid.info.height = size_y
    self.grid.info.origin.position.x = origin_x
    self.grid.info.origin.position.y = origin_y
    self.grid.info.origin.orientation.w = 1.0
    self.grid.data = [-1] * (size_x * size_y)
    self.numScansReceived = 0

    # Insert additional code here if needed

  # ----------------------------------------------------------------------------
  # Convert from world coordinates to grid coordinates. This is convenience 
  # wrapper around the to_grid function from the first part of the assignment.
  # Usage:
  #   (x_grid, y_grid) = self.to_grid(x_world, y_world)
  def to_grid(self, x, y):
    return to_grid(x, y, self.origin_x, self.origin_y, self.size_x, self.size_y, self.resolution)    

  # ----------------------------------------------------------------------------
  # Convert from grid coordinates to world coordinates. This is convenience 
  # wrapper around the to_world function from the first part of the assignment.
  # Usage:
  #   (x_world, y_world) = self.to_world(x_grid, y_grid)
  def to_world(self, gx, gy):
    return to_world(gx, gy, self.origin_x, self.origin_y, self.size_x, self.size_y, self.resolution)    

  # ----------------------------------------------------------------------------
  # Process odometry message. You code should go here.
  def process_odom(self, msg):

    None

  # ----------------------------------------------------------------------------
  # Process laserscan message. You code should go here.
  def process_scan(self, msg):

    self.numScansReceived+=1

    None        

  # ----------------------------------------------------------------------------
  # Visualize robot pose, current laserscan, free map cells and occupied map
  # cells. This function is useful for debugging your code. Feel free to modify
  # this to display additional information.
  # 
  # Parameters:
  #   robot_pose      robot pose represented by a tuple (x, y, theta)
  #   rays            laserscan rays represented as an array of tuples i.e. ((x_0, y_0), ... , (x_n, y_n))
  #   free_cells      grid coordinates of the free cells represented as an array of tuples i.e. ((x_0, y_0), ... , (x_n, y_n))
  #   occupied_cells  grid coordinates of the occupied cells represented as an array of tuples i.e. ((x_0, y_0), ... , (x_n, y_n))
  #   pause           if True this function will stop execution until a key is pressed
  # Usage:
  #   self.visualize_scans(self, robot_pose, rays, free_cells, occupied_cells, pause)
  # If you want to visualize laserscans only and no cell information:
  #   self.visualize_scans(self, robot_pose, rays, [], [], pause)
  def visualize_scans(self, robot_pose, rays, free_cells, occupied_cells, pause):

    # Initialize figure
    my_dpi = 96
    plt.figure(1, figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
    plt.cla()
    plt.xlim ( self.grid.info.origin.position.x, self.grid.info.origin.position.x + self.grid.info.width )
    plt.ylim ( self.grid.info.origin.position.y, self.grid.info.origin.position.y + self.grid.info.height )
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('Laserscan ' + str(self.numScansReceived))
    plt.xlabel('X world')
    plt.xlabel('Y world')
    ax = plt.axes()

    # Add free cells
    free_cells = self.unique_list(free_cells)
    for cell in free_cells:
      (x, y) = self.to_world(cell[0], cell[1])
      patch = patches.Rectangle ( (x - self.resolution/2, y - self.resolution/2), self.resolution, self.resolution, color='b', alpha=0.5)
      ax.add_patch(patch)

    # Add occupied cells
    occupied_cells = self.unique_list(occupied_cells)
    for cell in occupied_cells:
      (x, y) = self.to_world(cell[0], cell[1])
      patch = patches.Rectangle ( (x - self.resolution/2, y - self.resolution/2), self.resolution, self.resolution, color='k', alpha=0.8)
      ax.add_patch(patch)

    # Add odometry frame
    self.plot_coordinate_frame((0.0, 0.0, 0.0), 4, "odom")

    # Add robot frame
    self.plot_coordinate_frame(robot_pose, 4, "base_link")

    # Add laserscanner rays
    for ray in rays:
      plt.plot([ray[0]], [ray[1]], 'ro', markersize=2, markeredgecolor='r')

    # Add grid (comment this out if your visualization code is too slow)
    ax = plt.axes()
    step = 5
    minor_ticks = range(self.grid.info.width / step)
    for i in range(len(minor_ticks)):
      minor_ticks[i] = minor_ticks[i] * 5 + int(self.grid.info.origin.position.x)
    ax.set_xticks(minor_ticks, minor=True)                                           
    ax.set_yticks(minor_ticks, minor=True) 
    ax.grid(which='minor')                                                            

    # Show plot
    plt.draw()
    if pause:
      k = plt.waitforbuttonpress(1)
      while not k:
        k = plt.waitforbuttonpress(1)
    else:
      plt.waitforbuttonpress(1e-6)

  None  

  # ----------------------------------------------------------------------------
  # Draw a coordinate frame
  def plot_coordinate_frame(self, pose, size, frame_id=""):
    (x, y, theta) = pose
    plt.plot( [x,  x + cos(theta)*size],
              [y,  y + sin(theta)*size],
              'r', linewidth=4)
    plt.plot( [x,  x - sin(theta)*size],
              [y,  y + cos(theta)*size],
              'g', linewidth=4)
    plt.plot(x, y, 'bo', markersize=6, markeredgecolor='b')
    ax = plt.axes()
    ax.text(x, y-1, frame_id)

    None

  # ----------------------------------------------------------------------------
  # Remove duplicate entries from a list
  def unique_list(self, list_in):
    return list(set(list_in))

