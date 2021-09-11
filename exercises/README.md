

uninstall k3s:
   /usr/local/bin/k3s-uninstall.sh

Errates:
- fix k3s containercreateError by installing apparmor
  https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-apparmor-start.html
  https://github.com/rancher/k3os/issues/702
  zypper in -t pattern apparmor
