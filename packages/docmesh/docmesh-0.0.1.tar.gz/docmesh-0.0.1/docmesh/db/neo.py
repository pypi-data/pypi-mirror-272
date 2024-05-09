import os

from pandas.core.frame import DataFrame

from neomodel import db, config
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    IntegerProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
)
from neomodel.integration.pandas import to_dataframe

if (url := os.getenv("NEO4J_URL")) is None:
    raise ValueError("You have not set neo4j database url using environment `NEO4J_URL`.")
else:
    config.DATABASE_URL = url
    # HACK: server may kill idle connection, to avoid being hung for
    # a long time, we kill the connection first, the max lifetime
    # should be less then 4 mins (240 seconds)
    config.MAX_CONNECTION_LIFETIME = 200


class FollowRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)


class ReadRel(StructuredRel):
    read_time = DateTimeProperty(default_now=True, index=True)


class Entity(StructuredNode):
    name = StringProperty(unique_index=True)

    reads = RelationshipTo("Paper", "read", model=ReadRel)
    follows = RelationshipTo("Entity", "follow", model=FollowRel)
    followers = RelationshipFrom("Entity", "follow", model=FollowRel)


class Paper(StructuredNode):
    paper_id = StringProperty(unique_index=True)
    title = StringProperty()
    abstract = StringProperty()
    summary = StringProperty()
    publication_date = DateTimeProperty()
    reference_count = IntegerProperty()
    citation_count = IntegerProperty()
    pdf = StringProperty()

    readers = RelationshipFrom("Entity", "read", model=ReadRel)
    references = RelationshipTo("Paper", "cite")
    citations = RelationshipFrom("Paper", "cite")


@db.transaction
def get_entity(name: str) -> Entity:
    entity = Entity.nodes.get(name=name)
    return entity


@db.transaction
def get_paper(paper_id: str) -> Paper:
    paper = Paper.nodes.get(paper_id=paper_id)
    return paper


@db.transaction
def add_entity(name: str) -> None:
    entity: Entity = Entity.create_or_update({"name": name})

    return entity


@db.transaction
def add_paper(paper: DataFrame, references: DataFrame) -> Paper:
    paper: Paper = Paper.create_or_update(*paper.to_dict(orient="records"))[0]

    if references.shape[0] != 0:
        references: list[Paper] = Paper.create_or_update(*references.to_dict(orient="records"))

        for reference in references:
            paper.references.connect(reference)

    return paper


@db.transaction
def read_paper(name: str, paper_id: str) -> None:
    entity = get_entity(name=name)
    paper = get_paper(paper_id=paper_id)
    entity.reads.connect(paper)


@db.transaction
def follow_entity(follower_name: str, follow_name: str) -> None:
    follower_entity = get_entity(follower_name)
    follow_entity = get_entity(follow_name)
    follower_entity.follows.connect(follow_entity)


@db.transaction
def get_latest_papers(name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e:Entity) -[r:read]-> (p:Paper)
        WHERE e.name = $name
        RETURN p.paper_id AS paper_id, p.title AS title
        ORDER BY r.read_time DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"name": name, "n": n},
        )
    )

    return df


@db.transaction
def get_latest_citegraph(name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e1:Entity) -[r:read]-> (p1:Paper) -[:cite]-> (p2:Paper) <-[:read]- (e2:Entity)
        WHERE e1.name = $name AND e2.name = $name
        RETURN p1.paper_id AS p1_paper_id, p2.paper_id AS p2_paper_id
        ORDER BY r.read_time DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"name": name, "n": n},
        )
    )

    return df


@db.transaction
def get_unread_follows_papers(name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e1:Entity) -[:follow]-> (:Entity) -[r:read]-> (p:Paper)
        WHERE e1.name = $name
        AND NOT EXISTS {
            (p) <-[:read]- (e2:Entity)
            WHERE e2.name = $name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY r.read_time, p.citation_count DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"name": name, "n": n},
        )
    )

    return df


@db.transaction
def get_unread_influential_papers(name: str, date_time: str) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (p:Paper)
        WHERE p.publication_date >= DATETIME($date_time).epochSeconds
        AND NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY p.citation_count DESC
        limit 10;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={"date_time": date_time, "name": name},
        )
    )

    return df
