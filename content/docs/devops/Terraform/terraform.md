[doc](https://developer.hashicorp.com/terraform/tutorials)|[registry](https://registry.terraform.io/)

terraform 是HashiCorp 的基础设施即代码（IaC）的管理工具。使用golang编写
安装

```bash
wget https://releases.hashicorp.com/terraform/1.9.2/terraform_1.9.2_linux_amd64.zip
unzip terraform_1.9.2_linux_amd64.zip
mv terraform /usr/bin/
```
验证
```bash
[root@jenkins01 ~]# terraform  --version
Terraform v1.9.2
on linux_amd64
```
安装命令补全
```bash
terraform -install-autocomplete && logout
```

### 快速开始

1. 创建一个空目录
    ```bash
    mkdir terraform-demo
    ```
    
2. 将以下内容写入 `terraform-demo/main.tf`
    ```json
    terraform {
      required_providers {
        docker = {
          source  = "kreuzwerker/docker"
          version = "~> 3.0.1"
        }
      }
    }
    
    provider "docker" {}
    
    resource "docker_image" "nginx" {
      name         = "nginx"
      keep_locally = false
    }
    
    resource "docker_container" "nginx" {
      image = docker_image.nginx.name
      name  = "nginx"
    
      ports {
        internal = 80
        external = 8000
      }
    }
    ```
    
3. 初始化
   
    > ```bash
    > wget https://github.com/kreuzwerker/terraform-provider-docker/releases/download/v3.0.2/terraform-provider-docker_3.0.2_linux_amd64.zip
    > ```
    >
    > ```bash
    >  mkdir -p ~/.terraform.d/plugins/registry.terraform.io/kreuzwerker/docker/3.0.2/linux_amd64
    > ```
    >
    > ```bash
    > unzip terraform-provider-docker_3.0.2_linux_amd64.zip -d  ~/.terraform.d/plugins/registry.terraform.io/kreuzwerker/docker/3.0.2/linux_amd64
    > ```
    >
    > ```bash
    > terraform init
    > ```

    ```bash
    [root@jenkins01 ~]# cd terraform-demo/
    [root@jenkins01 terraform-demo]# terraform init
    
    Initializing the backend...
    Initializing provider plugins...
    - Finding kreuzwerker/docker versions matching "~> 3.0.1"...
    - Installing kreuzwerker/docker v3.0.2...
    - Installed kreuzwerker/docker v3.0.2 (self-signed, key ID BD080C4571C6104C)
    Partner and community providers are signed by their developers.
    If you'd like to know more about provider signing, you can read about it here:
    https://www.terraform.io/docs/cli/plugins/signing.html
    Terraform has created a lock file .terraform.lock.hcl to record the provider
    selections it made above. Include this file in your version control repository
    so that Terraform can guarantee to make the same selections by default when
    you run "terraform init" in the future.
    
    Terraform has been successfully initialized!
    
    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.
    
    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
    ```
    
4. 预览应用计划
    ```bash
    [root@192 test]# terraform plan
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    + create
    
    Terraform will perform the following actions:
    
    # docker_container.nginx will be created
    + resource "docker_container" "nginx" {
        + attach                                      = false
        + bridge                                      = (known after apply)
        + command                                     = (known after apply)
        + container_logs                              = (known after apply)
        + container_read_refresh_timeout_milliseconds = 15000
        + entrypoint                                  = (known after apply)
        + env                                         = (known after apply)
        + exit_code                                   = (known after apply)
        + hostname                                    = (known after apply)
        + id                                          = (known after apply)
        + image                                       = (known after apply)
        + init                                        = (known after apply)
        + ipc_mode                                    = (known after apply)
        + log_driver                                  = (known after apply)
        + logs                                        = false
        + must_run                                    = true
        + name                                        = "tutorial"
        + network_data                                = (known after apply)
        + read_only                                   = false
        + remove_volumes                              = true
        + restart                                     = "no"
        + rm                                          = false
        + runtime                                     = (known after apply)
        + security_opts                               = (known after apply)
        + shm_size                                    = (known after apply)
        + start                                       = true
        + stdin_open                                  = false
        + stop_signal                                 = (known after apply)
        + stop_timeout                                = (known after apply)
        + tty                                         = false
        + wait                                        = false
        + wait_timeout                                = 60
    
        + healthcheck (known after apply)
    
        + labels (known after apply)
    
        + ports {
            + external = 8000
            + internal = 80
            + ip       = "0.0.0.0"
            + protocol = "tcp"
            }
        }
    
    # docker_image.nginx will be created
    + resource "docker_image" "nginx" {
        + id           = (known after apply)
        + image_id     = (known after apply)
        + keep_locally = false
        + name         = "nginx"
        + repo_digest  = (known after apply)
        }
    
    Plan: 2 to add, 0 to change, 0 to destroy.
    
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply"
    now.
    ```
    
5. 应用该配置
    ```bash
    [root@192 test]# terraform apply
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    + create
    
    Terraform will perform the following actions:
    
    # docker_container.nginx will be created
    + resource "docker_container" "nginx" {
        + attach                                      = false
        + bridge                                      = (known after apply)
        + command                                     = (known after apply)
        + container_logs                              = (known after apply)
        + container_read_refresh_timeout_milliseconds = 15000
        + entrypoint                                  = (known after apply)
        + env                                         = (known after apply)
        + exit_code                                   = (known after apply)
        + hostname                                    = (known after apply)
        + id                                          = (known after apply)
        + image                                       = (known after apply)
        + init                                        = (known after apply)
        + ipc_mode                                    = (known after apply)
        + log_driver                                  = (known after apply)
        + logs                                        = false
        + must_run                                    = true
        + name                                        = "tutorial"
        + network_data                                = (known after apply)
        + read_only                                   = false
        + remove_volumes                              = true
        + restart                                     = "no"
        + rm                                          = false
        + runtime                                     = (known after apply)
        + security_opts                               = (known after apply)
        + shm_size                                    = (known after apply)
        + start                                       = true
        + stdin_open                                  = false
        + stop_signal                                 = (known after apply)
        + stop_timeout                                = (known after apply)
        + tty                                         = false
        + wait                                        = false
        + wait_timeout                                = 60
    
        + healthcheck (known after apply)
    
        + labels (known after apply)
    
        + ports {
            + external = 8000
            + internal = 80
            + ip       = "0.0.0.0"
            + protocol = "tcp"
            }
        }
    
    # docker_image.nginx will be created
    + resource "docker_image" "nginx" {
        + id           = (known after apply)
        + image_id     = (known after apply)
        + keep_locally = false
        + name         = "nginx"
        + repo_digest  = (known after apply)
        }
    
    Plan: 2 to add, 0 to change, 0 to destroy.
    
    Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.
    
    Enter a value: yes
    
    docker_image.nginx: Creating...
    
    docker_image.nginx: Still creating... [10s elapsed]
    docker_image.nginx: Creation complete after 20s [id=sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765cnginx]
    docker_container.nginx: Creating...
    docker_container.nginx: Creation complete after 1s [id=360704dcbb82c35c9e4c65f604ad6af22e4277fed5bb34b0b75eed58ead3ced6]
    
    Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
    ```
    
    创建了一个pod
    ```bash
    [root@192 test]# docker ps 
    CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                                                                                                                             NAMES
    360704dcbb82   fffffc90d343      "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   0.0.0.0:8000->80/tcp                                                                                                              tutorial
    ```
    
5. 销毁pod
    ```bash
    [root@192 test]# terraform destroy 
    docker_image.nginx: Refreshing state... [id=sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765cnginx]
    docker_container.nginx: Refreshing state... [id=360704dcbb82c35c9e4c65f604ad6af22e4277fed5bb34b0b75eed58ead3ced6]
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy
    
    Terraform will perform the following actions:
    
    # docker_container.nginx will be destroyed
    - resource "docker_container" "nginx" {
        - attach                                      = false -> null
        - command                                     = [
            - "nginx",
            - "-g",
            - "daemon off;",
            ] -> null
        - container_read_refresh_timeout_milliseconds = 15000 -> null
        - cpu_shares                                  = 0 -> null
        - dns                                         = [] -> null
        - dns_opts                                    = [] -> null
        - dns_search                                  = [] -> null
        - entrypoint                                  = [
            - "/docker-entrypoint.sh",
            ] -> null
        - env                                         = [] -> null
        - group_add                                   = [] -> null
        - hostname                                    = "360704dcbb82" -> null
        - id                                          = "360704dcbb82c35c9e4c65f604ad6af22e4277fed5bb34b0b75eed58ead3ced6" -> null
        - image                                       = "sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765c" -> null
        - init                                        = false -> null
        - ipc_mode                                    = "private" -> null
        - log_driver                                  = "json-file" -> null
        - log_opts                                    = {} -> null
        - logs                                        = false -> null
        - max_retry_count                             = 0 -> null
        - memory                                      = 0 -> null
        - memory_swap                                 = 0 -> null
        - must_run                                    = true -> null
        - name                                        = "tutorial" -> null
        - network_data                                = [
            - {
                - gateway                   = "172.17.0.1"
                - global_ipv6_prefix_length = 0
                - ip_address                = "172.17.0.3"
                - ip_prefix_length          = 16
                - mac_address               = "02:42:ac:11:00:03"
                - network_name              = "bridge"
                    # (2 unchanged attributes hidden)
                },
            ] -> null
        - network_mode                                = "default" -> null
        - privileged                                  = false -> null
        - publish_all_ports                           = false -> null
        - read_only                                   = false -> null
        - remove_volumes                              = true -> null
        - restart                                     = "no" -> null
        - rm                                          = false -> null
        - runtime                                     = "runc" -> null
        - security_opts                               = [] -> null
        - shm_size                                    = 64 -> null
        - start                                       = true -> null
        - stdin_open                                  = false -> null
        - stop_signal                                 = "SIGQUIT" -> null
        - stop_timeout                                = 0 -> null
        - storage_opts                                = {} -> null
        - sysctls                                     = {} -> null
        - tmpfs                                       = {} -> null
        - tty                                         = false -> null
        - wait                                        = false -> null
        - wait_timeout                                = 60 -> null
            # (7 unchanged attributes hidden)
    
        - ports {
            - external = 8000 -> null
            - internal = 80 -> null
            - ip       = "0.0.0.0" -> null
            - protocol = "tcp" -> null
            }
        }
    
    # docker_image.nginx will be destroyed
    - resource "docker_image" "nginx" {
        - id           = "sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765cnginx" -> null
        - image_id     = "sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765c" -> null
        - keep_locally = false -> null
        - name         = "nginx" -> null
        - repo_digest  = "nginx@sha256:67682bda769fae1ccf5183192b8daf37b64cae99c6c3302650f6f8bf5f0f95df" -> null
        }
    
    Plan: 0 to add, 0 to change, 2 to destroy.
    
    Do you really want to destroy all resources?
    Terraform will destroy all your managed infrastructure, as shown above.
    There is no undo. Only 'yes' will be accepted to confirm.
    
    Enter a value: yes
    
    docker_container.nginx: Destroying... [id=360704dcbb82c35c9e4c65f604ad6af22e4277fed5bb34b0b75eed58ead3ced6]
    docker_container.nginx: Destruction complete after 1s
    docker_image.nginx: Destroying... [id=sha256:fffffc90d343cbcb01a5032edac86db5998c536cd0a366514121a45c6723765cnginx]
    docker_image.nginx: Destruction complete after 0s
    
    Destroy complete! Resources: 2 destroyed.
    ```

```bash
[root@jenkins01 terraform-exsi]# cat main.tf 
terraform {
  required_version = ">= 0.13"
  required_providers {
    vsphere = {
      source  = "hashicorp/vsphere"
      version = ">= 2.0.0"
    }
  }
}

provider "vsphere" {
  user           = "administrator@vsphere.local"
  password       = "Cc1020304050!"
  vsphere_server = "192.168.0.214"
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "datacenter" {
  name = "Beijing"
}

data "vsphere_resource_pool" "pool" {
  name          = "Resources"
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_datastore" "store" {
  name          = "data"
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

data "vsphere_network" "network" {
  name          = "VM Network"
  datacenter_id = data.vsphere_datacenter.datacenter.id
}

resource "vsphere_virtual_machine" "example_vm" {
  name             = "ExampleVM"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.store.id
  num_cpus         = 2
  memory           = 4096
  guest_id         = "otherGuest"

  network_interface {
    network_id = data.vsphere_network.network.id
  }

  disk {
    label = "disk0"
    size  = 40
  }

  cdrom {
    path          = "CentOS-7.9-x86_64-DVD-2009.iso"
    datastore_id = data.vsphere_datastore.store.id
  }
}
```



```bash
datastore1/template-centos7/centos7-template-1.vmdk
datastore1/template-centos7/centos7-template.ovf

```
