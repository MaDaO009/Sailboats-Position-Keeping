import numpy as np

import pylab as pl

from pykalman import KalmanFilter

import random

# specify parameters

random_state = np.random.RandomState(0)

transition_matrix = [[1, 0.1], [0, 1]]

transition_offset = [-0.1, 0.1]

observation_matrix = np.eye(2) + random_state.randn(2, 2) * 0.1

observation_offset = [1.0, -1.0]

transition_covariance = np.eye(2)

observation_covariance = np.eye(2) + random_state.randn(2, 2) * 0.1

initial_state_mean = [5, -5]

initial_state_covariance = [[1, 0.1], [-0.1, 1]]



# sample from model

kf = KalmanFilter(

    transition_matrix, observation_matrix, transition_covariance,

    observation_covariance, transition_offset, observation_offset,

    initial_state_mean, initial_state_covariance,

    random_state=random_state

)

states, observations = kf.sample(

    n_timesteps=50,

    initial_state=initial_state_mean

)
# print(observations[0])
observations=np.array([[0,0]])
for i in range(0,50):
    # observations=np.delete(observations,0,0)
    a=i+random.random()
    
    observations=np.append(observations,[[i+random.random(),i+random.random()+5]],axis=0)
observations=np.delete(observations,0,axis=0)
    # print(observations[0])
    # # print(observations)
    # # observations[0].append(i+random.random())
    # # observations[1].append(i+random.random()+10)
    # observations[1]=np.append(observations[1],[i+random.random()+15],0)
print(observations,'!!!!')
# estimate state with filtering and smoothing

filtered_state_estimates = kf.filter(observations)[0]

smoothed_state_estimates = kf.smooth(observations)[0]
print(smoothed_state_estimates[49])
# print(observations)
# print(states)
# print('!!!!!!!!!!!!!!!!!!!!!!')
# print(smoothed_state_estimates)


# draw estimates

pl.figure()

lines_true = pl.plot(states, color='b')

lines_filt = pl.plot(filtered_state_estimates, color='r')

lines_smooth = pl.plot(smoothed_state_estimates, color='g')

pl.legend((lines_true[0], lines_filt[0], lines_smooth[0]),

          ('true', 'filt', 'smooth'),

          loc='lower right'

)

pl.show()