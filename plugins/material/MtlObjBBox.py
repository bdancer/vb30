#
# V-Ray For Blender
#
# http://vray.cgdo.ru
#
# Author: Andrei Izrantcev
# E-Mail: andrei.izrantcev@chaosgroup.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# All Rights Reserved. V-Ray(R) is a registered trademark of Chaos Software.
#

import bpy

from vb25.lib   import ExportUtils
from vb25.ui.ui import GetContextType, GetRegionWidthFromContext, narrowui


TYPE = 'MATERIAL'
ID   = 'MtlObjBBox'
NAME = 'MtlObjBBox'
DESC = ""

PluginParams = (
    {
        'attr' : 'base_mtl',
        'desc' : "Base material",
        'type' : 'PLUGIN',
        'default' : "",
    },
    {
        'attr' : 'bbox_min',
        'desc' : "Min. coordinates for object bounding box",
        'type' : 'VECTOR',
        'default' : (0, 0, 0),
    },
    {
        'attr' : 'bbox_max',
        'desc' : "Max. coordinates for object bounding box",
        'type' : 'VECTOR',
        'default' : (0, 0, 0),
    },
)
