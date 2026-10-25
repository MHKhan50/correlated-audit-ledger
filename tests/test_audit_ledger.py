import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_ledger import Episode, predict, metrics, make_episode
class Tests(unittest.TestCase):
 def test_deterministic_generation(self): self.assertEqual(make_episode(12,.1,.1),make_episode(12,.1,.1))
 def test_scores_bounded(self):
  e=make_episode(4,.3,.25); self.assertGreaterEqual(e.evidence_score,0); self.assertLessEqual(e.evidence_score,1)
 def test_strict_threshold(self): self.assertEqual(predict(Episode(1,.1,0,.79),'strict_complete',.8),0)
 def test_optimistic_threshold(self): self.assertEqual(predict(Episode(1,.1,0,.6),'optimistic_missing'),1)
 def test_metric_perfect(self): self.assertEqual(metrics([0,1],[0,1])['f1'],1)
 def test_cost_weights_false_negative(self): self.assertEqual(metrics([1],[0])['weighted_cost'],5)
 def test_cost_weights_false_positive(self): self.assertEqual(metrics([0],[1])['weighted_cost'],1)
if __name__=='__main__': unittest.main()
