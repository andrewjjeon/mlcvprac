from typing import Dict, List, Tuple 
from util import Color, Sat, User, Vector3

max_beams = 32
max_angle = 45
min_angle = 10
color_beams = [Color.A, Color.B, Color.C, Color.D]

def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    """
    Solves the beam assignment problem by assigning users to satellites and colors
    while adhering to angle and interference constraints.

    Args:
        users (Dict[UserID, Vector3]): Mapping of user IDs to their 3D positions.
        sats (Dict[SatelliteId, Vector3]): Mapping of satellite IDs to their 3D positions.

    Returns:
        Dict[UserID, Tuple[SatelliteId, Color]]: Mapping of user IDs to their assigned satellite and color.
    """
    assignments = {}
    sat_info = {
        sat: {
            "beamcount": 0,
            "color_vecs": {color: [] for color in color_beams} # all the beams for each color for a satellite
        }
        for sat in sats
    }
    for user in users:
        for sat in sats:
            user_pos = users[user]
            sat_pos = sats[sat]
            
            if (180 - user_pos.angle_between(sat_pos, Vector3(0, 0, 0))) > max_angle:
                continue
            if sat_info[sat]["beamcount"] >= max_beams:
                continue

            for color in sat_info[sat]["color_vecs"]:
                conflict = False
                for color_vec in sat_info[sat]["color_vecs"][color]:
                    existing_user_pos = sat_pos + color_vec
                    if sat_pos.angle_between(existing_user_pos, user_pos) < min_angle:
                        conflict = True
                        break # move on to next color, there is a conflict
                
                if conflict == False:
                    assignments[user] = (sat, color)
                    sat_info[sat]["beamcount"] += 1
                    user_vec = user_pos - sat_pos
                    sat_info[sat]["color_vecs"][color].append(user_vec)
                    break # stop considering any other colors, a match has been made
            
            if user in assignments:
                break # stop considering other satellites, a match has been made
    return assignments

