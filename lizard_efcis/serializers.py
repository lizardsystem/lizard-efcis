import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import pagination
from rest_framework import serializers
from rest_framework.reverse import reverse
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

    loc_id = serializers.CharField(
        read_only=True,
        source='locatie.loc_id')
    loc_oms = serializers.CharField(
        read_only=True,
        source='locatie.loc_oms')
    wns_oms = serializers.CharField(
        read_only=True,
        source='wns.wns_oms')
    activiteit = serializers.CharField(
        read_only=True,
        source='activiteit.activiteit')
    detectiegrens = serializers.CharField(
        read_only=True,
        source='detect.teken')
    eenheid_oms = serializers.CharField(
        read_only=True,
        source='wns.eenheid.eenheid_oms')
    comp_oms = serializers.CharField(
        read_only=True,
        source='wns.compartiment.comp_oms')
    hoed_oms = serializers.CharField(
        read_only=True,
        source='wns.hoedanigheid.hoed_oms')
    par_oms = serializers.CharField(
        read_only=True,
        source='wns.parameter.par_oms')

    validatiestatus = serializers.SerializerMethodField()
    grondsoort = serializers.CharField(
        read_only=True,
        source='locatie.grondsoort')
    landgebruik = serializers.CharField(
        read_only=True,
        source='locatie.landgebruik')
    afvoergebied = serializers.CharField(
        read_only=True,
        source='locatie.afvoergebied')
    watertype = serializers.CharField(
        read_only=True,
        source='locatie.watertype.code')

    def get_validatiestatus(self, obj):
        return obj.get_validation_state_display()

    class Meta:
        model = models.Opname
        fields = ('id', 'wns_oms', 'activiteit', 'loc_id',
                  'loc_oms', 'waarde_n', 'waarde_a',
                  'detectiegrens', 'url',
                  'datum', 'tijd',
                  'par_oms',
                  'validatiestatus',
                  'eenheid_oms', 'hoed_oms', 'comp_oms',
                  'grondsoort',
                  'landgebruik',
                  'afvoergebied',
                  'watertype',
                  )


class OpnameDetailSerializer(OpnameSerializer):
    par_code = serializers.CharField(
        read_only=True,
        source='wns.parameter.par_code')
    par_oms = serializers.CharField(
        read_only=True,
        source='wns.parameter.par_oms')
    x1 = serializers.CharField(
        read_only=True,
        source='locatie.x1')
    y1 = serializers.CharField(
        read_only=True,
        source='locatie.y1')
    x2 = serializers.CharField(
        read_only=True,
        source='locatie.x2')
    y2 = serializers.CharField(
        read_only=True,
        source='locatie.y2')
    waterlichaam = serializers.CharField(
        read_only=True,
        source='locatie.waterlichaam.wl_naam')
    watertype = serializers.CharField(
        read_only=True,
        source='locatie.watertype.code')
    status_krw = serializers.CharField(
        read_only=True,
        source='locatie.status_krw.code')
    meetnet = serializers.SerializerMethodField()
    activiteit_type = serializers.CharField(
        read_only=True,
        source='activiteit.act_type')
    uitvoerende = serializers.CharField(
        read_only=True,
        source='activiteit.uitvoerende')
    act_oms = serializers.CharField(
        read_only=True,
        source='activiteit.act_oms')
    met_mafa = serializers.CharField(
        read_only=True,
        source='activiteit.met_mafa')
    met_mafy = serializers.CharField(
        read_only=True,
        source='activiteit.met_mafy')
    met_fyt = serializers.CharField(
        read_only=True,
        source='activiteit.met_fyt')
    met_vis = serializers.CharField(
        read_only=True,
        source='activiteit.met_vis')
    met_fc = serializers.CharField(
        read_only=True,
        source='activiteit.met_fc')
    met_toets = serializers.CharField(
        read_only=True,
        source='activiteit.met_toets')
    eenheid = serializers.CharField(
        read_only=True,
        source='wns.eenheid.eenheid')
    hoedanigheid = serializers.CharField(
        read_only=True,
        source='wns.hoedanigheid.hoedanigheid')
    compartiment = serializers.CharField(
        read_only=True,
        source='wns.compartiment.compartiment')
    wns_code = serializers.CharField(
        read_only=True,
        source='wns.wns_code')
    validatiestatus = serializers.SerializerMethodField()
    grondsoort = serializers.CharField(
        read_only=True,
        source='locatie.grondsoort')
    landgebruik = serializers.CharField(
        read_only=True,
        source='locatie.landgebruik')
    afvoergebied = serializers.CharField(
        read_only=True,
        source='locatie.afvoergebied')
    admin_link = serializers.SerializerMethodField()

    def get_validatiestatus(self, obj):
        return obj.get_validation_state_display()

    def get_meetnet(self, obj):
        meetnetten = obj.locatie.meetnet.all().values_list(
            'code', flat=True)
        return ', '.join(meetnetten)

    def get_admin_link(self, obj):
        if not self.context['show_admin_link']:
            return
        return reverse('admin:lizard_efcis_opname_change',
                       args=(obj.id,),
                       request=self.context['request'])

    class Meta:
        model = models.Opname
        fields = ('wns_oms', 'wns_code', 'activiteit', 'loc_id',
                  'loc_oms', 'waarde_n', 'waarde_a',
                  'detectiegrens', 'par_code',
                  'par_oms',
                  'validatiestatus',
                  'datum', 'tijd', 'meetnet', 'x1', 'y1', 'x2', 'y2',
                  'waterlichaam', 'watertype', 'status_krw',
                  'activiteit_type', 'uitvoerende',
                  'act_oms', 'met_mafa', 'met_mafy', 'met_fyt',
                  'met_vis', 'met_fc', 'met_toets', 'eenheid',
                  'eenheid_oms', 'hoedanigheid', 'hoed_oms',
                  'compartiment', 'comp_oms',
                  'grondsoort',
                  'landgebruik',
                  'afvoergebied',
                  'watertype',
                  'admin_link',
                  'opmerkingen', 'vis_opp_ha', 'vis_kg', 'vis_cm',
        )


class PaginatedOpnameSerializer(pagination.BasePaginationSerializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')
    count = serializers.ReadOnlyField(source='paginator.count')

    class Meta:
        object_serializer_class = OpnameSerializer


class LocatieSerializer(gis_serializers.GeoFeatureModelSerializer):

    geo_punt_2 = gis_serializers.GeometryField(source='geo_punt2')
    geo_punt_1 = gis_serializers.GeometryField(source='geo_punt1')

    class Meta:
        model = models.Locatie
        fields = (
            'id', 'loc_id', 'loc_oms', 'geo_punt_2',
            'waterlichaam', 'watertype', 'status_krw'
        )
        geo_field = 'geo_punt_1'


class JsonDict(dict):
    # Copy/pasted from the 0.9.2+ master version of djangorestframework-gis as
    # it isn't in 0.8 yet.

    def __init__(self, data):
        self._geojson_string = data
        super(JsonDict, self).__init__(json.loads(data))

    def __str__(self):
        return self._geojson_string


class GeometrySerializerMethodField(serializers.SerializerMethodField):
    # Copy/pasted from the 0.9.2+ master version of djangorestframework-gis as
    # it isn't in 0.8 yet.

    def to_representation(self, value):
        value = super(GeometrySerializerMethodField, self).to_representation(value)
        return JsonDict(GEOSGeometry(value).geojson)


class MapSerializer(gis_serializers.GeoFeatureModelSerializer):
    geo_punt_1 = GeometrySerializerMethodField()
    color_value = serializers.SerializerMethodField()
    abs_color_value = serializers.SerializerMethodField()
    latest_value = serializers.SerializerMethodField()
    latest_krw_value = serializers.SerializerMethodField()
    latest_datetime = serializers.SerializerMethodField()
    boxplot_data = serializers.SerializerMethodField()
    is_krw_score = serializers.SerializerMethodField()

    def get_geo_punt_1(self, obj):
        if obj.is_krw_area:
            return obj.area
        else:
            return obj.geo_punt1

    def get_is_krw_score(self, ob):
        return self.context['is_krw_score']

    def get_color_value(self, obj):
        return self.context['color_values'].get(obj.id)

    def get_abs_color_value(self, obj):
        return self.context['abs_color_values'].get(obj.id)

    def get_latest_value(self, obj):
        return self.context['latest_values'].get(obj.id)

    def get_latest_krw_value(self, obj):
        return self.context['latest_krw_values'].get(obj.id)

    def get_latest_datetime(self, obj):
        return self.context['latest_datetimes'].get(obj.id)

    def get_boxplot_data(self, obj):
        return self.context['boxplot_values'].get(obj.id)

    class Meta:
        model = models.Locatie
        fields = ('id', 'loc_id', 'loc_oms', 'color_value', 'latest_value',
                  'latest_krw_value',
                  'abs_color_value',
                  'is_krw_score',
                  'latest_datetime', 'boxplot_data', 'photo_url',
                  'is_krw_area')
        geo_field = 'geo_punt_1'


class KRWAreaSerializer(gis_serializers.GeoFeatureModelSerializer):
    area = gis_serializers.GeometryField()

    class Meta:
        model = models.Locatie
        fields = ('id', 'loc_id', 'loc_oms', 'area')
        geo_field = 'area'
