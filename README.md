# NTNU Database 2022 Final Project

## Install dependencies

- Node.js  
It's recommended to manage node.js versions with [nvm](https://github.com/nvm-sh/nvm). One of its advantages is you don't need to prepend `sudo` in order to install package globally.

```sh
# nvm install script
$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
# Verify that nvm has been installed
$ command -v nvm
# Install the specified version
$ nvm install 16.15.1
# Use the installed version
$ nvm use node
```
- [yarn](https://yarnpkg.com/getting-started/install)

```sh
$ corepack enable
$ yarn set version stable
```


- [pipenv](https://github.com/pypa/pipenv)

```sh
$ sudo apt install pipenv
$ pipenv install            # Install all dependencies from Pipfile
```

If you have installed `pip` before, you may encounter problems creating a virtual environment for Python. Try `pip uninstall pip` to uninstall the duplicate.

## Developing

- Activate the virtual environment

```sh
$ pipenv shell
```

Launch development server
```sh
$ flask run
```

## Notice

Try to follow [Conventional Commits](https://www.conventionalcommits.org/) when writing commit messages. Meaningless commit messages may be rejected.