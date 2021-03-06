# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bottle import jinja2_template, request, redirect

from findex_gui.controllers.helpers import data_strap
from findex_gui.controllers.request import var_parse
from findex_gui.controllers.views.searcher import Searcher

from findex_common.exceptions import SearchException


class Search():
    def __init__(self, cfg, db):
        self.cfg = cfg
        self.db = db

    @data_strap
    def search(self, env):
        search_vars = var_parse(request.query)
        if 'key' in search_vars:
            try:
                data = Searcher(self.cfg, self.db).search(search_vars)

                results = {-2: [], -1: [], 0: [], 1: [], 2: [], 3: [], 4: []}
                for f in data['results']['data']:
                    if f.file_isdir:
                        results[-2].append(f)
                    else:
                        results[f.file_format].append(f)

                results[-1] = data['results']['data']

                data['results']['data'] = results

                return jinja2_template('main/search_results', env=env, data=data, exception=None)
            except SearchException as ex:
                return jinja2_template('main/search', env=env, message=str(ex))
            except Exception as ex:
                return jinja2_template('main/search', env=env, message='Something went wrong \:D/')

        return jinja2_template('main/search', env=env, message='')