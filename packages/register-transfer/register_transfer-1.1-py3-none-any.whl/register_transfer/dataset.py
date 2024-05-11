import torch.utils.data as data
import os
from PIL import Image
import torchvision.transforms.functional as TF
from torchvision import transforms
import random
import glob
import torch
from torchvision.transforms import ColorJitter


class ContentStyleTripleDataset(data.Dataset):
    def __init__(self, root, transform) -> None:
        super().__init__()
        # 获取文件夹包含source，target以及result
        self.root = root
        self.data_folders = os.listdir(root)
        try:
            self.data_folders.remove('.DS_Store')
        except:
            print("no .Ds_store file in this system which is great :)")
        self.transform = transform

    def __getitem__(self, index):
        path = os.path.join(self.root, self.data_folders[index])
        # 读取source,target,source_transfered
        source_img_path = os.path.join(path, 'low_res_in.png')
        target_img_path = os.path.join(path, 'style.png')
        source_transfered_path = os.path.join(path, 'low_res_out.png')

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')
        source_transfered_img = Image.open(source_transfered_path).convert('RGB')

        source_img = self.transform(source_img)
        target_img = self.transform(target_img)
        source_transfered_img = self.transform(source_transfered_img)
        return source_img, target_img, source_transfered_img

    def __len__(self):
        return len(self.data_folders)

    def name(self):
        return 'ContentStyleTripleDataset'


class ContentStyleTripleArgDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target以及result
        self.root = root
        self.data_folders = os.listdir(root)
        try:
            self.data_folders.remove('.DS_Store')
        except:
            print("no .Ds_store file in this system which is great :)")

    def transform(self, source, target, source_transfered):
        resize = transforms.Resize(size=(512, 512))

        target = resize(target)
        source = resize(source)
        source_transfered = resize(source_transfered)

        # random crop or use full image
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(256, 256))

        source = TF.crop(source, i, j, h, w)
        target = TF.crop(target, i, j, h, w)
        source_transfered = TF.crop(source_transfered, i, j, h, w)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        source_transfered = toTensor(source_transfered)

        return source, target, source_transfered

    def __getitem__(self, index):
        path = os.path.join(self.root, self.data_folders[index])
        # 读取source,target,source_transfered
        source_img_path = os.path.join(path, 'low_res_in.png')
        target_img_path = os.path.join(path, 'style.png')
        source_transfered_path = os.path.join(path, 'low_res_out.png')

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')
        source_transfered_img = Image.open(source_transfered_path).convert('RGB')

        source_img, target_img, source_transfered_img = self.transform(source_img, target_img, source_transfered_img)

        return source_img, target_img, source_transfered_img

    def __len__(self):
        return len(self.data_folders)

    def name(self):
        return 'ContentStyleTripleDataset'


class ContentStyleDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source, target):
        resize = transforms.Resize(size=(512, 512))
        source = resize(source)
        target = resize(target)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(256, 256))
        source = TF.crop(source, i, j, h, w)
        target = TF.crop(target, i, j, h, w)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)

        return source, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img = self.transform(source_img, target_img)

        return source_img, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResColorJitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source, target):
        resize = transforms.Resize(size=(256, 256))
        source = resize(source)
        target = resize(target)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(128, 128))
        source = TF.crop(source, i, j, h, w)
        target = TF.crop(target, i, j, h, w)

        # random jitter
        if random.random() < 0.5:
            color_jitter = transforms.ColorJitter(brightness=0.1,
                                                  contrast=0.1,
                                                  hue=0.1,
                                                  saturation=0.1)
            source = color_jitter(source)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)

        return source, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img = self.transform(source_img, target_img)

        return source_img, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResColorJitterRandomCropDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source, target):
        resize = transforms.Resize(size=(256, 256))
        corp_resize = transforms.Resize(size=(128, 128))
        source = resize(source)
        target = resize(target)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(128, 128))
        source_crop = TF.crop(source, i, j, h, w)
        target_crop = TF.crop(target, i, j, h, w)

        # random jitter
        if random.random() < 0.5:
            color_jitter = transforms.ColorJitter(brightness=0.1,
                                                  contrast=0.1,
                                                  hue=0.1,
                                                  saturation=0.1)
            source_crop = color_jitter(source_crop)

        toTensor = transforms.ToTensor()
        source_crop = toTensor(source_crop)
        target_crop = toTensor(target_crop)

        if random.random() < 0.5:
            # small source, large target
            target = corp_resize(target)
            target = toTensor(target)
            return source_crop, target_crop, target
        else:
            # small source, small target
            return source_crop, target_crop, target_crop

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img, full_target_img = self.transform(source_img, target_img)

        return source_img, target_img, full_target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResAffineDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source, target):
        resize = transforms.Resize(size=(256, 256))
        source = resize(source)
        target = resize(target)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(128, 128))
        source = TF.crop(source, i, j, h, w)
        target = TF.crop(target, i, j, h, w)

        # affine transform
        randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)
        if random.random() < 0.5:
            target_random = randp(target)
        else:
            target_random = target

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResAffineRandomCropDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source_ori, target_ori):
        resize = transforms.Resize(size=(256, 256))
        crop_resize = transforms.Resize(size=(128, 128))
        source = resize(source_ori)
        target = resize(target_ori)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(128, 128))
        source = TF.crop(source, i, j, h, w)
        target = TF.crop(target, i, j, h, w)

        # affine transform
        randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)
        if random.random() < 0.5:
            target_random = randp(target)
        else:
            if random.random() < 0.5:
                target_random = target
            else:
                target_random = crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResGlobalAffineRandomCropDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source_ori, target_ori):
        resize = transforms.Resize(size=(256, 256))
        crop_resize = transforms.Resize(size=(128, 128))
        source = resize(source_ori)
        target = resize(target_ori)

        random_crop_flag = random.random() < 0.6
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source, output_size=(128, 128))
            source = TF.crop(source, i, j, h, w)
            target = TF.crop(target, i, j, h, w)
        else:
            source = crop_resize(source_ori)
            target = crop_resize(target_ori)

        # affine transform
        randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)
        if random.random() < 0.5:
            target_random = randp(target)
        else:
            if random.random() < 0.5:
                target_random = target
            else:
                target_random = crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleGlobalAffineColorjitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.color = ColorJitter(brightness=[0.8, 1.2],
                                 contrast=[0.8, 1.2],
                                 saturation=[0.5, 1.5],
                                 hue=[-0.05, 0.05])
        self.resize = transforms.Resize(size=(256, 256))
        self.crop_resize = transforms.Resize(size=(128, 128))
        self.randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)

    def transform(self, source_ori, target_ori):
        if random.random() < 0.8:
            source_ori = self.color(source_ori)
            target_ori = self.color(target_ori)

        source = self.resize(source_ori)
        target = self.resize(target_ori)

        random_crop_flag = random.random() < 0.5
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source_ori, output_size=(128, 128))
            source = TF.crop(source_ori, i, j, h, w)
            target = TF.crop(target_ori, i, j, h, w)
        else:
            source = self.crop_resize(source_ori)
            target = self.crop_resize(target_ori)

        # affine transform
        if random.random() < 0.5:
            target_random = self.randp(target)
        else:
            target_random = target

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


def mask_unselected(tensor, i, j, h, w):
    mask = torch.ones_like(tensor)
    mask[:, i:i + h, j:j + w] = 0
    mask = mask > 0
    masked_tensor = torch.masked_fill(tensor, mask, 0)
    return masked_tensor


class ContentStyleMaskedDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

    def transform(self, source, target):
        resize = transforms.Resize(size=(256, 256))
        source = resize(source)
        target = resize(target)

        # random crop
        i, j, h, w = transforms.RandomCrop.get_params(
            source, output_size=(128, 128))

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)

        masked_source = mask_unselected(source, i, j, h, w)
        masked_target = mask_unselected(target, i, j, h, w)

        return masked_source, target, masked_target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        masked_source_img, target_img, masked_target_img = self.transform(source_img, target_img)

        return masked_source_img, target_img, masked_target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleGlobalColorjitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.color = ColorJitter(brightness=[0.8, 1.2],
                                 contrast=[0.8, 1.2],
                                 saturation=[0.5, 1.5],
                                 hue=[-0.05, 0.05])

        self.crop_resize = transforms.Resize(size=(128, 128))

    def transform(self, source_ori, target_ori):

        source_ori = self.color(source_ori)
        target_ori = self.color(target_ori)

        random_crop_flag = random.random() < 0.5
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source_ori, output_size=(128, 128))
            source = TF.crop(source_ori, i, j, h, w)
            target = TF.crop(target_ori, i, j, h, w)
        else:
            source = self.crop_resize(source_ori)
            target = self.crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        # target_random = toTensor(target_random)

        return source, target, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.resize = transforms.Resize(size=(128, 128))

    def transform(self, source_ori, target_ori):

        source = self.resize(source_ori)
        target = self.resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)

        return source, target, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResGlobalAffineRandomCropColorjitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.color = ColorJitter(brightness=[0.8, 1.2],
                                 contrast=[0.8, 1.2],
                                 saturation=[0.5, 1.5],
                                 hue=[-0.05, 0.05])
        self.resize = transforms.Resize(size=(256, 256))
        self.crop_resize = transforms.Resize(size=(128, 128))
        self.randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)

    def transform(self, source_ori, target_ori):
        if random.random() < 0.8:
            source_ori = self.color(source_ori)
            target_ori = self.color(target_ori)

        source = self.resize(source_ori)
        target = self.resize(target_ori)

        random_crop_flag = random.random() < 0.6
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source, output_size=(128, 128))
            source = TF.crop(source, i, j, h, w)
            target = TF.crop(target, i, j, h, w)
        else:
            source = self.crop_resize(source_ori)
            target = self.crop_resize(target_ori)

        # affine transform
        if random.random() < 0.5:
            target_random = self.randp(target)
        else:
            if random.random() < 0.5:
                target_random = target
            else:
                target_random = self.crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleLowResGlobalAffineRandomCropColorjitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.color = ColorJitter(brightness=[0.8, 1.2],
                                 contrast=[0.8, 1.2],
                                 saturation=[0.5, 1.5],
                                 hue=[-0.05, 0.05])
        self.resize = transforms.Resize(size=(256, 256))
        self.crop_resize = transforms.Resize(size=(128, 128))
        self.randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)

    def transform(self, source_ori, target_ori):
        if random.random() < 0.8:
            source_ori = self.color(source_ori)
            target_ori = self.color(target_ori)

        source = self.resize(source_ori)
        target = self.resize(target_ori)

        random_crop_flag = random.random() < 0.6
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source, output_size=(128, 128))
            source = TF.crop(source, i, j, h, w)
            target = TF.crop(target, i, j, h, w)
        else:
            source = self.crop_resize(source_ori)
            target = self.crop_resize(target_ori)

        # affine transform
        if random.random() < 0.5:
            target_random = self.randp(target)
        else:
            if random.random() < 0.5:
                target_random = target
            else:
                target_random = self.crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


class ContentStyleHighResGlobalAffineRandomCropColorjitterDataset(data.Dataset):
    def __init__(self, root) -> None:
        super().__init__()
        # 获取文件夹包含source，target
        self.root = root

        self.source_dir = os.path.join(root, 'source_crop')
        self.target_dir = os.path.join(root, 'target_crop')

        target_image_list = []
        for file in glob.glob(self.target_dir + '/*'):
            target_image_list.append(file)

        source_image_list = []
        for file in glob.glob(self.source_dir + '/*'):
            source_image_list.append(file)

        self.source_paths = source_image_list
        self.target_paths = target_image_list

        self.target_paths.sort()
        self.source_paths.sort()

        self.color = ColorJitter(brightness=[0.8, 1.2],
                                 contrast=[0.8, 1.2],
                                 saturation=[0.5, 1.5],
                                 hue=[-0.05, 0.05])
        self.resize = transforms.Resize(size=(512, 512))
        self.crop_resize = transforms.Resize(size=(256, 256))
        self.randp = transforms.RandomPerspective(distortion_scale=0.6, p=1.0)

    def transform(self, source_ori, target_ori):
        if random.random() < 0.8:
            source_ori = self.color(source_ori)
            target_ori = self.color(target_ori)

        source = self.resize(source_ori)
        target = self.resize(target_ori)

        random_crop_flag = random.random() < 0.6
        # random crop
        if random_crop_flag:
            i, j, h, w = transforms.RandomCrop.get_params(
                source, output_size=(256, 256))
            source = TF.crop(source, i, j, h, w)
            target = TF.crop(target, i, j, h, w)
        else:
            source = self.crop_resize(source_ori)
            target = self.crop_resize(target_ori)

        # affine transform
        if random.random() < 0.5:
            target_random = self.randp(target)
        else:
            if random.random() < 0.5:
                target_random = target
            else:
                target_random = self.crop_resize(target_ori)

        toTensor = transforms.ToTensor()
        source = toTensor(source)
        target = toTensor(target)
        target_random = toTensor(target_random)

        return source, target_random, target

    def __getitem__(self, index):
        if random.random() < 0.5:
            source_img_path = self.source_paths[index]
            target_img_path = self.target_paths[index]
        else:
            source_img_path = self.target_paths[index]
            target_img_path = self.source_paths[index]

        source_img = Image.open(source_img_path).convert('RGB')
        target_img = Image.open(target_img_path).convert('RGB')

        source_img, target_img_random, target_img = self.transform(source_img, target_img)

        return source_img, target_img_random, target_img

    def __len__(self):
        return len(self.source_paths)

    def name(self):
        return 'ContentStyleDataset'


def getFileList(dir, Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir：文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getFileList(newDir, Filelist, ext)
    return Filelist
