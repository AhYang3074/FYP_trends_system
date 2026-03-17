from collections import defaultdict

class TrendProcessor:
    def __init__(self):
        self.generic_words = ["news", "price", "data", "review"]
        self.replacements = {
            "ai": "artificial intelligence",
            "artificial intelligence (ai)": "artificial intelligence",
            "ml": "machine learning"
        }

    def clean_topic(self, name):
        name = name.lower().strip()
        if len(name.split()) < 2 or name in self.generic_words:
            return None
        return name

    def normalize(self, name):
        return self.replacements.get(name, name)

    def process_results(self, raw_data):
        aggregated = defaultdict(int)
        topics = raw_data.get("related_topics", {}).get("top", [])
        
        for t in topics:
            raw_name = t["topic"]["title"]
            score = int(t["value"])
            
            clean_name = self.clean_topic(raw_name)
            if clean_name:
                final_name = self.normalize(clean_name)
                aggregated[final_name] += score
                
        # 排序后返回
        return sorted(aggregated.items(), key=lambda x: x[1], reverse=True)