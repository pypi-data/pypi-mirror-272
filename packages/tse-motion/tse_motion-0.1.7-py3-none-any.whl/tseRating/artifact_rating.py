import sys
import torch
import nibabel as nib
from torchvision.transforms import CenterCrop
from monai.networks.nets import DenseNet121

def rate_motion_artifact(input_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=5)
    model.load_state_dict(torch.load('./checkpoint/weight_20.pth', map_location=device))
    model = model.to(device)
    model.eval()

    transform = CenterCrop((512, 512))
    imgs = torch.tensor(nib.load(input_path).get_fdata()).permute(-1, 0, 1).to(device).float()
    ratings = [model(transform(img).unsqueeze(0).unsqueeze(0)).softmax(dim=1).argmax().detach().cpu() for img in imgs]
    rating = torch.stack(ratings).float().mean()
    return rating.item()

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m motion_artifact_rating <path_to_nifti_file>")
        sys.exit(1)
    input_path = sys.argv[1]
    rating = rate_motion_artifact(input_path)
    print(f'Input: {input_path} | Motion Rating: {rating}')

if __name__ == '__main__':
    main()
