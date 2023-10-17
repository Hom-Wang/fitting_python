import numpy as np
import matplotlib.pyplot as plt

def spherical_coordinate(n_theta: int, n_phi: int) -> tuple:
    # theta: 0 ~ 2*pi, phi: 0 ~ pi
    theta, phi = np.mgrid[0:2*np.pi:complex(0, n_theta), 0:np.pi:complex(0, n_phi)]

    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)

    return (x, y, z)

def fibonacci_lattices(n: int) -> tuple:
    '''
    Evenly distributing n points on a sphere
    https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
    '''

    indices = np.arange(0, n, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / n)
    theta = np.pi * (1 + 5**0.5) * indices
    x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)

    return (x, y, z)

def get_sphere(n: int, method: str='fibonacci') -> np.array:
    '''
    Input
        - n: number of sphere points
        - method: 'fibonacci', 'spherical'
    '''

    p = ([], [], [])

    method = method.lower()

    if method == 'spherical':
        n_phi = int(np.round(np.sqrt(n / 1.5)))
        n_theta = int(np.round(n / n_phi))
        p = spherical_coordinate(n_theta, n_phi)

    elif method == 'fibonacci':
        p = fibonacci_lattices(n)

    return np.array(p)
