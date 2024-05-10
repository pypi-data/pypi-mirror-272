# -*- coding: utf-8 -*-
"""
"""
import biosteam as bst

__all__ = (
    'load_process_settings',
)

# TODO: Potentially add Boiler-Turbogenerator and Cooling Tower

GWP = 'GWP'

def load_process_settings():
    settings = bst.settings
    settings.define_impact_indicator(GWP, 'kg*CO2e')
    for i in settings.heating_agents:
        settings.set_utility_agent_CF(
            i.ID, GWP, 0.2958e-3, 'kJ' # [kg*CO2*eq / kJ] From GREET 2020; Natural gas, on-site
        )
    settings.set_electricity_CF(
        GWP, 0.38 # [kg*CO2*eq / kWhr] From GREET 2020; NG-Fired Simple-Cycle Gas Turbine CHP Plant
    )
    settings.CEPCI = 816.0 # 2022
    settings.electricity_price = 0.07
    settings.set_utility_agent_CF(
        # Assuming cooling tower uses 0.00454 kWh / kg of recirculated water
        'cooling_water', GWP, 0.00454 * 0.38, 'kg'
    )
    hps = settings.get_heating_agent("high_pressure_steam")
    hps.heat_transfer_efficiency = 0.85
    hps.regeneration_price = 0.08064
    hps.T = 529.2
    hps.P = 44e5
    mps = settings.get_heating_agent("medium_pressure_steam")
    mps.heat_transfer_efficiency = 0.90
    mps.regeneration_price = 0.07974
    mps.T = 480.3
    mps.P = 18e5
    lps = settings.get_heating_agent("low_pressure_steam")
    lps.heat_transfer_efficiency = 0.95
    lps.regeneration_price = 0.06768
    lps.T = 428.6
    lps.P = 55e4