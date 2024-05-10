# -*- coding: utf-8 -*-
"""

"""
import biosteam as bst
from .property_package import create_property_package
from .process_settings import GWP as GWP_key, load_process_settings
from .systems import create_single_layer_batch_separation_system
from .tea import create_baseline_tea
from chaospy import distributions as shape
from plastics import strap

__all__ = (
    'BaselineSTRAPModel',
)

class BaselineSTRAPModel(bst.ProcessModel):
    """
    Create a model for a solvent targeted precipitation and dissolution process.
    The dissolution and precipitation steps default to PE.
    
    """
    cache = {}
    def __new__(
            cls,
            simulate=True,
            dissolution_step=None,
            precipitation_step=None,
            EVOH=True,
        ):
        chemicals = create_property_package()
        bst.settings.set_thermo(chemicals)
        load_process_settings()
        if dissolution_step is None:
            dissolution_step = strap.dissolution_steps.PE_dissolution()
        if precipitation_step is None:
            precipitation_step = strap.precipitation_steps.PE_precipitation()
        key = (dissolution_step, precipitation_step, EVOH)
        if key in cls.cache: return cls.cache[key]
        self = super().__new__(cls)
        if EVOH:
            chemicals.define_group('Plastic', ['PE', 'EVOH', 'PET'], [4.2, 3.22, 93.32], wt=True)
        else:
            chemicals.define_group('Plastic', ['PE', 'PET'], [4.2, 93.32], wt=True)
        if EVOH:
            with bst.System() as system:
                PE_sys = create_single_layer_batch_separation_system(
                    mockup=True,
                    dissolution_step=dissolution_step,
                    precipitation_step=precipitation_step
                )
                EVOH_sys = create_single_layer_batch_separation_system(
                    mockup=True,
                    shred=False,
                    ins=PE_sys.get_outlet('coproduct'),
                    dissolution_step=strap.dissolution_steps.EVOH_dissolution(),
                    precipitation_step=strap.precipitation_steps.EVOH_precipitation(),
                    vent_sink=bst.F.unit.vent_sink if 'vent_sink' in bst.F.unit else None,
                    facilities=True,
                )
            products = [
                PE_sys.outs[1], # PE_resin
                EVOH_sys.outs[1], # EVOH_resin
                EVOH_sys.get_outlet('coproduct'),
            ]
        else:
            system = create_single_layer_batch_separation_system(
                dissolution_step=dissolution_step,
                precipitation_step=precipitation_step,
                facilities=True,
            )
            products = [
                system.get_outlet('product'),
                system.get_outlet('coproduct'),
            ]
        self.name = 'STRAP-B'
        self.dissolution_step = dissolution_step
        self.precipitation_step = precipitation_step
        self.tea = create_baseline_tea(system)
        
        system.define_process_impact(
            key=GWP_key,
            name='Direct non-biogenic emissions',
            basis='kg',
            inventory=lambda: self.emissions.imass['CO2'] * system.operating_hours,
            CF=1.,
        )
        
        model = bst.Model(system)
        parameter = model.parameter
        metric = model.metric
        self.tea_parameters = []
        def tea_param(f):
            self.tea_parameters.append(f)
            return f
        
        self.lca_parameters = []
        def lca_param(f):
            self.lca_parameters.append(f)
            return f
        
        self.general_parameters = []
        def gen_param(f):
            self.tea_parameters.append(f)
            self.lca_parameters.append(f)
            self.general_parameters.append(f)
            return f
        
        @metric(units='kg*CO2e/kg', element='product')
        def GWP():
            GWP = system.get_property_allocated_impact(
                key=GWP_key, name='mass', basis='kg',
                products=[i for i in system.outs if 'resin' in i.ID or 'product' in i.ID]
            ) # kg-CO2e / kg
            if GWP < 0: breakpoint()
            return GWP
        
        @metric(units='USD/kg')
        def MSP():
            return self.tea.solve_price(products)
        
        # Feedstock price will be equal to transportation cost.
        # TODO: Base estimate to transportation cost on availability of 
        # post-industrial plastic per area.
        
        @tea_param
        @parameter(
            baseline=0.035,
            element='Feedstock',
            units='USD/kg',
            distribution=shape.Uniform(0.01, 0.05)
        )
        def set_feedstock_price(price):
            self.feedstock.price = price
        
        # @tea_param
        # @parameter(
        #     baseline=0,
        #     element='Coproduct',
        #     units='USD/kg',
        #     distribution=shape.Uniform(0, 1.2)
        # )
        # def set_coproduct_price(price):
        #     self.coproduct.price = price
        
        baseline = 2.17
        @tea_param
        @parameter(
            baseline=baseline,
            element='Solvent',
            units='USD/kg',
            distribution=shape.Uniform(0.5 * baseline, 1.5 * baseline)
        )
        def set_solvent_price(price):
            self.solvent.price = price
        
        @tea_param
        @parameter(
            baseline=0.1,
            units='%',
            distribution=shape.Uniform(0.1, 0.2)
        )
        def set_IRR(IRR):
            self.tea.IRR = IRR
        
        @gen_param
        @parameter(
            baseline=0.3,
            element='polymer',
            distribution=shape.Uniform(0.02, 0.98)
        )
        def set_mass_fraction(mass_fraction):
            s = self.feedstock
            F_mass = s.F_mass
            plastic = self.dissolution_step.plastic
            s.imass[plastic] = 0
            other_composition = s.mass / s.F_mass
            s.mass = other_composition * F_mass * (1 - mass_fraction)
            s.imass[plastic] = mass_fraction * F_mass
        
        def solvent_content(baseline, *args, **kwargs):
            bounds = (baseline - 0.1, baseline + 0.1)
            return parameter(*args, bounds=bounds, baseline=baseline,
                             distribution=shape.Uniform(*bounds), 
                             units='%', **kwargs)
        
        @gen_param
        @solvent_content(
            dissolution_step.solvent_content,
            element='centrifuged plastic'
        )
        def set_centrifuged_plastic_solvent_content(solvent_content):
            dissolution_step.solvent_content = solvent_content
        
        @gen_param
        @solvent_content(
            precipitation_step.centrifuge_solvent_content,
            element='centrifuged precipitate'
        )
        def set_centrifuged_precipitate_solvent_content(solvent_content):
            precipitation_step.centrifuge_solvent_content = solvent_content
        
        @gen_param
        @solvent_content(
            precipitation_step.screw_press_solvent_content,
            element='screw pressed precipitate'
        )
        def set_screw_press_solvent_content(solvent_content):
            precipitation_step.screw_press_solvent_content = solvent_content
        
        chemicals = bst.settings.chemicals
        solvent = chemicals[dissolution_step.solvent]
        T = dissolution_step.T
        solvent.Psat.method = 'BOILING_CRITICAL'
        # This line resets the extrapolation coefficients
        solvent.Psat.extrapolation_coeffs.clear()
        
        @gen_param
        @parameter(
            baseline=solvent.Tb,
            element='Solvent', units='K',
            distribution=shape.Uniform(solvent.Tb - 25, solvent.Tb + 25),
        )
        def set_boiling_point(normal_boiling_point):
            solvent.Tb = normal_boiling_point
            # This line resets the extrapolation coefficients
            solvent.Psat.extrapolation_coeffs.clear()
        
        Tmax = solvent.Tb - 5
        Tmin = max(solvent.Tm + 15, 265)
        
        @gen_param
        @parameter(
            element='Dissolution', units='K',
            distribution=shape.Triangle(Tmin, T, Tmax)
        )
        def set_dissolution_temperature(temperature):
            dissolution_step.T = temperature
        
        @gen_param
        @parameter(
            element='Precipitation', units='%',
            distribution=shape.Uniform(0, 100),
        )
        def set_precipitation_temperature_drop(temperature_drop):
            T = dissolution_step.T
            precipitation_step.T = (
                T - temperature_drop / 100 * (T - Tmin)
            )
        
        @gen_param
        @parameter(
            element='Dissolution', units='wt %',
            distribution=shape.Uniform(1, 10),
        )
        def set_dissolution_capacity(solvent_capacity):
            dissolution_step.capacity = solvent_capacity / 100
        
        self.load_system(system)
        self.load_model(model)
        for i in model.parameters:
            if i.baseline is not None: i.setter(i.baseline)
        if simulate: system.simulate()
        self.natural_gas.set_CF(
            GWP_key,
            0.33, # Natural gas from shell conventional recovery, GREET; includes non-biogenic emissions
        )
        cls.cache[key] = self
        return self
            