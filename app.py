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
    start_total = time.time()

    for size in input_sizes:
        start = time.time()
        algorithm_fn(size)
        end = time.time()
        execution_times.append(end - start)

    total_time = time.time() - start_total
    
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
        "algorithm": algo,
        "n": n,
        "steps": steps,
        "input_sizes": input_sizes,
        "execution_times": execution_times,
        "total_time_seconds": total_time,
        "graph_image_base64": image_base64

    })

if __name__ == "__main__":
    app.run(debug=True, port=3000)
