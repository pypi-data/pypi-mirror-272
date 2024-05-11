import os
import torch
from PIL import Image, ImageOps
from os.path import basename
from os.path import splitext
from torchvision import transforms
from .dataset import getFileList
import natsort
from .fastGuideFilter import DeepGuidedFilterConvGFHeader
from . import transformer as transformer
from . import StyTR as StyTR
import torchvision.transforms as T
from .image_utils import EMPatches


def patch_loader(image_numpy, patchsize, overlap):
    # split into patches
    totensor = toTensor()
    emp = EMPatches()
    img_patches, indices = emp.extract_patches(image_numpy, patchsize=patchsize, overlap=overlap)
    # maps to tensor for each patch
    img_patches_tensor = [totensor(patch).unsqueeze(0) for patch in img_patches]
    # reformat as a batch of image
    img_patches_tensors = torch.cat(img_patches_tensor, 0)
    return img_patches_tensors, emp, indices


def patch_merger(emp, indices, image_patches_tensor):
    # to cpu
    image_patches_tensor = image_patches_tensor.cpu().clone()
    # clip and rescale
    # image_patches_tensor = image_patches_tensor.clamp(0,1)
    # image_patches_tensor = image_patches_tensor * 255.0
    image_patches_tensor = image_patches_tensor.permute(0, 2, 3, 1)
    image_patches = image_patches_tensor.numpy()
    # merge patch
    merged_img = emp.merge_patches(image_patches, indices, mode='avg')
    # back to tensor
    merged_img = torch.from_numpy(merged_img).permute(2, 0, 1).unsqueeze(0).contiguous()
    return merged_img


def transform(size):
    transform_list = []
    transform_list.append(transforms.Resize((size[0], size[1])))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform


def toTensor():
    transform_list = []
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform


def image_loader_icc_slim(image_name):
    image = Image.open(image_name).convert("RGB")
    icc_profile = image.info.get("icc_profile")
    return image, icc_profile


def image_saver_with_icc(tensor, path, icc):
    unloader = transforms.ToPILImage()
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    image.save(path, icc_profile=icc)


def blur_delta(result_tensor, source_tensor):
    blur = T.GaussianBlur(kernel_size=(7, 7), sigma=(1, 2))
    delta = blur(blur(result_tensor - source_tensor))
    new_result = source_tensor + delta
    return new_result


def main():
    # parser = argparse.ArgumentParser()
    # # Basic options
    # parser.add_argument('--source_dir', type=str, default='./input/content',
    #                     help='Directory path to a batch of content images')
    # parser.add_argument('--target_dir', type=str, default='./input/style',
    #                     help='Directory path to a batch of style images')
    # parser.add_argument('--output', type=str, default='output',
    #                     help='Directory to save the output image(s)')
    # parser.add_argument('--model_path', type=str,
    #                     default='experiments/sty_iter_450000_phase1_256_cumulate_face_enhance.pth')
    # parser.add_argument('--filter_path', type=str, default='experiments/deep_filter_10000.pth')
    # parser.add_argument('--style_interpolation_weights', type=str, default="")
    # parser.add_argument('--a', type=float, default=1.0)
    # parser.add_argument('--position_embedding', default='sine', type=str, choices=('sine', 'learned'),
    #                     help="Type of positional embedding to use on top of the image features")
    # parser.add_argument('--hidden_dim', default=512, type=int,
    #                     help="Size of the embeddings (dimension of the transformer)")
    # parser.add_argument('--regist', action="store_true")
    # parser.add_argument('--face', action="store_true")
    # args = parser.parse_args()

    # Advanced options
    content_size = [512, 512]
    style_size = [512, 512]
    save_ext = '.png'
    # output_path = args.output
    output_path = '../result'
    # alpha = args.a

    device = torch.device("cuda")
    print(device)

    # style_paths = natsort.natsorted(getFileList(args.target_dir, [], 'jpg'))
    # content_paths = natsort.natsorted(getFileList(args.source_dir, [], 'jpg'))

    style_paths = natsort.natsorted(getFileList('../test/style', [], 'png'))
    content_paths = natsort.natsorted(getFileList('../test/content', [], 'png'))

    print(style_paths)
    print(content_paths)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    Trans = transformer.Transformer()
    embedding = StyTR.PatchEmbed(img_size=512)
    decoder = StyTR.decoder

    Trans.eval()

    network = StyTR.StyTransYuvInfer(decoder, embedding, Trans)
    # network.load_state_dict(torch.load(args.model_path))
    network.load_state_dict(torch.load('sty_iter_450000_phase1_256_cumulate_face_enhance.pth'))
    network.eval()
    network.to(device)

    deep_filter = DeepGuidedFilterConvGFHeader()
    # deep_filter.load_state_dict(torch.load(args.filter_path))
    deep_filter.load_state_dict(torch.load('deep_filter_10000.pth'))
    deep_filter.eval()
    deep_filter.to(device)

    content_tf = transform(content_size)
    style_tf = transform(style_size)
    totensor = toTensor()

    # regist = Registration()

    for content_path, style_path in zip(content_paths, style_paths):
        print("content:", content_path)
        print("style:", style_path)
        if '.DS_Store' in str(content_path):
            continue
        if '.DS_Store' in str(style_path):
            continue

        result_path = os.path.join(output_path, '{:s}_{:s}'.format(splitext(basename(content_path))[0],
                                                                   splitext(basename(style_path))[0])) + save_ext

        content_, content_icc = image_loader_icc_slim(content_path)
        content_ = ImageOps.exif_transpose(content_)
        style_, style_icc = image_loader_icc_slim(style_path)
        style_ = ImageOps.exif_transpose(style_)

        # if args.regist:
        #     style_ = regist.register(content_, style_)
        #     if style_ is None:
        #         style_, style_icc = image_loader_icc_slim(style_path)
        #         style_ = ImageOps.exif_transpose(style_)

        content_ = content_.resize(content_size)
        style_ = style_.resize(style_size)

        origin_content_, content_icc = image_loader_icc_slim(content_path)
        origin_content_ = ImageOps.exif_transpose(origin_content_)
        origin_style_, style_icc = image_loader_icc_slim(style_path)
        origin_style_ = ImageOps.exif_transpose(origin_style_)

        origin_content = totensor(origin_content_)
        origin_style = totensor(origin_style_)
        content = content_tf(content_)
        style = style_tf(style_)

        style = style.to(device).unsqueeze(0)
        content = content.to(device).unsqueeze(0)
        origin_content = origin_content.to(device).unsqueeze(0)
        origin_style = origin_style.to(device).unsqueeze(0)

        with torch.no_grad():
            output = network(content, style)
        output = blur_delta(output, content)
        ori_output = deep_filter(x_lr=content, y_lr=output, x_hr=origin_content)
        ori_output = ori_output.cpu()
        ori_output = ori_output.clamp(0, 1)
        image_saver_with_icc(ori_output, result_path, icc=style_icc)


if __name__ == '__main__':
    main()