# HandWall – AI Virtual Handwriting System

HandWall is an AI-powered virtual handwriting application that allows users to write and draw in the air using hand gestures through a webcam.

It uses computer vision and hand landmark detection to track finger movements and convert them into digital drawings in real time.

## Features

- Real-time hand tracking using a webcam
- Virtual drawing using index finger gestures
- Gesture-based drawing control
- Multiple drawing colors
- Neon-style drawing effects
- Clear the canvas anytime

## Technologies Used

- Python
- OpenCV
- MediaPipe Tasks
- NumPy

## Gesture Controls

| Gesture / Key | Action |
|---|---|
| Index finger up | Draw |
| Index and middle fingers up | Stop drawing |
| 1–5 | Change drawing color |
| C | Clear canvas |
| Q | Quit application |

## Installation and Setup

1. Clone this repository:

```bash
git clone https://github.com/mythri2486-ux/HandWall-AI-Virtual-Writing.git
```

2. Open the project folder:

```bash
cd HandWall-AI-Virtual-Writing
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the environment on Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python handwall.py
```

Make sure your webcam is connected and allow camera access.

## Project Model

The project uses the `hand_landmarker.task` model for hand landmark detection.

## Future Improvements

- Support for both hands
- More customizable gestures
- Save handwritten drawings as images
- Browser-based version

## Author

Developed as an AI and Computer Vision project.

**HandWall – Write in the Air, Create on Screen!**
