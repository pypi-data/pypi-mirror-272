# -*- coding: utf-8 -*-
"""
"""
import thermosteam as tmo

class PrecipitationStep:
    __slots__ = (
        'solvent',
        'plastic',
        'dissolved_plastic',
        'solubility', # Solubility [wt / wt]
        'centrifuge_solvent_content', # Moisture content after centrifugation
        'screw_press_solvent_content', # Moisture content after screw press
        'T', # Precipitation temperature
        'tau', # Precipitation time
        'T_condensation',
    )
    
    def __init__(self,
            solvent: str,
            plastic: str,
            dissolved_plastic: str,
            solubility: float,
            centrifuge_solvent_content: float,
            screw_press_solvent_content: float,
            T: float,
            tau: float,
            T_condensation: float,
        ):
        self.solvent = solvent
        self.plastic = plastic
        self.dissolved_plastic = dissolved_plastic
        self.solubility = solubility
        self.centrifuge_solvent_content = centrifuge_solvent_content
        self.screw_press_solvent_content = screw_press_solvent_content
        self.T = T
        self.tau = tau
        self.T_condensation = T_condensation

    def __eq__(self, other):
        return type(self) is type(other) and (self.solvent, self.plastic, self.dissolved_plastic) == (other.solvent, other.plastic, other.dissolved_plastic)

    def __hash__(self):
        return hash((self.solvent, self.plastic, self.dissolved_plastic))

    def precipitate(self, stream):
        x = self.solubility
        F_mass = stream.F_mass
        mass_solute = stream.imass[self.dissolved_plastic, self.plastic].sum()
        x_max = mass_solute / F_mass
        if x_max <= 0.:
            liquid = 0.
            solid = mass_solute
        elif x >= x_max:
            liquid = mass_solute
            solid = 0.
        else:
            liquid = F_mass * x / (1 - x)
            solid = mass_solute - liquid        
        stream.imass[self.dissolved_plastic, self.plastic] = [liquid, solid]
        
    def __repr__(self):
        return f"{type(self).__name__}({self.solvent}, {self.plastic}, {self.dissolved_plastic}, {self.solubility}, {self.centrifuge_solvent_content}, {self.screw_press_solvent_content}, {self.T}, {self.tau}, {self.T_condensation})"
    

def EVOH_precipitation():
    return PrecipitationStep(
        'DMSOWater', 'EVOH', 'EVOHoligomer',
        0.001, 0.8, 0.4, 308.15, 0.5, 
        max(tmo.settings.chemicals.DMSO.Tm + 5, 
            tmo.settings.get_cooling_agent('chilled_brine').T + 10)
    )

def PE_precipitation():
    return PrecipitationStep(
        'Toluene', 'PE', 'PEoligomer',
        0.001, 0.8, 0.4, 308.15, 0.5, 
        max(tmo.settings.chemicals.Toluene.Tm + 5, 
            tmo.settings.get_cooling_agent('chilled_brine').T + 10)
    )

