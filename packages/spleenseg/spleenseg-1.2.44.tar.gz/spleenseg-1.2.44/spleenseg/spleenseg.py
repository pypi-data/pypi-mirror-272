#!/usr/bin/env python

# from collections.abc import Iterable
from pathlib import Path
from argparse import Namespace

# from dataclasses import dataclass

# from matplotlib.pyplot import plot
from monai.config.deviceconfig import print_config

# from contextlib import redirect_stderr
# from io import StringIO

# import os
import sys
import re
import pudb

# from typing import Any, Optional, Callable

from spleenseg.core import neuralnet
from spleenseg.models.data import TrainingParams

# from spleenseg.transforms import transforms
from spleenseg.plotting import plotting
from spleenseg.comms import rpc
import warnings
from pyfiglet import Figlet

from chris_plugin import chris_plugin

warnings.filterwarnings(
    "ignore",
    message="For details about installing the optional dependencies, please visit:",
)


DISPLAY_TITLE = r"""

███████╗██████╗ ██╗     ███████╗███████╗███╗   ██╗███████╗███████╗ ██████╗
██╔════╝██╔══██╗██║     ██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝██╔════╝
███████╗██████╔╝██║     █████╗  █████╗  ██╔██╗ ██║███████╗█████╗  ██║  ███╗
╚════██║██╔═══╝ ██║     ██╔══╝  ██╔══╝  ██║╚██╗██║╚════██║██╔══╝  ██║   ██║
███████║██║     ███████╗███████╗███████╗██║ ╚████║███████║███████╗╚██████╔╝
╚══════╝╚═╝     ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝
"""

__version__ = "1.2.44"
import spleenseg.splparser as spl

description: str = """
A ChRIS DS plugin based on Project MONAI 3D Spleen Segmentation.
This plugin implements both training and inference, with some
refactoring and pervasive type hinting.
"""


def trainingData_prep(options: Namespace) -> list[dict[str, str]]:
    """
    Generates a list of dictionary entries, each of which is simply the name
    of an image file and its corresponding label file.
    """
    trainRaw: list[Path] = []
    trainLbl: list[Path] = []
    for group in [options.trainImageDir, options.trainLabelsDir]:
        for path in Path(options.inputdir).rglob(group):
            if group == path.name and path.name == options.trainImageDir:
                trainRaw.extend(path.glob(options.pattern))
            elif group == path.name and path.name == options.trainLabelsDir:
                trainLbl.extend(path.glob(options.pattern))
    trainRaw.sort()
    trainLbl.sort()
    return [
        {"image": str(image_name), "label": str(label_name)}
        for image_name, label_name in zip(trainRaw, trainLbl)
    ]


def testingData_prep(options: Namespace) -> list[dict[str, str]]:
    """
    Generates a list of dictionary entries, each of which is simply the name
    of a test image file with its location
    """
    testRaw: list[Path] = []
    for path in Path(options.inputdir).rglob(options.testImageDir):
        testRaw.extend(path.glob(options.pattern))
    testRaw.sort()
    return [{"image": str(image_name)} for image_name in testRaw]


def inputFilesSets_trainValidateFind(
    options: Namespace,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Returns a list of image+label filenames to use for training and
    a list to use for validation.
    """
    trainingSpace: list[dict[str, str]] = trainingData_prep(options)
    trainingSet: list[dict[str, str]] = trainingSpace[: -options.validateSize]
    validateSet: list[dict[str, str]] = trainingSpace[-options.validateSize :]
    return trainingSet, validateSet


def envDetail_print(options: Namespace, **kwargs):
    """
    Custom version of print_config() that suppresses the optional dependencies message.
    """
    if options.man:
        spl.manPage_print()
        sys.exit(1)
    print(DISPLAY_TITLE)
    f = Figlet(font="doom")
    print(f.renderText(f"{options.mode}"))
    print(f"Device = {options.device}")
    print_config()


def env_outputDirsMake(options: Namespace) -> None:
    params: TrainingParams = TrainingParams(options)
    if "training" in options.mode:
        params.preTrainingIO.mkdir(parents=True, exist_ok=True)
        params.whileTrainingIO.mkdir(parents=True, exist_ok=True)
        params.whileTrainingValidation.mkdir(parents=True, exist_ok=True)
        params.postTrainingValidation.mkdir(parents=True, exist_ok=True)
        params.postTrainingImageSpacings.mkdir(parents=True, exist_ok=True)
    if "inference" in options.mode:
        params.novelInference.mkdir(parents=True, exist_ok=True)


def modelFile_inputdirGet(options: Namespace) -> Path:
    modelTarget: Path = options.useModel
    inputDir: Path = Path(options.inputdir)
    modelFile: Path = Path("")
    path: Path
    for path in inputDir.rglob(str(modelTarget)):
        if path.is_file():
            modelFile = path
            break
    if not modelFile.exists():
        raise FileNotFoundError(f"The model '{modelFile}' does not exist.")
    return modelFile


def training_do(neuralNet: neuralnet.NeuralNet, options: Namespace) -> bool:
    trainingOK: bool = True

    neuralNet.trainingFileSet, neuralNet.validationFileSet = (
        inputFilesSets_trainValidateFind(options)
    )

    if not neuralNet.trainingTransformsAndSpace_setup():
        return False

    if options.mode == "training":
        neuralNet.train()
    if options.mode == "trainingContinue":
        neuralNet.train(modelFile_inputdirGet(options))

    plotting.plot_trainingMetrics(
        neuralNet.trainingLog,
        neuralNet.trainingParams,
        neuralNet.trainingParams.outputDir / "training" / "trainingLog.png",
    )

    neuralNet.bestModel_runOverValidationSpace()

    neuralNet.bestModel_evaluateImageSpacings()
    return trainingOK


def inference_do(neuralNet: neuralnet.NeuralNet, options: Namespace) -> bool:
    inferenceOK: bool = True
    neuralNet.testingFileSet = testingData_prep(options)

    neuralNet.infer_usingModel(modelFile_inputdirGet(options))

    return inferenceOK


def inference_pfmsDo(neuralNet: neuralnet.NeuralNet, options: Namespace) -> bool:
    # pudb.set_trace()
    neuralNet.testingFileSet = testingData_prep(options)
    remoteInfo: list[str] = options.mode.split("@")
    modelID: str = remoteInfo[0]
    url: str = remoteInfo[1]
    rpcOptions: Namespace = rpc.parser_interpret(rpc.parser_setup(""), asModule=True)
    rpcOptions.modelID = modelID
    rpcOptions.pfms = url
    rpcOptions.do = "infer"
    rpcOptions.outputdir = options.outputdir
    count: int
    inputDict: dict[str, str]
    for count, inputDict in enumerate(neuralNet.testingFileSet):
        rpcOptions.outputfile = f"output-{count}.nii.gz"
        rpcOptions.NIfTIfile = inputDict["image"]
        print(f"{rpcOptions.NIfTIfile:46} ━━━🭬 [{rpcOptions.pfms}] ━━━🭬 ", end="")
        remote = rpc.Rpc(rpcOptions)
        remote.do()


sparser = spl.parser_setup(description)


@chris_plugin(
    parser=sparser,
    title="Spleen 3D image segmentation (MONAI)",
    category="",  # ref. https://chrisstore.co/plugins
    min_memory_limit="24Gi",  # supported units: Mi, Gi
    min_cpu_limit="2000m",  # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=1,  # set min_gpu_limit=1 to enable GPU
    max_gpu_limit=2,
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """

    # pudb.set_trace()

    envDetail_print(options)
    env_outputDirsMake(options)
    neuralNet: neuralnet.NeuralNet = neuralnet.NeuralNet(options)

    if "training" in options.mode:
        training_do(neuralNet, options)

    if "inference" in options.mode:
        inference_do(neuralNet, options)

    if "http" in options.mode:
        inference_pfmsDo(neuralNet, options)


if __name__ == "__main__":
    main()
