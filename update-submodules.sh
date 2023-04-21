#! /usr/bin/bash

if [ $# -eq 0 ]; then
    >&2 echo "Usage: ./update-submodules.sh R-<version>.tar.gz"
    exit 1
fi

TAR=$1
DIR=$(tar tf $TAR | cut -d"/" -f1 | uniq)
SPEC=$PWD/R.spec

tar -xf $TAR
pushd $DIR/src/library/Recommended
for PKG in *.tar.gz; do
    PKG="${PKG%.tar.gz}"
    PKG_NAME="${PKG%_*}"
    PKG_VERS="${PKG#*_}"
    sed -i "s/submodule  $PKG_NAME.*/submodule  $PKG_NAME $PKG_VERS/" $SPEC
    sed -i "s/R-$PKG_NAME-devel = .*/R-$PKG_NAME-devel = ${PKG_VERS//-/.}/" $SPEC
done
popd
rm -rf $DIR
