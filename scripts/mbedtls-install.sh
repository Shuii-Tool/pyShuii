#!/bin/sh -e

#https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/v2.28.1.tar.gz
VERSION="2.28.1"
archive="v${VERSION}.tar.gz"
URL="https://github.com/Mbed-TLS/mbedtls/archive/refs/tags/${archive}"
pkgname="mbedtls-${VERSION}"

command -v wget || { echo "no wget :(" 1>&2; exit 1; }

if [ ! -f "$archive" -a ! -f "$pkgname" ]; then
    echo "downloading from ${URL}"
    wget "$URL"
fi

tar -xzf "$archive"
cd "$pkgname"
#make SHARED=1 CFLAGS=-fPIC
make DESTDIR=/usr install