"""Synthetic benchmark for responsibility-gap detection under missing multi-agent logs."""
from dataclasses import dataclass

@dataclass
class Episode:
    true_gap: int
    missing_rate: float
    outage_rate: float
    evidence_score: float


def make_episode(seed, missing_rate, outage_rate):
    """Create a reproducible synthetic episode; not real-world agent data."""
    import random
    rng = random.Random(seed)
    true_gap = int(rng.random() < 0.35)
    score = (0.78 if true_gap else 0.18) + rng.gauss(0, 0.20)
    # Field omissions and shared outages reduce observable evidence.
    if rng.random() < outage_rate:
        score = 0.0
    else:
        for _ in range(3):
            if rng.random() < missing_rate:
                score *= 0.78
    return Episode(true_gap, missing_rate, outage_rate, max(0.0, min(1.0, score)))


def predict(ep, rule, threshold=0.8):
    if rule == 'strict_complete':
        return int(ep.evidence_score >= threshold)
    if rule == 'optimistic_missing':
        return int(ep.evidence_score >= 0.5)
    if rule == 'score_threshold':
        return int(ep.evidence_score >= threshold)
    raise ValueError(f'unknown rule: {rule}')


def metrics(labels, preds):
    tp=sum(y==1 and p==1 for y,p in zip(labels,preds)); fp=sum(y==0 and p==1 for y,p in zip(labels,preds))
    fn=sum(y==1 and p==0 for y,p in zip(labels,preds)); tn=sum(y==0 and p==0 for y,p in zip(labels,preds))
    precision=tp/(tp+fp) if tp+fp else 0.0; recall=tp/(tp+fn) if tp+fn else 0.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {'precision':precision,'recall':recall,'f1':f1,'fpr':fp/(fp+tn) if fp+tn else 0.0,'weighted_cost':5*fn+fp,'tp':tp,'fp':fp,'fn':fn,'tn':tn}
