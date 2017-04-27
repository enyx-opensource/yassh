#!/bin/sh

set -e

cd $(dirname $0)

virtualenv env && source env/bin/activate
pip install -r requirements.txt

python setup.py check --restructuredtext --metadata --strict
behave

rm -rf dist/*
python setup.py sdist bdist_wheel

version=$(python -c 'import yassh; print yassh.__version__')

while true; do
    read -p "Do you wish to upload ${version} to pypi.python.org [Yn] ?" yn
    yn=${yn:-y}
    case $yn in
        [Yy])
            twine upload dist/*
            git tag v${version}
            git push origin v${version}
            break
            ;;
        [Nn])
            break
            ;;
        *)
            echo "Please answer yes or no."
            ;;
    esac
done

