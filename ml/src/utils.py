import os
from pathlib import Path
from pprint import pprint
from tqdm import tqdm

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from shapely import simplify
from shapely.geometry import Polygon
from skimage.measure import find_contours, label


def process_nii_file(file_path, area_thresh=5, simp_tol=1):
    # Load the .nii file
    img = nib.load(file_path)
    data = img.get_fdata()

    # Binarize the data (assuming the input is not binary)
    data_binary = (data > data.mean()).astype(int)

    polygons_with_metadata = []

    # Loop through each slice where a mask is present
    for slice_idx in range(data_binary.shape[2]):
        slice_data = data_binary[:, :, slice_idx]

        # Detect blobs (islands) of pixels
        labeled_blobs, num_blobs = label(slice_data, return_num=True)

        # Convert blobs to closed polygons and simplify them
        for blob_idx in range(1, num_blobs + 1):
            blob_mask = labeled_blobs == blob_idx
            contours = find_contours(blob_mask, 0.5, fully_connected="high")

            # Assume there is only one contour per blob
            contour = contours[0]

            # Convert the contour to a polygon and simplify it
            polygon = Polygon(contour)
            simplified_polygon = simplify(
                polygon, tolerance=simp_tol, preserve_topology=True
            )

            # Store the slice index, polygon, and file path
            if simplified_polygon.area > area_thresh:
                polygons_with_metadata.append(
                    (slice_idx, simplified_polygon, file_path)
                )

    return polygons_with_metadata


def visualize_polygons(polygons_with_metadata, slice_idx):
    # Find the polygons for the given slice index
    slice_polygons = [poly for i, poly, _ in polygons_with_metadata if i == slice_idx]

    # Load the .nii file and get the data for the given slice
    file_path = polygons_with_metadata[0][2]
    img = nib.load(file_path)
    data = img.get_fdata()
    slice_data = data[:, :, slice_idx]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the original slice data
    ax.imshow(slice_data, cmap="gray")

    # Plot the polygons on top of the slice data
    for polygon in slice_polygons:
        y, x = polygon.exterior.xy
        ax.plot(x, y, color="r", linewidth=1)

    ax.set_title(f"Slice {slice_idx}")
    plt.show()


def save_to_yolo_format(polygons_with_metadata, output_file):
    img = np.zeros((512, 512))
    with open(output_file, "w") as f:
        for slice_idx, polygon, file_path in polygons_with_metadata:
            # Get the coordinates of the polygon's exterior
            y, x = polygon.exterior.xy

            # Convert the coordinates to the YOLO format
            yolo_coords = [0]
            for i in range(len(x) - 1):
                yolo_coords.extend([x[i] / img.shape[1], y[i] / img.shape[0]])

            # Write the YOLO format line to the file
            f.write(" ".join(map(str, yolo_coords)) + "\n")


if __name__ == "__main__":
    mask_path = Path("data/masks/")
    output_path = Path("data/yolo/labels/")

    for mask_file in mask_path.iterdir():
        file_polygons = process_nii_file(mask_file)

        found_slices = set()
        for tup in file_polygons:
            found_slices.add(tup[0])

        for slice_idx in tqdm(found_slices):
            eligible_slices = list(filter(lambda x: x[0] == slice_idx, file_polygons))
            save_to_yolo_format(
                eligible_slices,
                output_path
                / f"{'_'.join(mask_file.stem.split('.')[0].split('_')[:2])}_slice{slice_idx}.txt",
            )

    # file_path = "data/masks/study_0255_mask.nii.gz"
    # polygons = process_nii_file(file_path)
    # from pprint import pprint
    # pprint(polygons)

    # visualize_polygons(polygons, slice_idx=10)

    # output_file = "yolo_format_output.txt"
    # save_to_yolo_format(polygons, output_file)
    # print(f"YOLO format output saved to: {output_file}")
