# -*- coding: utf-8 -*-
"""
"""
import biosteam as bst
import thermo as tm
import thermosteam as tmo
import numpy as np
from .property_package import create_property_package
from .precipitation_steps import EVOH_precipitation, PE_precipitation
from .dissolution_steps import EVOH_dissolution, PE_dissolution
from .units import (
    PseudoContinuousPlasticDissolutionTank, BatchPlasticDissolution,
    PrecipitationTank, JacketedSurgeTank, Microfilter, VacuumDryer, ScrewPressDegasser
)
s = bst.stream_kwargs

__all__ = (
    'create_psuedo_continuous_system',
    'create_single_layer_batch_separation_system',
    'create_multilayer_batch_separation_system',
)

# TODO: 
# [-] Make sure feed and product storage is well accounted for

@bst.SystemFactory(
    ID='batch_sys',
    ins=[s("plastic", Plastic=300, bst="kg/hr")],
    outs=[s("PET_resin", price=2.4023)],
    fthermo=create_property_package,
)
def create_multilayer_batch_separation_system(
        ins, outs,
        dissolution_steps=None, 
        precipitation_steps=None,
        shred=True,
    ):
    if precipitation_steps is None: 
        precipitation_steps = (EVOH_precipitation(), PE_precipitation())
    if dissolution_steps is None:
        dissolution_steps = (EVOH_dissolution(), PE_dissolution())
    # TODO: Work on solvent and plastic prices
    solvents = [bst.Stream(i.solvent, price=2.17) for i in dissolution_steps]
    products = [bst.Stream(i.plastic, price=2.4023) for i in precipitation_steps]
    ins.extend(solvents)
    outs.extend(products)
    shred = True
    plastic = ins[0]
    plastic.register_alias('feedstock', override=False, safe=False)
    for ds, ps, solvent, product in zip(dissolution_steps, precipitation_steps, solvents, products):
        intermediate = bst.Stream()
        sys = create_single_layer_batch_separation_system(
            ins=[plastic, solvent], 
            outs=[intermediate, product], 
            shred=shred, mockup=True,
            dissolution_step=ds,
            precipitation_step=ps,
        )
        plastic = intermediate
        shred = False
    sys.outs[0] = outs[0]

@bst.SystemFactory(
    ID='batch_sys',
    ins=[s("plastic", Plastic=300, bst="kg/hr")],
    outs=[s("coproduct")],
    fixed_ins_size=False,
    fixed_outs_size=False,
    fthermo=create_property_package,
)
def create_single_layer_batch_separation_system(
        ins, outs,
        dissolution_step=None, 
        precipitation_step=None,
        shred=True,
        vent_sink=None,
        convective_drying=False,
        facilities=False,
    ):
    """This configuration follows recommendations from the Michigan 
    Technological University (MTU). Because centrifugation and ultrafiltrations
    is performed between every plastic dissolution, it can handle extreemly 
    small plastic sizes."""
    if dissolution_step is None:
        dissolution_step = EVOH_dissolution()
    if precipitation_step is None:
        precipitation_step = EVOH_precipitation()
    # TODO: Make prices part of the dissolution and precipitation step variables
    if len(ins) == 1:
        plastic, = ins
        solvent = bst.Stream(dissolution_step.solvent, price=2.17)
        solvent.register_alias('solvent', override=False, safe=False)
        ins.append(solvent)
    else:
        plastic, solvent = ins
    plastic.register_alias('feedstock', override=False, safe=False)
    if len(outs) == 1:
        undissolved_plastic, = outs
        product = bst.Stream(precipitation_step.plastic + '_resin', price=2.4023)
        outs.append(product)
    else:
        undissolved_plastic, product = outs
    product.register_alias('product', override=False, safe=False)
    if shred:
        shredder = bst.Shredder(ins=plastic)
        plastic = shredder-0
    plastic_storage = bst.StorageTank(
        ins=plastic, tau=7 * 24, vessel_material="Carbon steel"
    )
    conveyor = bst.ConveyingBelt(ins=plastic_storage-0)
    storage = bst.StorageTank(
        ins=solvent, tau=7 * 24, vessel_material="Carbon steel",
        vessel_type='Floating roof', 
    )
    pump = bst.Pump(ins=storage-0, P=2 * 101325)
    recycle = bst.Stream()
    solvent_mixer = bst.Mixer(ins=[pump-0, recycle])
    surge_tank = bst.StorageTank(
        ins=solvent_mixer-0, vessel_type='Floating roof', 
        vessel_material="Stainless steel", tau=0.15,
    )
    surge_tank.line = 'Surge tank'
    solvent_pump = bst.Pump(ins=surge_tank-0, P=10 * 101325)
    if convective_drying:
        solvent2dissolution = bst.Stream()
    else:
        solvent2dissolution = solvent_pump-0
    hx = bst.HXutility(ins=solvent2dissolution, heat_only=True, T=dissolution_step.T)
    
    dissolution = BatchPlasticDissolution(
        ins=(conveyor-0, hx-0), 
        vessel_material="Stainless steel 304", 
        dissolution_step=dissolution_step,
        adiabatic=True
    )
    @dissolution.add_specification(
        args=(solvent_mixer, dissolution, dissolution_step, hx),
        impacted_units=[storage], 
    )
    def adjust_fresh_solvent_flow(mixer, dissolution, step, hx):
        dissolution.run()
        feed, solvent = dissolution.ins
        _, recycle = mixer.ins
        storage.ins[0].imol[step.solvent] = max(solvent.imol[step.solvent] - recycle.imol[step.solvent], 0 )
        hx_solvent = hx.ins[0]
        hx_solvent.copy_flow(solvent)
        plastic = conveyor.outs[0]
        mixed = hx_solvent + plastic
        H_actual = mixed.H
        mixed.T = dissolution_step.T
        H_target = mixed.H
        target = hx_solvent.copy()
        target.H += H_target - H_actual
        hx.T = target.T
    
    effluent, = dissolution.outs
    surge_tank = JacketedSurgeTank(
        ins=effluent, vessel_type='Floating roof', 
        vessel_material="Carbon steel", tau=dissolution.tau,
    )
    # TODO: Add option for design specification
    # @surge_tank.add_design_specification(design=True)
    # def adjust_surge_time():
    #     surge_tank.tau = dissolution.design_results['Batch time']
        
    surge_tank.line = 'Jacketed surge tank'
    pump = bst.Pump(ins=surge_tank-0, P=2 * 101325)
    centrifuge = bst.SolidsCentrifuge(
        ins=pump-0, split=0, 
        moisture_content=dissolution_step.solvent_content,
        strict_moisture_content=False,
        moisture_ID=dissolution_step.solvent,
    )
    @centrifuge.add_specification(run=True, args=(centrifuge,))
    def adjust_moisture(centrifuge):
        centrifuge.moisture_content = dissolution_step.solvent_content
        
    solids = [i.ID for i in centrifuge.chemicals if i.locked_state == 's']
    centrifuge.isplit[solids] = 0.999
    dummy = bst.Stream(None)
    dummy.imol[dissolution_step.solvent] = 1
    P = 0.1 * 101325
    bp = dummy.bubble_point_at_P(P)
    if convective_drying:
        dryer0 = bst.DrumDryer(
            ins=centrifuge-0,
            outs=('', '', ''),
            split=0,
            R=1.4,
            H=20,
            length_to_diameter=25,
            T=10 + bp.T, # TODO: expose assumption as a parameter
            moisture_content=0,
            moisture_ID=dissolution_step.solvent,
            utility_agent="Steam",
        )
        hx_driers_vent = bst.Stream()
        flash = bst.Flash(
            ins=hx_driers_vent, outs=['vent', ''],
            T=precipitation_step.T_condensation,
            P=101325
        )
        condensate = flash-1
    else:
        dryer0 = VacuumDryer(
            ins=centrifuge-0,
            split=0,
            T=50 + bp.T, # TODO: expose assumption as a parameter
            moisture_content=0,
            moisture_ID=dissolution_step.solvent,
            P=P
        )
        condensate = dryer0-1
        
    # @flash.add_specification(args=(flash,))
    # def use_CEOS(flash):
    #     inlet = flash.ins[0]
    #     chemicals = inlet.available_chemicals
    #     IDs = [i.ID for i in chemicals]
    #     flows = inlet.imol[IDs]
    #     F_mol = flows.sum()
    #     zs = flows / F_mol
    #     zs = zs.tolist()
    #     T = flash.T
    #     P = flash.P
    #     # Use equations of state for the gas and liquid phases.
    #     flashpkg = tmo.equilibrium.FlashPackage(
    #         chemicals=chemicals,
    #         G=tm.CEOSGas, L=tm.CEOSLiquid, S=tm.GibbsExcessSolid,
    #         GE=tm.UNIFAC, GEkw=dict(version=1), Gkw=dict(eos_class=tm.PRMIX),
    #     )
    #     flasher = flashpkg.flasher(N_liquid=1)
    #     PT = flasher.flash(zs=zs, T=T, P=P)
    #     V = PT.VF
    #     gas_zs = PT.gas.zs
    #     vapor, liquid = flash.outs
    #     for i in (vapor, liquid): 
    #         i.T = T
    #         i.P = P
    #     vapor.imol[IDs] = vapor_flows = F_mol * V * np.asarray(gas_zs)
    #     liquid.imol[IDs] = flows - vapor_flows
    #     vapor.imol['N2', 'O2'] += liquid.imol['N2', 'O2']
    #     liquid.imol['N2', 'O2'] = 0.
    
    microfilter = Microfilter(
        ins=centrifuge-1, 
        split=0,
        moisture_ID=dissolution_step.solvent,
        moisture_content=0,
    )
    microfilter.isplit[solids] = 0.999
    mixer = bst.Mixer(ins=(microfilter-0, dryer0-0), outs=undissolved_plastic)
    
    precipitation_tank = PrecipitationTank(ins=microfilter-1, precipitation_step=precipitation_step)
    centrifuge = bst.SolidsCentrifuge(
        ins=precipitation_tank-0,
        split=1,
        strict_moisture_content=False,
        moisture_content=precipitation_step.centrifuge_solvent_content,
        moisture_ID=precipitation_step.solvent
    )
    @centrifuge.add_specification(run=True, args=(centrifuge,))
    def adjust_moisture(centrifuge):
        centrifuge.moisture_content = precipitation_step.centrifuge_solvent_content
        
    centrifuge.isplit[precipitation_step.dissolved_plastic] = 0.
    if convective_drying:
        screw_press = bst.ScrewPress(
            ins=centrifuge-0,
            split=1,
            moisture_content=precipitation_step.screw_press_solvent_content,
            moisture_ID=precipitation_step.solvent,
            strict_moisture_content=False,
        )
        @screw_press.add_specification(run=True, args=(screw_press,))
        def adjust_moisture(screw_press):
            screw_press.moisture_content = precipitation_step.screw_press_solvent_content
        dummy = bst.Stream(None)
        dummy.imol[precipitation_step.solvent] = 1
        bp = dummy.bubble_point_at_P()
        dryer = bst.DrumDryer(
            ins=screw_press-0,
            outs=(product, '', ''),
            split=0,
            R=1.4,
            H=20,
            length_to_diameter=25,
            T=10 + bp.T,
            moisture_content=0,
            moisture_ID=precipitation_step.solvent,
            gas_composition=[('N2', 1.0)],
            utility_agent="Steam",
        )
    
        mixer = bst.Mixer(
            ins=[centrifuge-1, screw_press-1, condensate],
            outs=[recycle]
        )
        mixer = bst.Mixer(
            ins=[dryer0-1, dryer-1],
        )
        hx = bst.HXprocess(
            ins=[solvent_pump-0, mixer-0],
            outs=[solvent2dissolution, hx_driers_vent],
        )
        if vent_sink is None:
            mixer = bst.Mixer(ins=[flash-0])
            mixer.register_alias('vent_sink')
            bst.ThermalOxidizer(ins=mixer-0, outs=['emissions'])
        else:
            vent_sink.ins.append(flash-0)
    else:
        melt_vacuum = bst.Flash(
            ins=centrifuge-0, P=0.2 * 101325, 
            V=0.999, # TODO: Make this multiple stages and adjust model to vaporize set fraction at a T and P
            thermo=centrifuge.thermo.ideal(), # Avoid VLLE
            has_vapor_condenser=True,
        )
        degasser = ScrewPressDegasser(
            ins=melt_vacuum-1,
            outs=[product, ''],
            split=0,
            T=50 + bp.T, # TODO: expose assumption as a parameter
            moisture_content=1e-9,
            moisture_ID=precipitation_step.solvent,
            P=101325 * 0.05
        )
        condenser = bst.HXutility(ins=degasser-1, V=0, rigorous=True)
        liq_mixer = bst.Mixer(
            ins=[centrifuge-1, condensate, melt_vacuum-0, condenser-0],
            outs=[recycle],
        )
    if facilities:
        bst.create_all_facilities(
            HXN=False, CIP=False, WWT=False, PWC=False,
            CHP_kwargs=dict(autopopulate=False),
        )
    # for i in recycles: bst.mark_disjunction(i) # Flow is completely determined by dissolution tank

    
@bst.SystemFactory(
    ID='psuedo_continuous_sys',
    ins=[s("plastic", Plastic=300, bst="kg/hr")],
    outs=[s("product", price=2.4023)],
    fthermo=create_property_package,
)
def create_psuedo_continuous_system(
        ins, outs,
        dissolution_steps=None, 
        precipitation_steps=None,
    ):
    """This configuration may only work with big plastic packing. Otherwise,
    best to use the batch system with ultrafiltration."""
    #: TODO: Cost filter.
    plastic, = ins
    undissolved_plastic, = outs
    if dissolution_steps is None:
        dissolution_steps = [EVOH_dissolution(), PE_dissolution()]
    if precipitation_steps is None:
        precipitation_steps = [EVOH_precipitation(), PE_precipitation()]
    # TODO: Make prices part of the dissolution and precipitation step variables
    solvents = [bst.Stream(i.solvent, price=2.17) for i in dissolution_steps]
    products = [bst.Stream(i.plastic, price=2.4023) for i in precipitation_steps]
    ins.extend(solvents)
    outs.extend(products)
    
    plastic_storage = bst.StorageTank(
        ins=plastic, tau=7 * 24, vessel_material="Carbon steel"
    )
    conveyor = bst.ConveyingBelt(ins=plastic_storage-0)
    mixers = []
    recycles = []
    solvents2dissolution = []
    dissolution_times = [i.tau for i in dissolution_steps]
    drying_time = 0.05
    surge_time = sum(dissolution_times) + len(dissolution_times) * drying_time # This is also the cycle time
    for solvent in solvents: 
        storage = bst.StorageTank(
            ins=solvent, tau=7 * 24, vessel_material="Carbon steel",
            vessel_type='Floating roof', 
        )
        pump = bst.Pump(ins=storage-0, P=2 * 101325)
        recycle = bst.Stream()
        recycles.append(recycle)
        mixer = bst.Mixer(ins=[pump-0, recycle])
        mixers.append(mixer)
        surge_tank = bst.StorageTank(
            ins=mixer-0, vessel_type='Floating roof', 
            vessel_material="Stainless steel", tau=surge_time,
        )
        surge_tank.line = 'Surge tank'
        pump = bst.Pump(ins=surge_tank-0, P=10 * 101325)
        solvents2dissolution.append(pump-0)
        
    dissolution_tanks = PseudoContinuousPlasticDissolutionTank(
        ins=(conveyor-0, *solvents2dissolution, 'air'), 
        outs=(undissolved_plastic, *len(solvents2dissolution) * [''], 'vent'),
        vessel_material="Stainless steel 304", 
        dissolution_steps=dissolution_steps, drying_time=drying_time
    )
    for mixer, solvent, step in zip(mixers, solvents2dissolution, dissolution_steps):
        @mixer.add_specification(run=True, args=(mixer, solvent, step))
        def adjust_fresh_solvent_flow(mixer, solvent, step):
            fresh, recycle = mixer.ins
            fresh.imol[step.solvent] = solvent.imol[step.solvent] - recycle.imol[step.solvent]
    
    plastic, *dissolved_plastics, vent = dissolution_tanks.outs
    vents = []
    for dissolved_plastic, precipitation_step, recycle, product in zip(dissolved_plastics, precipitation_steps, recycles, products):
        surge_tank = bst.StorageTank(
            ins=dissolved_plastic, vessel_type='Floating roof', 
            vessel_material="Carbon steel", tau=surge_time,
        )
        surge_tank.line = 'Surge tank'
        pump = bst.Pump(ins=surge_tank-0, P=2 * 101325)
        cooler = bst.HXutility(ins=pump-0, T=precipitation_step.T)
        @cooler.add_specification(args=(cooler, precipitation_step,))
        def precipitate(cooler, precipitation_step):
            cooler.T = precipitation_step.T
            cooler.run()
            precipitation_step.precipitate(cooler.outs[0])
        
        centrifuge = bst.SolidsCentrifuge(
            ins=cooler-0,
            split=1,
            moisture_content=precipitation_step.solvent_content,
            moisture_ID=precipitation_step.solvent
        )
        centrifuge.isplit[precipitation_step.dissolved_plastic] = 0.
        screw_press = bst.ScrewPress(
            ins=centrifuge-0,
            split=1,
            moisture_content=precipitation_step.solvent_contents[1],
            moisture_ID=precipitation_step.solvent
        )
        pellet_mill = bst.PelletMill(ins=screw_press-0)
        dummy = bst.Stream(None)
        dummy.imol[precipitation_step.solvent] = 1
        bp = dummy.bubble_point_at_P()
        dryer = bst.DrumDryer(
            ins=pellet_mill-0,
            outs=(product, '', ''),
            split=0,
            R=1.4,
            H=20,
            length_to_diameter=25,
            T=10 + bp.T,
            moisture_content=precipitation_step.solvent_contents[2],
            moisture_ID=precipitation_step.solvent,
            gas_composition=[('N2', 1.0)],
            utility_agent="Steam",
        )
        
        flash = bst.Flash(
            ins=dryer-1, 
            T=precipitation_step.T_condensation,
            P=101325
        )
        
        @flash.add_specification(args=(flash,))
        def use_CEOS(flash):
            inlet = flash.ins[0]
            chemicals = inlet.available_chemicals
            IDs = [i.ID for i in chemicals]
            flows = inlet.imol[IDs]
            F_mol = flows.sum()
            zs = flows / F_mol
            zs = zs.tolist()
            T = flash.T
            P = flash.P
            # Use activity coefficients for the liquid phase 
            # and equations of state for the gas phase.
            flashpkg = tmo.equilibrium.FlashPackage(
                chemicals=chemicals,
                G=tm.CEOSGas, L=tm.GibbsExcessLiquid, S=tm.GibbsExcessSolid,
                GE=tm.UNIFAC, GEkw=dict(version=1), Gkw=dict(eos_class=tm.PRMIX),
            )
            flasher = flashpkg.flasher(N_liquid=1)
            PT = flasher.flash(zs=zs, T=T, P=P)
            V = PT.VF
            gas_zs = PT.gas.zs
            vapor, liquid = flash.outs
            for i in (vapor, liquid): 
                i.T = T
                i.P = P
            vapor.imol[IDs] = vapor_flows = F_mol * V * np.asarray(gas_zs)
            liquid.imol[IDs] = flows - vapor_flows
            
        vents.append(flash-0)
        mixer = bst.Mixer(
            ins=[centrifuge-1, screw_press-1, flash-1],
            outs=recycle
        )
    mixer = bst.Mixer(ins=vents)
    bst.ThermalOxidizer(ins=mixer-0)
    # for i in recycles: bst.mark_disjunction(i) # Flow is completely determined by dissolution tank

    

    
