#!/bin/sh

cd $(dirname $0)

version=$(python -c 'import yassh; print yassh.__version__')

rm dist/*
python setup.py sdist bdist_wheel

while true; do
    read -p "Do you wish to upload ${version} to pypi.python.org?" yn
    case $yn in
        [Yy]*)
            twine upload dist/*
            break
            ;;
        [Nn]*)
            break
            ;;
        *)
            echo "Please answer yes or no."
            ;;
    esac
done

