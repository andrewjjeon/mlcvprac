import json
import math
import numpy as np


def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def angle_2vec(v1, v2):
    '''
    Get angle using the formula cos(theta) = uv / norm(u)norm(v)
    '''
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    ang = np.arccos(cos_theta)
    ang = np.degrees(ang)
    return ang

def find_pairs(data):
    valid_pairs = []
    for sat in data["satellites"]:
        sat_pos = sat["position"]
        sat_pos = np.array(sat_pos)
        for user in data["users"]:
            user_pos = user["position"]
            user_pos = np.array(user_pos)
            sat2user_vec = user_pos - sat_pos
            sat2earth_vec = np.zeros_like(sat_pos) - sat_pos # satellite nadir is direction straight down to earth
            nadir_angle = angle_2vec(sat2user_vec, sat2earth_vec)
            if nadir_angle <= 45:
                valid_pairs.append((sat["id"], user["id"], sat["position"], user["position"], nadir_angle))

    return valid_pairs

def get_ang(x):
    return x[4]

def beam_allocation(js):
    data = load_data(js)
    valid_pairs = find_pairs(data)
    valid_pairs.sort(key=get_ang) # sort by lowest nadir angles, sorted by closest matches (users directly under satellites get prioritized)
    
    assignments = []
    assigned_users = set()

    sat_info = {}
    for sat in data["satellites"]:
        satid = sat["id"]
        sat_info[satid] = {
            "max_beams": sat["max_beams"],
            "assigned_beams": 0,
            "color_vectors": {color: [] for color in data["beam_colors"]}
        }

    for satid, userid, _, sat_pos, user_pos in valid_pairs:
        if userid not in assigned_users: # 1 beam per user
            if not sat_info[satid]["assigned_beams"] >= sat_info[satid]["max_beams"]:
                beam_vec = user_pos - sat_pos
                for color in sat_info[satid]["color_vectors"]:
                    conflict = False
                    for vec in sat_info[satid]["color_vectors"][color]:
                        angle = angle_2vec(beam_vec, vec)
                        if angle < 10:
                            conflict = True
                            break
                    
                    if not conflict:
                        assignments.append({
                            "sat_id": satid,
                            "user_id": userid,
                            "beam_color": color
                        })
                        assigned_users.add(userid)
                        sat_info[satid]["assigned_beams"] += 1
                        sat_info[satid]["color_vectors"][color].append(beam_vec)
                        break

    return assignments




    
if __name__ == "__main__":
    js = r"C:\Users\Andrew Jeon\OneDrive\Desktop\spacex_beam_allocation\input.json"
    results = beam_allocation(js)
    output = json.dumps(results, indent=4)

    with open("results.json", "w") as file:
        file.write(output)

