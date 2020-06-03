## InAccel Kubeless Python runtime

In order to configure the InAccel Python runtime you can copy the result of
executing `jsonnet python.jsonnet` and paste it in the Kubeless `ConfigMap`:

```
$ jsonnet python.jsonnet
# Copy the result and
# Paste the result within the "runtime-images" section
$ kubectl edit -n kubeless configmap kubeless-config
# Restart the controller pod
$ kubectl delete pod -n kubeless -l kubeless=controller
```

