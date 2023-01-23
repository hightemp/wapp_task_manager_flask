FROM cdrx/pyinstaller-linux:python3

RUN pip install --upgrade setuptools
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN pip install --ignore-installed apscheduler

