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

### Example function (resnet50)

* **deploy** ResNet50:

    To request FPGA resources, edit the `resources:limits` field in the
    Container manifest. FPGA resource names have the form `vendor/foo` where
    `vendor` is replaced with the FPGA manufacturer and `foo` is a descriptive
    platform name. For example:

    ```sh
    cat << EOF | kubectl create -f -
    apiVersion: kubeless.io/v1beta1
    kind: Function
    metadata:
      label:
        created-by: inaccel
        function: resnet50
      name: resnet50
    spec:
      deps: |
        inaccel-keras
        scikit-image
        tensorflow
      function: https://raw.githubusercontent.com/inaccel/kubeless/master/runtimes/python/examples/ResNet50.py
      function-content-type: url
      handler: ResNet50.predict
      deployment:
        spec:
          template:
            spec:
              containers:
              - args:
                - https://store.inaccel.com/artifactory/bitstreams/xilinx/u250/xdma_201830.2/xilinx/com/researchlabs/1.1/1resnet50
                resources:
                  limits:
                    xilinx/u250: 1
      runtime: inaccel_python3.6
    EOF
    ```

* **call** predict:

    ```sh
    kubeless function call resnet50 \
    	--data '[https://github.com/inaccel/keras/raw/master/examples/data/dog.jpg, https://github.com/inaccel/keras/raw/master/examples/data/elephant.jpg]'
    ```
