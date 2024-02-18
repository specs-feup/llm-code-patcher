conda create --name torchcuda python=3.9 pip

conda activate torchcuda

conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia

pip install -r requirements.txt