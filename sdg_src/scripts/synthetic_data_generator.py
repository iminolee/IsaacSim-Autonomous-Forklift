from omni.isaac.kit import SimulationApp
import os
import argparse

parser = argparse.ArgumentParser("Synthetic Data Generator")
parser.add_argument("--headless", type=bool, default=True, help="Launch script headless, default is True")
parser.add_argument("--stage_path", type=str, default="/Isaac/Environments/Simple_Warehouse/warehouse.usd", 
                    help="Path to the stage file to open, default is the warehouse stage.")
parser.add_argument("--height", type=int, default=544, help="Height of image")
parser.add_argument("--width", type=int, default=960, help="Width of image")
parser.add_argument("--num_frames", type=int, default=100, help="Number of frames to record")
parser.add_argument("--data_dir", type=str, default=os.getcwd() + "/pallet_data",
                    help="Location where data will be output")
parser.add_argument("--randomize_lighting", action="store_true", help="Randomize the lighting of the scene")
parser.add_argument("--randomize_floor_material", action="store_true", help="Randomize the warehouse floor material")
parser.add_argument("--randomize_wall_material", action="store_true", help="Randomize the warehouse wall material")

args, unknown_args = parser.parse_known_args()

# This is the config used to launch simulation
CONFIG = {"renderer": "RayTracedLighting",
          "headless": args.headless,
          "width": args.width,
          "height": args.height,
          "num_frames": args.num_frames}

simulation_app = SimulationApp(launch_config=CONFIG)

import carb
import omni
import omni.usd
import omni.replicator.core as rep
from pxr import Semantics
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import get_current_stage, open_stage
from omni.isaac.core.utils.semantics import get_semantics
import random

## Increase subframes if shadows/ghosting appears of moving objects
## See known issues: https://docs.omniverse.nvidia.com/prod_extensions/prod_extensions/ext_replicator.html#known-issues
rep.settings.carb_settings("/omni/replicator/RTSubframes", 4)

# ENV_URL = "/Isaac/Environments/Simple_Warehouse/warehouse.usd"
# open_stage(prefix_with_isaac_asset_server(ENV_URL))

# with rep.new_layer():
#     PALLETS = [
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_A1.usd",
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_B1.usd",
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_C1.usd"]
#     PALLETJACKS = [
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Scale_A/PalletTruckScale_A01_PR_NVD_01.usd",
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Heavy_Duty_A/HeavyDutyPalletTruck_A01_PR_NVD_01.usd",
#         "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Low_Profile_A/LowProfilePalletTruck_A01_PR_NVD_01.usd"]

PALLETS = [
    "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_A1.usd",
    "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_B1.usd",
    "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Pallets/Pallet_C1.usd"]

FORKLIFTS = ["omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Equipment/Forklifts/Forklift_C/Forklift_C01_PR_V_NVD_01.usd",
             "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Equipment/Forklifts/Forklift_A/Forklift_A01_PR_V_NVD_01.usd",
             "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Equipment/Forklifts/Forklift_B/Forklift_B01_PR_V_NVD_01.usd",
             "omniverse://localhost/NVIDIA/Assets/Isaac/4.2/Isaac/Robots/Forklift/forklift_b.usd",
             "omniverse://localhost/NVIDIA/Assets/Isaac/4.2/Isaac/Robots/Forklift/forklift_c.usd"]

CARRIERS = ["omniverse://localhost/NVIDIA/Assets/simready_content/common_assets/props/container_f03/container_f03.usd",
            "omniverse://localhost/NVIDIA/Assets/simready_content/common_assets/props/container_f10/container_f10.usd",
            "omniverse://localhost/NVIDIA/Assets/simready_content/common_assets/props/container_f27/container_f27.usd",
            "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Storage/Containers/Container_F/Container_F20_116x80x80cm_PR_V_NVD_01.usd",
            "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Storage/Totes/Tote_B/Tote_B04_60x40x30cm_PR_V_NVD_01.usd"]

STILLAGES = ["omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Equipment/Carts/SteelBoxTruck_A/SteelBoxTruck_A01_01.usd",
             "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Storage/Containers/Container_H/Container_H04_60x40x22cm_PR_V_NVD_01.usd",
             "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Storage/Containers/Container_G/Container_G05_120x100x80cm_PR_V_NVD_01.usd",
             "omniverse://localhost/NVIDIA/Assets/DigitalTwin/Assets/Warehouse/Storage/Containers/Container_F/Container_F14_120x80x89cm_PR_V_NVD_01.usd"]

PALLETJACKS = ["http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Scale_A/PalletTruckScale_A01_PR_NVD_01.usd",
               "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Heavy_Duty_A/HeavyDutyPalletTruck_A01_PR_NVD_01.usd",
               "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/DigitalTwin/Assets/Warehouse/Equipment/Pallet_Trucks/Low_Profile_A/LowProfilePalletTruck_A01_PR_NVD_01.usd"]

TEXTURES = [
    "/Isaac/Materials/Textures/Patterns/nv_asphalt_yellow_weathered.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_tile_hexagonal_green_white.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_rubber_woven_charcoal.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_granite_tile.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_tile_square_green.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_marble.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_brick_reclaimed.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_concrete_aged_with_lines.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_wooden_wall.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_stone_painted_grey.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_wood_shingles_brown.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_tile_hexagonal_various.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_carpet_abstract_pattern.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_wood_siding_weathered_green.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_animalfur_pattern_greys.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_artificialgrass_green.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_bamboo_desktop.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_brick_reclaimed.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_brick_red_stacked.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_fireplace_wall.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_fabric_square_grid.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_granite_tile.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_marble.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_gravel_grey_leaves.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_plastic_blue.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_stone_red_hatch.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_stucco_red_painted.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_rubber_woven_charcoal.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_stucco_smooth_blue.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_wood_shingles_brown.jpg",
    "/Isaac/Materials/Textures/Patterns/nv_wooden_wall.jpg"]

def prefix_with_isaac_asset_server(relative_path):
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        raise Exception("Nucleus server not found, could not access Isaac Sim assets folder")
    if isinstance(relative_path, list):
        return [assets_root_path + path for path in relative_path]
    return assets_root_path + relative_path

def update_semantics(stage, keep_semantics):
    for prim in stage.Traverse():
        if prim.HasAPI(Semantics.SemanticsAPI):
            processed_instances = set()
            for property in prim.GetProperties():
                is_semantic = Semantics.SemanticsAPI.IsSemanticsAPIPath(property.GetPath())
                if is_semantic:
                    instance_name = property.SplitName()[1]
                    if instance_name in processed_instances:
                        continue

                    processed_instances.add(instance_name)
                    sem = Semantics.SemanticsAPI.Get(prim, instance_name)
                    type_attr = sem.GetSemanticTypeAttr()
                    data_attr = sem.GetSemanticDataAttr()

                    if data_attr.Get() in keep_semantics:
                        continue
                    else:
                        print(f"Semantic data: {data_attr.Get()}")
                        prim.RemoveProperty(type_attr.GetName())
                        prim.RemoveProperty(data_attr.GetName())
                        prim.RemoveAPI(Semantics.SemanticsAPI, instance_name)

def full_textures_list():
    full_tex_list = []
    for texture in TEXTURES:
        full_tex_list.append(prefix_with_isaac_asset_server(texture))
    return full_tex_list

def add_pallets():
    PALLET = random.sample(PALLETS, 3)
    rep_obj_list = [rep.create.from_usd(pallet_path, semantics=[("class", "pallet")], count=2) for pallet_path in
                    PALLET]
    rep_pallet_group = rep.create.group(rep_obj_list)

    return rep_pallet_group

def add_forklifts():
    FORKLIFT = random.sample(FORKLIFTS, 1)
    rep_obj_list = [rep.create.from_usd(forklift_path, semantics=[("class", "forklift")], count=1) for forklift_path in
                    FORKLIFT]
    rep_forklift_group = rep.create.group(rep_obj_list)

    return rep_forklift_group

def add_carriers():
    CARRIER = random.sample(CARRIERS, 2)
    rep_obj_list = [rep.create.from_usd(pallet_path, semantics=[("class", "small_load_carrier")], count=1) for pallet_path in
                    CARRIER]
    rep_carrier_group = rep.create.group(rep_obj_list)

    return rep_carrier_group

def add_stillages():
    STILLAGE = random.sample(STILLAGES, 2)
    rep_obj_list = [rep.create.from_usd(pallet_path, semantics=[("class", "stillage")], count=1) for pallet_path in
                    STILLAGE]
    rep_stillage_group = rep.create.group(rep_obj_list)

    return rep_stillage_group

def add_palletjacks():
    PALLETJACK = random.sample(PALLETJACKS, 1)
    rep_obj_list = [rep.create.from_usd(pallet_path, semantics=[("class", "pallet_truck")], count=1) for pallet_path in
                    PALLETJACK]
    rep_palletjack_group = rep.create.group(rep_obj_list)

    return rep_palletjack_group

def run_orchestrator():
    rep.orchestrator.run()
    while not rep.orchestrator.get_is_started():
        simulation_app.update()
    while rep.orchestrator.get_is_started():
        simulation_app.update()
    rep.BackendDispatch.wait_until_done()
    rep.orchestrator.stop()

def randomize(groups,plane):
    with rep.utils.sequential():
        no_collision_group = []
        for group in groups:
            with group:
                #rep.physics.rigid_body(overwrite=True)
                #rep.physics.collider(approximation_shape="boundingSphere")
                rep.physics.collider(approximation_shape="boundingCube")
                rep.modify.pose(scale=0.01)
                rep.modify.pose(rotation=rep.distribution.uniform((0, 0, -180), (0, 0, 180)))
                if len(no_collision_group) == 0:
                    rep.randomizer.scatter_2d(plane, check_for_collisions= True)
                    #rep.modify.pose(rotation=rep.distribution.uniform((0, 0, -180), (0, 0, 180)))
                    #                scale=0.01)
                else:
                    rep.randomizer.scatter_2d(plane, check_for_collisions= True, no_coll_prims = no_collision_group)
                    #rep.modify.pose(rotation=rep.distribution.uniform((0, 0, -180), (0, 0, 180)))
                    #                scale=0.01)
                no_collision_group.append(group)

def main():
    print(f"Loading Stage {args.stage_path}")
    open_stage(prefix_with_isaac_asset_server(args.stage_path))
    # open_stage("omniverse://localhost/warehouse-v1-09-12.usd")
    stage = get_current_stage()
    plane = rep.create.plane(
        scale=(11, 7, 0) # (9, 6, 0), (8, 14, 0), (31, 25, 0)
    )

    for i in range(100):
        if i % 10 == 0:
            print(f"App update {i}..")
        simulation_app.update()

    rep_pallet_group = add_pallets()
    rep_forklift_group = add_forklifts()
    rep_carrier_group = add_carriers()
    rep_stillage_group = add_stillages()
    rep_palletjack_group = add_palletjacks()
    textures = full_textures_list()

    # rep_background_group = rep.get.prims(path_match="Background")
    update_semantics(stage=stage, keep_semantics=["pallet","forklift","small_load_carrier","stillage","pallet_truck"])

    ## Create camera with Replicator API for gathering data
    cam = rep.create.camera(clipping_range=(0.1, 1000000))

    with rep.trigger.on_frame(max_execs=CONFIG["num_frames"]):

        ## Move the camera around in the scene, focus on the center of warehouse
        with cam:
            rep.modify.pose(position=rep.distribution.uniform((-9, -6, 0.4), (9, 6, 5)),
                            look_at=rep.distribution.uniform((-2, -1, 0.4), (2, 1, 2)))
            #rep.modify.pose(position=rep.distribution.uniform((-4, -1, 0), (4, 1, 5)),
            #                rotation=rep.distribution.uniform((-5, 0, -180), (5, 0, 180)))

        with rep.get.prims(path_pattern="Pallet"):
            rep.randomizer.texture(textures=prefix_with_isaac_asset_server(TEXTURES))
            # rep.randomizer.color(colors=rep.distribution.uniform((0, 0, 0), (1, 1, 1)))

        randomize([rep_forklift_group,rep_pallet_group,rep_carrier_group,rep_stillage_group,rep_palletjack_group],plane)

        ## Randomize the lighting of the scene
        if args.randomize_lighting:
            rep_lights_group = rep.get.prims(path_pattern="Light", path_pattern_exclusion="forklift")
            with rep_lights_group:
                rep.modify.attribute("color", rep.distribution.uniform((0, 0, 0), (1, 1, 1)))
                rep.modify.attribute("intensity", rep.distribution.normal(50000.0, 200000.0))
                rep.modify.visibility(rep.distribution.choice([True,False]))

        ## Randomize the warehouse floor material
        if args.randomize_floor_material:
            random_mat_floor = rep.create.material_omnipbr(diffuse_texture=rep.distribution.choice(textures),
                                                        roughness=rep.distribution.uniform(0, 1),
                                                        metallic=rep.distribution.choice([0, 1]),
                                                        emissive_texture=rep.distribution.choice(textures),
                                                        emissive_intensity=rep.distribution.uniform(0, 1000),)
            with rep.get.prims(path_pattern="SM_Floor"):
                rep.randomizer.materials(random_mat_floor)

        ## Randomize the warehouse wall material
        if args.randomize_wall_material:
            random_mat_wall = rep.create.material_omnipbr(diffuse_texture=rep.distribution.choice(textures),
                                                        roughness=rep.distribution.uniform(0, 1),
                                                        metallic=rep.distribution.choice([0, 1]),
                                                        emissive_texture=rep.distribution.choice(textures),
                                                        emissive_intensity=rep.distribution.uniform(0, 1000),)
            with rep.get.prims(path_pattern="SM_Wall"):
                rep.randomizer.materials(random_mat_wall)

    ## Set up the writer
    writer = rep.WriterRegistry.get("BasicWriter")

    output_directory = args.data_dir
    print("Outputting data to ", output_directory)

    ## Use writer for bounding boxes, rgb images, segmentation and etc..
    writer.initialize(output_dir=output_directory,
                      rgb=True,
                      bounding_box_2d_tight=True)

    RESOLUTION = (CONFIG["width"], CONFIG["height"])
    render_product = rep.create.render_product(cam, RESOLUTION)
    writer.attach(render_product)

    run_orchestrator()
    simulation_app.update()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        carb.log_error(f"Exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        simulation_app.close()