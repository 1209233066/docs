---
date: '{{ .Date }}'
draft: false
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
type: blog
toc_hide: false
hide_summary: true
weight: 1
description: >
  k8s {{ .File.ContentBaseName }}
tags: ["kubernetes"]
categories: ["kubernetes"]
url: kubernetes/{{.File.ContentBaseName }}.html
---