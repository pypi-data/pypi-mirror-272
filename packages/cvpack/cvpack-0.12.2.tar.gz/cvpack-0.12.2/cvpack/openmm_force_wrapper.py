"""
.. class:: OpenMMForceWrapper
   :platform: Linux, MacOS, Windows
   :synopsis: A collective variable built from the potential energy of an OpenMM force

.. classauthor:: Charlles Abreu <craabreu@gmail.com>

"""

import typing as t

import openmm
from openmm import unit as mmunit

from .collective_variable import CollectiveVariable
from .units import Unit, VectorQuantity


class OpenMMForceWrapper(CollectiveVariable, openmm.Force):
    r"""
    A collective variable whose numerical value is computed from the potential energy,
    in kJ/mol, of an OpenMM force object.

    Parameters
    ----------
    openmmForce
        The OpenMM force whose potential energy will be used to define the collective
        variable. It can be passed as an instance of :OpenMM:`Force` or as a string
        containing the XML serialization of the force.
    unit
        The unit of measurement of the collective variable. It must be compatible
        with the MD unit system (mass in `daltons`, distance in `nanometers`, time
        in `picoseconds`, temperature in `kelvin`, energy in `kilojoules_per_mol`,
        angle in `radians`). If the collective variables does not have a unit, use
        `dimensionless`.
    periodicBounds
        The periodic bounds of the collective variable if it is periodic, or `None` if
        it is not.
    name
        The name of the collective variable.

    Example
    -------
    >>> import cvpack
    >>> import numpy as np
    >>> import openmm
    >>> from openmm import unit
    >>> from openmmtools import testsystems
    >>> model = testsystems.AlanineDipeptideVacuum()
    >>> angle = openmm.CustomAngleForce("theta")
    >>> _ = angle.addAngle(0, 1, 2)
    >>> cv = cvpack.OpenMMForceWrapper(
    ...     angle,
    ...     unit.radian,
    ...     periodicBounds=[-np.pi, np.pi] * unit.radian,
    ... )
    >>> cv.addToSystem(model.system)
    >>> integrator = openmm.VerletIntegrator(0)
    >>> platform = openmm.Platform.getPlatformByName("Reference")
    >>> context = openmm.Context(model.system, integrator, platform)
    >>> context.setPositions(model.positions)
    >>> cv.getValue(context)
    1.911... rad
    >>> cv.getEffectiveMass(context)
    0.00538... nm**2 Da/(rad**2)
    """

    def __init__(  # pylint: disable=super-init-not-called
        self,
        openmmForce: t.Union[openmm.Force, str],
        unit: mmunit.Unit,
        periodicBounds: t.Optional[VectorQuantity] = None,
        name: str = "openmm_force_wrapper",
    ) -> None:
        if isinstance(openmmForce, openmm.Force):
            openmmForce = openmm.XmlSerializer.serialize(openmmForce)
        unit = Unit(unit)
        self._wrapped_force = openmm.XmlSerializer.deserialize(openmmForce)
        self.this = self._wrapped_force.this
        self._registerCV(
            name,
            unit,
            openmmForce=openmmForce,
            unit=unit,
            periodicBounds=periodicBounds,
        )
        if periodicBounds is not None:
            self._registerPeriodicBounds(*periodicBounds)

    def __getattr__(self, name: str) -> t.Any:
        attr = getattr(self._wrapped_force, name)
        if callable(attr):

            def _wrapped_method(*args, **kwargs):
                return attr(*args, **kwargs)

            return _wrapped_method

        return attr


OpenMMForceWrapper.registerTag("!cvpack.OpenMMForceWrapper")
