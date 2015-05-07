from rest_framework import pagination
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from lizard_efcis import models


class ParameterGroepSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.CharField(source='code')
    class Meta:
        model = models.ParameterGroep
        fields = ('id', 'code', 'children', 'text')


class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Parameter
        fields = ('id', 'par_oms')


class MeetnetSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.CharField(source='code')
    class Meta:
        model = models.Meetnet
        fields = ('id', 'code', 'children', 'text')


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
    moment = serializers.DateTimeField(format='%d-%m-%Y')

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
                  'par_oms')


class PaginatedOpnameSerializer(pagination.BasePaginationSerializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')
    count = serializers.ReadOnlyField(source='paginator.count')

    class Meta:
        object_serializer_class = OpnameSerializer


class LocatieSerializer(gis_serializers.GeoFeatureModelSerializer):
    geo_punt_1 = gis_serializers.GeometryField(source='geo_punt1')
    color_value = serializers.SerializerMethodField()
    latest_value = serializers.SerializerMethodField()

    def get_color_value(self, obj):
        return self.context['color_values'].get(obj.id)

    def get_latest_value(self, obj):
        return self.context['latest_values'].get(obj.id)

    class Meta:
        model = models.Locatie
        fields = ('id', 'loc_id', 'loc_oms', 'color_value', 'latest_value')
        geo_field = 'geo_punt_1'
