---
title: "HOME"
---

{{< blocks/cover title="" subtitle="" image_anchor="center" height="full" color="orange" >}}
<style>
  /* 响应式内边距样式：默认大桌面尺寸 */
  .responsive-top-padding {
    padding-top: 30rem;
  }
  /* 平板尺寸（≤992px） */
  @media (max-width: 992px) {
    .responsive-top-padding {
      padding-top: 18rem;
    }
  }
  /* 手机尺寸（≤768px） */
  @media (max-width: 768px) {
    .responsive-top-padding {
      padding-top: 12rem;
    }
  }
</style>
<div class="responsive-top-padding"></div>

<div class="mx-auto">
	<a class="btn btn-lg btn-primary me-3 mb-4" href="/docs">
		了解文档 <i class="fa-solid fa-circle-right ms-2"></i>
	</a>
	<a class="btn btn-lg btn-secondary me-3 mb-4" href="/blog">
		查看博客 <i class="fa-solid fa-blog ms-2"></i>
	</a>
  
</div>
{{< /blocks/cover >}}

{{< blocks/lead color="orange" >}}
技术分享，涵盖 kubernetes、prometheus、golang

{{< /blocks/lead >}}



{{< blocks/section color="black" type="row" >}}
{{% blocks/feature icon="fa-brands fa-docker" title="build once run anywhere" url=/docs/kubernetes %}}
kubernetes 云原生时代最有力的容器编排工具
{{% /blocks/feature %}}

{{% blocks/feature icon="fab fa-watchman-monitoring" title="monitor anyone anywhere!" url="/docs/prometheus" %}}
prometheus 云原生时代最灵活的监控工具
{{% /blocks/feature %}}

{{% blocks/feature icon="fa-brands fa-golang" title="cloud native language!" url="/docs/golang" %}}
golang 云原生时代最流行的开发语言
{{% /blocks/feature %}}


{{< /blocks/section >}}