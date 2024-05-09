PourPy
=============
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/cmbm-ethz%2Fpourbaix-diagrams/main?labpath=.%2Fexamples%2Fnotebooks%2Firon.ipynb)
	
A Python-based library to generate Pourbaix diagrams (potential/pH
diagram). **PourPy** is an open-source python package,
capable of generating thermodynamic stability diagrams of solid phases
and complexes in aqueous electrolytes. These so-called Pourbaix
diagrams provide valuable information about the reactivity of chemical
elements and compounds as a function of the electrochemical potential
and the pH.

**PourPy** is intended as a tool, enabling users to inspect
the reactivity of aqueous systems under full control of all chemical
species considered. Users can define custom reactive systems
containing elements, solid, aqueous and gaseous species thereof and
build all (electro)chemical reactions to be displayed.

Dependencies
===============
Here is the list of dependencies:
- argparse
- shapely (https://shapely.readthedocs.io/en/stable/)
- bokeh (for using bokeh as plotting backend)
- matplotlib (for using matplotlib as plotting backend)
- python (<= 3.10) and pip to install the Python package

Optional : For generationg documentation
- nbsphinx
- sphinx-autoapi
- sphinx_rtd_theme


Installation
===============
Install the latest release from the Package repository:
```
pip install PourPy
```

Documentation
=================
The latest documentation is available on
[readthedocs](https://readthedocs.org/). Please refer to the
documentation on how to use the PourPy package:
[pourbaix-diagrams.rtfd.io](https://pourbaix-diagrams.readthedocs.io/en/latest/)

Webapp
======
PourPy is also available as a webapp with all the functionalities [PourPy Weabpp](https://pourpy-webapp.runmercury.com/app/pourpy-mercury)


Examples
==========
For live and interacting examples mentioned in the documentation, please check the following link:
[Interactive examples](https://mybinder.org/v2/gl/cmbm-ethz%2Fpourbaix-diagrams/a20c113396cf23bf1b642c8ccdacc74124a3db5f?urlpath=lab%2Ftree%2Fexamples%2Fnotebooks%2Firon.ipynb)

Contributing
============
Contributions to PourPy are welcome! Please follow the guidelines below.

Report an issue
If you have an account on [gitlab](https://gitlab.com/), you can submit an issue.

Submit a patch / merge-request
Follow this [guide](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html#new-merge-request-from-a-fork) to create a merge request on GitLab. Please target the repository's `main` branch.

License
=========
PourPy is distributed under the terms of [GNU LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.en.html)

