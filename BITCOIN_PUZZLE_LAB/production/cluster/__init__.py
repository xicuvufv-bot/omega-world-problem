"""production.cluster — Hyper-Distributed Task Execution Cluster.

Provides the coordinator brain, worker node daemon, lease-based scheduler,
and HMAC-authenticated transport that together run puzzle-key scanning as
a coordinated, fault-tolerant multi-GPU fleet.
"""