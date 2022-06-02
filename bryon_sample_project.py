# -*- coding: utf-8 -*-
"""bryon_sample_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wrMpOrRuk5TD7-jwEOXWMPVqmTzASk4L
"""
import fire
import numpy as np
from numpy.random import default_rng
import random
from decimal import *

def sphere(vec):
  return sum(i**2 for i in vec)

def sphere_batch(batch):
  return np.array([sphere(i) for i in batch])

def rastrigin(vec, A=10):
  sum = A*vec.size
  for i in vec:
    sum += i**2 - A*np.cos(2*np.pi*i)
  return sum

def rastrigin_batch(batch):
  return np.array([rastrigin(i) for i in batch])


class Content:
  def __init__(self, num_dim):
    self.X = np.full(num_dim, fill_value=np.nan)
    self.P = np.nan

class Map:
  def __init__(self, num_dim, gran=0.1):
    self.gran = gran
    self.empty_x = np.full(num_dim, fill_value=np.nan)
    '''
    the main map object- the first value in the list at each cell is the solution
    and the second value is its performance. I initialized them to nan to distinguish
    empty cells from valid solutions.
    '''
    self.dims = int(2.0/gran)
    self.map = np.empty(shape=(self.dims, self.dims), dtype=object)
    self.map[:] = Content(num_dim)
    # self.map = np.full(shape=(dims, dims), fill_value=[self.empty_x, np.nan],dtype=object)

  #map from a float in the range [-1, 1] to an integer in the range [0, self.dims - 1]
  def indices(self, b):
    x, y = np.digitize(list(b),bins=[self.gran*i for i in range(1, self.dims)])
    print((x, y))
    return (x, y)

  def get(self, b):
    x, y = self.indices(b)
    cell = self.map[x][y]
    X = cell.X
    P = cell.P
    return (self.map[x][y].X, self.map[x][y].P)

  def set(self, b, X, P):
    x, y = self.indices(b)
    self.map[x][y].X = X
    self.map[x][y].P = P

  def get_P(self, b):
    X, P = self.get(b)
    return P

  def is_empty(self, b):
    X, P = self.get(b)
    return np.isnan(P)

  # uniformly selects from the archive indices
  def random_selection(self):
    x, y -

def generate_random(num_dim):
  rng = default_rng()
  return rng.standard_normal(num_dim)

def generate_variation(x, sigma=0.15):
  x += random.gauss(0, sigma)
  for i in range(x.size):
    if x[i] < -1:
      x[i] = -1
    elif x[i] > 1:
      x[i] = 1
  return x

def performance(x):
  return -1*sphere(x)

def map_elites(num_dim=10, num_iter=100, num_rand=20, gran=0.1, sigma=0.15):

  archive = Map(num_dim, gran)
  for i in range(num_iter):
    if i < num_rand:
      x_p = generate_random(num_dim)
    else:
      x = archive.random_selection()
      x_p = generate_variation(x, sigma)
    b = (x_p[0], x_p[1])
    p = performance(x_p)
    if archive.is_empty(b) or archive.get_P(b) < p:
      archive.set(b, x_p, p)
  return archive


if __name__ == '__main__':
  
  rng = default_rng()
  vals = rng.standard_normal(size=(10, 2))
  print(vals)

  fire.Fire(rastrigin_batch(vals))
  fire.Fire(sphere_batch(vals))
  map_elites()