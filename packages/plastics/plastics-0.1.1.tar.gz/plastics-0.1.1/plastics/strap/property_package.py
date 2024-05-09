# -*- coding: utf-8 -*-
"""
"""
import biosteam as bst

__all__ = (
    'create_property_package',
)


def create_property_package():
    chemicals = bst.Chemicals([
        "Toluene", 
        "DMSO", 
        bst.Chemical(
            'PE', 
            aliases=set(['Polyethylene']), 
            formula='C2H4',
            search_db=False,
            phase='s',
            rho=0.5 * (880 + 960), # kg / m3
            Cp=0.5 * (1.330 + 2.400), # J / g
            Tm=0.5 * (115 + 135) + 273.15, # K
            default=True,
        ),
        bst.Chemical(
            'PEoligomer', 
            search_ID='1-Hexene',
        ),
        bst.Chemical(
            "PET", 
            aliases=set(['Polyethylene terephthalate']),
            formula='C10H8O4',
            search_db=False,
            phase='s',
            rho=1380, # kg / m3,
            Tm=523,
            Tb=623,
            Cp=1,
            default=True,
        ),
        bst.Chemical(
            'EVOH',
            aliases=set(['Ethylene vinyl alcohol']),
            formula='C2H4OC2H4',
            search_db=False,
            phase='s',
            rho=0.5 * (1120 + 1140),
            Cp=2.4,
            default=True,
        ),
        bst.Chemical(
            'EVOHoligomer', 
            search_ID='3-buten-2-ol', # Approximate monomer
        ),
        "Water", 
        bst.Chemical("N2", phase='g'), 
        bst.Chemical("O2", phase='g'), 
        "CH4", 
        "CO2",
        "SO2",
        bst.Chemical("Ash", search_db=False, rho=1540, phase='s', default=True, MW=1)
    ])
    chemicals.compile()
    return chemicals