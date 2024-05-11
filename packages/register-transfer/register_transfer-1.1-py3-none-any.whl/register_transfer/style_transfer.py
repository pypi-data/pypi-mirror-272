import collections
import cv2
from .predict import *
from pathlib import Path
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import warnings
import numpy as np

warnings.filterwarnings("ignore")
cur_path = Path(__file__).parent
model_path = f'{cur_path}/model'
st_model = f'{model_path}/sty_iter_450000_phase1_256_cumulate_face_enhance.pth'
df_model = f'{model_path}/deep_filter_10000.pth'


class TransferDataset(Dataset):
    def __init__(self, data_path):
        super(TransferDataset, self).__init__()
        self.data_list = []
        items = list(Path(data_path).glob('*'))
        for item in items:
            # name = item.stem
            self.data_list.append(item)
        self.name = [i.stem for i in self.data_list]

    def __len__(self):
        return len(self.data_list)

    def _get_name(self, idx):
        return self.name[idx]

    def __getitem__(self, idx):
        item_path = self.data_list[idx]
        name = item_path.stem
        source_img = (torch.tensor(np.load(f'{str(item_path)}/{name}_source_sift.npy'), dtype=torch.float32) / 255.).permute(2,0,1)
        target_img = (torch.tensor(np.load(f'{str(item_path)}/{name}_target_sift.npy'), dtype=torch.float32) / 255.).permute(2,0,1)
        return {'source': source_img, 'target': target_img, 'name': name}


class StyleTransferObj(nn.Module):
    def __init__(self, st_model, df_model, device=None):
        super(StyleTransferObj, self).__init__()
        if device is None:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        Trans = transformer.Transformer()
        embedding = StyTR.PatchEmbed(img_size=512)
        decoder = StyTR.decoder
        Trans.eval()
        self.network = StyTR.StyTransYuvInfer(decoder, embedding, Trans)
        self.network.load_state_dict(torch.load(st_model))
        self.network.to(device)
        self.network.eval()
        self.deep_filter = DeepGuidedFilterConvGFHeader()
        self.deep_filter.load_state_dict(torch.load(df_model))
        self.deep_filter.to(device)
        self.deep_filter.eval()
        embedding = None
        decoder = None
        Trans = None

    def forward(self, src, dst):
        content = transforms.Resize((512, 512))(src)
        style = transforms.Resize((512, 512))(dst)

        output = self.network(content, style)
        output = blur_delta(output, content)
        return self.deep_filter(x_lr=content, y_lr=output, x_hr=src).clamp_(0, 1)


def transfer(data_path, batch_size=17, num_workers=0, device=None, color_range=None):
    if color_range is None:
        color_range = (0, 255)
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    global st_model
    global df_model
    dataset = TransferDataset(data_path)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers)
    # testloader = DataLoader(dataset, batch_size=1, num_workers=1)
    model = StyleTransferObj(st_model=st_model, df_model=df_model).to(device)
    # results = []
    # names = []

    with torch.no_grad():
        dataloader = tqdm(dataloader, total=len(dataloader))
        for i, data in enumerate(dataloader):
            torch.cuda.empty_cache()
            source = data['source'].to(device)
            target = data['target'].to(device)
            name = data['name']
            out = model(source, target)
            # print(data['target'].shape)
            # results.append(out.detach().cpu())
            for _name, _out in zip(name, out):
                _out = (_out.detach().cpu().permute(1, 2, 0).clamp_(0, 1) * 255).numpy().astype(np.uint8)
                _out = _out.clip(color_range[0], color_range[1])
                cv2.imwrite(f'{data_path}/{_name}/{_name}_source_sift_transfer.png', cv2.cvtColor(_out, cv2.COLOR_RGB2BGR))
                _out_pth = (torch.tensor(_out.astype(np.float32)) / 255.).permute(2, 0, 1).unsqueeze(0)
                torch.save(_out_pth, f'{data_path}/{_name}/{_name}_source_sift_transfer.pth')
