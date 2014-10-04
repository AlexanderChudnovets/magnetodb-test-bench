import json
import random
import string
import locust
from gevent import GreenletExit
from locust import task
import config as cfg
import ks_config as kscfg
import queries as qry

table_10_fields_no_lsi_list = []
table_10_fields_1_lsi_list = []

key_10_fields_no_lsi_list = []
key_10_fields_1_lsi_list = []

PROJECT_ID = kscfg.PROJECT_ID


class UserBehavior(locust.TaskSet):

    def on_start(self):
        self.load_table_list()
        self.load_item_key_list()

    def on_stop(self):
        pass

    def run(self, *args, **kwargs):
        try:
            super(UserBehavior, self).run(args, kwargs)
        except GreenletExit:
            if hasattr(self, "on_stop"):
                self.on_stop()
            raise

    def random_name(self, length):
        return ''.join(random.choice(string.lowercase + string.digits)
                       for i in range(length))

    def load_table_list(self):
        global table_10_fields_no_lsi_list
        global table_10_fields_1_lsi_list

        with open(cfg.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_10_fields_no_lsi_list = table_list['table_10_fields_no_lsi']
            table_10_fields_1_lsi_list = table_list['table_10_fields_1_lsi']

    def load_item_key_list(self):
        global key_10_fields_no_lsi_list
        global key_10_fields_1_lsi_list

        with open(cfg.ITEM_KEY_LIST) as item_key_list_file:
            item_key_list = json.load(item_key_list_file)
            key_10_fields_no_lsi_list = item_key_list['key_10_fields_no_lsi']
            key_10_fields_1_lsi_list = item_key_list['key_10_fields_1_lsi']


    ########## Update Item: insert new, put action, 1 attribute to be updated,
    # without expected conditions, return none
    @task(1)
    def update_item_new_item_1_attr_no_expected_return_none_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        query = qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        subject_key = self.random_name(20)
        last_postby = self.random_name(20)
        self.client.post(req_url,
                         query % (subject_key, last_postby),
                         headers=kscfg.req_headers,
                         name="update_item_new_item_1_attr_no_expected_return_none_10_fields")

    ########## Update Item: insert new, put action, 5 attributes to be updated,
    # without expected conditions, return none
    @task(1)
    def update_item_new_item_5_attr_no_expected_return_none_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        query = qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        subject_key = self.random_name(20)
        last_postby = self.random_name(20)
        additional_field_1 = self.random_name(20)
        additional_field_2 = self.random_name(20)
        additional_field_3 = self.random_name(20)
        additional_field_4 = self.random_name(20)
        self.client.post(req_url,
                         query % (
                             subject_key, last_postby, additional_field_1,
                         additional_field_2, additional_field_3,
                         additional_field_4),
                         headers=kscfg.req_headers,
                         name="update_item_new_item_5_attr_no_expected_return_none_10_fields")

    ########## Update Item: update existing, put action, 1 attribute to be updated  #############
    ##########              with or w/o expected conditions, return none or all_old #############
    @task(1)
    def update_item_existing_1_attr_no_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby = self.random_name(20)
            self.client.post(req_url, query % (subject_key, last_postby),
                             headers=kscfg.req_headers, name="update_item_existing_1_attr_no_expected_return_none_10_fields")


    @task(1)
    def update_item_existing_1_attr_no_expected_return_all_old_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_1_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_1_LSI_RQ
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby = self.random_name(20)
            self.client.post(req_url, query % (subject_key, last_postby),
                             headers=kscfg.req_headers, name="update_item_existing_1_attr_no_expected_return_all_old_10_fields")


    @task(1)
    def update_item_existing_1_attr_1_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        query = qry.UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            last_postby = self.random_name(20)
            resp = self.client.post(req_url, query % (
                subject_key, last_postby, last_postby_expected),
                headers=kscfg.req_headers,
                name="update_item_existing_1_attr_1_expected_return_none_10_fields")
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = last_postby

    @task(1)
    def update_item_existing_1_attr_1_expected_return_all_old_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_1_ATTR_1_EXPECTED_RETURN_ALL_OLD_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            last_postby = self.random_name(20)
            resp = self.client.post(req_url, query % (subject_key, last_postby, last_postby_expected),
                                    headers=kscfg.req_headers, name="update_item_existing_1_attr_1_expected_return_all_old_10_fields")
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = last_postby

    ########## Update Item: update existing, put action, 5 attributes to be updated:#############
    ##########              with or w/o expected conditions, return none or all_old #############
    @task(1)
    def update_item_existing_5_attr_no_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby = self.random_name(20)
            additional_field_1 = self.random_name(20)
            additional_field_2 = self.random_name(20)
            additional_field_3 = self.random_name(20)
            additional_field_4 = self.random_name(20)

            self.client.post(req_url,
                             query % (
                                 subject_key, last_postby, additional_field_1, additional_field_2, additional_field_3,
                                 additional_field_4),
                             headers=kscfg.req_headers,
                             name="update_item_existing_5_attr_no_expected_return_none_10_fields")


    @task(1)
    def update_item_existing_5_attr_no_expected_return_all_old_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_5_ATTR_NO_EXPECTED_RETURN_ALL_OLD_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby = self.random_name(20)
            additional_field_1 = self.random_name(20)
            additional_field_2 = self.random_name(20)
            additional_field_3 = self.random_name(20)
            additional_field_4 = self.random_name(20)
            self.client.post(req_url,
                             query % (
                                 subject_key, last_postby, additional_field_1, additional_field_2, additional_field_3,
                                 additional_field_4),
                             headers=kscfg.req_headers,
                             name="update_item_existing_5_attr_no_expected_return_all_old_10_fields")


    @task(1)
    def update_item_existing_5_attr_5_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            last_postby = self.random_name(20)
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_1 = self.random_name(20)
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_2 = self.random_name(20)
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_3 = self.random_name(20)
            additional_field_4_expected = attribute_key["AdditionalField4"]
            additional_field_4 = self.random_name(20)

            resp = self.client.post(req_url,
                                    query % (
                                    subject_key,
                                    last_postby,
                                    additional_field_1,
                                    additional_field_2,
                                    additional_field_3,
                                    additional_field_4,
                                    last_postby_expected,
                                    additional_field_1_expected,
                                    additional_field_2_expected,
                                    additional_field_3_expected,
                                    additional_field_4_expected
                                ),
                                headers=kscfg.req_headers,
                                name="update_item_existing_5_attr_5_expected_return_none_10_fields"
            )
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = last_postby
                attribute_key["AdditionalField1"] = additional_field_1
                attribute_key["AdditionalField2"] = additional_field_2
                attribute_key["AdditionalField3"] = additional_field_3
                attribute_key["AdditionalField4"] = additional_field_4


    @task(1)
    def update_item_existing_5_attr_5_expected_return_all_old_10_fields(
            self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_ALL_OLD_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_5_ATTR_5_EXPECTED_RETURN_ALL_OLD_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            last_postby = self.random_name(20)
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_1 = self.random_name(20)
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_2 = self.random_name(20)
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_3 = self.random_name(20)
            additional_field_4_expected = attribute_key["AdditionalField4"]
            additional_field_4 = self.random_name(20)

            resp = self.client.post(req_url,
                                    query % (
                                        subject_key,
                                        last_postby,
                                        additional_field_1,
                                        additional_field_2,
                                        additional_field_3,
                                        additional_field_4,
                                        last_postby_expected,
                                        additional_field_1_expected,
                                        additional_field_2_expected,
                                        additional_field_3_expected,
                                        additional_field_4_expected
                                    ),
                                    headers=kscfg.req_headers,
                                    name="update_item_existing_5_attr_5_expected_return_all_old_10_fields"
            )
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = last_postby
                attribute_key["AdditionalField1"] = additional_field_1
                attribute_key["AdditionalField2"] = additional_field_2
                attribute_key["AdditionalField3"] = additional_field_3
                attribute_key["AdditionalField4"] = additional_field_4

    ########## Update Item: update existing, delete action                               #############
    ##########              attribute to be deleted: 1 or 5, expected conditions: 1 or 5 #############
    @task(1)
    def update_item_delete_existing_1_attr_1_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_DELETE_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_DELETE_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            if last_postby_expected is None:
                return

            resp = self.client.post(req_url, query % (
                subject_key, last_postby_expected),
                headers=kscfg.req_headers,
                name="update_item_delete_existing_1_attr_1_expected_return_none_10_fields")
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = None

    @task(1)
    def update_item_delete_existing_5_attr_5_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_DELETE_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_DELETE_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_4_expected = attribute_key["AdditionalField4"]
            if not all([last_postby_expected,
                        additional_field_1_expected,
                        additional_field_2_expected,
                        additional_field_3_expected,
                        additional_field_4_expected]):
                return

            resp = self.client.post(req_url, query % (
                subject_key, last_postby_expected, additional_field_1_expected,
                additional_field_2_expected, additional_field_3_expected,
                additional_field_4_expected),
                headers=kscfg.req_headers,
                name="update_item_delete_existing_5_attr_5_expected_return_none_10_fields")
            if resp.status_code == 200:
                attribute_key["LastPostedBy"] = None
                attribute_key["AdditionalField1"] = None
                attribute_key["AdditionalField2"] = None
                attribute_key["AdditionalField3"] = None
                attribute_key["AdditionalField4"] = None

    ########## Update Item: update existing, add action (atomic counter)               #############
    ##########              attribute to be added: 1 or 5, expected conditions: 1 or 5 #############
    @task(1)
    def update_item_add_count_existing_1_attr_1_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_COUNT_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_COUNT_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            if last_postby_expected is None:
                return

            resp = self.client.post(req_url, query % (
                subject_key, last_postby_expected),
                headers=kscfg.req_headers,
                name="update_item_add_count_existing_1_attr_1_expected_return_none_10_fields")

    @task(1)
    def update_item_add_count_existing_5_attr_5_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_COUNT_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_COUNT_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_4_expected = attribute_key["AdditionalField4"]
            if not all([last_postby_expected,
                        additional_field_1_expected,
                        additional_field_2_expected,
                        additional_field_3_expected,
                        additional_field_4_expected]):
                return

            resp = self.client.post(req_url, query % (
                subject_key, last_postby_expected, additional_field_1_expected,
                additional_field_2_expected, additional_field_3_expected,
                additional_field_4_expected),
                headers=kscfg.req_headers,
                name="update_item_add_count_existing_5_attr_5_expected_return_none_10_fields")


    ########## Update Item: update existing, add action (set)                          #############
    ##########              attribute to be added: 1 or 5, expected conditions: 1 or 5 #############
    @task(1)
    def update_item_add_set_existing_1_attr_1_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_SET_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_SET_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            if last_postby_expected is None:
                return

            add_set = self.random_name(20)
            resp = self.client.post(req_url, query % (
                subject_key, add_set, last_postby_expected),
                headers=kscfg.req_headers,
                name="update_item_add_set_existing_1_attr_1_expected_return_none_10_fields")

    @task(1)
    def update_item_add_set_existing_5_attr_5_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_SET_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_SET_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_4_expected = attribute_key["AdditionalField4"]
            if not all([last_postby_expected,
                        additional_field_1_expected,
                        additional_field_2_expected,
                        additional_field_3_expected,
                        additional_field_4_expected]):
                return

            add_set = self.random_name(20)
            resp = self.client.post(req_url, query % (
                subject_key, add_set,
                last_postby_expected, additional_field_1_expected,
                additional_field_2_expected, additional_field_3_expected,
                additional_field_4_expected),
                headers=kscfg.req_headers,
                name="update_item_add_set_existing_5_attr_5_expected_return_none_10_fields")

    ########## Update Item: update existing, add action (map)                          #############
    ##########              attribute to be added: 1 or 5, expected conditions: 1 or 5 #############
    @task(1)
    def update_item_add_map_existing_1_attr_1_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_MAP_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_MAP_1_ATTR_1_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            if last_postby_expected is None:
                return

            add_map_key = self.random_name(20)
            add_map_val = self.random_name(20)
            resp = self.client.post(req_url, query % (
                subject_key, add_map_key, add_map_val, last_postby_expected),
                headers=kscfg.req_headers,
                name="update_item_add_map_existing_1_attr_1_expected_return_none_10_fields")

    @task(1)
    def update_item_add_map_existing_5_attr_5_expected_return_none_10_fields(self):
        table_name = random.choice(table_10_fields_no_lsi_list
                                   if cfg.NO_LSI else table_10_fields_1_lsi_list)
        key_list = key_10_fields_no_lsi_list if cfg.NO_LSI else key_10_fields_1_lsi_list
        query = qry.UPDATE_ITEM_ADD_MAP_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_NO_LSI_RQ if cfg.NO_LSI else qry.UPDATE_ITEM_ADD_MAP_5_ATTR_5_EXPECTED_RETURN_NONE_10_FIELDS_1_LSI_RQ
        req_url = ('/v1/' +
                   PROJECT_ID +
                   '/data/tables/' + table_name + '/update_item')
        if len(key_list) > 0:
            attribute_key = random.choice(key_list)
            subject_key = attribute_key["Subject"]
            last_postby_expected = attribute_key["LastPostedBy"]
            additional_field_1_expected = attribute_key["AdditionalField1"]
            additional_field_2_expected = attribute_key["AdditionalField2"]
            additional_field_3_expected = attribute_key["AdditionalField3"]
            additional_field_4_expected = attribute_key["AdditionalField4"]
            if not all([last_postby_expected,
                        additional_field_1_expected,
                        additional_field_2_expected,
                        additional_field_3_expected,
                        additional_field_4_expected]):
                return

            add_map_key = self.random_name(20)
            add_map_val = self.random_name(20)
            resp = self.client.post(req_url, query % (
                subject_key, add_map_key, add_map_val,
                last_postby_expected, additional_field_1_expected,
                additional_field_2_expected, additional_field_3_expected,
                additional_field_4_expected),
                headers=kscfg.req_headers,
                name="update_item_add_map_existing_5_attr_5_expected_return_none_10_fields")


class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = cfg.MIN_WAIT
    max_wait = cfg.MAX_WAIT


IS_FIRST_RUN = True
# Master code
def on_slave_report(client_id, data):
    global IS_FIRST_RUN
    runner = locust.runners.locust_runner

    if IS_FIRST_RUN and runner.slave_count == cfg.SLAVE_COUNT:
        runner.start_hatching(cfg.LOCUST_COUNT, cfg.HATCH_RATE)
        IS_FIRST_RUN = False

    num_rq = sum([val.num_requests + val.num_failures for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report
