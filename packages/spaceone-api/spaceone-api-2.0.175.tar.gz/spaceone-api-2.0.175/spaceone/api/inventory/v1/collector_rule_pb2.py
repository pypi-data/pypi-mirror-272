# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory/v1/collector_rule.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v2 import query_pb2 as spaceone_dot_api_dot_core_dot_v2_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.spaceone/api/inventory/v1/collector_rule.proto\x12\x19spaceone.api.inventory.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"F\n\x16\x43ollectorRuleCondition\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08operator\x18\x03 \x01(\t\"+\n\tMatchRule\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"\xe6\x01\n\x14\x43ollectorRuleActions\x12\x16\n\x0e\x63hange_project\x18\x01 \x01(\t\x12;\n\rmatch_project\x18\x02 \x01(\x0b\x32$.spaceone.api.inventory.v1.MatchRule\x12\x43\n\x15match_service_account\x18\x03 \x01(\x0b\x32$.spaceone.api.inventory.v1.MatchRule\x12\x34\n\x13\x61\x64\x64_additional_info\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"/\n\x14\x43ollectorRuleOptions\x12\x17\n\x0fstop_processing\x18\x01 \x01(\x08\"\xfa\x02\n\x1a\x43reateCollectorRuleRequest\x12\x14\n\x0c\x63ollector_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x45\n\nconditions\x18\x03 \x03(\x0b\x32\x31.spaceone.api.inventory.v1.CollectorRuleCondition\x12\x46\n\x11\x63onditions_policy\x18\x04 \x01(\x0e\x32+.spaceone.api.inventory.v1.ConditionsPolicy\x12@\n\x07\x61\x63tions\x18\x05 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleActions\x12@\n\x07options\x18\x06 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleOptions\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xff\x02\n\x1aUpdateCollectorRuleRequest\x12\x19\n\x11\x63ollector_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x45\n\nconditions\x18\x03 \x03(\x0b\x32\x31.spaceone.api.inventory.v1.CollectorRuleCondition\x12\x46\n\x11\x63onditions_policy\x18\x04 \x01(\x0e\x32+.spaceone.api.inventory.v1.ConditionsPolicy\x12@\n\x07\x61\x63tions\x18\x05 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleActions\x12@\n\x07options\x18\x06 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleOptions\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\"K\n\x1f\x43hangeCollectorRuleOrderRequest\x12\x19\n\x11\x63ollector_rule_id\x18\x01 \x01(\t\x12\r\n\x05order\x18\x02 \x01(\x05\"1\n\x14\x43ollectorRuleRequest\x12\x19\n\x11\x63ollector_rule_id\x18\x01 \x01(\t\"\x99\x02\n\x12\x43ollectorRuleQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x19\n\x11\x63ollector_rule_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12I\n\trule_type\x18\x04 \x01(\x0e\x32\x36.spaceone.api.inventory.v1.CollectorRuleQuery.RuleType\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\x12\x14\n\x0c\x63ollector_id\x18\x16 \x01(\t\"7\n\x08RuleType\x12\x12\n\x0eRULE_TYPE_NONE\x10\x00\x12\x0b\n\x07MANAGED\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\"\xf4\x05\n\x11\x43ollectorRuleInfo\x12\x19\n\x11\x63ollector_rule_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12H\n\trule_type\x18\x03 \x01(\x0e\x32\x35.spaceone.api.inventory.v1.CollectorRuleInfo.RuleType\x12\r\n\x05order\x18\x04 \x01(\x05\x12\x45\n\nconditions\x18\x05 \x03(\x0b\x32\x31.spaceone.api.inventory.v1.CollectorRuleCondition\x12\x46\n\x11\x63onditions_policy\x18\x06 \x01(\x0e\x32+.spaceone.api.inventory.v1.ConditionsPolicy\x12@\n\x07\x61\x63tions\x18\x07 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleActions\x12@\n\x07options\x18\x08 \x01(\x0b\x32/.spaceone.api.inventory.v1.CollectorRuleOptions\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12R\n\x0eresource_group\x18\x14 \x01(\x0e\x32:.spaceone.api.inventory.v1.CollectorRuleInfo.ResourceGroup\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x14\n\x0c\x63ollector_id\x18\x17 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"7\n\x08RuleType\x12\x12\n\x0eRULE_TYPE_NONE\x10\x00\x12\x0b\n\x07MANAGED\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\"h\n\x12\x43ollectorRulesInfo\x12=\n\x07results\x18\x01 \x03(\x0b\x32,.spaceone.api.inventory.v1.CollectorRuleInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"N\n\x16\x43ollectorRuleStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery*:\n\x10\x43onditionsPolicy\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03\x41LL\x10\x01\x12\x07\n\x03\x41NY\x10\x02\x12\n\n\x06\x41LWAYS\x10\x03\x32\xb2\x08\n\rCollectorRule\x12\x9d\x01\n\x06\x63reate\x12\x35.spaceone.api.inventory.v1.CreateCollectorRuleRequest\x1a,.spaceone.api.inventory.v1.CollectorRuleInfo\".\x82\xd3\xe4\x93\x02(\"#/inventory/v1/collector-rule/create:\x01*\x12\x9d\x01\n\x06update\x12\x35.spaceone.api.inventory.v1.UpdateCollectorRuleRequest\x1a,.spaceone.api.inventory.v1.CollectorRuleInfo\".\x82\xd3\xe4\x93\x02(\"#/inventory/v1/collector-rule/update:\x01*\x12\xae\x01\n\x0c\x63hange_order\x12:.spaceone.api.inventory.v1.ChangeCollectorRuleOrderRequest\x1a,.spaceone.api.inventory.v1.CollectorRuleInfo\"4\x82\xd3\xe4\x93\x02.\")/inventory/v1/collector-rule/change-order:\x01*\x12\x81\x01\n\x06\x64\x65lete\x12/.spaceone.api.inventory.v1.CollectorRuleRequest\x1a\x16.google.protobuf.Empty\".\x82\xd3\xe4\x93\x02(\"#/inventory/v1/collector-rule/delete:\x01*\x12\x91\x01\n\x03get\x12/.spaceone.api.inventory.v1.CollectorRuleRequest\x1a,.spaceone.api.inventory.v1.CollectorRuleInfo\"+\x82\xd3\xe4\x93\x02%\" /inventory/v1/collector-rule/get:\x01*\x12\x93\x01\n\x04list\x12-.spaceone.api.inventory.v1.CollectorRuleQuery\x1a-.spaceone.api.inventory.v1.CollectorRulesInfo\"-\x82\xd3\xe4\x93\x02\'\"\"/inventory/v1/collector-rules/list:\x01*\x12\x81\x01\n\x04stat\x12\x31.spaceone.api.inventory.v1.CollectorRuleStatQuery\x1a\x17.google.protobuf.Struct\"-\x82\xd3\xe4\x93\x02\'\"\"/inventory/v1/collector-rules/stat:\x01*B@Z>github.com/cloudforet-io/api/dist/go/spaceone/api/inventory/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.inventory.v1.collector_rule_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z>github.com/cloudforet-io/api/dist/go/spaceone/api/inventory/v1'
  _globals['_COLLECTORRULE'].methods_by_name['create']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002(\"#/inventory/v1/collector-rule/create:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['update']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002(\"#/inventory/v1/collector-rule/update:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['change_order']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['change_order']._serialized_options = b'\202\323\344\223\002.\")/inventory/v1/collector-rule/change-order:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['delete']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002(\"#/inventory/v1/collector-rule/delete:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['get']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002%\" /inventory/v1/collector-rule/get:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['list']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\'\"\"/inventory/v1/collector-rules/list:\001*'
  _globals['_COLLECTORRULE'].methods_by_name['stat']._loaded_options = None
  _globals['_COLLECTORRULE'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\'\"\"/inventory/v1/collector-rules/stat:\001*'
  _globals['_CONDITIONSPOLICY']._serialized_start=2723
  _globals['_CONDITIONSPOLICY']._serialized_end=2781
  _globals['_COLLECTORRULECONDITION']._serialized_start=200
  _globals['_COLLECTORRULECONDITION']._serialized_end=270
  _globals['_MATCHRULE']._serialized_start=272
  _globals['_MATCHRULE']._serialized_end=315
  _globals['_COLLECTORRULEACTIONS']._serialized_start=318
  _globals['_COLLECTORRULEACTIONS']._serialized_end=548
  _globals['_COLLECTORRULEOPTIONS']._serialized_start=550
  _globals['_COLLECTORRULEOPTIONS']._serialized_end=597
  _globals['_CREATECOLLECTORRULEREQUEST']._serialized_start=600
  _globals['_CREATECOLLECTORRULEREQUEST']._serialized_end=978
  _globals['_UPDATECOLLECTORRULEREQUEST']._serialized_start=981
  _globals['_UPDATECOLLECTORRULEREQUEST']._serialized_end=1364
  _globals['_CHANGECOLLECTORRULEORDERREQUEST']._serialized_start=1366
  _globals['_CHANGECOLLECTORRULEORDERREQUEST']._serialized_end=1441
  _globals['_COLLECTORRULEREQUEST']._serialized_start=1443
  _globals['_COLLECTORRULEREQUEST']._serialized_end=1492
  _globals['_COLLECTORRULEQUERY']._serialized_start=1495
  _globals['_COLLECTORRULEQUERY']._serialized_end=1776
  _globals['_COLLECTORRULEQUERY_RULETYPE']._serialized_start=1721
  _globals['_COLLECTORRULEQUERY_RULETYPE']._serialized_end=1776
  _globals['_COLLECTORRULEINFO']._serialized_start=1779
  _globals['_COLLECTORRULEINFO']._serialized_end=2535
  _globals['_COLLECTORRULEINFO_RESOURCEGROUP']._serialized_start=2411
  _globals['_COLLECTORRULEINFO_RESOURCEGROUP']._serialized_end=2478
  _globals['_COLLECTORRULEINFO_RULETYPE']._serialized_start=1721
  _globals['_COLLECTORRULEINFO_RULETYPE']._serialized_end=1776
  _globals['_COLLECTORRULESINFO']._serialized_start=2537
  _globals['_COLLECTORRULESINFO']._serialized_end=2641
  _globals['_COLLECTORRULESTATQUERY']._serialized_start=2643
  _globals['_COLLECTORRULESTATQUERY']._serialized_end=2721
  _globals['_COLLECTORRULE']._serialized_start=2784
  _globals['_COLLECTORRULE']._serialized_end=3858
# @@protoc_insertion_point(module_scope)
