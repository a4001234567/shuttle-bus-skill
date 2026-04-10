#!/usr/bin/env python3
"""
无界学城穿梭巴士 — 实时车辆位置查询
Wujie Xuecheng Shuttle Bus — real-time vehicle positions

Usage:
    python3 shuttle-bus.py [line_id]

    line_id options:
        1  ->  无界学城一号线
        2c ->  无界学城二号线（顺时针）
        2a ->  无界学城二号线（逆时针）
        (omit to query all lines)

Output: JSON with each vehicle's current position, station, and heading.
"""

import sys
import json
import urllib.request
import urllib.parse

TENANT_ID = "2009511491423047680"
QR_CODE_ID = "2011322258011197440"

LINES = {
    "1":  {"id": "2011381432170582016", "name": "无界学城一号线"},
    "2c": {"id": "2011388115668176896", "name": "无界学城二号线（顺时针）"},
    "2a": {"id": "2011395328499519488", "name": "无界学城二号线（逆时针）"},
}

# Station sequences (stationSort → name, lat, lng)
# Used to map the vehicle's stationId back to a human-readable name + position
LINE_STATIONS = {
    "1": [
        {"sort": 1,  "id": "2009519847609208832", "name": "清华国际一期",       "lng": 113.980515, "lat": 22.58534},
        {"sort": 2,  "id": "2009519847609208834", "name": "大学城体育馆",       "lng": 113.978483, "lat": 22.58854},
        {"sort": 3,  "id": "2009519847609208836", "name": "北大彩虹桥",         "lng": 113.977712, "lat": 22.590414},
        {"sort": 4,  "id": "2009519847609208838", "name": "北大",               "lng": 113.975325, "lat": 22.590803},
        {"sort": 5,  "id": "2009519847609208840", "name": "平安银行",           "lng": 113.974391, "lat": 22.588332},
        {"sort": 6,  "id": "2009519847609208842", "name": "清华能源环境大楼",   "lng": 113.97383,  "lat": 22.58807},
        {"sort": 7,  "id": "2009519847609208846", "name": "大学城国际会议中心", "lng": 113.970977, "lat": 22.588476},
        {"sort": 8,  "id": "2009519847609208849", "name": "清华教学楼C栋(去程)","lng": 113.97074,  "lat": 22.590331},
        {"sort": 9,  "id": "2009519847609208850", "name": "清华信息楼",         "lng": 113.967855, "lat": 22.592466},
        {"sort": 10, "id": "2009519847609208848", "name": "清华教学楼C栋(回程)","lng": 113.970531, "lat": 22.590698},
        {"sort": 11, "id": "2009519847609208847", "name": "大学城国际会议中心", "lng": 113.970808, "lat": 22.588746},
        {"sort": 12, "id": "2009519847609208845", "name": "哈工大信息楼",       "lng": 113.972669, "lat": 22.587644},
        {"sort": 13, "id": "2009519847609208841", "name": "平安银行",           "lng": 113.974187, "lat": 22.588178},
        {"sort": 14, "id": "2011389065673838592", "name": "北大",               "lng": 113.975096, "lat": 22.590595},
        {"sort": 15, "id": "2009519847609208837", "name": "北大彩虹桥",         "lng": 113.977399, "lat": 22.590484},
        {"sort": 16, "id": "2009519847609208835", "name": "大学城体育馆",       "lng": 113.978266, "lat": 22.58869},
        {"sort": 17, "id": "2009519847609208833", "name": "清华国际一期",       "lng": 113.980567, "lat": 22.585733},
    ],
    "2c": [
        {"sort": 1,  "id": "2011387195370770432", "name": "大学城国际会议中心",     "lng": 113.970999, "lat": 22.58932},
        {"sort": 2,  "id": "2011387634875109376", "name": "大学城图书馆",           "lng": 113.973335, "lat": 22.590062},
        {"sort": 3,  "id": "2009519847609208839", "name": "北大",                   "lng": 113.974998, "lat": 22.590647},
        {"sort": 4,  "id": "2011384655761641472", "name": "北大学生活动中心",       "lng": 113.98012,  "lat": 22.590899},
        {"sort": 5,  "id": "2011389065673838592", "name": "北大",                   "lng": 113.975096, "lat": 22.590595},
        {"sort": 6,  "id": "2009519847609208840", "name": "平安银行",               "lng": 113.974391, "lat": 22.588332},
        {"sort": 7,  "id": "2011385258747367424", "name": "哈工大火箭广场",         "lng": 113.97476,  "lat": 22.585196},
        {"sort": 8,  "id": "2011385660356169728", "name": "哈工大南门",             "lng": 113.972008, "lat": 22.584908},
        {"sort": 9,  "id": "2011386062233407488", "name": "哈工大一食堂",           "lng": 113.968463, "lat": 22.586501},
        {"sort": 10, "id": "2011386521358700544", "name": "哈工大商学院",           "lng": 113.967776, "lat": 22.589165},
        {"sort": 11, "id": "2011386942261301248", "name": "大学城国际会议中心",     "lng": 113.970518, "lat": 22.589297},
    ],
    "2a": [
        {"sort": 1,  "id": "2011386942261301248", "name": "大学城国际会议中心",     "lng": 113.970518, "lat": 22.589297},
        {"sort": 2,  "id": "2011386521358700544", "name": "哈工大商学院",           "lng": 113.967776, "lat": 22.589165},
        {"sort": 3,  "id": "2011386062233407488", "name": "哈工大一食堂",           "lng": 113.968463, "lat": 22.586501},
        {"sort": 4,  "id": "2011385660356169728", "name": "哈工大南门",             "lng": 113.972008, "lat": 22.584908},
        {"sort": 5,  "id": "2011732156259766272", "name": "哈工大火箭广场",         "lng": 113.974249, "lat": 22.585095},
        {"sort": 6,  "id": "2009519847609208841", "name": "平安银行",               "lng": 113.974187, "lat": 22.588178},
        {"sort": 7,  "id": "2011389065673838592", "name": "北大",                   "lng": 113.975096, "lat": 22.590595},
        {"sort": 8,  "id": "2011733439456743424", "name": "北大学生活动中心",       "lng": 113.979788, "lat": 22.590858},
        {"sort": 9,  "id": "2009519847609208839", "name": "北大",                   "lng": 113.974998, "lat": 22.590647},
        {"sort": 10, "id": "2011387634875109376", "name": "大学城图书馆",           "lng": 113.973335, "lat": 22.590062},
        {"sort": 11, "id": "2011387195370770432", "name": "大学城国际会议中心",     "lng": 113.970999, "lat": 22.58932},
    ],
}


def api_post(path, data, token="", form=False):
    url = f"https://predict.ipubtrans.com{path}"
    headers = {
        "tenantId": TENANT_ID,
        "qrCodeId": QR_CODE_ID,
        "token": token,
    }
    if form:
        body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    else:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def login():
    result = api_post("/mobile/login/guise", {})
    if result["returnCode"] != 200:
        raise RuntimeError(f"Login failed: {result['returnInfo']}")
    return result["returnData"]["token"]


def station_name_by_id(line_key, station_id):
    for s in LINE_STATIONS.get(line_key, []):
        if s["id"] == station_id:
            return f"站{s['sort']} {s['name']}"
    return f"未知站 ({station_id})"


def direction_label(deg):
    if deg is None:
        return "?"
    dirs = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
    idx = round(deg / 45) % 8
    return dirs[idx]


def get_vehicles(token, line_key):
    line = LINES[line_key]
    result = api_post("/mobile/predict/line/vehList", {"lineId": line["id"]}, token=token, form=True)
    if result["returnCode"] != 200:
        return []
    vehicles = []
    for v in result.get("returnData") or []:
        gps = v.get("gps") or {}
        veh = {
            "plate": v.get("vehCode", "?"),
            "online": gps.get("onlineStatus") == 1,
            "lat": gps.get("lat"),
            "lng": gps.get("lng"),
            "speed_kmh": gps.get("speed"),
            "direction_deg": gps.get("direction"),
            "direction": direction_label(gps.get("direction")),
            "gps_time": gps.get("gpsTime"),
            "current_station_id": v.get("stationId"),
            "current_station": station_name_by_id(line_key, v.get("stationId", "")),
            "station_sort": v.get("sort"),
            "line": line["name"],
            "line_key": line_key,
        }
        vehicles.append(veh)
    return vehicles


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg and arg not in LINES:
        print(f"Unknown line '{arg}'. Valid: {', '.join(LINES)}", file=sys.stderr)
        sys.exit(1)

    token = login()
    line_keys = [arg] if arg else list(LINES)

    all_vehicles = []
    for key in line_keys:
        all_vehicles.extend(get_vehicles(token, key))

    print(json.dumps(all_vehicles, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
