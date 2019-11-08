from django.db import connection
from rest_framework.response import Response
from rest_framework import viewsets, status

from eventapp.models import Event
from api.v1.serializers import EventSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    model = Event
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @staticmethod
    def add_pagination(page, per_page, sql):
        if per_page:
            sql += 'LIMIT {} '.format(per_page)
        else:
            sql += 'LIMIT 25 '
        if page:
            sql += 'OFFSET {}'.format(int(page) * 100)

        return sql

    @staticmethod
    def __group_by_control_for_select_clause(group_by, shows, addition_to_select):
        if group_by:
            for show in shows:
                if show not in ['tp', 'date', 'country', 'name']:
                    addition_to_select += "sum({}) as {}, ".format(show, show)
                elif show != 'tp':
                    addition_to_select += "array_agg(DISTINCT CONCAT({})) as {}, ".format(show, show)
            addition_to_select += "{}".format(group_by)

        elif shows and 'tp' not in shows:
            addition_to_select += "{},".format(','.join(shows))

        return addition_to_select

    def __create_select_clause( self, show, group_by, ):

        sql = 'SELECT {} FROM eventapp_event '
        addition_to_select = ''

        shows = show and show.split(',') or []

        if 'tp' in shows:
            addition_to_select = 'CAST(sum(revenue) AS FLOAT)/CAST(sum(ticket_count) AS FLOAT) as tp ,'

        addition_to_select = self.__group_by_control_for_select_clause(group_by, shows, addition_to_select)

        # delete unnecessary semicolon
        addition_to_select = addition_to_select[:-1] if addition_to_select[-1:] == ',' else addition_to_select

        sql = sql.format(addition_to_select) if addition_to_select else sql.format('*')

        return sql

    @staticmethod
    def __add_group_by(group_by):
        if group_by:
            return "GROUP BY " + "{} ".format(group_by)

    @staticmethod
    def __add_sort_by(sort_by):
        if sort_by:
            sort_by = sort_by.split(':')
            if len(sort_by) == 2:
                return " ORDER BY {} {} ".format(sort_by[0], sort_by[1])
            else:
                return " ORDER BY {} ".format(sort_by[0])

    def create_sql(self, request):
        where_condition = []

        sql = self.__create_select_clause(request.GET.get('show'), request.GET.get('group_by'))

        '''Creating where clause'''
        if request.GET.get('date_to'):
            where_condition.append("date <= '{}' ".format(request.GET.get('date_to')))

        if request.GET.get('date_from'):
            where_condition.append("date >= '{}' ".format(request.GET.get('date_from')))

        if request.GET.get('name'):
            where_condition.append(" OR ".join(
                map(lambda x: "name = '{}'".format(x), request.GET.get('name').split(','))))

        if request.GET.get('country'):
            where_condition.append(" OR ".join(
                map(lambda x: "country = '{}'".format(x), request.GET.get('country').split(','))))

        if where_condition:
            sql += ' WHERE '
            sql += ' AND '.join(where_condition)
        sql += self.__add_group_by(request.GET.get('group_by')) or ''
        sql += self.__add_sort_by(request.GET.get('sort_by')) or ''

        return self.add_pagination(request.GET.get('page'), request.GET.get('per_page'), sql)

    def list(self, request,  *args, **kwargs):

        with connection.cursor() as cursor:
            try:
                cursor.execute("{}".format(self.create_sql(request)))
                columns = [col[0] for col in cursor.description]
                return Response([
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ], status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)


