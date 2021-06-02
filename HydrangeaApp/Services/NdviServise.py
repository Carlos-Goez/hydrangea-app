import numpy as np
import imageio


class IndexFlower:

    @staticmethod
    def get_ndvi(image1, image2, order, number_flower):
        """
        A function that takes an RGB image and a NIR image. Calculates NDVI
        Based on NIR being the average of the three channels in the NIR image
        """
        # Read in data
        im1 = imageio.imread(image1)
        im2 = imageio.imread(image2)

        folder_images = '/home/agoez/Pictures/'
        out_file_ndvi = folder_images + order + '-' + \
                             'ndvi' + '-' + number_flower + '.png'
        out_file_gci = folder_images + order + '-' + \
                        'gci' + '-' + number_flower + '.png'

        dict_index = {'NDVI': 0, 'GCI': 0}

        ndvi_im = np.full((im1.shape[0], im1.shape[1]), 0.)
        ndvi_im_gci = np.full((im1.shape[0], im1.shape[1]), 0.)

        # rescale each pixel by NDVI value
        for x in range(im1.shape[0]):
            for y in range(im1.shape[1]):
                NIR_val = sum(im2[x, y, :]) / 3
                # NIR_val = im2[x,y,0] for when have single NIR channel
                if (int(NIR_val) + int(im1[x, y, 0])) == 0:
                    ndvi_im[x, y] = 0
                else:
                    ndvi_im[x, y] = (int(NIR_val) - int(im1[x, y, 0])) / (int(im1[x, y, 0]) + int(NIR_val))
        # Save out result
        imageio.imwrite(out_file_ndvi, ndvi_im)

        return dict_index


