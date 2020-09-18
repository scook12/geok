import arcgis
import geok
import json
import pydantic
from enum import Enum
from typing import Union, List
from geok._types import PolygonType


class AbstractModel(pydantic.BaseModel):
    """
    Extends BaseModel with methods for automatically aliasing attributes to camelCase
    """

    class Config:
        arbitrary_types_allowed = True

    def _alias_fields(self):
        # TODO: add support for integrating a dictionary of manual aliases from self.__config__
        keys = list(self.__fields__.keys())

        def to_camel(val):
            if "_" in val:
                split = val.split("_")
                return split[0] + "".join([x.capitalize() for x in split[1:]])
            return val

        aliased_keys = list(map(lambda field: to_camel(field), keys))
        self.__config__.fields = dict(zip(self.__fields__.keys(), aliased_keys))
        return True

    def aliased_fields(self):
        """
        Returns a dictionary { snake_attrs: aliasedAttrs }
        """
        if (
            self.__config__ is not None
            and hasattr(self.__config__, "fields")
            and self.__config__.fields
        ):
            return self.__config__.fields
        else:
            self._alias_fields()
            return self.__config__.fields

    def aliased_dict(self):
        """
        Return attribute values in a dict with keys aliased as camelCase
        """
        d = self.dict()
        if (
            self.__config__ is not None
            and hasattr(self.__config__, "fields")
            and self.__config__.fields
        ):
            return {
                self.__config__.fields[k]: v for k, v in d.items() if d[k] is not None
            }
        else:
            self._alias_fields()
            return {
                self.__config__.fields[k]: v for k, v in d.items() if d[k] is not None
            }

    def aliased_json(self):
        return json.dumps(self.aliased_dict())


class EsriSqlType(str, Enum):
    bit = "sqlTypeBit"
    big_int = "sqlTypeBigInt"
    integer = "sqlTypeInteger"
    tiny_int = "sqlTypeTinyInt"
    time = "sqlTypeTime"
    timestamp = "sqlTypeTimestamp"
    other = "sqlTypeOther"
    none = "none"
    na = "NA"
    varchar = "sqlTypeNVarchar"


class EsriFieldType(str, Enum):
    oid = "esriFieldTypeOID"
    string = "esriFieldTypeString"
    date = "esriFieldTypeDate"
    small_integer = "esriFieldTypeSmallInteger"
    integer = "esriFieldTypeInteger"
    big_integer = "esriFieldTypeBigInteger"
    double = "esriFieldTypeDouble"
    single = "esriFieldTypeSingle"
    geometry = "esriFieldTypeGeometry"


esri_sql_field_map = {
    EsriFieldType.string: (EsriSqlType.time, EsriSqlType.timestamp, EsriSqlType.none),
    EsriFieldType.date: (EsriSqlType.na),
    EsriFieldType.small_integer: (
        EsriSqlType.integer,
        EsriSqlType.tiny_int,
        EsriSqlType.bit,
    ),
    EsriFieldType.integer: (EsriSqlType.big_int, EsriSqlType.integer),
    EsriFieldType.oid: (EsriSqlType.big_int),
}


class UniqueIdField(AbstractModel):
    name: str = "OBJECTID"
    is_system_maintained: bool = True


class SpatialReferenceModel(AbstractModel):
    wkid: int = 4326
    latest_wkid: int = None
    vcs_wkid: int = None
    latest_vcs_wkid: int = None


class FieldModel(AbstractModel):
    name: str
    type: EsriFieldType = EsriFieldType.string
    alias: str
    sql_type: str = EsriSqlType.other
    domain: Union[str, None]
    default_value: str = ""


OID_FIELD = FieldModel(
    **{
        "name": "OBJECTID",
        "type": EsriFieldType.oid,
        "alias": "OBJECTID",
        "sql_type": EsriSqlType.integer,
        "domain": "",
        "default_value": "",
    }
)


class FeatureModel(AbstractModel):
    # TODO: add internal validation of attributes with FieldModel
    geometry: dict
    attributes: dict


class FeaturesModel(AbstractModel):
    object_id_fieldname: str = "OBJECTID"
    global_id_fieldname: str = ""
    has_z: bool = False
    has_m: bool = False
    exceeded_transfer_limit: bool = False
    esri_fields: List[FieldModel]
    features: list
    unique_id_field: UniqueIdField = UniqueIdField()
    spatial_reference: SpatialReferenceModel = SpatialReferenceModel()

    class Config:
        # TODO: support integrating subset manual aliases in AbstractModel
        fields = {
            "object_id_fieldname": "objectIdFields",
            "global_id_fieldname": "globalIdFieldname",
            "has_z": "hasZ",
            "has_m": "hasM",
            "exceeded_transfer_limit": "exceededTransferLimit",
            "esri_fields": "fields",
            "features": "features",
            "unique_id_field": "uniqueIdField",
            "spatial_reference": "spatialReference",
        }


class PointModel(AbstractModel):
    x: Union[int, float]
    y: Union[int, float]
    spatial_reference: SpatialReferenceModel


class MultiPointModel(AbstractModel):
    coordinates = Union[
        List[Union[int, float, PointModel, arcgis.geometry.Point]],
        arcgis.geometry.MultiPoint,
    ]


class PolylineModel(AbstractModel):
    coordinates = Union[List[Union[int, float, PointModel]], arcgis.geometry.Polyline]


class PolygonModel(AbstractModel):
    coordinates = Union[
        List[Union[int, float, geok._types.PolygonType]], arcgis.geometry.Polygon
    ]


# TODO: server model
# TODO: feature layer model
# TODO: version model
# TODO: stats model
