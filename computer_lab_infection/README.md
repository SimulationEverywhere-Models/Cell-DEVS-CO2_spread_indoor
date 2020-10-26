Thus new version of the CO2 model was created quickly as a backup for the hackathon. 
It needs revision and testing.

I added the following parameters to the json

"risky_concentration"
"flow_weight"
"risky_exposure_time"
"airflow_dir_x"
"airflow_dir_y"

Changes in the model

Added the risk of infection:
I added a new type of occupant (susceptible)
If a cell has a concentration of "risky_concentration" for a period equal to  "risky_exposure_time" or more, the occupant (green in the video) of that cell becomes susceptible or at risk (red occupant in the video). If the concentration decreases, the risk gets mitigated and the occupant is back to normal.
Added constant airflow. This is independent of the vents. It is based on the values read from the json
The air cells calculate their concentration based on "flow_weight", "airflow_dir_x", and "airflow_dir_y"
The cell where the air is coming from (x and y coordinates ) accounts for flow_weight ( between 0 and 1) of the new calculated concentration in the current cell. The rest of the neighbors account equally for the remaining portion of the concentration. For example, in the attached video the flow_weight in the json is set to 0.8 meaning that 80% of each cell concentration comes from the neighbor with relative position ("airflow_dir_x", "airflow_dir_y").

