import os
import json
import hashlib
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

data_dir = "/home/user/IsaacSim-Autonomous-Forklift/sdg_src/data"
out_dir = "/home/user/IsaacSim-Autonomous-Forklift/sdg_src/viz_result"

def data_to_colour(data):
    if isinstance(data, str):
        data = bytes(data, "utf-8")
    else:
        data = bytes(data)
    m = hashlib.sha256()
    m.update(data)
    key = int(m.hexdigest()[:8], 16)
    r = ((((key >> 0) & 0xFF) + 1) * 33) % 255
    g = ((((key >> 8) & 0xFF) + 1) * 33) % 255
    b = ((((key >> 16) & 0xFF) + 1) * 33) % 255

    inv_norm_i = 128 * (3.0 / (r + g + b))

    return (int(r * inv_norm_i) / 255, int(g * inv_norm_i) / 255, int(b * inv_norm_i) / 255)

def colorize_bbox_2d(rgb_path, data, id_to_labels, file_path):
    rgb_img = Image.open(rgb_path)
    colors = [data_to_colour(bbox["semanticId"]) for bbox in data]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(rgb_img)

    legend_labels = set() 
    has_labels = False
    
    for bbox_2d, color in zip(data, colors):
        semantic_id = str(bbox_2d["semanticId"])
        label_dict = id_to_labels.get(semantic_id, {"class": "Unknown"})
        label = label_dict.get("class", "Unknown") 
        
        if label not in legend_labels:
            legend_labels.add(label)
            has_labels = True
            rect = patches.Rectangle(
                xy=(bbox_2d["x_min"], bbox_2d["y_min"]),
                width=bbox_2d["x_max"] - bbox_2d["x_min"],
                height=bbox_2d["y_max"] - bbox_2d["y_min"],
                edgecolor=color,
                linewidth=2,
                label=label,
                fill=False,
            )
        else:
            rect = patches.Rectangle(
                xy=(bbox_2d["x_min"], bbox_2d["y_min"]),
                width=bbox_2d["x_max"] - bbox_2d["x_min"],
                height=bbox_2d["y_max"] - bbox_2d["y_min"],
                edgecolor=color,
                linewidth=2,
                fill=False,
            )
        ax.add_patch(rect)

    if has_labels:
        plt.legend(loc="upper left")
    else:
        print("No valid labels found for the legend.")

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close(fig)

for i in range(100):
    number = str(i).zfill(4)
    
    rgb_path = os.path.join(data_dir, f"rgb_{number}.png")
    npy_path = os.path.join(data_dir, f"bounding_box_2d_tight_{number}.npy")
    json_path = os.path.join(data_dir, f"bounding_box_2d_tight_labels_{number}.json")
    
    if os.path.exists(rgb_path) and os.path.exists(npy_path) and os.path.exists(json_path):
        data = np.load(npy_path)

        with open(json_path, "r") as json_data:
            bbox2d_tight_id_to_labels = json.load(json_data)
        
        output_path = os.path.join(out_dir, f"viz_label_result_{number}.png")
        colorize_bbox_2d(rgb_path, data, bbox2d_tight_id_to_labels, output_path)
        print(f"Processed {number}")
    else:
        print(f"Skipping {number}: Files not found.")