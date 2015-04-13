#!/usr/bin/env bash

SAMPLES=(
    "re"
    "collections"
    "multiprocessing"
    "simplejson"
    "sqlalchemy"
)

virtualenv vvv
source vvv/bin/activate

cd ..

python setup.py install
pip install simplejson
pip install sqlalchemy

cd -

for i in ${SAMPLES[@]}
do
    profimp --html "import ${i}" > ${i}.html
done

deactivate
rm -rf vvv
