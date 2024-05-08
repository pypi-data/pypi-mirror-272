#!/bin/bash
#
# This script should be called by `cibuildwheel` in the `before-all` stage.

nproc=$(python -c 'import multiprocessing as mp; print(mp.cpu_count())')


function install_packages
{
  /bin/echo -e "\n==> Installing packages using the package manager ...\n"
  yum install -y \
    gsl-devel \
    wget
}


function download_and_build_fftw
{
  /bin/echo -e "\n==> Downloading and unpacking FFTW ${FFTW_VERSION} ...\n"
  site="https://fftw.org"
  directory="pub/fftw"
  file="fftw-${FFTW_VERSION}.tar.gz"
  url="${site}/${directory}/${file}"
  curl -fsSLo - "${url}" | tar -C "${WORKDIR}" -xzf -

  /bin/echo -e "\n==> Building and installing FFTW ${FFTW_VERSION} ...\n"
  cd "${WORKDIR}/fftw-${FFTW_VERSION}"
  ./configure \
    --quiet \
    --prefix /usr/local \
    --enable-threads \
    --enable-shared \
    --enable-float
  make --jobs="${nproc}" --quiet install
}


function download_and_build_hdf5
{
  /bin/echo -e "\n==> Downloading and unpacking HDF5 ${HDF5_VERSION} ...\n"
  site="https://www.hdfgroup.org"
  directory="ftp/HDF5/releases/hdf5-${HDF5_VERSION%.*}/hdf5-${HDF5_VERSION}/src"
  file="hdf5-${HDF5_VERSION}.tar.gz"
  url="${site}/${directory}/${file}"
  curl -fsSLo - "${url}" | tar -C "${WORKDIR}" -xzf -

  /bin/echo -e "\n==> Building and installing HDF5 ${HDF5_VERSION} ...\n"
  cd "${WORKDIR}/hdf5-${HDF5_VERSION}"
  ./configure \
    --quiet \
    --prefix /usr/local \
    --enable-build-mode=production \
    --with-szlib \
    --enable-cxx
  make --jobs="${nproc}" --quiet install
}


set -euo pipefail
install_packages
download_and_build_fftw
download_and_build_hdf5
