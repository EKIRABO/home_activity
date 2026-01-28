Time Complexity Analyzer API

This project is a simple Flask API that measures how long different algorithms take to run as the input size increases. It also creates a graph to show the performance and returns the graph as a Base64-encoded image in JSON format.

Features

Supports multiple algorithms:

Bubble Sort

Linear Search

Binary Search

Nested Loops

Uses query parameters to control:

The algorithm to run

The maximum input size (n)

The number of steps (steps)

Measures execution time for different input sizes

Generates a performance graph using Matplotlib

Returns results and the graph as JSON data

Technologies Used

Python 3

Flask

Matplotlib

NumPy

Base64

Project Structure
home_activity/
├── app.py           # Flask application
├── factorial.py     # Algorithm implementations (provided externally)
├── venv/            # Virtual environment (not committed)
├── README.md        # Project documentation
└── .gitignore

Setup Instructions
Clone the repository
git clone <your-repo-url>
cd home_activity

Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

Install dependencies
pip install flask matplotlib numpy

Running the Application
python app.py


The server runs on:

http://localhost:3000

API Endpoints
Status Check

GET /status

Response:

{
  "app": "time-complexity-analyzer",
  "status": "running"
}

Runtime Measurement Endpoint

GET /analyze

Query Parameters:

Parameter	Type	Required	Description
algo	string	No	Algorithm to run (bubble, linear, binary, nested). Defaults to bubble.
n	integer	Yes	Maximum input size
steps	integer	Yes	Number of input size intervals

Example request:

/analyze?algo=bubble&n=100&steps=5


Example response (shortened):

{
  "algorithm": "bubble",
  "n": 100,
  "steps": 5,
  "input_sizes": [20, 40, 60, 80, 100],
  "execution_times": [0.07, 0.0004, 0.001, 0.002, 0.003],
  "total_time_seconds": 0.45,
  "graph_image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}

Viewing the Graph Image

The graph is returned as a Base64-encoded PNG string.

To view the image, copy the Base64 string and paste it in your browser like this:

data:image/png;base64,<PASTE_BASE64_STRING_HERE>
