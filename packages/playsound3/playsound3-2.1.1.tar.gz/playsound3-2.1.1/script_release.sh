#
# Copyright (c) 2022-2024 Szymon Mikler
#

hatch build

twine upload --skip-existing dist/* --verbose
