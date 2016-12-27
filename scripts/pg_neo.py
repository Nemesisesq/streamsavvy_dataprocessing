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
    session.begin_transaction()

    db_name = get_env_variable("MGO_CONTENT_DB")

    db = mongo_client[db_name]
    collection = db.shows

    shows = Content.objects.all()

    shows = chunks(shows, 20)

    for i in shows:

        show_json = MigrationContentSerializer(i, many=True).data

        for show in show_json:
            mongo_id = collection.update_one(show, upsert=True)

            with session.transaction as tx:
                tx.run("MERGE (c:Content {title:{title}})", title=show['title'])
                tx.run("MERGE (m:MongoRecord {mongo_id:{mongo_id}})", mongo_id=mongo_id)
                tx.run("MERGE (m)-[:DETAIL {source:'guidebox', datastore:'mongodb', mongo_id:{mongo_id}}]->(c)", mongo_id=mongo_id)

                tx.commit()

    return "it worked"
