# PyGolomb

![PyPI - Version](https://img.shields.io/pypi/v/pygolomb)
![GitHub License](https://img.shields.io/github/license/alxwnth/pygolomb)
![GitHub Release](https://img.shields.io/github/v/release/alxwnth/pygolomb)

> A small Python library to test binary sequences with Golomb's randomness postulates.

## Installation

Python >=3.10 is required.

```
pip install pygolomb
```

## Developing

Create venv and install dependencies.

```
python3 -m venv .venv
. .venv/bin/activate
poetry install
```

## Testing

```
. .venv/bin/activate
pytest
```

To check test coverage:

```
pytest --cov=pygolomb tests/
```

## Roadmap

The overall code quality is largely at the same level it was back in 2018. This is to be improved in the future.

## GUI application

There are no plans to have a new GUI at the moment. The old Tkinter application remains in `gui` directory only for historic purposes.

## Contributing

Contributions are welcome. Please fork the project and use feature a feature branch. For bugs and suggestions, please open an issue.

## License

The project is licensed under the GNU Lesser General Public License. See [COPYING](/COPYING) for full terms.

## Acknowledgements

1. Menezes, A.J., Van Oorschot, P.C. and Vanstone, S.A. (2018) Handbook of Applied Cryptography. 1st edn. CRC Press. Available at: https://doi.org/10.1201/9780429466335.
2. Pinaki, M. (no date) ‘Golomb’s Randomness Postulates’. Available at: https://www.iitg.ac.in/pinaki/Golomb.pdf (Accessed: 8 May 2024).
