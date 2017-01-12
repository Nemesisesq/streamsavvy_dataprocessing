from neo4j.v1 import GraphDatabase, basic_auth
from pymongo import MongoClient

from data_processor.models import Content
from data_processor.serializers import MigrationContentSerializer
from streamsavvy_dataprocessing.settings import get_env_variable


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def convert_content_pg_mongoneo():
    mongo_url = get_env_variable("MONGODB_URI")
    neo_url = get_env_variable("NEO4JBOLT")

    mongo_client = MongoClient(mongo_url)
    auth_token = basic_auth("nem", "prelude")
    driver = GraphDatabase.driver(neo_url, auth=auth_token)

    session = driver.session()

    db_name = get_env_variable("MGO_CONTENT_DB")

    db = mongo_client[db_name]
    collection = db.shows

    shows = Content.objects.all()

    shows = chunks(shows, 20)

    for i in shows:
        session.begin_transaction()
        tx = session.transaction
        show_json = MigrationContentSerializer(i, many=True).data

        save_block_to_neo(collection, show_json, tx)

        tx.commit()

    return "it worked"


def save_block_to_neo(collection, show_json, tx):
    for show in show_json:
        try:
            mongo_id = collection.update_one({"guidebox_data.id": show['guidebox_data']['id']}, {"$set": show},
                                             upsert=True)
        except:
            if show['title'] is not None:
                mongo_id = collection.update_one({"id": show['id']}, {"$set": show}, upsert=True)
            else:
                continue

        if mongo_id.upserted_id is None:
            id = None
            if 'guidebox_data' in show and 'id' in show['guidebox_data']:
                mongo_id = collection.find_one({"guidebox_data.id": show['guidebox_data']['id']})
                id = str(mongo_id['_id'])
        else:
            id = str(mongo_id.upserted_id)

        if mongo_id is not None and id is not None:
            tx.run("MERGE (c:Content {title:{title}}) "
                   "MERGE (m:MongoRecord {mongo_id:{mongo_id}}) "
                   "MERGE (m)-[:DETAIL {source:'guidebox', datastore:'mongodb', mongo_id:{mongo_id}}]->(c) ",
                   {"mongo_id": id, "title": show['title']})

