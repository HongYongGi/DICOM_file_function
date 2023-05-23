"""
Log 

* Written by HongYongGi / email: hyg4438@gmail.com

* Written date : 20230523


# Evaluation code

* Evaluate the performance of the model

"""

import os, glob, shutil
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nibabel as nib
import pydicom
from pydicom import read_file
from tqdm import tqdm
import ipywidgets as widgets
from datetime import date
import skimage



def confusion_matrix(label, predict, cm_flag = False):
    """
    Calculate confusion matrix

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        ndarray: Confusion matrix
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    if cm_flag:
        return tp, fp, fn, tn
    else:
        dice = 2 * tp / (2 * tp + fp + fn)
        sensitivity = tp / (tp + fn)
        precision = tp / (tp + fp)    
        recall = tp / (tp + fn)
        f1_score = 2 * (precision * recall) / (precision + recall)
        fpr = fp / (fp + tn) # False Positive Rate
        return dice, sensitivity, precision, recall, f1_score, fpr
    

def dice(label, predict):
    """calculate dice

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        dice: dice score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    dice = 2 * tp / (2 * tp + fp + fn)
    return dice

def sensitivity(label, predict):
    """calculate sensitivity

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        sensitivity: sensitivity score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    sensitivity = tp / (tp + fn)
    return sensitivity

def precision(label, predict):
    """calculate precision

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        precision: precision score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    precision = tp / (tp + fp)
    return precision


def recall(label, predict):
    """calculate recall

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        recall: recall score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    recall = tp / (tp + fn)
    return recall



def f1_score(label, predict):
    """calculate f1_score

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        f1_score: f1_score score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score


def fpr(label, predict):
    """calculate fpr

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        fpr: fpr score
    """
    predict_eq_0 = predict == 0
    predict_eq_1 = predict == 1
    target_eq_0 = label == 0
    target_eq_1 = label == 1
    tp = np.sum(np.logical_and(predict_eq_1, target_eq_1))
    fp = np.sum(np.logical_and(predict_eq_1, target_eq_0))
    fn = np.sum(np.logical_and(predict_eq_0, target_eq_1))
    tn = np.sum(np.logical_and(predict_eq_0, target_eq_0))
    fpr = fp / (fp + tn)
    return fpr



def ssim (label, predict):
    """calculate ssim

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        ssim: ssim score
    """
    ssim = skimage.measure.compare_ssim(label, predict, data_range=1.0, multichannel=True)
    return ssim

def psnr(label, predict):
    """calculate psnr

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        psnr: psnr score
    """
    psnr = skimage.measure.compare_psnr(label, predict, data_range=1.0)
    return psnr


def mae(label, predict):
    """calculate mae

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        mae: mae score
    """
    mae = np.mean(np.abs(label - predict))
    return mae


def mse(label, predict):
    """calculate mse

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        mse: mse score
    """
    mse = np.mean((label - predict) ** 2)
    return mse

def rmse(label, predict):
    """calculate rmse

    Args:
        label (ndarray): Label numpy array
        predict (ndarray): prediction numpy array
        
    Returns:
        rmse: rmse score
    """
    rmse = np.sqrt(np.mean((label - predict) ** 2))
    return rmse



