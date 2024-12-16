from aioprometheus import Counter

created_successes_votes_amount = Counter(
    name="created_successes_votes_amount",
    doc="Кол-во успешно созданных голосов",
)
