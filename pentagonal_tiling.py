"""
Generate a dxf file with the pentagonal tiling as discovered by
Casey Mann, Jennifer McLoud-Mann & David Von Derau
doi:10.1007/s10711-017-0270-9
"""
import ezdxf
import numpy as np

a = 10.0  # in mm. boundingbox = x2.898 by x1.225
d = a * np.sqrt(2) / (np.sqrt(3) - 1)
c15 = np.cos(2 * np.pi * 15 / 360)
s15 = np.sin(2 * np.pi * 15 / 360)
e_e = a * (2 + np.sqrt(3)) / np.sqrt(2)
# create the polygon tile
points = [(0, a * np.sin(np.pi / 4))]
points.append((points[-1][0] + a * np.cos(np.pi / 4),
               points[-1][1] - a * np.sin(np.pi / 4)))
points.append((points[-1][0] + d,
               points[-1][1] + 0))
points.append((points[-1][0] + a * s15,
               points[-1][1] + a * c15))
points.append((points[-1][0] - a * c15,
               points[-1][1] + a * s15))
points.append((points[-1][0] - 2 * a * c15,
               points[-1][1] - 2 * a * s15))

doc = ezdxf.new('R2018')
msp = doc.modelspace()
poly_unit = doc.blocks.new(name='POLY_UNIT')
poly_unit.add_lwpolyline(points)
# create shifted tile unit
shifted_poly_unit = doc.blocks.new(name='S_POLY_UNIT')
shifted_poly_unit.add_blockref('POLY_UNIT', (0, -a * np.sin(np.pi / 4)))
# create the 2-tile unit
double_poly_unit = doc.blocks.new(name='D_POLY_UNIT')
double_poly_unit.add_blockref('POLY_UNIT', (0, 0))
double_poly_unit.add_blockref('POLY_UNIT', (0, 0), dxfattribs={'xscale': 1,
                                                               'yscale': -1,
                                                               'rotation': 0
                                                               })
# create the 4-tile unit
quad_poly_unit = doc.blocks.new(name='Q_POLY_UNIT')
quad_poly_unit.add_blockref('D_POLY_UNIT', (0, 0), dxfattribs={'xscale': 1,
                                                               'yscale': 1,
                                                               'rotation': 0
                                                               })
quad_poly_unit.add_blockref('D_POLY_UNIT', (a * (c15 + s15) + e_e, 2 * a * c15), dxfattribs={'xscale': 1,
                                                                                             'yscale': 1,
                                                                                             'rotation': 270
                                                                                             })
# create the 6-tile unit
six_poly_unit = doc.blocks.new(name='SIX_POLY_UNIT')
six_poly_unit.add_blockref('Q_POLY_UNIT', (0, 0), dxfattribs={'xscale': 1,
                                                                 'yscale': 1,
                                                                 'rotation': 0
                                                                 })
six_poly_unit.add_blockref('S_POLY_UNIT', (- 2 * a *c15, a* np.sqrt(3 / 2)), dxfattribs={'xscale': 1,
                                                                                          'yscale': 1,
                                                                                          'rotation': -30
                                                                                          })
six_poly_unit.add_blockref('S_POLY_UNIT', (d + a / np.sqrt(2), c15 * 2 * a + d), dxfattribs={'xscale': 1,
                                                                                             'yscale': -1,
                                                                                             'rotation': -60
                                                                                             })

# create the 12-tile unit
twelve_poly_unit = doc.blocks.new(name='T_POLY_UNIT')
twelve_poly_unit.add_blockref('SIX_POLY_UNIT', (0, 0), dxfattribs={'xscale': 1,
                                                                   'yscale': 1,
                                                                   'rotation': 0
                                                                   })
twelve_poly_unit.add_blockref('SIX_POLY_UNIT', (-4 * a * c15 + a * s15, a * np.sqrt(3 / 2) + a * s15),
                              dxfattribs={'xscale': 1,
                                          'yscale': 1,
                                          'rotation': 180
                                          })
# add to document
many_poly_unit = doc.blocks.new(name='M_POLY_UNIT')
for i in range(10):
    many_poly_unit.add_blockref('T_POLY_UNIT', (-i * c15 * 2 * a, i * c15 * 2 * a), dxfattribs={'xscale': 1,
                                                                                                'yscale': 1,
                                                                                                'rotation': 0
                                                                                                })
msp.add_blockref('M_POLY_UNIT', (0, 0), dxfattribs={'xscale': 1,
                                                    'yscale': 1,
                                                    'rotation': -45
                                                    })
doc.saveas('pentagonal_tiling.dxf')
