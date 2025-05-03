from typing import Dict, List, Tuple 
from util import Color, Sat, User, Vector3

beamcolors = [Color.A, Color.B, Color.C, Color.D]
max_angle = 45
max_beams = 32
min_angle = 10

def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    """
    """
    assignments = {}

    sat_info = {
        sat_id: {
            "assigned_beams": 0,
            "color_beams": {color: [] for color in beamcolors}
        }
        for sat_id in sats
    }

    for user_id, user_pos in users.items():
        for sat_id, sat_pos in sats.items():
            if sat_info[sat_id]["assigned_beams"] >= max_beams:
                continue # if satellite is at max capacity, continue to next sat
            
            user_angle = 180 - user_pos.angle_between(Vector3(0, 0, 0), sat_pos)
            if user_angle > max_angle: # if satellite2user angle is above 45, continue to next sat
                continue

            for color in beamcolors:
                conflict = False
                for vec in sat_info[sat_id]["color_beams"][color]:
                    existing_user_pos = sat_pos + vec
                    twovec_angle = sat_pos.angle_between(user_pos, existing_user_pos)
                    if twovec_angle < min_angle: # if existing beam and current beam are within 10 degree, 
                        conflict = True
                        break # break out and move on to next color
                
                if conflict == False: # if there were no conflicts in this color
                    assignments[user_id] = (sat_id, color) # add the assignment
                    sat_info[sat_id]["assigned_beams"] += 1 # add 1 to assigned count of satellite
                    beam_vec = user_pos - sat_pos
                    sat_info[sat_id]["color_beams"][color].append(beam_vec) # add the beam vector to color vector list
                    break # assigned, so break out stop considering other colors and vectors
        
            if user_id in assignments: # if we were assigned above, break out, stop considering other satellites
                break # move on to next user
    
    return assignments