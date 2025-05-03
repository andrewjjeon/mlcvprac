# Satellite Beam Allocation Optimization

## Objective:

In the Starlink/Starshield constellation, each satellite can form multiple independent beams to serve users on Earth. Efficient allocation of these beams is crucial to maximize coverage and minimize interference.
Develop an algorithm to assign satellites to users by allocating communication beams, ensuring optimal coverage while adhering to specific constraints.

Starlink 
- Satellite internet constellation provides internet
- Mesh network beams internet data to user dishes on Earth
- Satellites commnicate via inter-satellite laser links

Starshield
- Defense-version of Starlink: earth observation, military comms, missile tracking, reconnaissance
- Basically Starlink but more encryption


## Inputs:

A list of satellites, each with:
- 3D position coordinates (x, y, z) in Earth-centered coordinates
- Maximum number of beams it can form simultaneously (e.g., 32)

A list of users, each with:
- 3D position coordinates (x, y, z) on Earth's surface

Beam characteristics:
- Each beam has a specific frequency "color" (e.g., 4 available frequencies)
- Beams of the same color must be separated by at least 10 degrees to avoid interference
- Beams can only serve users within a 45-degree elevation angle from the satellite's nadir

Constraints:
<img src="satellite.jpg" alt="Satellite Image" style="transform: rotate(-90deg);">

A satellite cannot...
- A beam can only serve a user if the user's position is within a 45-degree angle from the satellite's nadir. 90 degree total cone.
- Each user must be assigned to exactly one beam from one satellite.
- A Satellite can't form more beams than its capacity (2 beams)
- No two beams of the same frequency color from the same satellite can be within 10 degrees of each other.

- Aim to maximize the number of users served under these constraints.

Deliverables:
- A program that reads input data (satellite and user positions) and outputs the assignment of users to satellite beams.
- The output should specify, for each user:
- The assigned satellite ID
- The beam ID or frequency color


### Output

A `output.json` file containing the assigned satellite and beam color for each user.