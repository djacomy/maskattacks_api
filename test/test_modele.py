import unittest
import json


from util.loader import import_references
from repository import reference as ref_repo
from model.orga import Reference, ReferenceType
from test.utils.mixins import BaseTest


class TestReferences(BaseTest):
    fixtures = ["users.json"]

    def test_import_references(self):
        import_references()

        self.assertEqual(51, Reference.query.count())

        obj1 = ref_repo.find_reference_by_type_and_code(ReferenceType.capacity_value, "batch30")
        obj2 = ref_repo.find_reference_by_type_and_libelle(ReferenceType.capacity_value, "30 lots")
        self.assertEqual(obj1.id, obj2.id)

        result = ref_repo.get_references()
        self.assertEqual({k: [o["code"] for o in list_obj] for k, list_obj in result.items()},
                         {'orga_status': ['running', 'active', 'suspend', 'rejected'],
                          'orga_availability': ['midtime', 'fulltime', 'na'],
                          'orga_role': ['man', 'tra', 'cus', 'pro'],
                          'manufactor_type': ['cou', 'print3d'],
                          'manufactor_capacity': ['low', 'medium'],
                          'skill_level': ['pro', 'semipro', 'noexp'],
                          'quality_need': ['max', 'good', 'noexp', 'na'],
                          'contract_type': ['volonteer', 'sharedprice', 'sharedprime'],
                          'transporter_type': ['tran'],
                          'capacity_value': ['truck', 'batch30'],
                          'capacity_type': ['class', 'volume', 'units'],
                          'range_type': ['km', 'dept'],
                          'provider_type': ['fm', 'pre', 'ent'],
                          'provider_subtype': ['fta', 'ftb', 'ft3d'],
                          'customer_type': ['med', 'pres', 'ent', 'ins', 'com', 'gsu'],
                          'customer_subtype': ['hop', 'cli', 'soilib', 'enta', 'entb', 'entc']})


if __name__ == '__main__':
    unittest.main()
