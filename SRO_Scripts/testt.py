import re
log = """upload: ./monitoring-scripts.tar.gz to s3://exotel-build/monitoring-scripts/pprod/monitoring-scripts-702.tar.gzz"""
matches = re.findall(r"monitoring-scripts-(\d+)\.tar\.gz", log)
print(matches[-1])  

