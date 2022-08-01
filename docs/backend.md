# backend
## setup

Initial require packages
* Python 3.6+
* virtualenv

Create virtual environment
```bash
virtualenv -p python3.6 .venv
``` 

Build project
```bash
.venv/bin/python setup.py develop
```

## generate migration
```bash
 .venv/bin/alembic -c config.ini revision --autogenerate -m *migration_name* 
```