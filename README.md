
# Voice-Controlled Card Suit Detector

An interactive computer vision system developed in Python that detects and classifies playing card suits (Hearts, Diamonds, Spades, Clubs) using real-time image processing and voice commands.

## 🌟 Key Features
* **Voice-Activated Interface**: Using the Google Speech Recognition API. Start the process, stop the program, or specify image filenames using Polish voice commands.
* **Perspective Correction**: Includes a manual tool to select card corners and perform a 4-point perspective transform, "flattening" the card for accurate analysis.
* **HSV Color Segmentation**: Advanced color filtering for both red (Hearts/Diamonds) and black (Spades/Clubs) suits, optimized for varying lighting conditions.
* **Shape Approximation**: Utilizes the Douglas-Peucker algorithm (`approxPolyDP`) to distinguish between suits based on the number of vertices in their contours.
* **Morphological Cleaning**: Implements erosion, dilation, and closing operations to eliminate noise and improve mask quality.



## Technical Workflow
1. **Input**: Voice command triggers the loading of a specific image.
2. **Preprocessing**: User selects 4 corners of the card; the system performs a perspective warp.
3. **Filtering**: The image is converted to HSV space to create precise color masks.
4. **Refinement**: Morphological transformations clean up the binary masks.
5. **Detection**: The system finds contours, filters them by area and aspect ratio, then approximates the shape to identify the suit.
