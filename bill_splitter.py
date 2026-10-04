def split_equally(total, number_of_people):
    """
    Split the bill into whole rupees.

    The amounts always add up exactly to the total.
    Example:
        ₹100 / 3
        → ₹34, ₹33, ₹33
    """

    if number_of_people < 1:
        raise ValueError(
            "Number of people must be at least 1."
        )

    total_rupees = round(total)

    base_amount = total_rupees // number_of_people
    remainder = total_rupees % number_of_people

    amounts = []

    for person in range(number_of_people):

        if person < remainder:
            amount = base_amount + 1
        else:
            amount = base_amount

        amounts.append(amount)

    return {
        "total": total_rupees,
        "number_of_people": number_of_people,
        "amounts": amounts
    }


def split_by_items(items, assignments):
    """
    Split items among people using whole rupees.

    The final amounts are reconciled so that the
    sum of all people's payments equals the
    rounded item total.
    """

    person_totals = {}

    # ------------------------------------------
    # Calculate exact totals first
    # ------------------------------------------

    for item in items:

        item_name = item.get("name")
        item_total = item.get("total") or 0

        person = assignments.get(item_name)

        if not person:
            continue

        if person not in person_totals:
            person_totals[person] = 0

        person_totals[person] += item_total

    if not person_totals:
        return {}

    # ------------------------------------------
    # Round using largest remainder method
    # ------------------------------------------

    rounded_totals = {}

    fractions = {}

    for person, amount in person_totals.items():

        floor_amount = int(amount)

        rounded_totals[person] = floor_amount

        fractions[person] = amount - floor_amount

    # ------------------------------------------
    # Determine exact rounded total
    # ------------------------------------------

    target_total = round(
        sum(person_totals.values())
    )

    current_total = sum(
        rounded_totals.values()
    )

    remaining = target_total - current_total

    # ------------------------------------------
    # Give remaining rupees to people with
    # largest decimal fractions
    # ------------------------------------------

    sorted_people = sorted(
        fractions,
        key=fractions.get,
        reverse=True
    )

    for i in range(remaining):

        person = sorted_people[i]

        rounded_totals[person] += 1

    return rounded_totals