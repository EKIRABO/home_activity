# Time Complexity Analyzer API

A simple Flask API that measures how long different algorithms take to run as the input size increases. It also generates a graph to visualize the performance and returns the graph as a Base64-encoded image in JSON format.

## Features

- Supports multiple algorithms:
  - Bubble Sort
  - Linear Search
  - Binary Search
  - Nested Loops
- Uses query parameters to control:
  - Algorithm selection
  - Maximum input size (`n`)
  - Number of steps (`steps`)
- Measures execution time for different input sizes
- Generates a performance graph using Matplotlib
- Returns results and the graph as JSON data

---

## Technologies Used

- Python 3  
- Flask  
- Matplotlib  
- NumPy  
- Base64  

---

## Project Structure

```
home_activity/
├── app.py
├── factorial.py
├── venv/
├── README.md
└── .gitignore
```

---

## Setup Instructions

### Clone the Repository

```bash
git clone <your-repo-url>
cd home_activity
```

---

### Create and Activate a Virtual Environment (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
```

---

### Install Dependencies

```powershell
pip install flask matplotlib numpy
```

---

## Running the Application

```powershell
python app.py
```

The server runs on:

```
http://localhost:3000
```

---

## API Endpoints

### Status Check

**GET** `/status`

```json
{
  "app": "time-complexity-analyzer",
  "status": "running"
}
```

---

### Runtime Endpoint

**GET** `/analyze`

#### Query Parameters

| Parameter | Required | Description |
|----------|----------|-------------|
| `algo` | No | Algorithm to run (`bubble`, `linear`, `binary`, `nested`) |
| `n` | Yes | Maximum input size |
| `steps` | Yes | Number of input size intervals |

---

#### Example Request

```
/analyze?algo=bubble&n=100&steps=5
```

---

#### Example Response

```json
{
  "algorithm": "bubble",
  "n": 100,
  "steps": 5,
  "input_sizes": [20, 40, 60, 80, 100],
  "execution_times": [0.07, 0.0004, 0.001, 0.002, 0.003],
  "total_time_seconds": 0.45,
  "graph_image_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```
---

### POST /save_analysis

Saves an analysis result to the database.

Request Body:
```json
{
  "algo": "bubble",
  "items": 100,
  "steps": 5,
  "start_time": 1700000000000,
  "end_time": 1700000000450,
  "total_time_ms": 450,
  "time_complexity": "O(n²)",
  "graph_data": "BASE64_IMAGE_STRING"
}
```
Response:
```json
{
  "status": "success",
  "analysis_id": 1
}
```
---

### GET /retrieve_analysis

Retrieves a previously saved analysis by ID.

Query Parameters:
- id (required): Analysis ID

Example Request:
/retrieve_analysis?id=1

Response:
```json
{
  "analysis_id": 1,
  "algo": "bubble",
  "items": 100,
  "steps": 5,
  "start_time": 1700000000000,
  "end_time": 1700000000450,
  "total_time_ms": 450,
  "time_complexity": "O(n²)",
  "graph_data": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```
---

## Viewing the Graph Image

The graph is returned as a Base64-encoded PNG string.

To view the image, copy the Base64 string and paste it into your browser:

```
data:image/png;base64,<PASTE_BASE64_STRING_HERE>
```
