from __future__ import annotations

import abc
import enum
import logging

from collections.abc import MutableMapping, Sequence
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    validator
)
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Self,
    Type,
    TypeAlias,
    TypeGuard,
    TypeVar,
    Union,
    overload
)

from g3tables.system_config import SWSystemDictWrapper
from g3tables.system_config.type_hinting import SystemDict, SWDeviceDict


logger = logging.getLogger('g3elements')


ElementType = TypeVar(
    'ElementType', bound='ElementABC'
    )

OptionalElementType = TypeVar(
    'OptionalElementType', bound=Optional['ElementABC']
    )


class ElementTypedMapping(MutableMapping, Generic[ElementType]):
    def __init__(
        self,
        *elements: ElementType,
        etype: Type[ElementType] | None = None,
    ) -> None:
        if etype is None:
            if not elements:
                raise ValueError(
                    'Element type must be specified if no elements are given.'
                    )
            etype = elements[0].__class__
        elif not issubclass(etype, ElementABC):
            raise TypeError(
                f'Element type must be a subclass of "ElementABC", '
                f'got type "{etype.__name__}".'
                )
        self.__element_type = etype
        self.__dict: dict[str, ElementType] = {}
        for e in elements:
            self[e.name] = e

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        element_type = self.__element_type.__name__
        if not self.__dict:
            return f'{cls_name}(etype={element_type})'
        elements = ", ".join((repr(e) for e in self.__dict.values()))
        return f'{cls_name}({elements}, etype={element_type})'

    def __str__(self) -> str:
        elements = ", ".join(
            (
                f"'{e.name}': {e.__class__.__name__}(name='{e.name}')"
                for e in self.__dict.values()
            )
        )
        return f'{{{elements}}}'

    def __setitem__(self, key: str, value: ElementType) -> None:
        if not isinstance(value, self.__element_type):
            raise TypeError(
                f'Element must be of type "{self.__element_type.__name__}", '
                f'got type "{value.__class__.__name__}".'
                )
        self.__dict[key] = value

    def __getitem__(self, key: str) -> ElementType:
        return self.__dict[key]

    def __delitem__(self, key: str) -> None:
        del self.__dict[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict)

    def __len__(self) -> int:
        return len(self.__dict)

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, ElementType],
        etype: Type[ElementType] | None = None
    ) -> Self:
        return cls(*mapping.values(), etype=etype)

    @property
    def etype(self) -> Type[ElementType]:
        return self.__element_type

    def add(self, element: ElementType) -> None:
        self[element.name] = element

    def delete(self, element: ElementType) -> None:
        del self[element.name]

    def set_parent(self, parent: ElementABC | None) -> None:
        for element in self.__dict.values():
            element.parent = parent

    def to_dict(self) -> dict[str, ElementType]:
        return self.__dict.copy()


class ConnectorNotSetError(AttributeError):
    def __init__(
        self,
        connector: str,
        element: ElementABC | None = None
    ) -> None:
        if element is None:
            message = f'Connector "{connector}" is not set.'
        else:
            message = (
                f'Connector "{connector}" of {element.__class__.__name__} '
                f'"{element.name}" is not set. '
                )
        super().__init__(message)


# =============================================================================
# ELEMENT
# =============================================================================

class ElementABC(BaseModel, abc.ABC, Generic[OptionalElementType]):
    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        strict=True  # prevent object copying on coercion
        )

    name: str
    is_safety: bool = False
    parent: OptionalElementType | None = None
    zone: Zone | None = None
    data: dict = Field(default_factory=dict, exclude=True, frozen=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name})'

    def __hash__(self) -> int:
        if (path := self._shv_path_relative()):
            return hash(path)
        zone_name = self.zone.name if self.zone is not None else None
        parent_names = self._get_parent_names()
        return hash((zone_name, parent_names, self.name))

    def __eq__(self, other: object) -> bool:
        # check if other is also an ElementABC instance
        if not isinstance(other, type(self)):
            return NotImplemented
        this_path = self._shv_path_relative()
        other_path = other._shv_path_relative()
        if this_path and other_path:
            return this_path == other_path
        # check if the names are equal
        if self.name != other.name:
            return False
        # check if the zone names are equal (both None or same name)
        this_zone_name = self.zone.name if self.zone is not None else None
        other_zone_name = other.zone.name if other.zone is not None else None
        if this_zone_name != other_zone_name:
            return False
        # check if the parent hierarchy names are equal
        this_parents = self._get_parent_names()
        other_parents = other._get_parent_names()
        return this_parents == other_parents

    def _get_parent_names(self) -> tuple:
        """Helper method to get a tuple of parent names."""
        parent_names: list[str] = []
        parent: ElementABC | None = self.parent
        while parent is not None:
            parent_names.append(parent.name)
            parent = parent.parent
        return tuple(parent_names)

    @validator('name')
    @classmethod
    def _check_name(cls, name: str) -> str:
        if not isinstance(name, str):
            raise ValueError(f'Name "{name}" is not a string.')
        if not name:
            raise ValueError('Name cannot be empty.')
        if not name.replace('_', '').isalnum():
            raise ValueError(
                f'Name "{name}" contains a non-alphanumeric character.'
                )
        return name

    def _set_field_to_self(
        self,
        field: str,
        child: ElementABC,
        raise_validation_error: bool = True
    ) -> None:
        """
        Bind the child element to this element.

        Try to set the child's field to `self`. This method relies on
        Pydantic's validation mechanism to check if the field can be set to
        `self` (if the field type is not compatible with the type of this
        element, a `ValidationError` is raised and optionally supperessed).

        Args:
            field (str): The field of the child element to set to this element.
            child (ElementABC): The child element to bind to this element.
            raise_validation_error (bool, optional): If `True`, raise
            a `ValidationError` if the field cannot be set to `self`.
            Otherwise, suppress the `ValidationError`. Defaults to `True`.

        Raises:
            ValueError: If the field does not exist in the child element.
            ValidationError: If the field cannot be set to `self` and
            `raise_validation_error` is `True`.
        """
        if field not in child.model_fields:
            raise ValueError(f'Field "{field}" does not exist.')
        if getattr(child, field) is self:
            return
        try:
            setattr(child, field, self)
        except ValidationError as err:
            if raise_validation_error:
                raise err
            else:
                pass

    def _set_field_to_self_bypass_pydantic_validation(
        self,
        field: str,
        child: ElementABC,
        raise_validation_error: bool = True
    ) -> None:
        """
        Bind the child element to this element.

        Check if the expected type of provided child field is the same as
        the type of this element. If it is, set the child's field to `self`,
        bypassing the standard validation and directly accessing
        child's `__dict__` attribute. If it is not, optionally raise a
        `ValidationError`.

        This is a bit hacky, but it works, assuming that the field is annotated
        as `field: <ElementType>` or `field: <ElementType> | <OtherType>`.

        This method is useful if there are any model 'after' validators
        (methods decorated with `@model_validator(mode='after')`) that attempt
        to assing a value to a field of the model, and `validate_assignment` is
        set to `True` in the model's `ConfigDict`. Such combination may raise
        a `RecursionError`, because the validator is recursively called on the
        model. A similar problem is discussed in the following issue:
        "https://github.com/pydantic/pydantic/issues/8185".

        Args:
            field (str): The field of the child element to set to this element.
            child (ElementABC): The child element to bind to this element.
            raise_validation_error (bool, optional): If `True`, raise
            a `ValidationError` if the field cannot be set to `self`.
            Otherwise, suppress the `ValidationError`. Defaults to `True`.

        Raises:
            ValueError: If the field does not exist in the child element.
            ValidationError: If the field cannot be set to `self` and
            `raise_validation_error` is `True`.
        """
        if field not in child.model_fields:
            raise ValueError(f'Field "{field}" does not exist.')
        if child.parent is self:
            return
        parent_type = child.model_fields[field].annotation
        if isinstance(self, parent_type):  # type: ignore
            child.__dict__['parent'] = self
        else:
            if raise_validation_error:
                raise ValidationError(
                    f'Cannot set field "{field}" of "{child}" to "{self}". '
                    f'Input should be of type "{parent_type}", '
                    f'got "{self.__class__.__name__}" instead.'
                    )
            else:
                pass

    def model_post_init(self, __context) -> None:
        for field_name in self.model_fields:
            if field_name in ('parent', 'zone'):
                continue
            field_value = getattr(self, field_name)
            if isinstance(field_value, ElementABC):
                self._set_field_to_self(
                    'parent', field_value, raise_validation_error=False
                    )
            elif isinstance(field_value, ElementTypedMapping):
                for item in field_value.values():
                    self._set_field_to_self(
                        'parent', item, raise_validation_error=False
                        )

    @abc.abstractmethod
    def _shv_path_relative(self) -> str:
        """
        Implement this method in the subclass to return the relative SHV path
        within the zone for the element. For example, for a signal element
        "SG01" in zone "Z01", the relative SHV path would be
        "devices/signal/SG01".
        """
        ...

    @property
    def shv_path(self) -> str:
        return self._shv_path_relative()

    @property
    def shv_path_full(self) -> str:
        if not self.zone:
            raise AttributeError('Zone element is not set.')
        return f'shv/{self.zone.name}/{self._shv_path_relative()}'

    def add_child(self, field: str, child: ElementABC) -> None:
        if field not in self.model_fields:  # prohibit adding new child fields
            raise ValueError(f'Field "{field}" does not exist.')
        field_value = getattr(self, field)  # estimate child field type ...
        if field_value is None or isinstance(field_value, ElementABC):
            # may be a single child field (holds ElementABC subtype or None)
            setattr(self, field, child)
            child.parent = self
        elif isinstance(field_value, ElementTypedMapping):
            # may be a typed mapping (holds ElementABC subtype instances)
            field_value.add(child)
            child.parent = self
        else:
            # may be an invalid field (holds something else, like "name")
            raise ValueError(f'Field "{field}" is not a valid child field.')


class Element(ElementABC[None]):

    def _shv_path_relative(self) -> str:
        return ''


@overload
def is_element(
    obj: Any, of_type: Type[ElementType]
) -> TypeGuard[ElementType]: ...


@overload
def is_element(
    obj: Any, of_type: None = None
) -> TypeGuard[ElementABC]: ...


def is_element(
    obj: Any, of_type: Type[ElementType] | None = None
) -> TypeGuard[Union[ElementABC, ElementType]]:
    if of_type is None:
        return isinstance(obj, ElementABC)
    return isinstance(obj, ElementABC) and isinstance(obj, of_type)


# =============================================================================
# CABINET
# =============================================================================

class _CabinetChild(ElementABC['Cabinet']):

    @property
    def cabinet(self) -> Cabinet:
        cabinet = self.parent
        if cabinet is None:
            raise ConnectorNotSetError('cabinet', self)
        return cabinet

    @cabinet.setter
    def cabinet(self, cabinet: Cabinet) -> None:
        self.parent = cabinet

    def _shv_path_relative(self) -> str:
        raise NotImplementedError


class CabinetControlPanel(_CabinetChild):

    def _shv_path_relative(self) -> str:
        return ''


def is_control_panel(obj: Any) -> TypeGuard[CabinetControlPanel]:
    return isinstance(obj, CabinetControlPanel)


class CabinetConvertor(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/cabinet/{self.cabinet}/convertor/{self.name}'


def is_convertor(obj: Any) -> TypeGuard[CabinetControlPanel]:
    return isinstance(obj, CabinetControlPanel)


class CabinetFuse(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/cabinet/{self.cabinet}/fuse/{self.name}'


def is_fuse(obj: Any) -> TypeGuard[CabinetFuse]:
    return isinstance(obj, CabinetFuse)


class CabinetBRC(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return ''


def is_brc(obj: Any) -> TypeGuard[CabinetBRC]:
    return isinstance(obj, CabinetBRC)


class CabinetMonitoringModule(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return ''


def is_monitoring_module(
    obj: Any
) -> TypeGuard[CabinetMonitoringModule]:
    return isinstance(obj, CabinetMonitoringModule)


class CabinetRFID(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/cabinet/{self.cabinet}/other/{self.name}'


def is_rfid(obj: Any) -> TypeGuard[CabinetRFID]:
    return isinstance(obj, CabinetRFID)


class CabinetUPS(_CabinetChild):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/cabinet/{self.cabinet}/ups/{self.name}'


def is_ups(obj: Any) -> TypeGuard[CabinetUPS]:
    return isinstance(obj, CabinetUPS)


class Cabinet(ElementABC[None]):
    brc: CabinetBRC | None = None
    panel: CabinetControlPanel | None = None
    module: CabinetMonitoringModule | None = None
    rfid: CabinetRFID | None = None
    ups: CabinetUPS | None = None
    convertors: ElementTypedMapping[CabinetConvertor] = Field(
        default_factory=lambda: ElementTypedMapping(etype=CabinetConvertor)
        )
    fuses: ElementTypedMapping[CabinetFuse] = Field(
        default_factory=lambda: ElementTypedMapping(etype=CabinetFuse)
        )

    def _shv_path_relative(self) -> str:
        return f'devices/cabinet/{self.name}'


def is_cabinet(obj: Any) -> TypeGuard[Cabinet]:
    return isinstance(obj, Cabinet)


# =============================================================================
# CROSSING
# =============================================================================

class Crossing(ElementABC[None]):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return ''


def is_crossing(obj: Any) -> TypeGuard[Crossing]:
    return isinstance(obj, Crossing)


# =============================================================================
# DETECTOR
# =============================================================================

class DetectorType(enum.StrEnum):
    OTHER = "Detector (unknown type)"
    MASS = "Mass detector"
    PANTOGRAPH = "Pantograph detector"
    TRACKCIRCUIT = "Track circuit detector"
    ULTRASONIC = "Ultrasonic detector"
    VIRTUAL = "Virtual detector"


class Detector(ElementABC[None]):
    type_: DetectorType = DetectorType.OTHER

    def _shv_path_relative(self) -> str:
        return f'devices/detector/{self.name}'


def is_detector(
    obj: Any, of_type: str | DetectorType | None = None
) -> TypeGuard[Detector]:
    if of_type is None:
        return isinstance(obj, Detector)
    of_type = DetectorType(of_type)
    return isinstance(obj, Detector) and obj.type_ == of_type


# =============================================================================
# GATE
# =============================================================================

class Gate(ElementABC[None]):
    sg_lamp: Signal | None = None

    def model_post_init(self, __context) -> None:
        if self.sg_lamp is not None:
            self._set_field_to_self('assigned_element', self.sg_lamp)

    def _shv_path_relative(self) -> str:
        return f'devices/zone/{self.zone}/gate/{self.name}'


def is_gate(obj: Any) -> TypeGuard[Gate]:
    return isinstance(obj, Gate)


# =============================================================================
# GPIO
# =============================================================================

class GPIO(ElementABC[None]):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/gpio/{self.name}'


def is_gpio(obj: Any) -> TypeGuard[GPIO]:
    return isinstance(obj, GPIO)


# =============================================================================
# HEATING
# =============================================================================

class HeatingContactorRod(ElementABC['HeatingContactor']):

    @property
    def contactor(self) -> HeatingContactor:
        contactor = self.parent
        if contactor is None:
            raise ConnectorNotSetError('contactor', self)
        return contactor

    @contactor.setter
    def contactor(self, contactor: HeatingContactor):
        self.parent = contactor

    def _shv_path_relative(self) -> str:
        return (
            f'devices/heating/{self.contactor.heating}/contactor'
            f'/{self.contactor}/rod/{self.name}'
            )


def is_heating_rod(obj: Any) -> TypeGuard[HeatingContactorRod]:
    return isinstance(obj, HeatingContactorRod)


class _HeatingChild(ElementABC['Heating']):

    @property
    def heating(self) -> Heating:
        heating = self.parent
        if heating is None:
            raise ConnectorNotSetError('heating', self)
        return heating

    @heating.setter
    def heating(self, heating: Heating) -> None:
        self.parent = heating

    def _shv_path_relative(self) -> str:
        raise NotImplementedError


class HeatingContactor(_HeatingChild):
    rods: ElementTypedMapping[HeatingContactorRod] = Field(
        default_factory=lambda: ElementTypedMapping(etype=HeatingContactorRod)
        )

    def _shv_path_relative(self) -> str:
        return f'devices/heating/{self.heating}/contactor/{self.name}'


def is_heating_contactor(
    obj: Any
) -> TypeGuard[HeatingContactor]:
    return isinstance(obj, HeatingContactor)


class HeatingMeteo(_HeatingChild):

    def _shv_path_relative(self) -> str:
        return ''


def is_heating_meteo(obj: Any) -> TypeGuard[HeatingMeteo]:
    return isinstance(obj, HeatingMeteo)


class Heating(ElementABC[None]):
    contactors: ElementTypedMapping[HeatingContactor] = Field(
        default_factory=lambda: ElementTypedMapping(etype=HeatingContactor)
        )
    meteo: HeatingMeteo | None = None

    def _shv_path_relative(self) -> str:
        return f'devices/heating/{self.name}'


def is_heating(obj: Any) -> TypeGuard[Heating]:
    return isinstance(obj, Heating)


# =============================================================================
# MATRIX
# =============================================================================

class Matrix(ElementABC[None]):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/signal/{self.name}'


def is_matrix(obj: Any) -> TypeGuard[Matrix]:
    return isinstance(obj, Matrix)


# =============================================================================
# POINTMACHINE
# =============================================================================

class PointMachinePosition(enum.StrEnum):
    LEFT = "ROUTE_DIRECTION_LEFT"
    RIGHT = "ROUTE_DIRECTION_RIGHT"
    MIDDLE = "ROUTE_DIRECTION_STRAIGHT"


class _PointMachine(ElementABC[None]):
    ppi_signals: ElementTypedMapping[Signal] = Field(
        default_factory=lambda: ElementTypedMapping(etype=Signal)
        )

    def model_post_init(self, __context) -> None:
        for signal in self.ppi_signals.values():
            self._set_field_to_self('assigned_element', signal)

    def _shv_path_relative(self) -> str:
        raise NotImplementedError


class PointMachineElectrical(_PointMachine):

    def _shv_path_relative(self) -> str:
        return f'devices/pointMachine/{self.name}'


class PointMachineMechanical(_PointMachine):

    def _shv_path_relative(self) -> str:
        return f'devices/pointMachine/{self.name}'


PointMachine: TypeAlias = Union[
    PointMachineElectrical, PointMachineMechanical
    ]


def is_pm(
    obj: Any
) -> TypeGuard[PointMachineElectrical | PointMachineMechanical]:
    return isinstance(obj, (PointMachineElectrical, PointMachineMechanical))


def is_pme(obj: Any) -> TypeGuard[PointMachineElectrical]:
    return isinstance(obj, PointMachineElectrical)


def is_pmm(obj: Any) -> TypeGuard[PointMachineMechanical]:
    return isinstance(obj, PointMachineMechanical)


# =============================================================================
# REQUESTOR
# =============================================================================

# GENERAL

class RequestorLoopFunction(enum.StrEnum):
    LOGIN = "Login"
    LOGOUT = "Logout"
    LOGIN_LOGOUT = "Login and Logout"
    OTHER = "Other"


class _Requestor(ElementABC[None]):

    def _shv_path_relative(self) -> str:
        raise NotImplementedError


def is_requestor(obj: Any) -> TypeGuard[_Requestor]:
    return isinstance(obj, _Requestor)


RequestorType = TypeVar('RequestorType', bound=_Requestor)


class _RequestorLoop(ElementABC[RequestorType]):
    is_safety: Literal[False] = False
    loop_func: RequestorLoopFunction = RequestorLoopFunction.OTHER

    @property
    def requestor(self) -> RequestorType:
        requestor = self.parent
        if requestor is None:
            raise ConnectorNotSetError('requestor', self)
        return requestor

    @requestor.setter
    def requestor(self, requestor: RequestorType) -> None:
        self.parent = requestor

    def _shv_path_relative(self) -> str:
        raise NotImplementedError


def is_requestor_loop(obj: Any) -> TypeGuard[_RequestorLoop]:
    return isinstance(obj, _RequestorLoop)


RequestorLoopType = TypeVar('RequestorLoopType', bound=_RequestorLoop)


# DIGITAL REQUESTOR

class RequestorDigital(_Requestor):

    def _shv_path_relative(self) -> str:
        return f'devices/localRouteSelector/{self.name}'


def is_digreq(obj: Any) -> TypeGuard[RequestorDigital]:
    return isinstance(obj, RequestorDigital)


# ROUTING TABLE

class RequestorRoutingTable(_Requestor):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return 'devices/routing/table'


def is_routing_table(
    obj: Any
) -> TypeGuard[RequestorRoutingTable]:
    return isinstance(obj, RequestorRoutingTable)


# VETRA

class RequestorVetra(_Requestor):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.name}'


def is_vetra(obj: Any) -> TypeGuard[RequestorVetra]:
    return isinstance(obj, RequestorVetra)


# VECOM

class RequestorVecom(_Requestor):
    is_safety: Literal[False] = False
    loops: ElementTypedMapping[RequestorVecomLoop] = Field(
        default_factory=lambda: ElementTypedMapping(etype=RequestorVecomLoop)
        )

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.name}'


def is_vecom(obj: Any) -> TypeGuard[RequestorVecom]:
    return isinstance(obj, RequestorVecom)


class RequestorVecomLoop(_RequestorLoop[RequestorVecom]):

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.requestor}/loop/{self.name}'


def is_vecom_loop(obj: Any) -> TypeGuard[RequestorVecomLoop]:
    return isinstance(obj, RequestorVecomLoop)


# SPIE

class RequestorSPIE(_Requestor):
    is_safety: Literal[False] = False
    loops: ElementTypedMapping[RequestorSPIELoop] = Field(
        default_factory=lambda: ElementTypedMapping(etype=RequestorSPIELoop)
        )

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.name}'


def is_spie(obj: Any) -> TypeGuard[RequestorSPIE]:
    return isinstance(obj, RequestorSPIE)


class RequestorSPIELoop(_RequestorLoop[RequestorSPIE]):

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.requestor}/loop/{self.name}'


def is_spie_loop(obj: Any) -> TypeGuard[RequestorSPIELoop]:
    return isinstance(obj, RequestorSPIELoop)


# DRR

class RequestorDRR(_Requestor):
    is_safety: Literal[False] = False
    transceivers: ElementTypedMapping[RequestorSPIELoop] = Field(
        default_factory=lambda: ElementTypedMapping(etype=RequestorSPIELoop)
        )

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.name}'


def is_drr(obj: Any) -> TypeGuard[RequestorDRR]:
    return isinstance(obj, RequestorDRR)


class RequestorDRRTransceiver(_RequestorLoop[RequestorDRR]):

    def _shv_path_relative(self) -> str:
        return (
            f'devices/vehicleCommunicator/{self.requestor}'
            f'/transceiver/{self.name}'
            )


def is_drr_transceiver(
    obj: Any
) -> TypeGuard[RequestorDRRTransceiver]:
    return isinstance(obj, RequestorDRRTransceiver)


# AWA

class RequestorAWA(_Requestor):
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return f'devices/vehicleCommunicator/{self.name}'


def is_awa(obj: Any) -> TypeGuard[RequestorAWA]:
    return isinstance(obj, RequestorAWA)


Requestor: TypeAlias = Union[
    _Requestor,
    RequestorDigital,
    RequestorRoutingTable,
    RequestorVetra,
    RequestorVecom,
    RequestorDRR,
    RequestorSPIE,
    RequestorAWA
    ]


# =============================================================================
# ROUTE
# =============================================================================

class Route(ElementABC[None]):
    layout: RouteLayout
    go_symbol: SignalSymbol | None = None

    def _shv_path_relative(self) -> str:
        return f'devices/zone/{self.zone}/route/{self.name}'

    def model_post_init(self, __context) -> None:
        self.layout._set_route(self)


def is_route(obj: Any) -> TypeGuard[Route]:
    return isinstance(obj, Route)


class _RouteLayoutElement:
    def __init__(
        self,
        element: ElementABC,
        start_offset: float,
        end_offset: float,
    ) -> None:
        super().__init__()
        self._core = element
        self._start_offset = start_offset
        self._end_offset = end_offset
        self._layout: RouteLayout | None = None
        self._data: dict[Any, Any] = {}

    def __str__(self) -> str:
        if self._layout and self._layout._route:
            route = self._layout._route.name
        else:
            route = 'Detached'
        return f'{self._core.name} ({route})'

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(element={self._core}, start_offset='
            f'{self._start_offset}, end_offset={self._end_offset})'
            )

    def _set_layout(self, layout: RouteLayout | None) -> None:
        if layout is not None and not isinstance(layout, RouteLayout):
            raise ValueError(
                f'Unable to assosiate layout element "{self.name}" with '
                f'object "{layout}" of type "{type(layout).__name__}". '
                f'Expected a "RouteLayout" object.'
                )
        self._layout = layout

    @property
    def core(self) -> ElementABC:
        return self._core

    @property
    def name(self) -> str:
        return self._core.name

    @property
    def data(self) -> dict[Any, Any]:
        return self._data

    @property
    def layout(self) -> RouteLayout:
        if self._layout is None:
            raise ValueError(
                f'Layout element "{self.name}" is not associated with a '
                f'RouteLayout object.'
                )
        return self._layout

    @property
    def start_offset(self) -> float:
        return self._start_offset

    @property
    def end_offset(self) -> float:
        return self._end_offset

    @property
    def length(self) -> float:
        return self._end_offset - self._start_offset


class RouteLayoutDetector(_RouteLayoutElement):
    def __init__(
        self,
        detector: Detector,
        start_offset: float,
        end_offset: float,
        releases: Iterable[
            RouteLayoutPointMachine | RouteLayoutCrossing
            ] | None = None
    ) -> None:
        super().__init__(detector, start_offset, end_offset)
        self._releases: set[
            RouteLayoutPointMachine | RouteLayoutCrossing
            ] = set()
        if releases:
            for element in releases:
                self._add_dependent_element(element)
                element._set_releaser(self)

    def _add_dependent_element(
        self, element: _RouteLayoutReleasedElement
    ) -> None:
        allowed_types = (RouteLayoutPointMachine, RouteLayoutCrossing)
        if not isinstance(element, allowed_types):
            raise ValueError(
                f'Unable to set detector "{self.name}" as a releaser of '
                f'object "{element}" of type "{type(element).__name__}". '
                f'Expected a "RouteLayoutPointMachine" object or '
                f'a "RouteLayoutCrossing" object.'
                )
        self._releases.add(element)

    @property
    def core(self) -> Detector:
        core = super().core
        assert is_detector(core)
        return core

    @property
    def releases(self) -> set[RouteLayoutPointMachine | RouteLayoutCrossing]:
        return set(self._releases)


class _RouteLayoutReleasedElement(_RouteLayoutElement):
    def __init__(
        self,
        element: ElementABC,
        start_offset: float,
        end_offset: float,
        releaser: RouteLayoutDetector | None = None
    ) -> None:
        super().__init__(element, start_offset, end_offset)
        self._releaser: RouteLayoutDetector | None = None
        if releaser:
            self._set_releaser(releaser)
            releaser._add_dependent_element(self)

    def _set_releaser(self, detector: RouteLayoutDetector | None) -> None:
        if detector and not isinstance(detector, RouteLayoutDetector):
            raise ValueError(
                f'Cannot set object "{detector}" of type '
                f'"{type(detector).__name__}" as a releaser of '
                f'{self.__class__.__name__} "{self.name}. '
                f'Expected a "RouteLayoutDetector" object.'
            )
        self._releaser = detector

    @property
    def releaser(self) -> RouteLayoutDetector | None:
        return self._releaser


class RouteLayoutPointMachine(_RouteLayoutReleasedElement):
    def __init__(
        self,
        pointmachine: PointMachine,
        start_offset: float,
        end_offset: float,
        position: PointMachinePosition | str,
        releaser: RouteLayoutDetector | None = None
    ) -> None:
        super().__init__(pointmachine, start_offset, end_offset, releaser)
        self._position = self._check_position(position)

    def _check_position(
        self, position: PointMachinePosition | str
    ) -> PointMachinePosition:
        try:
            return PointMachinePosition(position)
        except ValueError as err:
            raise ValueError(
                f'Invalid position argument "{position}" '
                f'for pointmachine "{self.name}".'
                ) from err

    @property
    def core(self) -> PointMachine:
        core = super().core
        assert is_pm(core)
        return core

    @property
    def position(self) -> PointMachinePosition:
        return self._position


class RouteLayoutCrossing(_RouteLayoutReleasedElement):
    def __init__(
        self,
        crossing: Crossing,
        start_offset: float,
        end_offset: float,
        releaser: RouteLayoutDetector | None = None
    ) -> None:
        super().__init__(crossing, start_offset, end_offset, releaser)

    @property
    def core(self) -> Crossing:
        core = super().core
        assert is_crossing(core)
        return core


RouteLayoutElement: TypeAlias = Union[
    RouteLayoutDetector,
    RouteLayoutPointMachine,
    RouteLayoutCrossing
    ]


RouteLayoutElementType = TypeVar(
    'RouteLayoutElementType', bound=RouteLayoutElement
    )


class RouteLayout(Sequence[RouteLayoutElement]):
    def __init__(
        self,
        entry_gate: Gate,
        exit_gate: Gate,
        elements: Sequence[RouteLayoutElement],
    ) -> None:
        self._entry_gate = entry_gate
        self._exit_gate = exit_gate
        self._elements = list(elements)
        self._route: Route | None = None
        self._check_if_layout_valid()
        self._set_element_relations()

    def __str__(self) -> str:
        elements = " -> ".join((e.name for e in self._elements))
        return f'{self._entry_gate.name} | {elements} | {self._exit_gate.name}'

    @overload
    def __getitem__(self, index: int) -> RouteLayoutElement: ...

    @overload
    def __getitem__(self, index: slice) -> list[RouteLayoutElement]: ...

    def __getitem__(
        self, index: int | slice
    ) -> RouteLayoutElement | list[RouteLayoutElement]:
        return self._elements[index]

    def __len__(self) -> int:
        return len(self._elements)

    def _check_if_layout_valid(self) -> None:
        if self._elements:
            if not isinstance(self._elements[0], RouteLayoutDetector):
                raise ValueError('Layout must start with a Detector.')
            if not isinstance(self._elements[-1], RouteLayoutDetector):
                raise ValueError('Layout must end with a Detector.')

    def _set_element_relations(self) -> None:
        dependent_elements: list[_RouteLayoutReleasedElement] = []
        for element in self._elements:
            if isinstance(element, RouteLayoutDetector):
                element._releases.clear()
                for dependent_element in dependent_elements:
                    dependent_element._set_releaser(element)
                    element._add_dependent_element(dependent_element)
                dependent_elements.clear()
            elif isinstance(element, _RouteLayoutReleasedElement):
                dependent_elements.append(element)
            element._set_layout(self)

    def _set_route(self, route: Route) -> None:
        if self._route is not None:
            raise ValueError('Layout is already associated with a Route.')
        self._route = route

    def _filter_elements(
        self, element_type: Type[RouteLayoutElementType]
    ) -> list[RouteLayoutElementType]:
        return [e for e in self._elements if isinstance(e, element_type)]

    @property
    def route(self) -> Route:
        if self._route is None:
            raise ValueError('Layout is not associated with a Route.')
        return self._route

    @property
    def entry_gate(self) -> Gate:
        return self._entry_gate

    @property
    def exit_gate(self) -> Gate:
        return self._exit_gate

    @property
    def detectors(self) -> list[RouteLayoutDetector]:
        return self._filter_elements(RouteLayoutDetector)

    @property
    def pointmachines(self) -> list[RouteLayoutPointMachine]:
        return self._filter_elements(RouteLayoutPointMachine)

    @property
    def crossings(self) -> list[RouteLayoutCrossing]:
        return self._filter_elements(RouteLayoutCrossing)

    @property
    def length(self) -> float:
        try:
            return self._elements[-1]._end_offset
        except IndexError:
            return 0.0

    def get(self, name: str) -> RouteLayoutElement:
        try:
            return next((e for e in self._elements if e.core.name == name))
        except StopIteration:
            raise KeyError(f'Layout does not contain element "{name}".')

    def to_list(self) -> list[RouteLayoutElement]:
        return self._elements.copy()


# =============================================================================
# SIGNAL
# =============================================================================


class Signal(ElementABC[None]):
    symbols: ElementTypedMapping[SignalSymbol] = Field(
        default_factory=lambda: ElementTypedMapping(etype=SignalSymbol)
        )
    assigned_element: Gate | PointMachine | None = None

    def model_post_init(self, __context) -> None:
        if self.assigned_element is None:
            return
        if is_gate(self.assigned_element):
            self._set_field_to_self('sg_lamp', self.assigned_element)
        elif is_pm(self.assigned_element):
            self.assigned_element.ppi_signals.add(self)

    def _shv_path_relative(self) -> str:
        return f'devices/signal/{self.name}'


def is_signal(obj: Any) -> TypeGuard[Signal]:
    return isinstance(obj, Signal)


class CurrMeasType(enum.StrEnum):
    """
    Current measurement capabilities:
    - 0 - No measurement;
    - 1 - Warning + Error;
    - 2 - Error;
    - 3 - Warning
    """
    NO_MEASUREMENT = "SIGNAL_SYMBOL_MEASURE_NONE"
    WARNING_ERROR = "SIGNAL_SYMBOL_MEASURE_BOTH"
    ERROR = "SIGNAL_SYMBOL_MEASURE_ERROR"
    WARNING = "SIGNAL_SYMBOL_MEASURE_WARNING"


class SignalSymbol(ElementABC[Signal]):
    curr_meas: CurrMeasType = CurrMeasType.NO_MEASUREMENT

    @property
    def signal(self) -> Signal:
        signal = self.parent
        if signal is None:
            raise ConnectorNotSetError('signal', self)
        return signal

    @signal.setter
    def signal(self, signal: Signal):
        self.parent = signal

    @property
    def measures_warning(self) -> bool:
        return self.curr_meas in [
            CurrMeasType.WARNING,
            CurrMeasType.WARNING_ERROR
            ]

    @property
    def measures_error(self) -> bool:
        return self.curr_meas in [
            CurrMeasType.ERROR,
            CurrMeasType.WARNING_ERROR
            ]

    def _shv_path_relative(self) -> str:
        return f'devices/signal/{self.signal}/symbol/{self.name}'


def is_symbol(obj: Any) -> TypeGuard[SignalSymbol]:
    return isinstance(obj, SignalSymbol)


# =============================================================================
# SYSTEM
# =============================================================================

class System(ElementABC[None]):
    name: str = 'System'
    is_safety: Literal[False] = False

    def _shv_path_relative(self) -> str:
        return 'system'


def is_system(obj: Any) -> TypeGuard[System]:
    return isinstance(obj, System)


class SystemSafety(ElementABC[None]):
    name: str = 'SystemSafety'
    is_safety: Literal[True] = True

    def _shv_path_relative(self) -> str:
        return 'systemSafety'


def is_system_safety(obj: Any) -> TypeGuard[SystemSafety]:
    return isinstance(obj, SystemSafety)


# =============================================================================
# ZONE
# =============================================================================

def collect_connected(
    element: ElementABC, ignore_zone: bool = True
) -> list[ElementABC]:

    def collect(element: ElementABC, already_collected: list) -> None:
        if (
            any(e is element for e in already_collected) or
            (ignore_zone and isinstance(element, Zone))
        ):
            return
        already_collected.append(element)
        for attr in vars(element).values():
            if isinstance(attr, ElementABC):
                collect(attr, already_collected)
            elif isinstance(attr, Mapping):
                for value in attr.values():
                    if isinstance(value, ElementABC):
                        collect(value, already_collected)
            elif isinstance(attr, Iterable):
                for value in attr:
                    if isinstance(value, str):
                        continue
                    if isinstance(value, ElementABC):
                        collect(value, already_collected)

    collected: list[ElementABC] = []
    collect(element, collected)
    return collected


class Zone(ElementABC[None]):
    elements: list[ElementABC] = Field(default_factory=list)

    def model_post_init(self, __context) -> None:

        def set_zone(element: ElementABC, zone: Zone) -> None:
            if element.zone != zone:
                element.zone = zone
            for field in element.model_fields:
                if isinstance(field, ElementABC):
                    set_zone(field)
                elif isinstance(field, ElementTypedMapping):
                    for item in field.values():
                        set_zone(item)

        for element in self.elements:
            set_zone(element, self)

    @classmethod
    def from_system_config(cls, zone_name: str, data: SystemDict) -> 'Zone':
        return SystemDictToZoneConverter(zone_name, data).create_zone()

    @property
    def all_elements(self) -> list[ElementABC]:
        return collect_connected(self, ignore_zone=False)

    def find_by_type(
        self, type_: Type[ElementType]
    ) -> list[ElementType]:
        return [
            element for element in self.all_elements
            if is_element(element, of_type=type_)
            ]

    def _shv_path_relative(self) -> str:
        return f'devices/zone/{self.name}'


def is_zone(obj: Any) -> TypeGuard[Zone]:
    return isinstance(obj, Zone)


class SystemDictToZoneConverter:
    TYPES: dict[str, type[ElementABC]] = {
        'zone': Zone,
        'gate': Gate,
        'route': Route,
        'detector': Detector,
        'pme': PointMachineElectrical,
        'pmm': PointMachineMechanical,
        'signal': Signal,
        'symbol': SignalSymbol,
        'matrix': Matrix,
        'routingtable': RequestorRoutingTable,
        'requestordigital': RequestorDigital,
        'vecomcontroller': RequestorVecom,
        'vecomloop': RequestorVecomLoop,
        'vetra': RequestorVetra,
        'spiecontroller': RequestorSPIE,
        'spieloop': RequestorSPIELoop,
        'drrcontroller': RequestorDRR,
        'drrtransceiver': RequestorDRRTransceiver,
        'awa': RequestorAWA,
        'cabinet': Cabinet,
        'brc': CabinetBRC,
        'panel': CabinetControlPanel,
        'convertor': CabinetConvertor,
        'fuse': CabinetFuse,
        'monitoringmodule': CabinetMonitoringModule,
        'rfid': CabinetRFID,
        'ups': CabinetUPS,
        'heating': Heating,
        'meteo': HeatingMeteo,
        'contactor': HeatingContactor,
        'rod': HeatingContactorRod,
        'gpio': GPIO,
        'system': System,
        'systemsafety': SystemSafety
    }

    def __init__(self, zone_name: str, data: SystemDict) -> None:
        self.zone_name = zone_name
        self.data_wrapper = SWSystemDictWrapper(data['Software'])
        self.elements: dict[str, ElementABC] = {}

    @staticmethod
    def _get_detector_type(type_: str) -> DetectorType:
        types: dict[str, DetectorType] = {
            'trackcircuit': DetectorType.TRACKCIRCUIT,
            'pantographdetector': DetectorType.PANTOGRAPH,
            'massdetector': DetectorType.MASS,
            'ultrasonicsensor': DetectorType.ULTRASONIC,
            'virtualdetector': DetectorType.VIRTUAL
            }
        type_ = type_.replace(' ', '').replace('_', '').casefold()
        return types.get(type_, DetectorType.OTHER)

    @staticmethod
    def _get_curr_meas_type(value: str) -> CurrMeasType:
        if not value:
            return CurrMeasType.NO_MEASUREMENT
        try:
            values = {m.value: m for m in CurrMeasType}
            return values[value.upper()]
        except KeyError:
            raise ValueError(f'Invalid current measurement type: "{value}".')

    def _create_default(
        self, type_: str, data: SWDeviceDict, **kwargs
    ) -> ElementABC:
        element_cls = self.TYPES.get(type_, Element)
        element_name = self.data_wrapper.get_device_name(data)
        element = element_cls(name=element_name, **kwargs)
        element.is_safety = self.data_wrapper.is_device_safety(data)
        element.data['device_dict'] = data
        return element

    def _create_detector(self, data: SWDeviceDict) -> Detector | ElementABC:
        detector_type = data['general'].get('type', '')
        detector_type = self._get_detector_type(detector_type)
        return self._create_default('detector', data, type=detector_type)

    def _create_pm(self, data: SWDeviceDict) -> PointMachine | ElementABC:
        pm_type = data['general'].get('type', '').lower()
        return self._create_default(pm_type, data)

    def _create_symbol(self, data: SWDeviceDict) -> SignalSymbol | ElementABC:
        config = data.get('control', {}).get('config', {})
        curr_meas = self._get_curr_meas_type(config.get('measureCurrent', ''))
        return self._create_default('symbol', data, curr_meas=curr_meas)

    def _create_route_layout(self, data: SWDeviceDict) -> RouteLayout:
        """side effect: creates and adds crossings to elements dict"""
        entry_gate_name = f"Gate/{data['general']['entryGate']}"
        entry_gate = self.elements[entry_gate_name]
        assert is_gate(entry_gate)
        exit_gate_name = f"Gate/{data['general']['exitGate']}"
        exit_gate = self.elements[exit_gate_name]
        assert is_gate(exit_gate)
        layout_data: list[dict] = data['general']['layout']
        layout_elements: list[RouteLayoutElement] = []
        element: RouteLayoutElement
        for item_data in layout_data:
            if item_data['type'] == 'detector':
                detector = self.elements[f"Detector/{item_data['name']}"]
                assert is_detector(detector)
                element = RouteLayoutDetector(
                    detector=detector,
                    start_offset=item_data['startoffset'],
                    end_offset=item_data['endoffset'],
                    )
            elif item_data['type'] == 'pointmachine':
                pm = self.elements[f"PointMachine/{item_data['name']}"]
                assert is_pm(pm)
                element = RouteLayoutPointMachine(
                    pointmachine=pm,
                    start_offset=item_data['startoffset'],
                    end_offset=item_data['endoffset'],
                    position=PointMachinePosition(item_data['position'])
                    )
            elif item_data['type'] == 'crossing':
                crossing_name = item_data['name']
                crossing_key = f"Crossing/{crossing_name}"
                crossing = self.elements.setdefault(
                    crossing_key, Crossing(name=crossing_name)
                    )
                crossing.data['device_dict'] = {}
                assert is_crossing(crossing)
                element = RouteLayoutCrossing(
                    crossing=crossing,
                    start_offset=item_data['startoffset'],
                    end_offset=item_data['endoffset'],
                    )
            else:
                raise TypeError(item_data['type'])
            element.data['route_element_dict'] = item_data
            layout_elements.append(element)
        return RouteLayout(entry_gate, exit_gate, layout_elements)

    def _crete_route_laout_empty(self, data: SWDeviceDict) -> RouteLayout:
        route_name = data['general']['name']
        entry_gate_name = data['general']['entryGate']
        if not entry_gate_name:
            entry_gate_name = f'undefinedEntryGate_{route_name}'
        exit_gate_name = data['general']['exitGate']
        if not exit_gate_name:
            exit_gate_name = f'undefinedExitGate_{route_name}'
        return RouteLayout(
            entry_gate=Gate(name=entry_gate_name),
            exit_gate=Gate(name=exit_gate_name),
            elements=[]
            )

    def _create_route(self, data: SWDeviceDict) -> Route | ElementABC:
        try:
            layout = self._create_route_layout(data)
        except Exception as e:
            route_name = data['general']['name']
            logger.warning(
                f'Failed to create layout for route "{route_name}" ({e}).'
                )
            layout = self._crete_route_laout_empty(data)
        return self._create_default('route', data, layout=layout)

    def _create_element(self, type_: str, data: SWDeviceDict) -> ElementABC:
        type_ = type_.casefold()
        # process special cases
        if type_ == 'zone' or type_ == 'route':
            name = self.data_wrapper.get_device_name(data)
            err = f'Cannot create {type_} "{name}" with default initalizer.'
            raise TypeError(err)
        if type_ == 'detector':
            return self._create_detector(data)
        if type_ == 'pointmachine':
            return self._create_pm(data)
        if type_ == 'symbol':
            return self._create_symbol(data)
        # process the rest
        return self._create_default(type_, data)

    def _bind_parent_child(self) -> None:
        iter_devices_zone = self.data_wrapper.iter_devices_zone
        for parent_path, path, _ in iter_devices_zone(self.zone_name):
            if not parent_path or 'Zone' in path:
                continue
            element = self.elements[path]
            parent = self.elements[parent_path]
            element.parent = parent

    def _bind_signal_assigned_element(self) -> None:
        signals: dict[str, Signal] = {}
        gates: dict[str, Gate] = {}
        pms: dict[str, PointMachine] = {}
        for element in self.elements.values():
            if is_signal(element):
                signals[element.name] = element
            elif is_pm(element):
                pms[element.name] = element
            elif is_gate(element):
                gates[element.name] = element
        for signal in signals.values():
            assigned_element_name = (
                signal.data['device_dict']['general']['assigned_element']
                )
            if not assigned_element_name:
                continue
            if assigned_element_name in gates:
                gate = gates[assigned_element_name]
                signal.assigned_element = gate
                gate.sg_lamp = signal
            elif assigned_element_name in pms:
                pm = pms[assigned_element_name]
                signal.assigned_element = pm
                pm.ppi_signals[signal.name] = signal

    def _bind_route_go_symbol(self) -> None:
        """should be ran after sg lamps are bound with gates"""
        for element in self.elements.values():
            if not is_route(element):
                continue
            try:
                general_data = element.data['device_dict']['general']
                go_symbol_name = general_data['go_symbol']
                if not go_symbol_name:
                    raise KeyError
            except KeyError:
                continue
            if (
                (sg_lamp := element.layout.entry_gate.sg_lamp) and
                (go_symbol := sg_lamp.symbols.get(go_symbol_name))
            ):
                element.go_symbol = go_symbol

    def _bind_elements(self) -> None:
        self._bind_parent_child()
        self._bind_signal_assigned_element()
        self._bind_route_go_symbol()

    def create_zone(self) -> Zone:
        iter_devices_zone = self.data_wrapper.iter_devices_zone
        # first traversal - init most of the elements, don't bind
        zone_data: SWDeviceDict | None = None
        for _, path, data in iter_devices_zone(self.zone_name):
            element_type = path.split('/')[-2]
            if element_type == 'Zone':
                zone_data = data
                continue
            if element_type == 'Route':
                continue
            self.elements[path] = self._create_element(element_type, data)
        # second traversal - init routes
        for _, path, data in iter_devices_zone(self.zone_name):
            if 'Route' not in path:
                continue
            self.elements[path] = self._create_route(data)
        # third traversal - init system
        for _, path, data in iter_devices_zone('Common'):
            element_type = path.split('/')[-2]
            if 'System' not in path:
                continue
            self.elements[path] = self._create_element(element_type, data)
        # bind elements with each other
        self._bind_elements()
        # init zone
        if zone_data is None:
            raise ValueError(
                'Zone device data was not found during '
                'the system configuration data traversal.'
                )
        zone = self._create_default(
            'zone',
            data=zone_data,
            elements=[e for e in self.elements.values()]
            )
        assert isinstance(zone, Zone)
        return zone
