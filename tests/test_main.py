"""
Copyright (C)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext.

For license issues, please contact:

Dr. Bing Ye
Life Sciences Institute
University of Michigan
210 Washtenaw Avenue, Room 5403
Ann Arbor, MI 48109-2216
USA

Email: bingye@umich.edu
"""

from LabGym.tools import DetectronImportError


def test_import_gui() -> None:
    """Ensure that importing LabGym.gui works.

    Importing `gui` ensures that the interpreter reads every file in LabGym,
    which will catch basic syntax errors and compatibility errors between
    Python 3.9 and 3.10.
    """
    try:
        from LabGym import gui  # noqa: F401
    except DetectronImportError:
        print("Detectron2 not installed! This is expected behavior.")
