# juskata

A demo package for converting numbers to french words.

## Installation

```bash
$ pip install juskata
```

## Usage

`juskata` provides a class `Num2Words` that can be used to convert numbers to words. The class takes a single argument `lang` which specifies the language style to use - either "FR" for French or "BE" for Belgium-style French.

Right now, only integer numbers within the range `0-999 999` are supported.

There are two methods available in the class:

- `convert_num(num: int) -> str`: Converts a number to words.
- `convert_num_list(num_list: List[int]) -> List[str]`: Converts a list of numbers to a list of words.

```python
from juskata import Num2Words

# initialize the class
n2w_fr = Num2Words(lang="FR")

# convert a number to words
print(n2w_fr.convert_num(17))  # dix-sept
print(n2w_fr.convert_num(80))  # quatre-vingts
print(n2w_fr.convert_num(180000))  # cent-quatre-vingt-milles

# convert a list of numbers to words
n2w_fr.convert_num_list([17, 80, 180000])  # ['dix-sept', 'quatre-vingts' 'cent-quatre-vingt-milles']


# initialize the class for Belgium-style French
n2w_be = Num2Words(lang="BE")

# convert a number to words
print(n2w_be.convert_num(17))  # dix-sept
print(n2w_be.convert_num(80))  # quatre-vingts
print(n2w_be.convert_num(180000))  # cent-quatre-vingt-milles
```


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`juskata` was created by [oceanumeric](https://github.com/oceanumeric). It is licensed under the terms of the MIT license.

## Credits

`juskata` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` project template.

During the development of this package, I found the following resources helpful:

- [Ruby Implementation by GaspardPO](https://github.com/GaspardPO/kata-number-to-french-converter)
- [Rust Implementation by Ballasi](https://github.com/Ballasi/num2words/blob/master/src/lang/fr.rs)
- [Python Implementation by savoirfairelinux](https://github.com/savoirfairelinux/num2words/blob/5e6fa94866eef0ea5b5df6843699c64379d02c81/num2words/lang_FR.py)

Almost all the code mentioned above used recursion to certain extent. However, I found
my implementation to be more readable and easier to understand. The above implementations
also have bugs in the conversion of numbers to words.


## Acknowledgements

Since I am not native French speaker, I had to rely on the internet to understand the French number system. I found the following resources helpful:

- [Conversion d'un chiffre en toutes lettres](https://www.heartandcoeur.com/convert/convert_chiffre_lettre.php)
    - I used this website to verify the conversion of numbers to words and generate text for doing unit tests.
- `Github Copilot` was used to generate some of the code snippets in the implementation
    - `Copilot` was not very helpful for giving the correct implementation of the conversion of numbers to words.
    - However, it was helpful in generating the boilerplate code for the package, such as unit tests, and writing the README.md file.
