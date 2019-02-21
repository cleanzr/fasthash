# Setup script
# Assumes presence of Anaconda

# Create an environment
conda create --name LSH python=2.7
source activate LSH

# Install packages from Anaconda
conda install numpy
conda install scipy

# Install packages using pip
pip install --pre subprocess32
pip install ngram
pip install sklearn
pip install matlib

# this fails due to dependency failure: matlib.h