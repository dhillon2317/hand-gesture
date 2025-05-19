import numpy as np

def get_angle(a, b, c):
    """
    Calculate the angle between three points (a, b, c).
    The angle is calculated at point b.
    
    Parameters:
    a, b, c: Tuples or lists representing the coordinates of the points (x, y).
    
    Returns:
    angle: The angle in degrees.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    # Calculate the vectors
    ba = a - b
    bc = c - b
    
    # Calculate the dot product and magnitudes of the vectors
    dot_product = np.dot(ba, bc)
    magnitude_ba = np.linalg.norm(ba)
    magnitude_bc = np.linalg.norm(bc)
    
    # Calculate the cosine of the angle
    cos_angle = dot_product / (magnitude_ba * magnitude_bc)
    
    # Calculate the angle in radians and then convert to degrees
    angle = np.arccos(cos_angle)
    angle_degrees = np.degrees(angle)
    
    return angle_degrees

def get_distance(a, b):
    """
    Calculate the Euclidean distance between two points (a, b).
    
    Parameters:
    a, b: Tuples or lists representing the coordinates of the points (x, y).
    
    Returns:
    distance: The Euclidean distance between the points.
    """
    a = np.array(a)
    b = np.array(b)
    distance = np.linalg.norm(a - b)
    return distance