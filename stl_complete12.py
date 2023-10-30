import numpy as np
from stl import mesh
import cv2  # OpenCV for image processing (you may need to install it)

# ... Existing code for FractalImage and STLModelGenerator ...

class STLModelGenerator:
    def __init__(self):
        # Initialize the necessary variables and data structures
        self.vertices = []
        self.slices = []
        self.slice_height = 8.0
        self.shape = None

    def add_slice(self, slice_data):
        # Determine the z-coordinate based on the number of slices
        z_coord = len(self.slices) * self.slice_height

        # Add vertices from a single slice to the vertices list with the corresponding z-coordinate
        for x, y in slice_data:
            self.vertices.extend([x, y, z_coord])

        # Add the slice data to the list of slices
        self.slices.append(slice_data)

    def generate_stl_file(self, filename):
        if self.shape is None:
            # Initialize the shape object
            self.shape = mesh.Mesh(np.zeros(0, dtype=mesh.Mesh.dtype))

        # Define the faces array based on the vertices
        faces = []

        # Define faces for connecting vertices to form triangles
        vertices_per_slice = len(self.slices[0])  # Assuming all slices have the same number of vertices

        for i in range(len(self.slices) - 1):
            # Iterate over the vertices in the current slice
            for j in range(vertices_per_slice - 1):
                # Define faces to connect vertices
                vertex1 = i * vertices_per_slice + j
                vertex2 = vertex1 + 1
                vertex3 = (i + 1) * vertices_per_slice + j
                vertex4 = vertex3 + 1

                # Add two triangles to form a quadrilateral
                face1 = [vertex1, vertex2, vertex3]
                face2 = [vertex2, vertex4, vertex3]

                faces.append(face1)
                faces.append(face2)

        # Initialize the shape object with the calculated number of faces and vertices
        num_faces = len(faces)
        num_vertices = len(self.vertices) // 3
        self.shape = mesh.Mesh(np.zeros(num_faces, dtype=mesh.Mesh.dtype))

        # Convert the vertices list to a NumPy array
        vertices = np.array(self.vertices)

        # Populate the shape vectors based on faces and vertices
        for i, f in enumerate(faces):
            for j in range(3):
                self.shape.vectors[i][j] = vertices[f[j] * 3:f[j] * 3 + 3]

        # Save the STL file
        self.shape.save(filename)
# Function to read a black-and-white PNG file and extract boundary coordinates
def read_png_and_extract_boundary(filename):
    # Read the PNG image using OpenCV (assuming white background)
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    # Threshold the image to convert it into a binary image
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    
    # Find contours with a detailed hierarchy
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Extract boundary coordinates from the outermost contour (assuming the black region is the outer contour)
    if contours:
        outer_contour = max(contours, key=cv2.contourArea)
        boundary_coordinates = outer_contour[:, 0, :].tolist()
        return boundary_coordinates
    else:
        return []


# Initialize the STLModelGenerator
stl_model_generator = STLModelGenerator()

# Set the number of images you want to process
img_count = 10  # Adjust this to the desired number of images
input_directory = "./test_images/"

for i in range(img_count):
    # Generate the image file name with zero padding and input directory
    image_file = input_directory + str(i).zfill(4) + ".png"

    # Read the PNG image and extract boundary coordinates
    boundary_coordinates = read_png_and_extract_boundary(image_file)

    # Generate an STLModelGenerator object from the boundary coordinates and add the slice data
    stl_model_generator.add_slice(boundary_coordinates)

# Generate an STL file for the 3D fractal model
stl_model_generator.generate_stl_file("fractal_model.stl")

