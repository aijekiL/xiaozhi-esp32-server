from plugins_func.register import register_function, Action, ActionResponse, ToolType
import requests


HEART_RATE_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_latest_heart_rate",
        "description": "查询指定设备(deviceName)的最新心率数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "deviceName": {
                    "type": "string",
                    "description": "设备名称，例如：智能手表1",
                }
            },
            "required": ["deviceName"],
        },
    },
}


@register_function(
    name="get_latest_heart_rate",
    desc=HEART_RATE_FUNCTION_DESC,
    type=ToolType.WAIT,
)
def get_latest_heart_rate(deviceName: str) -> ActionResponse:
    """通过本地服务获取最新心率

    请求地址: http://localhost:8950/devices/getLatestHeartData
    请求参数: deviceName (中文设备名，例如“智能手表1”)
    返回: 直接回复的话术
    """
    try:
        url = "http://localhost:8950/devices/getLatestHeartData"
        resp = requests.get(url, params={"deviceName": deviceName}, timeout=5)
        resp.raise_for_status()
        payload = resp.json()

        if not isinstance(payload, dict) or payload.get("code") != 200 or "data" not in payload:
            return ActionResponse(
                action=Action.RESPONSE,
                response=f"没有查到设备「{deviceName}」的最新心率数据。",
            )

        info = payload.get("data") or {}
        heart_rate = info.get("heartRate")
        unit = info.get("unit", "bpm")
        measure_time = info.get("measureTime")
        device_name = info.get("deviceName", deviceName)

        if not heart_rate:
            return ActionResponse(
                action=Action.RESPONSE,
                response=f"设备「{device_name}」暂无心率数据。",
            )

        message = f"设备「{device_name}」最新心率为 {heart_rate} {unit}，测量时间 {measure_time}。"
        return ActionResponse(action=Action.RESPONSE, response=message)

    except requests.exceptions.RequestException as e:
        return ActionResponse(
            action=Action.RESPONSE,
            response=f"查询失败：网络异常或服务不可用（{str(e)}）。",
        )
    except Exception as e:
        return ActionResponse(
            action=Action.RESPONSE,
            response=f"查询失败：{str(e)}",
        )
