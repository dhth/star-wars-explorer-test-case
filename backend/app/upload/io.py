import csv
import datetime
import json
import uuid
from typing import List

import requests

import petl as etl
from hello_django import settings as app_settings

from .models import Person, PersonCollection
from . import util


def fetch_data(url: str) -> dict:
    """
    Fetches data from url, and returns a dictionary of parsed json.
    """
    try:
        r = requests.get(url)
        return json.loads(r.text)
    except Exception as e:
        util.log(
            "error",
            message="Error fetching data",
            context={"url": url, "error": str(e)},
        )
        return None


def fetch_specific_field(url: str, field_to_fetch: str):
    """
    Fetches a specific field from a url response.
    """
    try:
        r = requests.get(url)
        home_world_data = json.loads(r.text)
        return home_world_data[field_to_fetch]
    except Exception as e:
        util.log(
            "error",
            message="Error fetching field",
            context={"url": url, "field_to_fetch": field_to_fetch, "error": str(e)},
        )


def get_date_from_date_string(date_str: str) -> str:
    """
    Obtains date in the format Y-m-d from a utc date string.
    """
    try:
        date_str_short = datetime.datetime.strptime(
            date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d")
    except Exception:
        date_str_short = None
        util.log("error", message="error parsing date", context={"date_str": date_str})
    return date_str_short


class DataHandler(object):
    """
    Processes API response and saves to relevant destinations.
    """

    def __init__(
        self, fields_to_fetch, csv_file_columns, export_dir, write_to_db=False
    ):
        self.homeworld_dict = {}
        self.field_to_fetch = fields_to_fetch
        self.file_name = f"{str(uuid.uuid4())}.csv"
        self.csv_file_columns = csv_file_columns
        self.export_dir = export_dir
        self.csv_file_name = f"{self.export_dir}/{self.file_name}"

        if write_to_db:
            self.write_to_db = True
        else:
            self.write_to_db = False

        self.setup()

    def setup(self):
        # write headers to CSV file
        etl.tocsv([self.csv_file_columns], self.csv_file_name)

        # create collection in database
        self.person_collection = PersonCollection(
            file_name=self.file_name, date=datetime.datetime.now(datetime.timezone.utc),
        )
        self.person_collection.save()

    def get_person_data(self, person_object_from_api):
        """
        Fetch relevant fields from person_object_from_api.
        Do necessary tranformations as per requirements.
        Resolve homeworld, and extract date from field 'edited'.
        """
        person_data = {
            field: person_object_from_api[field] for field in self.field_to_fetch
        }
        if self.homeworld_dict.get(person_object_from_api["homeworld"], -1) == -1:
            # homeworld not resolved, fetch it
            self.homeworld_dict["homeworld"] = fetch_specific_field(
                person_object_from_api["homeworld"], "name"
            )
        person_data["homeworld"] = self.homeworld_dict["homeworld"]
        person_data["date"] = get_date_from_date_string(
            person_object_from_api["edited"]
        )
        return person_data

    def get_person_row_for_csv(self, person_data):
        return person_data.values()

    def save_to_csv_file(self, processed_person_array):
        list_of_rows = [
            self.get_person_row_for_csv(person_object)
            for person_object in processed_person_array
        ]
        etl.appendcsv(list_of_rows, self.csv_file_name)
        util.log(
            "info",
            message="Saved to file",
            context={"person_collection_id": self.person_collection.id},
        )

    def get_person_object_for_db(self, person_data):
        person = Person(
            person_collection=self.person_collection,
            name=person_data["name"],
            height=person_data["height"],
            mass=person_data["mass"],
            hair_color=person_data["hair_color"],
            skin_color=person_data["skin_color"],
            eye_color=person_data["eye_color"],
            birth_year=person_data["birth_year"],
            gender=person_data["gender"],
            homeworld=person_data["homeworld"],
            date=person_data["date"],
        )
        return person

    def save_to_db(self, person_array):
        list_of_objects = [
            self.get_person_object_for_db(person_data) for person_data in person_array
        ]
        Person.objects.bulk_create(list_of_objects)
        util.log(
            "info",
            message="Saved to db",
            context={"person_collection_id": self.person_collection.id},
        )

    def update_database(self):
        self.person_collection.last_successful_fetch_page += 1
        self.person_collection.date = datetime.datetime.now(datetime.timezone.utc)
        self.person_collection.save()

    def finalize_db(self):
        self.person_collection.data_fetch_complete += True
        self.person_collection.save()
        return self.person_collection

    def save(self, response_object):
        api_response_array = response_object["results"]
        processed_person_array = [
            self.get_person_data(person_object_from_api)
            for person_object_from_api in api_response_array
        ]

        self.save_to_csv_file(processed_person_array)

        if self.write_to_db:
            self.save_to_db(processed_person_array)

        self.update_database()

    def cleanup(self):
        self.person_collection.remove()


def fetch_and_save_data_from_endpoint(start_url: str):
    """
    Fetches data from start_url, saves response to file
    (and database, if configured), and repeats as per API
    pagination.
    """

    next_url = start_url
    pagination_count = 1
    max_pagination_count = 20

    data_handler = DataHandler(
        fields_to_fetch=app_settings.fields_to_fetch,
        csv_file_columns=app_settings.csv_file_columns,
        export_dir=app_settings.export_dir,
        write_to_db=app_settings.use_database_for_storage,
    )
    try:
        while next_url and pagination_count <= max_pagination_count:
            # fetch response from API
            response = fetch_data(next_url)

            # process and save data
            data_handler.save(response)

            # Get next paginated url
            next_url = response["next"]
            pagination_count += 1

        person_collection = data_handler.finalize_db()
        util.log(
            "info",
            message="Finished data fetch",
            context={"person_collection_id": person_collection.id},
        )
    except Exception as e:
        data_handler.cleanup()
        util.log(
            "error",
            message="Error while processing",
            context={"start_url": start_url, "error": str(e)},
        )
        person_collection = None

    # return newly created collection
    return person_collection


def read_specific_lines(csv_reader: csv.reader, lines_list: List[int]):
    """
    Yield specific lines from a file, improves memory usage for
    large files.
    """
    lines_set = set(lines_list)
    for line_number, row in enumerate(csv_reader):
        if line_number in lines_set:
            yield row
            lines_set.remove(line_number)
            if not lines_set:
                break


def get_rows_from_csv_file(
    file_name: str, page_num: int, page_size: int = 10
) -> List[List]:
    """
    Get content from page_size lines in a csv file, paginated via
    page_num.
    """
    lines_to_read = list(
        range(
            page_size * (page_num - 1) + 1, page_size * (page_num - 1) + 1 + page_size
        )
    )
    data = []
    with open(file_name) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in read_specific_lines(csvreader, lines_to_read):
            d = {app_settings.csv_file_columns[i]: value for i, value in enumerate(row)}
            data.append(d)
    return data


def get_value_counts_from_csv_file(
    collection_file_name: str, fields_to_fetch: List[str]
) -> List:
    table_data = etl.fromcsv(collection_file_name)
    value_counts = etl.valuecounts(table_data, *fields_to_fetch)
    return list(etl.cutout(value_counts, "frequency").dicts())
