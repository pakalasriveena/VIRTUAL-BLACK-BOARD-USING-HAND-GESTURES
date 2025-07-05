
✋🖊 Hand Gesture-Based Virtual Blackboard

A smart, contact-free digital blackboard powered by computer vision and hand gesture recognition. This project is designed to enhance both online and offline education by allowing users to draw or write on a virtual board using hand gestures—without touching any hardware.

🔍 Project Overview

With the rising demand for virtual classrooms and smart class environments, this virtual blackboard provides an intuitive solution for interactive teaching and digital drawing. The system tracks hand landmarks using real-time video input and allows drawing only when specific finger gestures are detected, minimizing accidental marks caused by unintended hand movements.

✅ Key Features

✍ Hand-gesture based drawing
Draw on the screen by bringing specific fingers close together—writing is enabled only when the finger distance falls within a defined threshold.

🎯 Gesture accuracy filtering
Prevents unwanted scribbles by avoiding random or unintended movements.

💡 No distance calibration required
Starts drawing instantly when valid hand gestures are detected—no need to set a fixed distance from the camera.

⌨ Keyboard controls

Press 'Esc' to close the virtual board.

Press 'x' to clear all drawings on the board.


🧠 Powered by Machine Learning & Computer Vision
Uses MediaPipe or similar libraries for real-time hand tracking and landmark detection.

🧑‍🏫 Multi-purpose Usage
Ideal for virtual classrooms, digital whiteboarding, design brainstorming, and more.


🛠 Technologies Used

Python

OpenCV

MediaPipe (or other hand-tracking libraries)

NumPy


🚀 Use Cases

Teachers & Educators: Use the board during online lectures or smart classrooms for drawing diagrams, writing formulas, and more.

Designers & Creators: A creative tool to sketch or visualize ideas without needing stylus or touchscreen.

Collaborators: Enables remote brainstorming in a unique and interactive way.


📌 How to Run

1. Clone the repository


2. Install required dependencies


3. Run the main Python file (python virtual_board.py)


4. Use your hand gestures in front of the webcam to draw!

