pip install -r example/requirements.txt
python setup.py install
mkdir -p example/media/static/ example/media/uploads/ example/static/ example/db/ example/logs/
python example/example/manage.py collectstatic --noinput
python example/example/manage.py syncdb --noinput
python example/example/manage.py migrate --noinput