{
  ID: "inaccel_python",
  versions: [
    {
      name: "inaccel_python",
      version: "1.0",
      images: [{
        phase: "installation",
        image: "python:3.7",
        command: "pip install --prefix=$KUBELESS_INSTALL_VOLUME -r $KUBELESS_DEPS_FILE"
      }, {
        phase: "runtime",
        image: "inaccel/kubeless:python3.7",
        env: {
          PYTHONPATH: "$(KUBELESS_INSTALL_VOLUME)/lib/python3.7/site-packages:$(KUBELESS_INSTALL_VOLUME)",
        },
      }],
    },
  ],
  depName: "requirements.txt",
  fileNameSuffix: ".py",
}
