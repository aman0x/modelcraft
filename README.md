
# Floorplan-to-3D Model Craft

## Overview
This project generates a 3D representation of a floorplan image using Python for image processing and Three.js for 3D visualization. The system detects walls from the floorplan image and renders them as 3D objects, providing an interactive 3D view of the structure.

## Features
- Automatically detect walls from a 2D floorplan image.
- Convert walls into 3D objects with adjustable height, width, and thickness.
- Interactive 3D visualization using **Three.js** with camera controls.
- Easily adaptable for different floorplan designs.

## Tech Stack
- **Python**: For image processing using OpenCV.
- **Flask**: Backend for serving data and HTML templates.
- **Three.js**: For rendering and visualizing the 3D floorplan.
- **HTML/JavaScript**: For frontend visualization and interactivity.

## Installation

### Prerequisites
- Python 3.x
- Node.js (optional, for managing Three.js dependencies)
- A modern web browser (Chrome, Firefox, or Edge)

### Clone the Repository
```bash
git clone <repository-url>
cd project-root
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Add Floorplan Images
Place your floorplan images in the `floorplans/` directory.

### Start the Flask Server
```bash
python app/main.py
```

The application will start and be accessible at `http://127.0.0.1:5000`.

## Project Structure
```
project-root/
├── app/
│   ├── static/
│   │   └── js/
│   │       └── three.min.js         # Three.js library
│   ├── templates/
│   │   └── index.html               # HTML for 3D rendering
│   ├── __init__.py                  # Initialize Flask app
│   ├── main.py                      # Flask routes and logic
│   ├── wall_detection.py            # Image processing logic
│   └── utils.py                     # Helper functions
├── floorplans/
│   └── floorplan.png                # Sample floorplan image
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

## Usage
1. Place your floorplan image in the `floorplans/` directory (e.g., `floorplan.png`).
2. Start the Flask server.
3. Open the application in your browser at `http://127.0.0.1:5000`.
4. Use the mouse to interact with the 3D view:
   - **Left-click and drag** to rotate the camera.
   - **Right-click and drag** to pan.
   - **Scroll** to zoom in/out.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Three.js](https://threejs.org) for 3D rendering.
- [OpenCV](https://opencv.org/) for image processing.

## Screenshots
*Coming soon!*
