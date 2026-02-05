from db import SessionLocal
from models import Visualizer
import matplotlib
matplotlib.use("Agg")
import io
import base64
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
import time
from factorial import bubble_sort, linear_search, binary_search, nested_loops

app = Flask(__name__)

ALGORITHMS = {
    "bubble": bubble_sort,
    "linear": linear_search,
    "binary": binary_search,
    "nested": nested_loops
}

TIME_COMPLEXITY = {
    "bubble": "O(n²)",
    "linear": "O(n)",
    "binary": "O(log n)",
    "nested": "O(n²)"
}

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "app": "time-complexity-analyzer",
        "status": "running"
    })

@app.route("/analyze", methods=["GET"])
def analyze():
    algo = request.args.get("algo")
    n_raw = request.args.get("n")
    steps_raw = request.args.get("steps")

    if n_raw is None:
        return jsonify({"error": "Missing required parameter: n"}), 400
    if steps_raw is None:
        return jsonify({"error": "Missing required parameter: steps"}), 400

    try:
        n = int(n_raw)
        steps = int(steps_raw)
    except ValueError:
        return jsonify({"error": "n and steps must be integers"}), 400

    if n <= 0:
        return jsonify({"error": "n must be greater than 0"}), 400
    if steps <= 0:
        return jsonify({"error": "steps must be greater than 0"}), 400
    if steps > n:
        return jsonify({"error": "steps must be less than or equal to n"}), 400

    if algo is None:
        algo = "bubble"

    if algo not in ALGORITHMS:
        return jsonify({
            "error": "Invalid algorithm",
            "allowed_algorithms": list(ALGORITHMS.keys())
        }), 400

    algorithm_fn = ALGORITHMS[algo]

    step_size = n // steps
    input_sizes = [i * step_size for i in range(1, steps + 1)]

    execution_times = []

    start_time = int(time.time() * 1000)

    for size in input_sizes:
        start = time.time()
        algorithm_fn(size)
        end = time.time()
        execution_times.append(end - start)


    end_time = int(time.time() * 1000)

 
    total_time_ms = end_time - start_time

    plt.figure()
    plt.plot(input_sizes, execution_times, marker="o")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Time Complexity Analysis - {algo}")

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    image_bytes = buffer.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return jsonify({
       
        "algo": algo,
        "items": n,
        "steps": steps,

        "start_time": start_time,
        "end_time": end_time,
        "total_time_ms": total_time_ms,
        "time_complexity": TIME_COMPLEXITY.get(algo),
        "graph_data": image_base64,
        "input_sizes": input_sizes,
        "execution_times": execution_times
    })

@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    data = request.get_json()

    required_fields = [
        "algo",
        "items",
        "steps",
        "start_time",
        "end_time",
        "total_time_ms",
        "time_complexity",
        "graph_data"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    db = SessionLocal()

    try:
        analysis = Visualizer(
            algo=data["algo"],
            items=data["items"],
            steps=data["steps"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            total_time_ms=data["total_time_ms"],
            time_complexity=data["time_complexity"],
            graph_data=data["graph_data"]
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return jsonify({
            "status": "success",
            "analysis_id": analysis.id
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
@app.route("/retrieve_analysis", methods=["GET"])
def retrieve_analysis():
    analysis_id = request.args.get("id")

    if not analysis_id:
        return jsonify({"error": "Missing required query parameter: id"}), 400

    try:
        analysis_id = int(analysis_id)
    except ValueError:
        return jsonify({"error": "id must be an integer"}), 400

    db = SessionLocal()

    try:
        analysis = db.query(Visualizer).filter(Visualizer.id == analysis_id).first()

        if not analysis:
            return jsonify({"error": "Analysis not found"}), 404

        return jsonify({
            "analysis_id": analysis.id,
            "algo": analysis.algo,
            "items": analysis.items,
            "steps": analysis.steps,
            "start_time": analysis.start_time,
            "end_time": analysis.end_time,
            "total_time_ms": analysis.total_time_ms,
            "time_complexity": analysis.time_complexity,
            "graph_data": analysis.graph_data
        }), 200

    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=3000)
