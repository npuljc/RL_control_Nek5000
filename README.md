# Reinforcement-learning-based flow control in the Nek5000 environment

This repo is to showcase how to apply reinforcement learning (RL) based control in the CFD environment of [Nek5000](https://nek5000.mcs.anl.gov/).
Using RL implemented in [TensorForce](https://github.com/tensorforce/tensorforce), this repo is developed by referring to the open-source RL-based flow control repo of [Rabault et al](https://github.com/jerabaul29/Cylinder2DFlowControlDRL).
So, they have almost the same structure. If you're familiar with Rabault's repo, it will be very easy for you to run the test case here.

The main differences are the simulation environment and reward functions:
- Nek5000 is used to simulate the confined cylinder wake flow.
- Reward function is defined by evaluating the shedding energy related to the SFD base flow.
- Stability-enhanced reward is presented by penalizing the original reward using the DMD eigenvalue.

## Installation

- python3 and pip3: `sudo apt install python3-pip`
- tensorflow: `pip3 install tensorflow==1.13.1`
- tensorforce: `pip3 install tensorforce==0.4.2`
- Nek5000: see the description [here](https://nek5000.github.io/NekDoc/quickstart.html)

## How to run

- Complie the CFD code in folder _flowcontrol/cylinder_: `makenek cylinder`
- Train the control policy in folder _flowcontrol_: `python3 perform_learning.py`
- Test the control performance in folder _flowcontrol_: `python3 single_runner.py`
- If you want to compute the SFD base flow by yourself, go to folder _SFDbase_ and run: 1. `makenek cylinder` 2. `nekmpi cylinder 5`

## Vortex shedding suppression performance

CFD solver: `Nek5000`
Reynolds number: `150`

The following is the comparison of two flows (the top is baseline and the bottom is controlled flow).
<p align="center">
  <img src="./figures/baseline.gif">
  <img src="./figures/control.gif">
</p>




