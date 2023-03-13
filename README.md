## Prerequisites
1. Update `alembic.ini` file line 58, database/config.py
```ini
sqlalchemy.url = mysql+mysqlconnector://root:pass@127.0.0.1:3306/mysqldb
```
2. Run alembic upgrade command.
```bash
alembic upgrade heads
```
3. Install requirements.
```bash
pip3 install -r requirements.txt
```
4. Populate database tables.
```bash
python3 database/populate_tables.py
```

## Start Flask Application
The application will run at `127.0.0.1:5000`.

## Run pytest Tests
1. Run tests.
```bash
python -m coverage run -m pytest
```
2. Run coverage report.
```bash
coverage report 
```