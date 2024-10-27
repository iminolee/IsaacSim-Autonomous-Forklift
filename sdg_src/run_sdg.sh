#!/bin/bash

# This is the path where Isaac Sim is installed which contains the python.sh script
ISAAC_SIM_PATH='/home/user/.local/share/ov/pkg/isaac-sim-2023.1.1'

echo "Starting Synthetic Data Generation"  

# Navigate to the Isaac Sim directory
cd $ISAAC_SIM_PATH

# Launch the synthetic data generation script with desired parameters
./python.sh /home/user/IsaacSim-Autonomous-Forklift/sdg_src/scripts/synthetic_data_generator.py \
    --headless True \
    --stage_path /Isaac/Environments/Simple_Warehouse/warehouse.usd \
    --height 544 \
    --width 960 \
    --num_frames 100 \
    --data_dir /home/user/IsaacSim-Autonomous-Forklift/sdg_src/data \
    # --randomize_lighting \
    # --randomize_floor_material  \
    # --randomize_wall_material 

echo "Synthetic Data Generation Complete"
