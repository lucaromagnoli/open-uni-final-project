import logging

import numpy as np
import requests
import tensorflow as tf
import tensorflow_hub as hub
from annoy import AnnoyIndex

logger = logging.getLogger(__name__)

module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
module = hub.load(module_handle)


def get_features_from_image_url(img):
    """Calculate features vector given an img URL"""
    logger.info(f'Getting feature vectors for image')
    img = tf.io.decode_jpeg(img, channels=3)
    img = tf.image.resize_with_pad(img, 224, 224)
    img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    features = module(img)
    return np.squeeze(features)


def create_annoy_index(vectors, dims=1792, trees=10000):
    logger.info('Creating Annoy Index')
    a = AnnoyIndex(dims, metric='angular')
    for pk, vector in vectors:
        a.add_item(pk, vector)
    a.build(trees)
    return a


def get_similar_products(image_content, vectors):
    """
    Get most similar products to image url
    :param image_content: the binary content of the image
    :param vectors: a list where the items are two-tuples of product.pk and product.image_vector
    :return:
    """
    features_vector = get_features_from_image_url(image_url)
    annoy_index = create_annoy_index(vectors)
    neighbours = annoy_index.get_nns_by_vector(features_vector, 20, include_distances=True)
    logger.info(neighbours)
    return neighbours[0]
