# Cloudacious IaC
Cloudacious's object-oriented IaC tooling. Call our classes all day long!

## Installation
Super easy to use! Just run:
```
python -m pip install cloudacious
```

## Usage
See the readmes for each category under the `src/` directory, for example `iac/`, which can be found at `src/cloudacious/iac`.

### Contents
#### IaC with Pulumi
* `ContainerImages`: Build a container image and upload it to a docker registry. 

See [readme](src/cloudacious/iac/README.md) for more.

## Support
Join our [Discord](https://discord.gg/d7YccKnenh)! We're happy to help. Likewise, join the tech learning group we sponsor, [Lost Newbs](https://lnkd.in/gFG5BJnj) if you're looking to hone your skills or would like to give back :D

## Roadmap


## Contributing
Have at it!

## Authors and acknowledgment


## License


## Project status
Under active development! It's our tooling and we use it, too :b

## Building
Building and pushing to PyPi

It's all in CI, baby!

Steps:

1. Changes are merged into main

2. Tag it and push it

You must use the CLI, for whatever reason creating the tag in the console (gitlab.com) doesn't work (ᗒᗣᗕ)
```
git tag -a "v0.0.2" -m "version 0.0.2"
git push origin v0.0.2
```
3. Manually run pipeline (for prod) 

4. If pipeline fails, delete tag:
```
git tag -d v0.0.2
```
and troubleshoot pipeline failure.
