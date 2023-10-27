from pyvndbhttp import VNDBQuery, And, Filter, QType, Or
import json


def main():
    api = VNDBQuery()
    id_to_search = "c51034"  # replace with the id you're searching for
    filters = Filter("id", "=", id_to_search)
    # , traits.name, height, hair, eyes, body, clothes, personality, role
    characters = api.Type(QType.CHARACTER).Filters(filters).Fields("name, "
                                                                   "image.url, "
                                                                   "description, "
                                                                   "aliases").Results(2).Get()
    # characters = api.Type(QType.CHARACTER).Fields("id, name, image.url, description, traits.name").Results(2).Filters(
    #     ).Get()

    print(json.dumps(characters))
    with open("haruka.json", "w") as f:
        json.dump(characters, f, indent=4)
    # # VN query example
    # # Fetch VNs id, title, and cover url from five VNs released after 2002-01-01 and before 2009, reverse ordered by rating. AKA, best rated VN is first
    # print(
    #     "Fetch VNs id, title, and cover url from five VNs released after 2002-01-01 and before 2009, reverse ordered by rating. AKA, best rated VN is first")
    # filters = Filter("release", "=", And(Filter("released", ">=", "2002-01-01"), Filter("released", "<", "2009")))
    # vns = api.Type(QType.VN).Fields("id,title,image.url").Filters(filters).Sort("rating").Reverse().Results(5).Get()
    # print(json.dumps(vns))
    # print("---------------------")
    #
    # # VN query example 2
    # # Get VN that does not have sexual content (g235) and have mutiple endings
    # print("Get VN that does not have sexual content (g235) and have mutiple endings")
    # filters = And(Filter("tag", "=", "g235"), Filter("tag", "=", "g148"))
    # vns2 = api.Type(QType.VN).Fields("title").Filters(filters).Get()
    # print(json.dumps(vns2))
    #
    # # Release query example
    # # Gets title, id and plateforms releases from 2nd result from the VNs query, released either on Blu-ray or Linux, ordered by release date
    # print(
    #     "Gets title, id and plateforms releases from 2nd result from the VNs query, released either on Blu-ray or Linux, ordered by release date")
    # filters = And(Filter("vn", "=", Filter("id", "=", vns["results"][1]["id"])),
    #               Or(Filter("platform", "=", "lin"), Filter("platform", "=", "bdp")))
    # releases = api.Type(QType.RELEASE).Fields("id,title,platforms,producers.name").Filters(filters).Sort(
    #     "released").Get()
    # print(json.dumps(releases))
    # print("---------------------")
    #
    # # Producer query example
    # # Search producers which name contains 'Team', can either be in aliases or names.
    # print("Search producers which name contains 'Team', can either be in aliases or names.")
    # filters = Filter("search", "=", "Team")
    # producers = api.Type(QType.PRODUCER).Fields("name,aliases").Search("Team").Get()
    # print(json.dumps(producers))
    # print("---------------------")
    #
    # # Character query example
    # # Get name, portrait url, description, and traits names from every female character that is proactive (i74) and has short hair (i29)
    # print(
    #     "Get name, portrait url, description, and traits names from every female character that is proactive (i74) and has short hair (i29)")
    # filters = And(Filter("sex", "=", "f"), Filter("trait", "=", "i74"), Filter("trait", "=", "i29"))
    # characters = api.Type(QType.CHARACTER).Fields("name, image.url, description, traits.name").Filters(filters).Get()
    # print(json.dumps(characters))
    # print("---------------------")
    #
    # # Character query example 2
    # # Search characters that are subject of bullying (i268), even if it's a major spoiler (2)
    # print("Search characters that are subject of bullying (i268), even if it's a major spoiler (2)")
    # filters = Filter("trait", "=", ["i268", 2])
    # characters = api.Type(QType.CHARACTER).Fields("id, name").Filters(filters).Get()
    # print(json.dumps(characters))
    # print("---------------------")
    #
    # # Tag query example
    # print("Search technical traits")
    # filters = Filter("category", "=", "tech")
    # tags = api.Type(QType.TAG).Fields("id, name, vn_count").Filters(filters).Get()
    # print(json.dumps(tags))
    # print("---------------------")
    #
    # # Trait query example
    # print("Search traits that are braided")
    # traits = api.Type(QType.TRAIT).Fields("id, name, group_name, description").Search("Braided").Get()
    # print(json.dumps(traits))
    # print("---------------------")
    #
    # # Manual pagination handling
    # # Goes through all character that has an unknown sex, 2 by 2.
    # print("Goes through all character that has an unknown sex, 2 by 2.")
    # filters = Filter("sex", "=", "unknown")
    # char = []
    # page = 1
    # res = {}
    # while True:
    #     res = api.Type(QType.CHARACTER).Filters(filters).Fields("id, name").Results(2).Page(page).Get()
    #     print("Page {0} :".format(page))
    #     print(res["results"])
    #     char.extend(res["results"])
    #     page = page + 1
    #
    #     if not res["more"]:
    #         break
    # print("---------------------")
    #
    # # Same pagination with Next() feature
    # print("Goes through all character that has an unknown sex, 2 by 2.")
    # filters = Filter("sex", "=", "unknown")
    # res = api.Type(QType.CHARACTER).Filters(filters).Fields("id, name").Results(2).Get()
    # char = []
    # while res is not None:
    #     print(json.dumps(res))
    #     char.extend(res["results"])
    #     res = api.Next()
    # print(char)
    # print("---------------------")
    #
    # # User list handling
    # # Get Yorhel's top 10 visual novels
    # filters = Filter("label", "=", 7)
    # top = api.List("u2").Fields("id, vote, vn.title").Filters(filters).Sort("vote").Reverse().Results(10).Get()
    # print(json.dumps(top))
    #

if __name__ == "__main__":
    main()