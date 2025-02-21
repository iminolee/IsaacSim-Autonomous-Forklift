# IsaacSim-Autonomous-Forklift

<p align="center">
  <b><i>Minho Lee; Jiyun Lee; Wonhyeok Jeong</i></b>
</p>

<p align="center">
    <a href='https://github.com/iminolee/IsaacSim-Autonomous-Forklift' target='_blank'><img alt="Static Badge" src="https://img.shields.io/badge/Autonomous Forklift-Github-blue"></a>
    <a href='#' target='_blank'><img src='https://img.shields.io/badge/Paper-Arxiv-red'></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

## ✨ Abstract
This project integrates **Isaac Sim/Gazebo Simulation Platform** and ROS, to enable autonomous forklift control, real-time monitoring, and interaction. The system autonomously navigates, detects pallets, and precisely docks for transport within a simulated warehouse environment.

<div style="display: flex; justify-content: center; align-items: center;">
    <img src="figures/isaac_env_v1.png" style="width:49%; height:auto; max-height:300px; margin-right:10px;"/>
    <img src="figures/gazebo_env.png" style="width:48%; height:auto; max-height:300px;"/>
</div>
<p align="center">
    <img src="figures/forklift.gif" width="99%" style="display:inline-block;"/>
</p>

### Overview of Pretraining Datasets: Real and Synthetic

<div align="center">

| ![Image 1](sdg_src/examples/custom_warehouse_default_per250_subset-1_rgb_0021.png) | ![Image 2](sdg_src/examples/simple_warehouse_default_per250_subset-3_rgb_0175.png) | ![Image 3](sdg_src/examples/full_warehouse_default_per250_subset-7_rgb_0126.png) |
|--------------------------------|--------------------------------|--------------------------------|
| ![Image 4](sdg_src/examples/custom_warehouse_lights_per250_subset-2_rgb_0000.png) | ![Image 5](sdg_src/examples/simple_warehouse_lights_per250_subset-3_rgb_0109.png) | ![Image 6](sdg_src/examples/full_warehouse_lights_per250_subset-3_rgb_0198.png) |

</div>

## 😎 TODOs
[O] Release synthetic data generation scripts for logistics objects detection. <br>
[O] Release Gazebo launch file for running the forklift model from Isaac Sim. <br>
[X] Release standalone python scripts for IsaacSim. <br>
[X] Release the main project code.