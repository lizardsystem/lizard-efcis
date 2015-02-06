
from rest_framework import serializers
from rest_framework import pagination

from lizard_efcis import models


class OpnameSerializer(serializers.HyperlinkedModelSerializer):
    
    loc_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='locatie.loc_id')
    loc_oms = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='locatie.loc_oms')
    wns_oms = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='wns.wns_oms')
    activiteit = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='activiteit.activiteit')
    detectiegrens = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='detect.teken')
    class Meta:
        model = models.Opname
        fields = ('wns_oms', 'activiteit', 'loc_id',
                  'loc_oms', 'waarde_n', 'waarde_a',
                  'moment', 'detectiegrens', 'url')


class OpnameDetailSerializer(OpnameSerializer):
    par_code = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='wns.parameter.par_code')
    par_oms = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='wns.parameter.par_oms')

    class Meta:
        model = models.Opname
        fields = ('wns_oms', 'activiteit', 'loc_id',
                  'loc_oms', 'waarde_n', 'waarde_a',
                  'moment', 'detectiegrens', 'par_code',
                  'par_oms', 'url')
    

class PaginatedOpnameSerializer(pagination.BasePaginationSerializer):

    class Meta:
        object_serializer_class = OpnameSerializer
