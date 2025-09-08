!pip install --upgrade "huggingface_hub[cli]"
from huggingface_hub import login

login()  # paste your HF token here

#Load huggingface
# installations
!pip install -U fiftyone
!pip install huggingface_hub[hf_xet]
!pip install --upgrade huggingface_hub

#load voxel 51 SLAKE
import fiftyone as fo
from fiftyone.utils.huggingface import load_from_hub
  # Load the dataset
  # Note: other available arguments include 'max_samples', etc
dataset = load_from_hub("Voxel51/SLAKE")
