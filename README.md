# OWLv2 Object Detection Web Application

The OWLv2 Object Detection Web Application allows users to upload images or provide image URLs for object detection using the OWLv2 model from Hugging Face. Users can set a confidence threshold and receive results displayed with bounding boxes and a detailed table of detected objects.

## Features

- **Image Upload and URL Input:** Users can either upload an image file or provide an image URL for object detection.
- **Object Detection:** Utilizes the OWLv2 model to detect objects based on provided keywords.
- **Confidence Threshold:** Users can set a confidence threshold to filter detection results.
- **Result Display:** Displays the processed image with bounding boxes and presents detection results in a table format.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/NevzatTalay/OWLv2_Test_WebApp.git
    cd OWLv2_Test_WebApp
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open a web browser and navigate to `http://127.0.0.1:5000/`.

3. Use the "Upload File" tab to select and upload an image file or use the "Paste Link" tab to provide an image URL.

4. Enter the desired keywords (comma-separated) for object detection.

5. Set the confidence threshold to filter detection results.

6. Click the "Start" button to process the image and view the results.

## Screenshots

*Include screenshots here to demonstrate how to use the application.*

## Example Results

*Include example results screenshots here.*

## Future Enhancements

- Add support for batch image processing.
- Implement user authentication and image history.
- Enhance the UI with more interactive elements and visualizations.

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
