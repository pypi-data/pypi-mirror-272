import toml
from pathlib import Path
from more_itertools import chunked

from operator import itemgetter

rank_requirements = toml.load(Path(__file__).parent / "data" / "requirements.toml")

eagle_badges_by_name = {}

for requirement, data in rank_requirements["Eagle"]["requirements"]["03"].items():
    if len(requirement) < 2:  # the requirement is one of the single-letter variety
        for badge in data["text"].split(" OR "):
            eagle_badges_by_name[badge] = requirement

alternate_names = {
    "Citizenship In Community": "Citizenship in the Community",
    "Citizenship In Nation": "Citizenship in the Nation",
    "Citizenship In World": "Citizenship in the World",
}


def allocate_merit_badges(merit_badges):

    if len(merit_badges) == 0:
        return None, None, None

    eagle_badges, palm_badges = get_eagle_badges(merit_badges)
    life_badges = get_life_badges(merit_badges)
    star_badges = get_star_badges(merit_badges)

    return star_badges, life_badges, eagle_badges, palm_badges


def get_eagle_badges(merit_badges):
    eagle_badges = {}
    for badge in sorted(
        filter(itemgetter("eagle_required"), merit_badges), key=itemgetter("date")
    ):

        name = alternate_names.get(badge["name"], badge["name"])

        slot = eagle_badges_by_name.get(name)

        if slot not in eagle_badges:
            eagle_badges[slot] = badge

    remaining_badges = [
        badge for badge in merit_badges if badge not in eagle_badges.values()
    ]
    for slot, badge in zip("opqrstu", sorted(remaining_badges, key=itemgetter("date"))):
        eagle_badges[slot] = badge

    palm_badges = [
        badge for badge in remaining_badges if badge not in eagle_badges.values()
    ]

    if all(eagle_badges.get(slot) for slot in "abcdefghijklmnopqrstu"):
        eagle_badges["completed"] = True
    else:
        eagle_badges["completed"] = False

    return eagle_badges, palm_badges


def get_life_badges(merit_badges):
    eagle_badges = sorted(
        filter(itemgetter("eagle_required"), merit_badges), key=itemgetter("date")
    )
    life_badges = {}

    life_badges["eagle_badges"] = eagle_badges[0:7]  # first 7 must be eagle required
    remaining_badges = sorted(
        [
            badge
            for badge in merit_badges
            if badge not in life_badges.get("eagle_badges")
        ],
        key=itemgetter("date"),
    )

    life_badges["elective_badges"] = remaining_badges[0:4]

    if (
        len(life_badges.get("eagle_badges")) == 7
        and len(life_badges.get("elective_badges")) == 4
    ):
        life_badges["completed"] = True
    else:
        life_badges["completed"] = False

    return life_badges


def get_star_badges(merit_badges):
    eagle_badges = sorted(
        filter(itemgetter("eagle_required"), merit_badges), key=itemgetter("date")
    )
    star_badges = {}

    star_badges["eagle_badges"] = eagle_badges[0:4]  # first 4 must be eagle required
    remaining_badges = sorted(
        [
            badge
            for badge in merit_badges
            if badge not in star_badges.get("eagle_badges")
        ],
        key=itemgetter("date"),
    )

    star_badges["elective_badges"] = remaining_badges[0:2]

    if (
        len(star_badges.get("eagle_badges")) == 4
        and len(star_badges.get("elective_badges")) == 2
    ):
        star_badges["completed"] = True
    else:
        star_badges["completed"] = False

    return star_badges


def record_star_badges(badges, scout):
    scout["Ranks"]["Star"]["03"] = {}

    for badge, code in zip(badges["eagle_badges"], "abcd"):
        scout["Ranks"]["Star"]["03"][code] = badge

    for badge, code in zip(badges["elective_badges"], "ef"):
        scout["Ranks"]["Star"]["03"][code] = badge

    if badges["completed"]:
        scout["Ranks"]["Star"]["03"]["date"] = max(
            badge["date"]
            for badge in (*badges["eagle_badges"], *badges["elective_badges"])
        )


def record_life_badges(badges, scout):
    scout["Ranks"]["Life"]["03"] = {}
    for badge, code in zip(badges["eagle_badges"][4:7], "abc"):
        scout["Ranks"]["Life"]["03"][code] = badge

    for badge, code in zip(badges["elective_badges"][2:4], "de"):
        scout["Ranks"]["Life"]["03"][code] = badge

    if badges["completed"]:
        scout["Ranks"]["Life"]["03"]["date"] = max(
            badge["date"]
            for badge in (*badges["eagle_badges"], *badges["elective_badges"])
        )


def record_eagle_badges(badges, scout):
    scout["Ranks"]["Eagle"]["03"] = {}
    for code in "abcdefghijklmnopqrstu":
        scout["Ranks"]["Eagle"]["03"][code] = badges.get(code)

    if badges["completed"]:
        scout["Ranks"]["Eagle"]["03"]["date"] = max(
            badges.get(code)["date"] for code in "abcdefghijklmnopqrstu"
        )


def record_palm_badges(badges, scout):
    badges.sort(key=itemgetter("date"))
    for badge_group, name in zip(
        chunked(badges, 5), rank_requirements["Eagle Palms"]["names"]
    ):
        if name not in scout["Ranks"]:
            scout["Ranks"][name] = {}
        scout["Ranks"][name]["04"] = {}
        for badge, code in zip(badge_group, "abcde"):
            scout["Ranks"][name]["04"][code] = badge
