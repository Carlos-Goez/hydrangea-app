def get_ndvi(image1, image2, out_file):
    """
    A function that takes an RGB image and a NIR image. Calculates NDVI
    Based on NIR being the average of the three channels in the NIR image
    """
    import numpy as np
    import imageio

    # Read in data
    im1 = imageio.imread(image1)
    im2 = imageio.imread(image2)

    ndvi_im = np.full((im1.shape[0], im1.shape[1]), 0.)

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
    imageio.imwrite(out_file, ndvi_im)


get_ndvi('noir.png', 'rgb.png', 'ndvi.png')
