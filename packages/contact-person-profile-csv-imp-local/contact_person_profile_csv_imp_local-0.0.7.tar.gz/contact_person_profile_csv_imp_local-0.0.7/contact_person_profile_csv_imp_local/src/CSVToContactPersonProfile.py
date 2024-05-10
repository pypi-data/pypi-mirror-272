import csv
import os

from contact_local.contact_local import ContactsLocal
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
# from text_block_local.text_block import TextBlocks
from user_context_remote.user_context import UserContext

CSV_LOCAL_PYTHON_COMPONENT_ID = 198
CSV_LOCAL_PYTHON_COMPONENT_NAME = 'contact-person-profile-csv-imp-local-python-package'

obj = {
    'component_id': CSV_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': CSV_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'sahar.g.m@circ.zone'
}

logger = Logger.create_logger(object=obj)
user_context = UserContext()

CLASS_NAME = "CSVToContactPersonProfile"


# Those methods should be called from the common method for this repo (contact-person-profile-csv-imp-local-python-package and google-contact-sync ...)

# TODO def process_first_name( original_first_name: str) -> str: (move to people-local-python-package)
#     normilized_first_name = the first word in original_first_name
#     GroupsLocal.add_update_group_and_link_to_contact( normilized_first_name, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case
#     return normilized_first_name

# TODO def process_last_name( original_last_name : str) -> str: (move to people-local-python-package)
#     normilized_last_name = Remove all the digits from the last_name
#     GroupsLocal.add_update_group_and_link_to_contact( normilized_last_name, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case

# TODO def process_phone( original_phone_number: str) -> str: (move to phone-local-python-package)
#     phone_id, normalized_phone = PhonesLocal.link_phone_to_contact( normilized_phone, contact_id) # Please use method written by @akiva and return normalized_phone_number

# TODO def process_job_title( job_title: str) -> str: (move to people-local-python-package)
#     normalized_job_title = GroupsLocal.add_update_group_and_link_to_contact( job_title, is_group=true, contact_id) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_email_address( email_address: str)
#          """ Returned email_address_id, domain_name, organization_name """
#           DomainsLocal.link_contact_to_domain( contact_id, domain_name )

# TODO def process_organization( organization_name: str, email_address: str) -> str: (move to people-local-python-package
#     if organization_name == None or empty
#          organization_name = extract_organization_from_email_address( email_address)
#     normalized_organization_name = GroupsLocal.add_update_group_and_link_to_contact( organization_name, is_organization=true) # When checking if the organization exists, remove suffix such as Ltd, Inc, בעמ... when searching ignore the uppper-case lower-case

# TODO def process_department( department_name: str) -> str: (move to people-local-python-package
#     normalized_department_name = GroupsLocal.add_update_group_and_link_to_contact( department_name, is_department=true) # When searching ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_continent( continent_name: str) -> str: (move to location-local-python-package)
#     continent_id, normalized_continent_name = GroupsLocal.add_update_group_and_link_to_contact( continent_name, is_continent=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_country( country_name: str) -> str: (move to location-local-python-package)
#     country_id, normalized_country_name = GroupsLocal.add_update_group_and_link_to_contact( country_name, is_country=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_state( state_name: str) -> str: (move to location-local-python-package)
#     state_id, normalized_state_name = GroupsLocal.add_update_group_and_link_to_contact( state_name, is_state=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_county_in_state( county_in_state_name_id: id) -> str: (move to location-local-python-package)
#     country_id, normalized_county_name = GroupsLocal.add_update_group_and_link_to_contact( county_in_state_id, is_county=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_region( region_name: str) -> str: (move to location-local-python-package)
#     region_id, normalized_region_name = GroupsLocal.add_update_group_and_link_to_contact( region_name, is_region=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_neighbourhood_in_city( neighbourhood_in_city_id: str) -> str: (move to location-local-python-package)
#     neighbourhood_id, normalized_neighbourhood_name = GroupsLocal.add_update_group_and_link_to_contact( neighbourhood_in_city_id, is_neighbourhood=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_street_in_city( street_in_city_id: int) -> str: (move to location-local-python-package)
#     street_id, normalized_street_name = GroupsLocal.add_update_group_and_link_to_contact( street_in_city_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_building_in_street( location_id: int) -> str: (move to location-local-python-package)
#     location_id, normalized_building_address_name = GroupsLocal.add_update_group_and_link_to_contact( location_id, is_street=true) # When checking if exists, ignore the upper-case lower-case, return the value with is_main == true

# TODO def process_website


class CSVToContactPersonProfile(GenericCRUD):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="field", default_id_column_name="field_id",
                         default_table_name="field_table", default_view_table_name="field_view",
                         is_test_data=is_test_data)

    def __get_fields_name_from_csv(self, data_source_id: int) -> dict:
        logger.start(object={'data_source_id': data_source_id})

        mapping = {
            'first_name': {"field_name": 'First Name'},
            'last_name': {"field_name": 'Last Name'},
            'name_prefix': {"field_name": 'Name Prefix'},
            'additional_name': {"field_name": 'Additional Name'},
            'name_suffix': {"field_name": 'Name Suffix'},
            'nickname': {"field_name": 'Nickname'},
            'full_name': {"field_name": 'Name'},
            'title': {"field_name": 'Education/University'},
            'phone1': {"field_name": 'Phone Number', "index": 1},
            'phone2': {"field_name": 'Phone Number', "index": 2},
            'phone3': {"field_name": 'Phone Number', "index": 3},
            'birthday': {"field_name": 'Birthday'},
            'hashtag': {"field_name": 'Hashtag'},
            'notes': {"field_name": 'Notes'},
            'email1': {"field_name": 'Email', "index": 1},
            'email2': {"field_name": 'Email', "index": 2},
            'email3': {"field_name": 'Email', "index": 3},
            'website1': {"field_name": 'Website', "index": 1},
            'website2': {"field_name": 'Website', "index": 2},
            'website3': {"field_name": 'Website', "index": 3},
            'display_as': {"field_name": 'Display As'},
            'job_title': {"field_name": 'Job Title'},
            'organization': {"field_name": 'Organization/Company'},
            'department': {"field_name": 'Department'},
            'handle': {"field_name": 'LinkedIn Profile ID'},
            'address1_street': {"field_name": 'Home Street'},
            'address1_city': {"field_name": 'City'},
            'address1_state': {"field_name": 'State'},
            'address1_postal_code': {"field_name": 'Home Postal Code'},
            'address1_country': {"field_name": 'Country'},
            'address2_street': {"field_name": 'Home Street 2'},
            'address2_city': {"field_name": 'Other City'},
            'address2_state': {"field_name": 'Other State'},
            'address2_postal_code': {"field_name": 'Other Postal Code'},
            'address2_country': {"field_name": 'Other Country/Region'},
        }
        contact_from_file_dict = {key: self.get_external_csv_field_name(
            data_source_id=data_source_id, field_name=value['field_name'], index=value.get('index'))
            for key, value in mapping.items()}

        return contact_from_file_dict

    # # TODO Does this function should be here on in https://github.com/circles-zone/variable-local-python-package/tree/dev/variable_local_python_package/variable_local/src "field/field.py"?
    # def __get_field_name(self, field_id: int, data_source_id: int) -> str:
    #     """
    #     Get the field name from the database
    #     :param field_id: The field ID
    #     :param data_source_id: The data source ID
    #     :return: The field name
    #     """
    #     logger.start(object={'field_id': field_id,
    #                  'data_source_id': data_source_id})

    #     self.set_schema(schema_name="data_source_field")
    #     data_source_field_tuples = self.select_multi_tuple_by_where(view_table_name="data_source_field_view",  
    #                                             select_clause_value="external_field_name",  
    #                                             where="data_source_id = %s AND field_id = %s",  
    #                                             params=(data_source_id, field_id))  

    #     if data_source_field_tuples:
    #         logger.end("success getting feilds")
    #         return data_source_field_tuples[0][0]
    #     return None

    # TODO what are the diff between csv_path and directory_name?
    # ans: csv_path is the full path to the csv file, directory_name is the directory where the csv file is located 

    # TODO I think file name should be after directory_name and csv_path
    # ans: it cannot be after directory_name and csv_path because it is a required parameter 

    # TODO: break this function into smaller functions
    def insert_update_contact_from_csv(
            self, *, data_source_id: int, file_name: str,
            directory_name: str = None, csv_path: str = None) -> dict:
        """
        Insert contacts from CSV file to the database
        :param data_source_id: The data source ID
        :param file_name: The CSV file name
        :param directory_name: The CSV file directory name if it wasent given it will search for the file in the same directory 
        :param csv_path: The CSV file path if it wasent given it will search for the file in the same directory 
        :return: None
        """
        logger.start(object={'data_source_id': data_source_id, 'file_name': file_name,
                             'directort_name': directory_name, 'csv_path': csv_path})

        # TODO Please explain
        # ans: if csv_path is provided then we will use the full path
        # if csv_path is not provided then we will use the directory_name and file_name to create the full path 
        # if directory_name is not provided the assumption is that the file is in the same directory as the script and not in a folder 
        if csv_path is not None:
            csv_file_path = csv_path
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file_path = os.path.join(
                script_dir, directory_name or '', file_name)
        result = {}
        contact_fields_to_keep = (
            'name_prefix', 'additional_name', 'name_suffix', 'nickname', 'full_name', 'title', 'department', 'notes',
            'first_name', 'last_name', 'phone1', 'phone2', 'phone3', 'birthday', 'email1', 'email2', 'email3',
            'hashtag',
            'website1', 'handle', 'address1_street', 'address1_city', 'address1_state', 'address1_postal_code',
            'address1_country', 'address2_street', 'address2_city', 'address2_state', 'address2_postal_code',
            'address2_country', 'job_title', 'organization', 'display_as')
        try:
            with (open(csv_file_path, 'r') as csv_file):
                csv_reader = csv.DictReader(csv_file)
                fields_dictonary = self.__get_fields_name_from_csv(data_source_id)
                keys = list(fields_dictonary.keys())
                for row in csv_reader:
                    csv_keys = list(row.keys())
                    ans = {}

                    for fields in keys:
                        if fields_dictonary[fields] not in csv_keys:
                            continue
                        if fields_dictonary[fields] is not None and isinstance(fields_dictonary[fields], str):
                            ans[fields] = row[fields_dictonary[fields]]
                        else:
                            ans[fields] = None

                        contact_data = {key: ans.get(key) for key in contact_fields_to_keep}
                        contact_data['is_test_data'] = self.is_test_data

                        # TODO Please call get_display_name(first_name, last_name, organization) if display_as is empty

                    # for phone in ['phone1', 'phone2', 'phone3']:  
                    #     if contact_data[phone] is None:
                    #         continue
                    #     phone_data = process_phone(original_phone_number=contact_data[phone])  
                    #     if phone_data is None:
                    #         continue
                    #     else:
                    #         contact_data[phone] = phone_data['normalized_phone_number']  

                    # contact_data['first_name'] = process_first_name(
                    #     original_first_name=contact_data['first_name'])
                    # contact_data['last_name'] = process_last_name(
                    #     original_last_name=contact_data['last_name'])

                    # TODO This should be executed also by Google Contact Sync (please make sure it is in people-local-python-package
                    #   i.e. get_display_name(first_name, last_name, organization) -> str 
                    if contact_data['display_as'] is None:
                        contact_data['display_as'] = contact_data['first_name'] or ""  # prevent None
                        if (contact_data['last_name'] is not None
                                and not contact_data['last_name'].isdigit()):
                            contact_data['display_as'] += " " + contact_data['last_name']
                        if not contact_data['display_as']:
                            contact_data['display_as'] += " " + contact_data['organization']

                        # TODO if contact_data['display_as'] still empty raise?

                    # TODO process_notes( contact_data[notes] )

                    # TODO We should take care of situation which the contact already exists and we need to update it
                    contact_id = ContactsLocal().insert_contact_dict(contact_dict=contact_data)
                    if contact_id:
                        result[contact_id] = contact_data
                    # groups_linked_by_job_title = process_job_title(contact_id=contact_id, job_title=contact_data['job_title'])  
                    # if groups_linked_by_job_title is None:
                    #     logger.info("No groups linked by job title to contact " + str(contact_id))  

                    logger.end("success insert csv")
                return result
        except Exception as err:
            logger.exception("insert from CSV Error:" + str(err), object={'error': str(err)})
            logger.end("failed insert csv", object={'error': str(err)})
            raise err

    # TODO def insert_update_contact_groups_from_contact_notes( contact_notes: str) -> int:
    # TODO Add contact_group with seq, attribute, is_sure using group-local-python-package

    # TODO def process_people_url( people_url ) -> str:
    # TODO Use regex to extract the data from the URL
    # TODO add to user_external using user-external-python-package
    @staticmethod
    def process_url(original_url: str) -> str:
        prefixes = ['http://', 'https://']
        for prefix in prefixes:
            if original_url.startswith(prefix):
                original_url = original_url[len(prefix):]
                break
        if original_url.endswith('/'):
            original_url = original_url[:-1]

        return original_url

    # TODO: add a method to add notes to text_block process them to retrieve the groups and create and link the groups to the user 

    def process_notes(self, contact_note: str) -> None:
        # TODO number_of_system_recommednded_groups_identified_in_contact_notes = get_system_recommended_groups_from_contact_notes( contact_notes: str)

        # TODO loop on all contact URLs/websites
        # TODO process_people_url( process_url( people_url ) )

        # TODO Process emails in the contact notes
        # Add or update the emails as a separate contact if they do not exist in contact_table

        # TODO Process contact notes using text-block-local-python-package

        # TODO Process the date in the contact notes and insert/update the person_milestones_table

        # TODO Process actions items after "---" and insert into action_items_table

        pass

    def get_location_type_id_by_name(self, location_type_name: str) -> int or None:
        """
        Get the location type ID by its name
        :param location_type_name: The location type name
        :return: The location type ID    
        """
        logger.start(object={'location_type_name': location_type_name})

        try:
            self.set_schema(schema_name="location")
            sql_query = "SELECT location_type_id FROM location.location_type_ml_table WHERE title = %s"
            location_type_id = self.cursor.execute(
                sql_query, (location_type_name,))
            if location_type_id:
                logger.end("success getting location type id " + str(location_type_id[0]),
                           object={'location_type_id': location_type_id[0]})
                return location_type_id[4]
            else:
                logger.end(
                    f"failed getting location type id for {location_type_name}", object=location_type_id)
                return None
        except Exception as err:
            logger.exception(f"get_location_type_id_by_name Error: {err}", object={
                'error': str(err)})
            logger.end("failed getting location type id",
                       object={'error': str(err)})
            raise err

    def get_external_csv_field_name(self, data_source_id: int, field_name: str, index: int = None) -> str or None:
        """
        Get the CSV field name by data source ID and field name
        :param data_source_id: The data source ID
        :param field_name: The field name
        :param index: The index of the field
        :return: The CSV field name
        """
        logger.start(
            object={'data_source_id': data_source_id, 'field_name': field_name})
        try:
            self.set_schema(schema_name="data_source_field")
            sql_query = 'SELECT DISTINCT dsft.external_field_name \
                        FROM data_source_field.data_source_field_table AS dsft \
                        JOIN field.field_table AS ft ON dsft.field_id = ft.field_id \
                        WHERE dsft.data_source_id = %s AND ft.name = %s;'
            self.cursor.execute(sql_query, (data_source_id, field_name))
            external_field_name = self.cursor.fetchall()  # return list of tuples
            if external_field_name is None or len(external_field_name) == 0:
                logger.end(f"failed getting external field name for {data_source_id} and {field_name}", object={
                    'data_source_id': data_source_id, 'field_name': field_name})
                return None
            else:
                if index is None:
                    logger.end("success getting external field name " + str(external_field_name[0][0]),
                               object={'external_field_name': external_field_name[0][0]})
                    return external_field_name[0][0]
                else:
                    for name in external_field_name:
                        if str(index) in name[0] or field_name in name[0]:
                            logger.end("success getting external field name " + str(name[0]),
                                       object={'external_field_name': name[0]})
                            return name[0]

        except Exception as err:
            logger.exception(f"get_external_csv_field_name Error: {err}", object={
                'error': str(err)})
            logger.end("failed getting external field name",
                       object={'error': str(err)})
            raise err
