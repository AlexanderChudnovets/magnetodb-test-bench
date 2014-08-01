import sys

import queries as qry
import put_item_get_query_with_no_table as test


def main(host):
    print "Initializing ..."
    table_name = test.random_name(20)
    test.table_3_fields_no_lsi_list.append(table_name)
    test.create_table_helper(host, table_name,
                             qry.CREATE_TABLE_3_fields_NO_LSI_RQ % table_name)

    table_name = test.random_name(20)
    test.table_3_fields_1_lsi_list.append(table_name)
    test.create_table_helper(host, table_name,
                             qry.CREATE_TABLE_3_fields_1_LSI_RQ % table_name)

    table_name = test.random_name(20)
    test.table_10_fields_5_lsi_list.append(table_name)
    test.create_table_helper(host, table_name,
                             qry.CREATE_TABLE_10_fields_5_LSI_RQ % table_name)

    test.dump_tables_created()
    print "Done."

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s host_url" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1])