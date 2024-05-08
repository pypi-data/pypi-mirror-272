#!/bin/bash

# SPDX-License-Identifier: LGPL-3.0-only

# Script to make python wheels for several versions

set -euo pipefail

ROOT_DIR=$(git rev-parse --show-toplevel)

cd "${ROOT_DIR}"

if ! which cibuildwheel > /dev/null
then
    echo "ERROR: You need cibuildwheel to build binary wheels." \
         "Use 'pip install cibuildwheel' to install it."
    exit 1
fi

cibuildwheel --platform linux
