# -*- coding: utf-8 -*-
"""
"""
import biosteam as bst
from math import sqrt, pi
from biosteam.units.design_tools import PressureVessel
from biosteam.units.decorators import cost
from thermosteam import separations as sep
from biosteam.units.design_tools import (
    CEPCI_by_year,
    cylinder_diameter_from_volume, 
    cylinder_area,
)
from math import exp, log
from biosteam.units import design_tools as design

JacketedSurgeTank = bst.StorageTank # TODO: Add cost of jacket


# TODO: Find cost for microfilter, the following only works for nanofilter.
# Membrane separation processes. Perry's Chemical Engineer's Handbook 7th Edition. 

Europe_investment_site_factor = 1.2
euro_to_dollar = 1.04
installation_cost = 115000 # euro
volume_treated = 10 * 24 * 30 * 18 # m3
membrane_area = 27.5 # m2
membrane_cost = 95 # euro / m2
cleaning_cost = 50 # euro / m2
maintenance_cost = installation_cost * 0.02
yearly_operating_hours = 8000
operating_cost = membrane_area * (membrane_cost + cleaning_cost) + maintenance_cost * yearly_operating_hours / (18 * 30 * 24)
operating_cost_per_volume_treated = operating_cost / volume_treated
US_operating_cost = euro_to_dollar * operating_cost_per_volume_treated / Europe_investment_site_factor
US_installation_cost = euro_to_dollar * installation_cost / Europe_investment_site_factor
CEPCI2013 = bst.units.design_tools.CEPCI_by_year[2013]
electricity_cost = 2e3 # euro / yr
electricity_price = 0.04 # euro / kWh
electricity_demand = electricity_cost / yearly_operating_hours / electricity_price

@cost('Flow rate', 'Microfiltration', kW=electricity_demand, S=10, units='m3/hr',
      cost=US_installation_cost, n=0.6, BM=1., CE=CEPCI2013)
@cost('Annual flow rate', 'Membranes and maintenance', S=1., units='m3/yr',
      cost=US_operating_cost, n=1., BM=1., CE=CEPCI2013,
      annual=True)
class Microfilter(bst.SolidsSeparator): # TODO: Add cost of ultrafilter
    pass

@cost('Flow rate', 'Screw feeder', units='ft3/hr', 
      lb=400, ub=10e4, CE=567, cost=1096, n=0.22)
class VacuumDryer(design.PressureVessel, bst.Unit):
    """
    Create a vacuum dryer that dries solids by vacuum, and heat.
    
    Parameters
    ----------
    ins : 
        * [0] Wet solids.
    outs : 
        * [0] Dried solids
        * [1] Hot gas
    split : dict[str, float]
        Component splits to hot gas (stream [1]).
    H : float, optional
        Specific evaporation rate [kg/hr/ft3]. Defaults to 0.566. 
    length_to_diameter : float, optional
        Note that the drum is horizontal. Defaults to 25.
    T : float, optional
        Operating temperature [K]. Defaults to 343.15.
    moisture_content : float
        Moisture content of solids [wt / wt]. Defaults to 0.10.
        
    Notes
    -----
    The default parameter values are based on heuristics for drying 
    dried distillers grains with solubles (DDGS). However, values should 
    be updated to match design for vacuum drier.
    
    """
    auxiliary_unit_names = (
        'vacuum_system', 'condenser', 'pump'
    )
    _units = {
        'Evaporation': 'kg/hr',
        'Volume': 'ft3',
    }
    _N_ins = 1
    _N_outs = 2
    
    @property
    def isplit(self):
        """[ChemicalIndexer] Componentwise split of feed to 0th outlet stream."""
        return self._isplit
    @property
    def split(self):
        """[Array] Componentwise split of feed to 0th outlet stream."""
        return self._isplit.data
    
    def _init(self, split, H=20., length_to_diameter=25, T=380.15, P=101325 * 0.1,
              moisture_content=1e-6, moisture_ID=None):
        self._isplit = self.chemicals.isplit(split)
        self.P = P
        self.T = T
        self.H = H
        self.length_to_diameter = length_to_diameter
        self.moisture_content = moisture_content
        self.moisture_ID = moisture_ID
        self.vessel_material = 'Carbon steel'
        condenser = self.auxiliary(
            'condenser', bst.HXutility, ins=[''], 
            V=0,
        )
        self.auxiliary(
            'pump', bst.HXutility, ins=condenser-0, outs=[self.outs[1]], 
            V=0,
        )
        
    def _run(self):
        wet_solids, = self.ins
        dry_solids, condensate, = self.outs
        hot_gas, = self.condenser.ins
        wet_solids.split_to(hot_gas, dry_solids, self.split)
        sep.adjust_moisture_content(dry_solids, hot_gas, self.moisture_content, self.moisture_ID)
        hot_gas.P = self.P
        hot_gas.phase = 'g'
        design_results = self.design_results
        design_results['Evaporation'] = hot_gas.F_mass
        dry_solids.T = hot_gas.T = self.T
        self.condenser.run()
        self.pump.run()
        
    def _design(self):
        self._decorated_design()
        feed = self.ins[0]
        F_mass = 0.0006124 * feed.F_mass # lb/s
        length_to_diameter = self.length_to_diameter
        design_results = self.design_results
        design_results['Volume'] = volume = design_results['Evaporation'] / self.H 
        design_results['Diameter'] = diameter = cylinder_diameter_from_volume(volume, length_to_diameter)
        design_results['Length'] = length = diameter * length_to_diameter
        design_results.update(
            self._horizontal_vessel_design(self.P, diameter, length)
        )
        self.power_utility(
            0.0146 * F_mass**0.85 * length * 0.7457
        )
        self.add_heat_utility(self.H_out - self.H_in, self.T)
        self.vacuum_system = bst.VacuumSystem(self)
        self.condenser._design()
        self.pump._design()
        
    def _cost(self):
        self._decorated_cost()
        design_results = self.design_results
        dct = self.baseline_purchase_costs
        dct.update(
            self._horizontal_vessel_purchase_cost(
                design_results['Weight'], 
                design_results['Diameter'],
                design_results['Length']
            )
        )
        dct['Heating jacket'] = dct.pop('Horizontal pressure vessel')
        self.condenser._cost()
        self.pump._cost()

class MeltDegasser(bst.Flash):
    pass # TODO: Make this into a system with 3-stages, a condenser, and a single vacuum system

@cost('Flow rate', units='lb/hr', CE=567, lb=150, ub=12000, BM=1.39, 
      f=lambda S: exp((11.0991 - 0.3580*log(S) + 0.05853*log(S)**2)),
      kW=0.0372) # kWh per biomass 
class ScrewPressDegasser(design.PressureVessel, bst.Unit):
    """
    Create a degasser that dries solids by expression, vacuum, and heat.
    
    Parameters
    ----------
    ins : 
        * [0] Wet solids.
    outs : 
        * [0] Dried solids
        * [1] Hot gas
    split : dict[str, float]
        Component splits to hot gas (stream [1]).
    H : float, optional
        Specific evaporation rate [kg/hr/ft3]. Defaults to 0.566. 
    length_to_diameter : float, optional
        Note that the drum is horizontal. Defaults to 25.
    T : float, optional
        Operating temperature [K]. Defaults to 343.15.
    moisture_content : float
        Moisture content of solids [wt / wt]. Defaults to 0.10.
        
    Notes
    -----
    The default parameter values are based on heuristics for drying 
    dried distillers grains with solubles (DDGS). However, values should 
    be updated to match design for vacuum drier.
    
    """
    auxiliary_unit_names = (
        'vacuum_system', 'condenser', 'pump'
    )
    _units = {
        'Evaporation': 'kg/hr',
        'Volume': 'ft3',
    }
    _N_ins = 1
    _N_outs = 2
    
    @property
    def isplit(self):
        """[ChemicalIndexer] Componentwise split of feed to 0th outlet stream."""
        return self._isplit
    @property
    def split(self):
        """[Array] Componentwise split of feed to 0th outlet stream."""
        return self._isplit.data
    
    def _init(self, split, H=20., length_to_diameter=25, T=380.15, P=101325 * 0.05,
              moisture_content=1e-6, moisture_ID=None):
        self._isplit = self.chemicals.isplit(split)
        self.P = P
        self.T = T
        self.H = H
        self.vessel_material = 'Carbon steel'
        self.length_to_diameter = length_to_diameter
        self.moisture_content = moisture_content
        self.moisture_ID = moisture_ID
        condenser = self.auxiliary(
            'condenser', bst.HXutility, ins=[''], V=0,
        )
        self.auxiliary(
            'pump', bst.HXutility, ins=condenser-0, outs=[self.outs[1]], 
            V=0,
        )
        
    def _run(self):
        wet_solids, = self.ins
        dry_solids, condensate, = self.outs
        hot_gas, = self.condenser.ins
        wet_solids.split_to(hot_gas, dry_solids, self.split)
        sep.adjust_moisture_content(dry_solids, hot_gas, self.moisture_content, self.moisture_ID)
        hot_gas.P = self.P
        hot_gas.phase = 'g'
        design_results = self.design_results
        design_results['Evaporation'] = hot_gas.F_mass
        dry_solids.T = hot_gas.T = self.T
        self.condenser.run()
        self.pump.run()
        
    def _design(self):
        self._decorated_design()
        length_to_diameter = self.length_to_diameter
        design_results = self.design_results
        design_results['Volume'] = volume = design_results['Evaporation'] / self.H 
        design_results['Diameter'] = diameter = cylinder_diameter_from_volume(volume, length_to_diameter)
        design_results['Length'] = length = diameter * length_to_diameter
        design_results.update(
            self._horizontal_vessel_design(self.P, diameter, length)
        )
        self.add_heat_utility(self.H_out - self.H_in, self.T)
        self.vacuum_system = bst.VacuumSystem(self)
        self.condenser._design()
        self.pump._design()
        
    def _cost(self):
        self._decorated_cost()
        design_results = self.design_results
        dct = self.baseline_purchase_costs
        dct.update(
            self._horizontal_vessel_purchase_cost(
                design_results['Weight'], 
                design_results['Diameter'],
                design_results['Length']
            )
        )
        dct['Heating jacket'] = dct.pop('Horizontal pressure vessel')
        self.condenser._cost()
        self.pump._cost()
        

class BatchPlasticDissolution(bst.STR):
    _N_ins = 2
    _N_outs = 1
    tau_0_default = 0.1
    
    def _init(self, dissolution_step, min_solvent=1.5, **kwargs):
        kwargs['tau'] = dissolution_step.tau
        super()._init(**kwargs)
        self.dissolution_step = dissolution_step
        self.min_solvent = min_solvent
        
    def _run(self):
        plastic, solvent = self.ins
        effluent, = self.outs
        ds = self.dissolution_step
        F_plastic = sum([i.imass[ds.plastic, ds.dissolved_plastic].sum() for i in self.ins])
        solvent.imass[ds.solvent] = max(F_plastic / ds.capacity, self.min_solvent * plastic.F_mass)
        effluent.mix_from([plastic, solvent], energy_balance=True)
        ds.reaction(effluent)


class PrecipitationTank(bst.BatchCrystallizer):
    tau_0 = 0.1
    
    def _init(self, precipitation_step, **kwargs):
        kwargs['tau'] = precipitation_step.tau
        self.precipitation_step = precipitation_step
        super()._init(**kwargs)
        self.V = 1e3 # TODO: Base this on common sizes
        
    @property
    def T(self):
        return self.precipitation_step.T
    @T.setter
    def T(self, T):
        self.precipitation_step.T = T
        
    def _run(self):
        feed, = self.ins
        outlet, = self.outs
        outlet.copy_like(feed)
        ps = self.precipitation_step
        outlet.T = ps.T
        ps.precipitate(outlet)


class PseudoContinuousPlasticDissolutionTank(PressureVessel, bst.Unit):
    _N_ins = 3
    _N_outs = 3
    _ins_size_is_fixed = False
    _outs_size_is_fixed = False
    refill_time = 0.5
    auxiliary_unit_names = (
        'compressor', 'air_heat_exchanger', 'heaters',
    )
    def _init(self, 
            dissolution_steps, # Iterable[DissolutionStep] 
            solvent_superficial_velocity=7.2, # m / hr; typical velocities are 4 to 14.4 m /hr for liquids; Adsorption basics Alan Gabelman (2017) Adsorption basics Part 1. AICHE
            air_superficial_velocity=1332, # Mid point in velocity range for gasses, m / hr; Alan Gabelman (2017) Adsorption basics Part 1. AICHE
            vessel_material='Stainless steel 316',
            vessel_type='Vertical',
            void_fraction=0.47, # Optional[float] Necessary for sizing length
            length_unused=1.219, # Optional[float] Additional length of a column to account for mass transfer limitations (due to unused bed). Defaults to +2 ft per column.
            drying_time=0.05, # Optional[float] Time for drying after regeneration
            T_air=None, # Optional[float] Defaults to maximum dissolution temperature +10 degC
        ):
        inlets = self.ins
        n_inlets = len(inlets)
        n_solvents = n_inlets - 2
        if n_solvents < 1:
            raise ValueError('no solvent inlet given; number of inlets must be greater than 2 '
                             '(the first inlet is the plastic, the last is air, and everything in between are the solvents)')
        outlets = self.outs
        n_outlets = len(outlets)
        n_missing = n_outlets - n_inlets
        if n_missing: outlets.extend([bst.Stream(thermo=self.thermo) for i in range(n_missing)])
        if T_air is None: T_air = max([i.T for i in dissolution_steps]) + 50
        if len(dissolution_steps) != n_solvents:
            raise ValueError('the number of dissolution groups does not match the number of solvents')
        self.solvent_superficial_velocity = solvent_superficial_velocity
        self.air_superficial_velocity = air_superficial_velocity
        self.vessel_material = vessel_material
        self.vessel_type = vessel_type
        self.length_unused = length_unused
        self.void_fraction = void_fraction
        self.T_air = T_air
        self.drying_time = drying_time
        self.dissolution_steps = dissolution_steps
        self.heaters = []
        for inlet, ds in zip(inlets[1:-1], dissolution_steps):
            self.auxiliary(
                'heaters', bst.HXutility, inlet, T=ds.T
            )
        compressor = self.auxiliary(
            'compressor', bst.IsentropicCompressor, self.air, eta=0.85, P=10 * 101325
        )
        self.auxiliary(
            'air_heat_exchanger', bst.HXutility, compressor-0, 
            T=T_air, rigorous=False, 
        )
        
    @property
    def air(self):
        return self._ins[-1]

    @property
    def vent(self):
        return self._outs[-1]    
    
    @property
    def hot_compressed_air(self):
        return self.air_heat_exchanger.outs[0]
    
    def _run(self):
        plastic, *solvents, air = self.ins
        air.phase = 'g'
        plastic_outlet, *spent_solvents, spent_air = self.outs
        solvent_superficial_velocity = self.solvent_superficial_velocity
        air_superficial_velocity = self.air_superficial_velocity
        dissolution_steps = self.dissolution_steps
        drying_time = self.drying_time
        refill_time = self.refill_time
        dissolution_time = sum([i.tau for i in dissolution_steps])
        n_dissolutions = len(dissolution_steps)
        total_drying_time = n_dissolutions * drying_time
        self.cycle_time = cycle_time = dissolution_time + total_drying_time + refill_time
        plastic_outlet.copy_flow(plastic)
        plastic_outlet.T = dissolution_steps[-1].T
        heaters = self.heaters
        volumetric_solvent_flows = []
        for i, ds in enumerate(dissolution_steps):
            heater = heaters[i]
            solvent = solvents[i]
            spent_solvent = spent_solvents[i]
            F_plastic = plastic_outlet.imass[ds.plastic]
            plastic_outlet.imass[ds.plastic] = 0. # Remove plastic film
            solvent.imass[ds.solvent] = F_plastic / ds.capacity
            heater.run()
            heated_solvent = heater.outlet
            spent_solvent.copy_like(heated_solvent)
            spent_solvent.imass[ds.plastic] = F_plastic
            ds.reaction(spent_solvent)
            volumetric_solvent_flows.append(heated_solvent.F_vol * cycle_time / ds.tau)
        required_diameters = [2 * sqrt(i / (solvent_superficial_velocity * pi)) for i in volumetric_solvent_flows]
        self.diameter = diameter = max(required_diameters)
        self.area = area = pi * diameter * diameter / 4
        self.length = length = (
            cycle_time * plastic.F_vol / (self.void_fraction * diameter)
        )
        self.vessel_volume = length * area   
        hot_compressed_air = self.hot_compressed_air
        hot_compressed_air.T = self.air_heat_exchanger.T = self.T_air
        mean_air_flow = total_drying_time / cycle_time * air_superficial_velocity * diameter
        hot_compressed_air.reset_flow(
            N2=0.78, O2=0.32, phase='g', total_flow=mean_air_flow, units='m3/hr'
        )
        air.copy_flow(hot_compressed_air)
        self.compressor._run()
        self.air_heat_exchanger._run()
        self.vent.copy_like(hot_compressed_air)
        
    def _design(self):
        design_results = self.design_results
        diameter = self.diameter
        length = self.length
        design_results['Number of vessels'] = 1
        design_results.update(
            self._vessel_design(
                self.hot_compressed_air.P * 0.000145038, # Pa to psi
                diameter * 3.28084, # m to ft
                length * 3.28084, # m to ft
            )
        )
        for i in self.auxiliary_units: i._design()
    
    def _cost(self):
        design_results = self.design_results
        baseline_purchase_costs = self.baseline_purchase_costs
        baseline_purchase_costs.update(
            self._vessel_purchase_cost(
                design_results['Weight'], 
                design_results['Diameter'], 
                design_results['Length']
            )
        )
        N_reactors = design_results['Number of vessels']
        for i, j in baseline_purchase_costs.items():
            baseline_purchase_costs[i] *= N_reactors
        for i in self.auxiliary_units: i._cost()
