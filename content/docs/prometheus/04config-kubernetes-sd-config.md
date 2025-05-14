---
title: "kubernetes_sd_configs"
linkTitle: "kubernetes_sd_configs"
date: 2025-05-12
toc_hide: false
hide_summary: true
weight: 4
description: >
  kubernetes_sd_configs|prometheus

tags: ["prometheus","配置","kubernetes_sd_configs"]
categories: ["prometheus","监控"]
url: prometheus/kubernetes-sd-configs.html
---


```yaml
# A scrape configuration for running Prometheus on a Kubernetes cluster.
# This uses separate scrape configs for cluster components (i.e. API server, node)
# and services to allow each to use different authentication configs.
#
# Kubernetes labels will be added as Prometheus labels on metrics via the
# `labelmap` relabeling action.
#
# If you are using Kubernetes 1.7.2 or earlier, please take note of the comments
# for the kubernetes-cadvisor job; you will need to edit or remove this job.

# Keep at most 100 sets of details of targets dropped by relabeling.
# This information is used to display in the UI for troubleshooting.
global:
  keep_dropped_targets: 100

# Scrape config for API servers.
#
# Kubernetes exposes API servers as endpoints to the default/kubernetes
# service so this uses `endpoints` role and uses relabelling to only keep
# the endpoints associated with the default/kubernetes service using the
# default named port `https`. This works for single API server deployments as
# well as HA API server deployments.
scrape_configs:
  - job_name: "kubernetes-apiservers"

    kubernetes_sd_configs:
      - role: endpoints

    # Default to scraping over https. If required, just disable this or change to
    # `http`.
    scheme: https

    # This TLS & authorization config is used to connect to the actual scrape
    # endpoints for cluster components. This is separate to discovery auth
    # configuration because discovery & scraping are two separate concerns in
    # Prometheus. The discovery auth config is automatic if Prometheus runs inside
    # the cluster. Otherwise, more config options have to be provided within the
    # <kubernetes_sd_config>.
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      # If your node certificates are self-signed or use a different CA to the
      # master CA, then disable certificate verification below. Note that
      # certificate verification is an integral part of a secure infrastructure
      # so this should only be disabled in a controlled environment. You can
      # disable certificate verification by uncommenting the line below.
      #
      # insecure_skip_verify: true
    authorization:
      credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    # Keep only the default/kubernetes service endpoints for the https port. This
    # will add targets for each API server which Kubernetes adds an endpoint to
    # the default/kubernetes service.
    relabel_configs:
      - source_labels:
          [
            __meta_kubernetes_namespace,
            __meta_kubernetes_service_name,
            __meta_kubernetes_endpoint_port_name,
          ]
        action: keep
        regex: default;kubernetes;https

  # Scrape config for nodes (kubelet).
  - job_name: "kubernetes-nodes"

    # Default to scraping over https. If required, just disable this or change to
    # `http`.
    scheme: https

    # This TLS & authorization config is used to connect to the actual scrape
    # endpoints for cluster components. This is separate to discovery auth
    # configuration because discovery & scraping are two separate concerns in
    # Prometheus. The discovery auth config is automatic if Prometheus runs inside
    # the cluster. Otherwise, more config options have to be provided within the
    # <kubernetes_sd_config>.
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      # If your node certificates are self-signed or use a different CA to the
      # master CA, then disable certificate verification below. Note that
      # certificate verification is an integral part of a secure infrastructure
      # so this should only be disabled in a controlled environment. You can
      # disable certificate verification by uncommenting the line below.
      #
      # insecure_skip_verify: true
    authorization:
      credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    kubernetes_sd_configs:
      - role: node

    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Scrape config for Kubelet cAdvisor.
  #
  # This is required for Kubernetes 1.7.3 and later, where cAdvisor metrics
  # (those whose names begin with 'container_') have been removed from the
  # Kubelet metrics endpoint.  This job scrapes the cAdvisor endpoint to
  # retrieve those metrics.
  #
  # In Kubernetes 1.7.0-1.7.2, these metrics are only exposed on the cAdvisor
  # HTTP endpoint; use the "/metrics" endpoint on the 4194 port of nodes. In
  # that case (and ensure cAdvisor's HTTP server hasn't been disabled with the
  # --cadvisor-port=0 Kubelet flag).
  #
  # This job is not necessary and should be removed in Kubernetes 1.6 and
  # earlier versions, or it will cause the metrics to be scraped twice.
  - job_name: "kubernetes-cadvisor"

    # Default to scraping over https. If required, just disable this or change to
    # `http`.
    scheme: https

    # Starting Kubernetes 1.7.3 the cAdvisor metrics are under /metrics/cadvisor.
    # Kubernetes CIS Benchmark recommends against enabling the insecure HTTP
    # servers of Kubernetes, therefore the cAdvisor metrics on the secure handler
    # are used.
    metrics_path: /metrics/cadvisor

    # This TLS & authorization config is used to connect to the actual scrape
    # endpoints for cluster components. This is separate to discovery auth
    # configuration because discovery & scraping are two separate concerns in
    # Prometheus. The discovery auth config is automatic if Prometheus runs inside
    # the cluster. Otherwise, more config options have to be provided within the
    # <kubernetes_sd_config>.
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      # If your node certificates are self-signed or use a different CA to the
      # master CA, then disable certificate verification below. Note that
      # certificate verification is an integral part of a secure infrastructure
      # so this should only be disabled in a controlled environment. You can
      # disable certificate verification by uncommenting the line below.
      #
      # insecure_skip_verify: true
    authorization:
      credentials_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    kubernetes_sd_configs:
      - role: node

    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Example scrape config for service endpoints.
  #
  # The relabeling allows the actual service scrape endpoint to be configured
  # for all or only some endpoints.
  - job_name: "kubernetes-service-endpoints"

    kubernetes_sd_configs:
      - role: endpoints

    relabel_configs:
      # Example relabel to scrape only endpoints that have
      # "example.io/should_be_scraped = true" annotation.
      #  - source_labels: [__meta_kubernetes_service_annotation_example_io_should_be_scraped]
      #    action: keep
      #    regex: true
      #
      # Example relabel to customize metric path based on endpoints
      # "example.io/metric_path = <metric path>" annotation.
      #  - source_labels: [__meta_kubernetes_service_annotation_example_io_metric_path]
      #    action: replace
      #    target_label: __metrics_path__
      #    regex: (.+)
      #
      # Example relabel to scrape only single, desired port for the service based
      # on endpoints "example.io/scrape_port = <port>" annotation.
      #  - source_labels: [__address__, __meta_kubernetes_service_annotation_example_io_scrape_port]
      #    action: replace
      #    regex: ([^:]+)(?::\d+)?;(\d+)
      #    replacement: $1:$2
      #    target_label: __address__
      #
      # Example relabel to configure scrape scheme for all service scrape targets
      # based on endpoints "example.io/scrape_scheme = <scheme>" annotation.
      #  - source_labels: [__meta_kubernetes_service_annotation_example_io_scrape_scheme]
      #    action: replace
      #    target_label: __scheme__
      #    regex: (https?)
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_service_name]
        action: replace
        target_label: service

  # Example scrape config for probing services via the Blackbox Exporter.
  #
  # The relabeling allows the actual service scrape endpoint to be configured
  # for all or only some services.
  - job_name: "kubernetes-services"

    metrics_path: /probe
    params:
      module: [http_2xx]

    kubernetes_sd_configs:
      - role: service

    relabel_configs:
      # Example relabel to probe only some services that have "example.io/should_be_probed = true" annotation
      #  - source_labels: [__meta_kubernetes_service_annotation_example_io_should_be_probed]
      #    action: keep
      #    regex: true
      - source_labels: [__address__]
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter.example.com:9115
      - source_labels: [__param_target]
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_service_name]
        target_label: service

  # Example scrape config for probing ingresses via the Blackbox Exporter.
  #
  # The relabeling allows the actual ingress scrape endpoint to be configured
  # for all or only some services.
  - job_name: "kubernetes-ingresses"

    metrics_path: /probe
    params:
      module: [http_2xx]

    kubernetes_sd_configs:
      - role: ingress

    relabel_configs:
      # Example relabel to probe only some ingresses that have "example.io/should_be_probed = true" annotation
      #  - source_labels: [__meta_kubernetes_ingress_annotation_example_io_should_be_probed]
      #    action: keep
      #    regex: true
      - source_labels:
          [
            __meta_kubernetes_ingress_scheme,
            __address__,
            __meta_kubernetes_ingress_path,
          ]
        regex: (.+);(.+);(.+)
        replacement: ${1}://${2}${3}
        target_label: __param_target
      - target_label: __address__
        replacement: blackbox-exporter.example.com:9115
      - source_labels: [__param_target]
        target_label: instance
      - action: labelmap
        regex: __meta_kubernetes_ingress_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_ingress_name]
        target_label: ingress

  # Example scrape config for pods
  #
  # The relabeling allows the actual pod scrape to be configured
  # for all the declared ports (or port-free target if none is declared)
  # or only some ports.
  - job_name: "kubernetes-pods"

    kubernetes_sd_configs:
      - role: pod

    relabel_configs:
      # Example relabel to scrape only pods that have
      # "example.io/should_be_scraped = true" annotation.
      #  - source_labels: [__meta_kubernetes_pod_annotation_example_io_should_be_scraped]
      #    action: keep
      #    regex: true
      #
      # Example relabel to customize metric path based on pod
      # "example.io/metric_path = <metric path>" annotation.
      #  - source_labels: [__meta_kubernetes_pod_annotation_example_io_metric_path]
      #    action: replace
      #    target_label: __metrics_path__
      #    regex: (.+)
      #
      # Example relabel to scrape only single, desired port for the pod
      # based on pod "example.io/scrape_port = <port>" annotation.
      #  - source_labels: [__address__, __meta_kubernetes_pod_annotation_example_io_scrape_port]
      #    action: replace
      #    regex: ([^:]+)(?::\d+)?;(\d+)
      #    replacement: $1:$2
      #    target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: pod
```


[<span id='kubernetes_sd_configs'>**kubernetes_sd_configs**</span>](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)

> ```bash
> curl --cacert /etc/kubernetes/pki/ca.crt \
> --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
> --key /etc/kubernetes/pki/apiserver-kubelet-client.key \
> https://192.168.0.244:6443/api/v1/services?limit=100&resourceVersion=0
> ```



node、service、pod、endpoints、endpointslice、ingress



```yaml
role: node
__meta_kubernetes_node_name
__meta_kubernetes_node_label_<labelname>
__meta_kubernete_node_labelpressent_<labelname>
__meta_kubernetes_node_label_<labelname>
__meta_kubernetes_node_annotationpresent_<annotationname>
__meta_kubernetes_node_address_<address_type>
##
role: service #这通常对于服务的黑盒监视很有用
__meta_kubernetes_namespace
__meta_kubernetes_service_name
__meta_kubernetes_service_port_name
__meta_kubernetes_service_port_protocol
__meta_kubernetes_service_type #服务的类型
__meta_kubernetes_service_label_<labelname>
__meta_kubernetes_service_labelpresent_<labelname>
__meta_kubernetes_service_annotation_<annotationname>
__meta_kubernetes_service_annotationpresent_<annotationname>
__meta_kubernetes_service_cluster_ip  # 服务的群集 IP 地址
__meta_kubernetes_service_external_name #服务的群集 IP 地址
###
role: pod
__meta_kubernetes_namespace：容器对象的命名空间。
__meta_kubernetes_pod_name：容器对象的名称。
__meta_kubernetes_pod_ip：容器对象的容器 IP。
__meta_kubernetes_pod_label_<labelname>：容器对象中的每个标签。
__meta_kubernetes_pod_labelpresent_<labelname>：对于容器对象中的每个标签。true
__meta_kubernetes_pod_annotation_<annotationname>：来自容器对象的每个注释。
__meta_kubernetes_pod_annotationpresent_<annotationname>：对于容器对象中的每个注释。true
__meta_kubernetes_pod_container_init：如果容器是InitContainertrue
__meta_kubernetes_pod_container_name：目标地址指向的容器的名称。
__meta_kubernetes_pod_container_port_name：容器端口的名称。
__meta_kubernetes_pod_container_port_number：容器端口的编号。
__meta_kubernetes_pod_container_port_protocol：容器端口的协议。
__meta_kubernetes_pod_ready：设置为或表示容器的就绪状态。truefalse
__meta_kubernetes_pod_phase：在生命周期中设置为 、、 或 。PendingRunningSucceededFailedUnknown
__meta_kubernetes_pod_node_name：调度 Pod 所到的节点的名称。
__meta_kubernetes_pod_host_ip：容器对象的当前主机 IP。
__meta_kubernetes_pod_uid：容器对象的 UID。
__meta_kubernetes_pod_controller_kind：容器控制器的对象类型。
__meta_kubernetes_pod_controller_name：容器控制器的名称
###
role: endpoints
__meta_kubernetes_namespace：终结点对象的命名空间。
__meta_kubernetes_endpoints_name：终结点对象的名称。
对于直接从终端节点列表中发现的所有目标（未从底层 Pod 额外推断出的目标），将附加以下标签：
__meta_kubernetes_endpoint_hostname：终结点的主机名。
__meta_kubernetes_endpoint_node_name：承载终结点的节点的名称。
__meta_kubernetes_endpoint_ready：设置为终结点的就绪状态或为其设置。truefalse
__meta_kubernetes_endpoint_port_name：终结点端口的名称。
__meta_kubernetes_endpoint_port_protocol：端点端口的协议。
__meta_kubernetes_endpoint_address_target_kind：终结点地址目标的类型。
__meta_kubernetes_endpoint_address_target_name：终结点地址目标的名称。
如果终结点属于某个服务，则会附加发现的所有标签。role: service
对于容器支持的所有目标，将附加发现的所有标签。role: pod

###
role: ingress
该角色为每个入口的每个路径发现一个目标。这通常对于入口的黑盒监视很有用。该地址将设置为入口规范中指定的主机。ingress

可用的元标签：

__meta_kubernetes_namespace：入口对象的命名空间。
__meta_kubernetes_ingress_name：入口对象的名称。
__meta_kubernetes_ingress_label_<labelname>：入口对象中的每个标签。
__meta_kubernetes_ingress_labelpresent_<labelname>：对于入口对象中的每个标签。true
__meta_kubernetes_ingress_annotation_<annotationname>：来自入口对象的每个批注。
__meta_kubernetes_ingress_annotationpresent_<annotationname>：对于入口对象中的每个批注。true
__meta_kubernetes_ingress_class_name：入口规范中的类名（如果存在）。
__meta_kubernetes_ingress_scheme：入口的协议方案（如果设置了 TLS 配置）。缺省值为 。httpshttp
__meta_kubernetes_ingress_path：入口规范的路径。缺省值为 。
```

