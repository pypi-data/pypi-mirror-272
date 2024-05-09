
def rate(img):
    imgs = torch.tensor(nib.load(input).get_fdata()).permute(-1,0,1).to(device).float()
    ratings = [model(transform(img).unsqueeze(0).unsqueeze(0)).softmax(dim=1).argmax().detach().cpu() for img in imgs]
    rating = torch.stack(ratings).float().mean()
    
    return rating

    print(f'Input: {input} | Motion Rating: {rating.item()}')
