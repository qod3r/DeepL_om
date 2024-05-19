import os
from pathlib import Path

from tqdm import tqdm
import nibabel as nib
import imageio
from skimage.io import imsave
from skimage.util import img_as_ubyte, img_as_uint


def save_nii_slices(nii_dir, save_dir, window_center=-600, window_width=1200):
    # Create the save directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)

    # Loop through each .nii file in the directory
    for nii_file in tqdm(nii_dir.glob("*.nii.gz"), desc="processing .nii files"):
        # Load the .nii file
        img = nib.load(str(nii_file))

        # Get the image data
        data = img.get_fdata()
        
        data = (data - (window_center - window_width / 2)) / window_width * 255
        data = data.clip(0, 255).astype('uint8')
        
        # Loop through each slice and save it as a separate image
        for slice_idx in range(data.shape[2]):
            # Create the output file path
            out_file = save_dir / f"{nii_file.stem.split('.')[0]}_slice{slice_idx}.png"

            # Save the slice as an image
            imsave(str(out_file), data[:, :, slice_idx])
            # imageio.imwrite(str(out_file), data[:, :, slice_idx], bitdepth=16)
            # print(f"Saved slice {slice_idx} from {nii_file.name} to {out_file.name}")


# Set the directory containing the .nii files
nii_dir = Path("data/studies/CT-1/")

# Set the directory to save the output images
save_dir = Path("data/yolo/images/")

# Call the function to save the .nii slices
save_nii_slices(nii_dir, save_dir)
