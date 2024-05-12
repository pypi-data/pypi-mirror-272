# Cloudacious IaC

We're working on both another repo for Pulumi Automation API and getting documentation auto-generated with pydocs.

In the meantime, to use the IaC in here, check in the `.py` file for specifications on what each class requires to instantiate. 

Since there's only one file, here's a little more:

## ContainerImages
```
from cloudacious.iac.ContainerImages import Image

image = Image(
    ...
)
```
Fill in the ... with everything in the docstrings in `ContainerImages.py` and you should be good to go! Be sure to hit us up with any questions or for help, links to the discord in the repo root :D
