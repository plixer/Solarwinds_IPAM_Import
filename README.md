# Solarwinds IPAM Integration

Quick and dirty REST API integration to import Solarwinds IPAM into Scrutinizer's IPGroups

## Getting Started

The binary compiled under /dist is made to run on any Scrutinizer appliance without the need to install any dependencies
I'm sure there are some bugs/errors that I overlooked so feel free to open issues on anything you find.

### Prerequisites

Most of the modules used should be installed with python3 and be installed on the server but a full list is below:

[requests](https://github.com/requests/requests)
[orionsdk](https://github.com/solarwinds/OrionSDK)
[os](https://docs.python.org/2/library/os.html)
[configparser](https://docs.python.org/2/library/configparser.html)
[getpass](https://docs.python.org/2/library/getpass.html)

## Deployment

Download the compiled binary from /dist onto your server and execute, a prompt for login information will be given and the script should run from there.

## Authors

* **Jake Bergeron (Plixer)** - *Initial work* - [Bergertron](https://github.com/Bergertron)
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


