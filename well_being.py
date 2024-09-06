def calculate_well_being(answers):
    def muunna_tulos(luku):
        if luku <= -60:
            return 0
        elif luku <= 0:
            return (luku + 60) / 12
        elif luku <= 60:
            return (luku / 12) + 5
        else:
            return 10

    ans1 = []
    for item in answers:
        item = int(item)
        print(item, type(item))
        ans1.append(item)

    (
        anger,
        anxiety,
        self_harming,
        suicidality,
        tiredness,
        sadness,
        happiness,
        joy,
        love,
        crush,
    ) = ans1

    total_negative = int(
        anger + suicidality + self_harming + anxiety + sadness + tiredness
    )
    total_positive = int(happiness + joy + love + crush) * 1.5

    if int(suicidality) > 5:
        total_negative = 60

    if total_negative >= total_positive:
        well_being = 10 - total_negative
    else:
        well_being = total_positive

    well_being = total_positive - total_negative
    well_being = muunna_tulos(well_being)

    return well_being
