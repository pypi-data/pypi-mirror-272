# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alphafold3']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'openfold', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'alphafold3',
    'version': '0.0.2',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# AlphaFold3\nImplementation of Alpha Fold 3 from the paper: "Accurate structure prediction of biomolecular interactions with AlphaFold3" in PyTorch\n\n\n## install\n`$pip install alphafold3`\n\n## Input Tensor Size Example\n\n```python\nimport torch\n\n# Define the batch size, number of nodes, and number of features\nbatch_size = 1\nnum_nodes = 5\nnum_features = 64\n\n# Generate random pair representations using torch.randn\n# Shape: (batch_size, num_nodes, num_nodes, num_features)\npair_representations = torch.randn(\n    batch_size, num_nodes, num_nodes, num_features\n)\n\n# Generate random single representations using torch.randn\n# Shape: (batch_size, num_nodes, num_features)\nsingle_representations = torch.randn(\n    batch_size, num_nodes, num_features\n)\n```\n\n## Genetic Diffusion\nNeed review but basically it operates on atomic coordinates.\n\n```python\nimport torch\nfrom alphafold3.diffusion import GeneticDiffusionModuleBlock\n\n# Create an instance of the GeneticDiffusionModuleBlock\nmodel = GeneticDiffusionModuleBlock(channels=3, training=True)\n\n# Generate random input coordinates\ninput_coords = torch.randn(10, 100, 100, 3)\n\n# Generate random ground truth coordinates\nground_truth = torch.randn(10, 100, 100, 3)\n\n# Pass the input coordinates and ground truth coordinates through the model\noutput_coords, loss = model(input_coords, ground_truth)\n\n# Print the output coordinates\nprint(output_coords)\n\n# Print the loss value\nprint(loss)\n```\n\n## Full Model Example Forward pass\n\n```python\nimport torch \nfrom alphafold3 import AlphaFold3\n\n# Create random tensors\nx = torch.randn(1, 5, 5, 64)  # Shape: (batch_size, seq_len, seq_len, dim)\ny = torch.randn(1, 5, 64)  # Shape: (batch_size, seq_len, dim)\n\n# Initialize AlphaFold3 model\nmodel = AlphaFold3(\n    dim=64,\n    seq_len=5,\n    heads=8,\n    dim_head=64,\n    attn_dropout=0.0,\n    ff_dropout=0.0,\n    global_column_attn=False,\n    pair_former_depth=48,\n    num_diffusion_steps=1000,\n    diffusion_depth=30,\n)\n\n# Forward pass through the model\noutput = model(x, y)\n\n# Print the shape of the output tensor\nprint(output.shape)\n```\n\n\n# Citation\n```bibtex\n@article{Abramson2024-fj,\n  title    = "Accurate structure prediction of biomolecular interactions with\n              {AlphaFold} 3",\n  author   = "Abramson, Josh and Adler, Jonas and Dunger, Jack and Evans,\n              Richard and Green, Tim and Pritzel, Alexander and Ronneberger,\n              Olaf and Willmore, Lindsay and Ballard, Andrew J and Bambrick,\n              Joshua and Bodenstein, Sebastian W and Evans, David A and Hung,\n              Chia-Chun and O\'Neill, Michael and Reiman, David and\n              Tunyasuvunakool, Kathryn and Wu, Zachary and {\\v Z}emgulyt{\\.e},\n              Akvil{\\.e} and Arvaniti, Eirini and Beattie, Charles and\n              Bertolli, Ottavia and Bridgland, Alex and Cherepanov, Alexey and\n              Congreve, Miles and Cowen-Rivers, Alexander I and Cowie, Andrew\n              and Figurnov, Michael and Fuchs, Fabian B and Gladman, Hannah and\n              Jain, Rishub and Khan, Yousuf A and Low, Caroline M R and Perlin,\n              Kuba and Potapenko, Anna and Savy, Pascal and Singh, Sukhdeep and\n              Stecula, Adrian and Thillaisundaram, Ashok and Tong, Catherine\n              and Yakneen, Sergei and Zhong, Ellen D and Zielinski, Michal and\n              {\\v Z}{\\\'\\i}dek, Augustin and Bapst, Victor and Kohli, Pushmeet\n              and Jaderberg, Max and Hassabis, Demis and Jumper, John M",\n  journal  = "Nature",\n  month    =  may,\n  year     =  2024\n}\n```\n\n\n\nsequences, ligands, ,covalent bonds -> input embedder [3] -> \n\n\n# Todo\n\n- [ ] Implement Figure A, implement triangle update, transition, \n- [ ] Impelment Figure B, per token, cond, \n- [ ] Implement Figure C: Network Chunk,\n- [ ] Implement confidence module\n- [ ] Implement Template Module\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AlphaFold3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
