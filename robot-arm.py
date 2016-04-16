from arm_controller import RobotArm
from flask import Flask, render_template, request, json

app = Flask(__name__)
robot_arm = RobotArm()

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/controller', methods=["POST"])
def controller():
    app.logger.info(request.json)
    data = json.loads(request.json)
    app.logger.info(type(data))
    servo_name = data['name']
    value = data['value']
    app.logger.info(servo_name, value)
    robot_arm.move(servo_name, value)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
