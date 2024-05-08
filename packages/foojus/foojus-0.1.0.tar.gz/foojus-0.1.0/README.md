# foojus

A test package for num2text

## Installation

```bash
$ pip install foojus
```

## Usage

`foojus` is a test package for num2text. It is a simple package that converts numbers to text for french language.

```python
from foojus import Num2Words

num2words = Num2Words(lang='FR')

print(num2words.convert(1))  # un
print(num2words.convert(17))  # dix-sept
print(num2words.convert(80))  # quatre-vingts
print(num2words.convert(1234))  # mille-deux-cent-trente-quatre
print(num2words.convert(300))

num2words = Num2Words(lang='BE')
print(num2words.convert(1))
print(num2words.convert(17))
print(num2words.convert(80)) # huitante
print(num2words.convert(1234))
print(num2words.convert(300))
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`foojus` was created by oceanumeric. It is licensed under the terms of the MIT license.

## Credits

`foojus` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
