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

1) SSH into Scrutinizer
2) Run the following commands:
  ...a) wget https://github.com/plixer/Solarwinds_IPAM_Import/raw/master/dist/solarwinds_ipam_import.run
  ...b) chmod 755 solarwinds_ipam_import.run
  ...c) ./solarwinds_ipam_import.run
3) Input the NPM Server IP and Username/Password
4) From here you should see the groups get imported into Scrutinizer.
5) To reset the configuration you can remove the INI file (.Solarwinds.ini) from the directory where the binary ran and re-run.

## Authors

* **Jake Bergeron (Plixer)** - *Initial work*
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


