def evaluate_metric(metric, test_case):
  metric.scorer.measure(test_case)
  return metric

def find_metric_by_name(metrics, name):
  for metric in metrics:
    if metric.name == name:
      return metric
  raise ValueError("There's no " + name + " metric in the provided list.")