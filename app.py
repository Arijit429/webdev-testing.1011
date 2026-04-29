from flask import Flask, request, jsonify
from advanced_env import CalendarOrchestrationEnv, Action
from inference import run_inference

app = Flask(__name__)

env = CalendarOrchestrationEnv()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Advanced Calendar Orchestration Environment is live"
    })


@app.route("/reset", methods=["POST", "GET"])
def reset():
    obs = env.reset()

    return jsonify({
        "status": "reset_ok",
        "observation": obs.model_dump()
    })


@app.route("/state", methods=["GET"])
def state():
    return jsonify(env.state())


@app.route("/step", methods=["POST"])
def step():
    data = request.get_json()

    action = Action(
        action_type=data.get("action_type", ""),
        target_meeting_id=data.get("target_meeting_id", ""),
        new_time=data.get("new_time", ""),
        reason=data.get("reason", "")
    )

    obs, reward, done, info = env.step(action)

    return jsonify({
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    })


@app.route("/run", methods=["GET"])
def run():
    run_inference()
    return jsonify({"status": "task_executed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)