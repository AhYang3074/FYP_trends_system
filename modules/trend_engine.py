from collections import defaultdict
from modules.topic_processing import TopicProcessor


def aggregate_and_score(raw_data):
    aggregated = defaultdict(int)
    topics = raw_data.get("related_topics", {}).get("top", [])

    for t in topics:
        raw_name = t["topic"]["title"]
        score = int(t["value"])

        clean_name = TopicProcessor.clean(raw_name)
        if clean_name:
            final_name = TopicProcessor.normalize(clean_name)
            aggregated[final_name] += score

    return sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
