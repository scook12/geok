import arcgis
import pytest
import geok
import json
import pydantic
from pydantic import ValidationError


def test_version():
    assert geok.__version__ == "0.1.0"


@pytest.fixture
def abstract_model():
    """
    This fixture is for testing the behavior of classes inheriting from AbstractBaseModel

    AbstractBaseModel is built to avoid repeating configurations and methods for aliasing
    snake_case to camelCase in output json
    """

    class TestAbstractModel(geok.core.AbstractModel):
        name: str = "OBJECTID"
        is_system_maintained: bool = True
        required_value: str

    return TestAbstractModel(required_value="value")


@pytest.fixture
def configured_model():
    """
    Fixture for configured model - this was how aliasing was achieved for the first schema,
    but since nearly every object will need aliasing methods, the models now inherit from
    AbstractModel - this fixture is for testing that AbstractModel behaves the same as a
    configured model with manually specified aliases and alias methods
    """

    class TestConfiguredModel(pydantic.BaseModel):
        name: str = "OBJECTID"
        is_system_maintained: bool = True
        required_value: str

        class Config:
            fields = {
                "name": "name",
                "is_system_maintained": "isSystemMaintained",
                "required_value": "requiredValue",
            }

        def aliased_dict(self):
            d = self.dict()
            return {
                self.__config__.fields[k]: v for k, v in d.items() if d[k] is not None
            }

        def aliased_json(self):
            return json.dumps(self.aliased_dict())

    # TODO: debug --- this configured model seems to only take the alias 'requiredValue' as input
    return TestConfiguredModel(requiredValue="value")


@pytest.fixture
def feature():
    """
    Fixture returns a single valid Esri Feature
    """
    return {
        "geometry": {"x": -10762285.448, "y": 3366656.255599998},
        "attributes": {
            "OBJECTID": 1,
            "APIUWI": "42239329770000",
            "DIST_MAX_1": 9.99999999,
            "DIST_AVG_1": 4.99999999,
            "DIST_MAX_M": 0.05263158,
            "DIST_AVG_M": 0.02631579,
            "TRANS_COST": 0.42982456,
            "TRUCK_LOAD": 190,
            "OpAlias": "SUE-ANN OPERATING, LC",
            "LeaseName": "YENDREY",
            "WellNo": "1",
            "EntityType": "WELL",
            "County": "JACKSON (TX)",
            "DIBasin": "GULF COAST WEST",
            "DISubplay": " ",
            "Reservoir": "YEGUA AY-3",
            "ProdType": "GAS",
            "ProdStatus": "ACTIVE",
            "DrillType": "V",
            "LeaseNo": "168912",
            "CumMMCFGE": 7960,
            "CumBCFGE": 8,
            "DailyGas": 151,
            "DailyLiq": 8,
            "Latitude": 28.9293446,
            "Longitude": -96.6792551,
            "Last12Liq": 2811,
            "Last12Gas": 55129,
            "Last12Wtr": 345,
            "EntityId": 1141955,
            "OtherNo": "0",
        },
    }


@pytest.fixture
def fields():
    """
    Feature returns 3 valid Esri Fields
    """
    return [
        {
            "name": "OBJECTID",
            "type": "esriFieldTypeOID",
            "alias": "OBJECTID",
            "sqlType": "sqlTypeInteger",
            "domain": None,
            "defaultValue": None,
        },
        {
            "name": "APIUWI",
            "type": "esriFieldTypeString",
            "alias": "APIUWI",
            "sqlType": "sqlTypeNVarchar",
            "length": 50,
            "domain": None,
            "defaultValue": None,
        },
        {
            "name": "CAT_NO1",
            "type": "esriFieldTypeInteger",
            "alias": "CAT_NO",
            "sqlType": "sqlTypeInteger",
            "domain": None,
            "defaultValue": None,
        },
    ]


def test_configured_model(configured_model):
    # attrs
    assert hasattr(configured_model, "required_value")
    assert hasattr(configured_model, "is_system_maintained")
    assert hasattr(configured_model, "name")
    # types
    assert isinstance(configured_model.name, str)
    assert isinstance(configured_model.required_value, str)
    assert isinstance(configured_model.is_system_maintained, bool)
    # aliased_dict
    expected = {
        "name": "OBJECTID",
        "isSystemMaintained": True,
        "requiredValue": "value",
    }
    d = configured_model.aliased_dict()
    assert all(["name" in d, "isSystemMaintained" in d, "requiredValue" in d])
    assert d["name"] == expected["name"]
    assert d["isSystemMaintained"] == expected["isSystemMaintained"]
    assert d["requiredValue"] == expected["requiredValue"]
    # TODO: better coverage for json, validation of json
    # aliased_json
    j = configured_model.aliased_json()
    assert j is not None
    assert isinstance(j, str)


def test_abstract_model(abstract_model, configured_model):
    """
    Compare the behavior of BaseModel configured manually with aliases
    and the behavior of AbstractModel with automated aliasing (snake -> camel)
    """
    # attrs
    assert hasattr(abstract_model, "required_value")
    assert hasattr(abstract_model, "is_system_maintained")
    assert hasattr(abstract_model, "name")
    # types
    assert isinstance(abstract_model.name, str)
    assert isinstance(abstract_model.is_system_maintained, bool)
    assert isinstance(abstract_model.required_value, str)
    # aliased_dict
    expected = {
        "name": "OBJECTID",
        "isSystemMaintained": True,
        "requiredValue": "value",
    }
    d = abstract_model.aliased_dict()
    assert all(["name" in d, "isSystemMaintained" in d, "requiredValue" in d])
    assert d["name"] == expected["name"]
    assert d["isSystemMaintained"] == expected["isSystemMaintained"]
    assert d["requiredValue"] == expected["requiredValue"]
    # TODO: increased coverage of json, testing validity
    # aliased_json
    j = abstract_model.aliased_json()
    assert j is not None
    assert isinstance(j, str)
    # identical to configured
    assert abstract_model.name == configured_model.name
    assert abstract_model.is_system_maintained == configured_model.is_system_maintained
    assert abstract_model.required_value == configured_model.required_value
    cd = configured_model.aliased_dict()
    assert all([k in cd.keys() for k in list(d.keys())])


def test_uid_field():
    # TODO: test dict, json representations of uid_field
    bad_sys = {"name": "FID", "is_system_maintained": "fals?"}

    # defaults
    default = geok.core.UniqueIdField()
    assert hasattr(default, "name")
    assert hasattr(default, "is_system_maintained")
    assert isinstance(default.name, str)
    assert isinstance(default.is_system_maintained, bool)
    assert default.name == "OBJECTID"
    assert default.is_system_maintained == True

    # manual assignment
    good_uid = geok.core.UniqueIdField(**{"name": "FID", "is_system_maintained": False})
    assert hasattr(good_uid, "name")
    assert hasattr(good_uid, "is_system_maintained")
    assert isinstance(good_uid.name, str)
    assert isinstance(good_uid.is_system_maintained, bool)
    assert good_uid.name == "FID"
    assert good_uid.is_system_maintained == False

    # coercion
    coerced_sys = geok.core.UniqueIdField(
        **{"name": "FID", "is_system_maintained": "false"}
    )
    assert hasattr(coerced_sys, "name")
    assert hasattr(coerced_sys, "is_system_maintained")
    assert isinstance(coerced_sys.name, str)
    assert isinstance(coerced_sys.is_system_maintained, bool)
    assert good_uid.name == "FID"
    assert good_uid.is_system_maintained == False

    # failure
    with pytest.raises(ValidationError):
        should_fail = geok.core.UniqueIdField(**bad_sys)


def test_field():
    # TODO: test dict, json representations of field
    good = {
        "type": "esriFieldTypeString",
        "name": "fieldName",
        "alias": "fieldAlias",
    }

    bad_type = {
        "type": "string",
        "name": "fieldName",
        "alias": "fieldAlias",
    }

    bad_name = {
        "type": "esriFieldTypeString",
        "name": 1,
        "alias": "zero_one",
    }

    req_attrs = ["type", "name", "alias", "domain", "sql_type", "default_value"]

    good_field = geok.core.FieldModel(**good)
    assert all(list(map(lambda x: hasattr(good_field, x), req_attrs)))
    assert good_field.type == geok.core.EsriFieldType.string
    assert good_field.sql_type == geok.core.EsriSqlType.other
    assert pytest.raises(ValidationError, geok.core.FieldModel, kwargs=bad_type)
    assert pytest.raises(ValidationError, geok.core.FieldModel, kwargs=bad_name)


def test_features(feature, fields):
    feat_model = geok.core.FeaturesModel(**{"features": [feature], "fields": fields,})
    req_attrs = [
        "object_id_fieldname",
        "global_id_fieldname",
        "has_z",
        "has_m",
        "exceeded_transfer_limit",
        "fields",
        "features",
        "unique_id_field",
        "spatial_reference",
    ]

    # has all required attributes
    assert isinstance(feat_model, geok.core.FeaturesModel)
    assert all(list(map(lambda x: hasattr(feat_model, x), req_attrs)))
    # interoperability with arcgis FeatureSet
    fset = arcgis.features.FeatureSet.from_dict(feat_model.aliased_dict())
    assert isinstance(fset, arcgis.features.FeatureSet)
    assert hasattr(fset, "features")
    assert fset.features is not None


def test_point():
    sr = geok.core.SpatialReferenceModel()
    model = geok.core.PointModel(x=32.1, y=32.1, spatial_reference=sr)
    assert isinstance(model, geok.core.PointModel)
    assert hasattr(model, 'x')
    assert hasattr(model, 'y')
    assert hasattr(model, 'spatial_reference')
    assert model.x == 32.1
    assert model.y == 32.1
    assert isinstance(model.spatial_reference, geok.core.SpatialReferenceModel)
    assert hasattr(model.spatial_reference, 'wkid')
    assert model.spatial_reference.wkid == 4326 

# TODO: all tests below
# def test_aliased_json():
#     pass


# def test_server():
#     pass


# def test_rest_info():
#     pass


# def test_layer():
#     pass


# def test_esri_version():
#     pass


# def test_stats():
#     pass


# def test_point():
#     pass


# def test_multipoint():
#     pass


# def test_polyline():
#     pass


# def test_polygon():
#     pass


# def test_multipolygon():
#     pass


# def test_sr():
#     pass


# def test_publishing():
#     pass
