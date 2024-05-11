import torch
import torch.nn.functional as F
from torch import nn
from .ViT_helper import to_2tuple
from .fastGuideFilter import FastGuidedFilter
from kornia.color import *

class PatchEmbed(nn.Module):
    """ Image to Patch Embedding
    """
    def __init__(self, img_size=256, patch_size=8, in_chans=3, embed_dim=512):
        super().__init__()
        img_size = to_2tuple(img_size)
        patch_size = to_2tuple(patch_size)
        num_patches = (img_size[1] // patch_size[1]) * (img_size[0] // patch_size[0])
        self.img_size = img_size
        self.patch_size = patch_size
        self.num_patches = num_patches
        
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.up1 = nn.Upsample(scale_factor=2, mode='nearest')

    def forward(self, x):
        B, C, H, W = x.shape
        x = self.proj(x)

        return x


decoder = nn.Sequential(
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 256, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 128, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 128, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 64, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 64, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 3, (3, 3)),
)

vgg = nn.Sequential(
    nn.Conv2d(3, 3, (1, 1)),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(3, 64, (3, 3)),
    nn.ReLU(),  # relu1-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 64, (3, 3)),
    nn.ReLU(),  # relu1-2
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 128, (3, 3)),
    nn.ReLU(),  # relu2-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 128, (3, 3)),
    nn.ReLU(),  # relu2-2
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 256, (3, 3)),
    nn.ReLU(),  # relu3-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),  # relu3-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),  # relu3-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),  # relu3-4
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 512, (3, 3)),
    nn.ReLU(),  # relu4-1, this is the last layer used
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu4-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu4-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu4-4
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu5-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu5-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(),  # relu5-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU()  # relu5-4
)

class MLP(nn.Module):
    """ Very simple multi-layer perceptron (also called FFN)"""

    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super().__init__()
        self.num_layers = num_layers
        h = [hidden_dim] * (num_layers - 1)
        self.layers = nn.ModuleList(nn.Linear(n, k) for n, k in zip([input_dim] + h, h + [output_dim]))

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = F.relu(layer(x)) if i < self.num_layers - 1 else layer(x)
        return x
    
class StyTrans(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs) + content_img

        return Ics
    
class StyTransIdentity(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        cc = self.transformer(content, mask , content, pos_c, pos_c)
        ss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(hs)
        Icc = self.decode(cc)
        Iss = self.decode(ss)

        return Ics,Icc,Iss
    
class StyTransAddRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        cc = self.transformer(content, mask , content, pos_c, pos_c)
        ss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(hs+content)
        Icc = self.decode(cc+content)
        Iss = self.decode(ss+style)

        return Ics,Icc,Iss
    
class StyTransAddResInfer(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        Ics = self.decode(hs+content)

        return Ics
    
class StyDeepGuidedTrans(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed
        self.filter = FastGuidedFilter(1,1e-8)

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img, guided):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        Ics = self.decode(hs)
        Ics = self.filter(lr_x=content_img,lr_y=Ics,hr_x=guided).clamp(0,1)
        return Ics 

class StyTransMultiTask(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
     
        self.embedding = PatchEmbed

        self.decode = nn.Sequential(
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 256, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 128, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 128, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 64, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        # nn.Conv2d(64, 64, (3, 3)),
        # nn.ReLU(),
        # nn.ReflectionPad2d((1, 1, 1, 1)),
        # nn.Conv2d(64, 3, (3, 3)),
        )

        self.delta_deocoder_head = nn.Sequential(nn.Conv2d(64, 64, (3, 3)),
                                                nn.ReLU(),
                                                nn.ReflectionPad2d((1, 1, 1, 1)),
                                                nn.Conv2d(64, 3, (3, 3)))
        self.direct_decoder_head = nn.Sequential(nn.Conv2d(64, 64, (3, 3)),
                                                nn.ReLU(),
                                                nn.ReflectionPad2d((1, 1, 1, 1)),
                                                nn.Conv2d(64, 3, (3, 3)))

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs)
        delta = self.delta_deocoder_head(Ics)
        direct = self.direct_decoder_head(Ics)
        return delta,direct
    
# class decoderWithContent(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.upsampling_decoder = nn.Sequential(
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(512, 256, (3, 3)),
#                 nn.ReLU(),
#                 nn.Upsample(scale_factor=2, mode='nearest'),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(256, 256, (3, 3)),
#                 nn.ReLU(),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(256, 256, (3, 3)),
#                 nn.ReLU(),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(256, 256, (3, 3)),
#                 nn.ReLU(),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(256, 128, (3, 3)),
#                 nn.ReLU(),
#                 nn.Upsample(scale_factor=2, mode='nearest'),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(128, 128, (3, 3)),
#                 nn.ReLU(),
#                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                 nn.Conv2d(128, 64, (3, 3)),
#                 nn.ReLU(),
#                 nn.Upsample(scale_factor=2, mode='nearest'),
#         )
#         self.content_encoder = nn.Sequential( nn.ReflectionPad2d((1, 1, 1, 1)),
#                                 nn.Conv2d(3, 128, (3, 3)),
#                                 nn.ReLU(),
#                                 nn.ReflectionPad2d((1, 1, 1, 1)),
#                                 nn.Conv2d(128, 64, (3, 3)))
        
#         self.final_decoder = nn.Sequential(nn.ReflectionPad2d((1, 1, 1, 1)),
#                                            nn.Conv2d(128, 64, (3, 3)),
#                                            nn.ReLU(),
#                                            nn.ReflectionPad2d((1, 1, 1, 1)),
#                                            nn.Conv2d(64, 3, (3, 3)))
    
#     def forward(self,x,content):
#         content_encoded = self.content_encoder(content)
#         x_decoded = self.upsampling_decoder(x)
#         x_combined = torch.cat([x_decoded,content_encoded],1)
#         final = self.final_decoder(x_combined)
#         return final

class decoderWithContent(nn.Module):
    def __init__(self):
        super().__init__()
        self.upsampling_decoder = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
        )
        self.content_encoder = nn.Sequential( nn.ReflectionPad2d((1, 1, 1, 1)),
                                nn.Conv2d(3, 128, (3, 3)),
                                nn.ReLU(),
                                nn.ReflectionPad2d((1, 1, 1, 1)),
                                nn.Conv2d(128, 64, (3, 3)))
        
        self.final_decoder = nn.Sequential(nn.ReflectionPad2d((1, 1, 1, 1)),
                                           nn.Conv2d(128+64, 3, (3, 3)))
    
    def forward(self,x,content):
        content_encoded = self.content_encoder(content)
        x_decoded = self.upsampling_decoder(x)
        x_combined = torch.cat([x_decoded,content_encoded],1)
        final = self.final_decoder(x_combined)
        return final
    
class StyTransModifyedDecoder(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(5):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs,content_img)

        return Ics
    
class upsampling_decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.decoder = nn.Sequential(
                      nn.ReflectionPad2d((1, 1, 1, 1)),
                      nn.Conv2d(6, 64, (3, 3)),
                      nn.ReLU(),
                      nn.ReflectionPad2d((1, 1, 1, 1)),
                      nn.Conv2d(64, 64, (3, 3)),
                      nn.ReLU(),
                      nn.ReflectionPad2d((1, 1, 1, 1)),
                      nn.Conv2d(64, 3, (3, 3)))
    def forward(self,x,content):
        x = torch.cat([x,content],dim=1)
        y = self.decoder(x)
        return y
    
class StyTransWithConstaint(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed
        self.up_decoder = upsampling_decoder()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs)
        Ics_with_content = self.up_decoder(Ics,content_img)
        return Ics, Ics_with_content
    
class StyTransWithConstaintDetach(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed
        self.up_decoder = upsampling_decoder()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs)
        Ics_with_content = self.up_decoder(Ics.detach(),content_img)
        return Ics, Ics_with_content

class StyTransRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        hs = torch.cat([hs,content],dim=1)   
        Ics = self.decode(hs)
       
        return Ics
    
class StyTransResIdentity(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        cc = self.transformer(content, mask , content, pos_c, pos_c)
        ss = self.transformer(style, mask , style, pos_s, pos_s)

        hs = torch.cat([hs,content],dim=1)
        cc = torch.cat([cc,content],dim=1)
        ss = torch.cat([ss,style],dim=1)

        Ics = self.decode(hs)
        Icc = self.decode(cc)
        Iss = self.decode(ss)

        return Ics,Icc,Iss

class SE_Block(nn.Module):
    "credits: https://github.com/moskomule/senet.pytorch/blob/master/senet/se_module.py#L4"
    def __init__(self, c, r=16):
        super().__init__()
        self.squeeze = nn.AdaptiveAvgPool2d(1)
        self.excitation = nn.Sequential(
            nn.Linear(c, c // r, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(c // r, c, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        bs, c, _, _ = x.shape
        y = self.squeeze(x).view(bs, c)
        y = self.excitation(y).view(bs, c, 1, 1)
        return x * y.expand_as(x)
    
class StyTransSERes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model
        self.se = SE_Block(1024)       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        hs = torch.cat([hs,content],dim=1)
        hs = self.se(hs)   
        Ics = self.decode(hs)
       
        return Ics
    
class StyTransExtraDecoder(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 256, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 128, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 128, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 64, (3, 3)),
        nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(64, 64, (3, 3)),
        nn.ReLU(),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(64, 3, (3, 3)),
        )
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s) 

        Ics = self.decode(hs)

        return Ics
    
class StyTransDirectRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        Ics = self.decode(hs)
        Ics = content_img + Ics
        return Ics
    
class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)
    
    
class DownBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DownBlock, self).__init__()
        self.double_conv = DoubleConv(in_channels, out_channels)
        self.down_sample = nn.MaxPool2d(2)

    def forward(self, x):
        skip_out = self.double_conv(x)
        down_out = self.down_sample(skip_out)
        return (down_out, skip_out)

    
class UpBlock(nn.Module):
    def __init__(self, in_channels, out_channels, up_sample_mode):
        super(UpBlock, self).__init__()
        if up_sample_mode == 'conv_transpose':
            self.up_sample = nn.ConvTranspose2d(in_channels-out_channels, in_channels-out_channels, kernel_size=2, stride=2)        
        elif up_sample_mode == 'bilinear':
            self.up_sample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:
            raise ValueError("Unsupported `up_sample_mode` (can take one of `conv_transpose` or `bilinear`)")
        self.double_conv = DoubleConv(in_channels, out_channels)

    def forward(self, down_input, skip_input):
        x = self.up_sample(down_input)
        x = torch.cat([x, skip_input], dim=1)
        return self.double_conv(x)

    
class UNetAlike(nn.Module):
    def __init__(self,up_sample_mode='conv_transpose'):
        super(UNetAlike, self).__init__()
        self.up_sample_mode = up_sample_mode
        # Downsampling Path
        self.down_conv1 = DownBlock(3, 64)
        self.down_conv2 = DownBlock(64, 128)
        self.down_conv3 = DownBlock(128, 256)
        # Upsampling Path
        self.up_conv3 = UpBlock(256 + 512, 256, self.up_sample_mode)
        self.up_conv2 = UpBlock(128 + 256, 128, self.up_sample_mode)
        self.up_conv1 = UpBlock(128 + 64, 64, self.up_sample_mode)
        # Final Convolution
        self.conv_last = nn.Conv2d(64, 3, kernel_size=3, padding=1)

    def forward(self, content, bottle_neck):
        x_content, skip1_out = self.down_conv1(content)
        x_content, skip2_out = self.down_conv2(x_content)
        _, skip3_out = self.down_conv3(x_content)

        x = self.up_conv3(bottle_neck, skip3_out)
        x = self.up_conv2(x, skip2_out)
        x = self.up_conv1(x, skip1_out)
        x = self.conv_last(x)
        return x
    

class StyTransUnetRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = UNetAlike()
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)
        Ics = self.decode(content_img,hs)
       
        return Ics

class StyTransDirectFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs) + content_img

        Icc = self.decode(self.transformer(content, mask , content, pos_c, pos_c)) + content_img
        Iss = self.decode(self.transformer(style, mask , style, pos_s, pos_s)) + style_img

        return Ics,Icc,Iss
    
class StyTransDirectYuvFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(hs)
        Icc = self.decode(self.transformer(content, mask , content, pos_c, pos_c))
        Iss = self.decode(self.transformer(style, mask , style, pos_s, pos_s))

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img) 
        Ics = self.yuv2rgb(Ics + content_yuv_img)
        Icc = self.yuv2rgb(Icc + content_yuv_img)
        Iss = self.yuv2rgb(Iss + style_yuv_img)

        return Ics,Icc,Iss
    
class StyTransDirectYuvFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(hs)
        Icc = self.decode(self.transformer(content, mask , content, pos_c, pos_c))
        Iss = self.decode(self.transformer(style, mask , style, pos_s, pos_s))

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img) 
        Ics = self.yuv2rgb(Ics + content_yuv_img)
        Icc = self.yuv2rgb(Icc + content_yuv_img)
        Iss = self.yuv2rgb(Iss + style_yuv_img)

        return Ics,Icc,Iss
    
class StyTransDirectYuvFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(hs)
        Icc = self.decode(self.transformer(content, mask , content, pos_c, pos_c))
        Iss = self.decode(self.transformer(style, mask , style, pos_s, pos_s))

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img) 
        Ics_rgb = self.yuv2rgb(Ics + content_yuv_img)
        Icc_rgb = self.yuv2rgb(Icc + content_yuv_img)
        Iss_rgb = self.yuv2rgb(Iss + style_yuv_img)
        
        return Ics_rgb,Icc_rgb,Iss_rgb,Ics
    
class StyTransYuvDirectYuvFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        style_img_yuv = self.rgb2yuv(style_img)
        content_img_yuv = self.rgb2yuv(content_img)

        ### Linear projection
        style = self.embedding(style_img_yuv)
        content = self.embedding(content_img_yuv)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(hs)
        Icc = self.decode(self.transformer(content, mask , content, pos_c, pos_c))
        Iss = self.decode(self.transformer(style, mask , style, pos_s, pos_s))

        Ics_rgb = self.yuv2rgb(Ics + content_img_yuv)
        Icc_rgb = self.yuv2rgb(Icc + content_img_yuv)
        Iss_rgb = self.yuv2rgb(Iss + style_img_yuv)
        
        return Ics_rgb,Icc_rgb,Iss_rgb,Ics
    
class StyTransDirectYuvFinalResInfer(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(hs)
        content_yuv_img = self.rgb2yuv(content_img)
        Ics_rgb = self.yuv2rgb(Ics + content_yuv_img)
        
        return Ics_rgb

class StyTransDirectFinalResSlim(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs) + content_img

        return Ics 
    
"""
 self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
"""
class StyTransYuvRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hcs = self.transformer(style, mask , content, pos_c, pos_s)
        hcc = self.transformer(content, mask , content, pos_c, pos_c)
        hss = self.transformer(style, mask , style, pos_s, pos_s)


        ics = torch.cat([hcs,style],dim=1)
        icc = torch.cat([hcc,content],dim=1)
        iss = torch.cat([hss,style],dim=1)

        Ics = self.decode(ics)
        Icc = self.decode(icc)
        Iss = self.decode(iss)

        Ics_rgb = self.yuv2rgb(Ics)
        Icc_rgb = self.yuv2rgb(Icc)
        Iss_rgb = self.yuv2rgb(Iss)
        
        return Ics_rgb,Icc_rgb,Iss_rgb
    
class StyTransYuvFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        icc = self.transformer(content, mask , content, pos_c, pos_c)
        iss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(ics)
        Icc = self.decode(icc)
        Iss = self.decode(iss)

        Ics_rgb = self.yuv2rgb(Ics+content_yuv_img)
        Icc_rgb = self.yuv2rgb(Icc+content_yuv_img)
        Iss_rgb = self.yuv2rgb(Iss+style_yuv_img)
        
        return Ics_rgb,Icc_rgb,Iss_rgb,Ics
    
class StyTransYuv(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        icc = self.transformer(content, mask , content, pos_c, pos_c)
        iss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(ics)
        Icc = self.decode(icc)
        Iss = self.decode(iss)

        Ics_rgb = self.yuv2rgb(Ics)
        Icc_rgb = self.yuv2rgb(Icc)
        Iss_rgb = self.yuv2rgb(Iss)
        
        return Ics_rgb,Icc_rgb,Iss_rgb
    
class StyTransRgb(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):
        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        icc = self.transformer(content, mask , content, pos_c, pos_c)
        iss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(ics)
        Icc = self.decode(icc)
        Iss = self.decode(iss)
        
        return Ics,Icc,Iss
    
class StyTransYuvEmbRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        icc = self.transformer(content, mask , content, pos_c, pos_c)
        iss = self.transformer(style, mask , style, pos_s, pos_s)

        Ics = self.decode(ics+content)
        Icc = self.decode(icc+content)
        Iss = self.decode(iss+style)

        Ics_rgb = self.yuv2rgb(Ics)
        Icc_rgb = self.yuv2rgb(Icc)
        Iss_rgb = self.yuv2rgb(Iss)
        
        return Ics_rgb,Icc_rgb,Iss_rgb

class StyTransYuvUpscale(nn.Module):
    def __init__(self,decoder,PatchEmbed, transformer,args) -> None:
        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self,ori_content_img,content_img,style_img):
        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        icc = self.transformer(content, mask , content, pos_c, pos_c)

        Ics = self.decode(ics)
        Icc = self.decode(icc)

        Ics_rgb = self.yuv2rgb(Ics)
        Icc_rgb = self.yuv2rgb(Icc)
     
        Ics_upscaled = self.upscale(x_lr=content_img, y_lr=Ics_rgb,x_hr=ori_content_img)
        Icc_upscaled = self.upscale(x_lr=content_img, y_lr=Icc_rgb,x_hr=ori_content_img)

        return Ics_upscaled,Icc_upscaled

class StyTransYuvInfer(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)
        Ics = self.decode(ics)
        Ics_rgb = self.yuv2rgb(Ics)
        
        return Ics_rgb
    
class StyTransYuvInferFinalRes(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        ics = self.transformer(style, mask , content, pos_c, pos_s)

        Ics = self.decode(ics)
        Ics_rgb = self.yuv2rgb(Ics+content_yuv_img)
        
        return Ics_rgb
    
class StyTransYuvResInfer(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = nn.Sequential(
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(1024, 512, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(512, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 256, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(256, 128, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 128, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(128, 64, (3, 3)),
                nn.ReLU(),
                nn.Upsample(scale_factor=2, mode='nearest'),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 64, (3, 3)),
                nn.ReLU(),
                nn.ReflectionPad2d((1, 1, 1, 1)),
                nn.Conv2d(64, 3, (3, 3)),
            )
        self.embedding = PatchEmbed

        self.rgb2yuv = RgbToYcbcr()
        self.yuv2rgb = YcbcrToRgb()

    def forward(self, content_img, style_img):

        content_yuv_img = self.rgb2yuv(content_img)
        style_yuv_img = self.rgb2yuv(style_img)
        ### Linear projection
        style = self.embedding(style_yuv_img)
        content = self.embedding(content_yuv_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hcs = self.transformer(style, mask , content, pos_c, pos_s)
        ics = torch.cat([hcs,style],dim=1)
        Ics = self.decode(ics)
        Ics_rgb = self.yuv2rgb(Ics)
        
        return Ics_rgb

class StyTransDirectFinalResInfer(nn.Module):
    """ This is the style transform transformer module """
    
    def __init__(self,decoder,PatchEmbed, transformer,args):

        super().__init__()
        self.transformer = transformer
        hidden_dim = transformer.d_model       
        self.decode = decoder
        self.embedding = PatchEmbed

    def forward(self, content_img, style_img):

        ### Linear projection
        style = self.embedding(style_img)
        content = self.embedding(content_img)
        
        # postional embedding is calculated in transformer.py
        pos_s = None
        pos_c = None

        mask = None
        hs = self.transformer(style, mask , content, pos_c, pos_s)   
        Ics = self.decode(hs) + content_img

        return Ics


