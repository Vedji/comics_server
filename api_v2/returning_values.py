from flask import jsonify


def return_error(msg: str, code: int):
    return jsonify({"message": msg, "status": "error"}), code


def return_success(data: dict, code: int):
    return jsonify({"data": data, "status": "success"}), code
