from argparse import Namespace, ArgumentParser
from argparse import RawTextHelpFormatter
import sys

from spleenseg.spleenseg import __version__
from spleenseg.spleenseg import DISPLAY_TITLE


def parser_setup(str_desc):
    parser = ArgumentParser(description=str_desc, formatter_class=RawTextHelpFormatter)

    # JSONarg
    parser.add_argument(
        "--JSONargs",
        action="store",
        dest="JSONargString",
        type=str,
        default="",
        help="JSON equivalent of CLI key/values",
    )

    parser.add_argument(
        "--man",
        default=False,
        action="store_true",
        help="If specified, print a manual page",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="training",
        help="mode of behaviour: 'training', 'inference' or <remote>",
    )
    parser.add_argument(
        "--logTransformVols",
        default=False,
        action="store_true",
        help="If specified, save intermediary and inference data as NIfTI volumes",
    )
    parser.add_argument(
        "--useModel",
        type=str,
        default="model.pth",
        help="model to use for inference processing",
    )
    parser.add_argument(
        "--trainImageDir",
        type=str,
        default="imagesTr",
        help="name of directory containing training images",
    )
    parser.add_argument(
        "--trainLabelsDir",
        type=str,
        default="labelsTr",
        help="name of directory containing training labels",
    )
    parser.add_argument(
        "--testImageDir",
        type=str,
        default="imagesTs",
        help="name of directory containing test data",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="GPU/CPU device to use",
    )
    parser.add_argument(
        "--determinismSeed",
        type=int,
        default=42,
        help="the determinism seed for training/evaluation",
    )
    parser.add_argument(
        "--maxEpochs",
        type=int,
        default=600,
        help="max number of epochs to consider",
    )
    parser.add_argument(
        "--validateSize",
        type=int,
        default=9,
        help="size of the validation set in the input raw/label space",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="**/[!._]*nii.gz",
        help="filter glob for input files",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def parser_interpret(parser, *args, **kwargs):
    """
    Interpret the list space of *args, or sys.argv[1:] if
    *args is empty
    """
    asModule: bool = False
    for k, v in kwargs.items():
        if k == "asModule":
            asModule = v
    if asModule:
        # Here, spleenseg is used a module to another app
        # and the CLI sys.argv  is that of the parent app
        # not spleenseg. Interpret the passwd parser and
        # return.
        args, unknown = parser.parse_known_args()
        return args
    if len(args):
        args = parser.parse_args(*args)
    else:
        args = parser.parse_args(sys.argv[1:])
    return args


def parser_JSONinterpret(parser, d_JSONargs):
    """
    Interpret a JSON dictionary in lieu of CLI.

    For each <key>:<value> in the d_JSONargs, append to
    list two strings ["--<key>", "<value>"] and then
    argparse.
    """
    l_args = []
    for k, v in d_JSONargs.items():
        if isinstance(v, bool):
            if v:
                l_args.append("--%s" % k)
            continue
        l_args.append("--%s" % k)
        l_args.append("%s" % v)
    return parser_interpret(parser, l_args)


def manPage_print() -> None:
    print(DISPLAY_TITLE)
    print(
        f"""

    NAME

        spleenseg

    VERSION

        {__version__}

    SYNOPSIS

        spleenseg [--mode <inference|training>]                             \\
                  [--man]                                                   \\
                  [--version]                                               \\
                  [--logTransformVols]                                      \\
                  [--useModel <modelFile>]                                  \\
                  [--trainImageDir <train> --trainLabelsDir <label>]        \\
                  [--testImageDir <dir>]                                    \\
                  [--device <device>]                                       \\
                  [--determinismSeed <seed>]                                \\
                  [--maxEpochs <count>]                                     \\
                  [--validateSize <size>]                                   \\
                  <inputDir> <outputDir>

    DESCRIPTION

        "spleenseg" is a stand-alone app/ChRIS-plugin that can perform the training
        and inference modes on detecting the spleen from abdominal images. It is based
        on the project MONAI `spleen_segmentation` notebook exemplar. This app represents
        a complete rewrite of the notebook code to allow for more functionality, telemetry
        and re-usability.

    ARGS
        --mode <inference|training|[<model>@<remote>]>
        The mode of operation. If the actual text "training" text has any additional characters,
        then the epoch training is skipped and only the post-training logic is executed --
        this allows the system to operate as if in training mode, but only perform the post
        training steps. For example, "--mode trainingPost" would invoke this mode.

        If the mode is specified as <model>@<remote> (e.g. splsegv1@http://pfms.org/api/v1/)
        then the pfms server at (in this example) http://pfms.org with base route /api/v1/
        is used to perform remote inference. Here, the model called "splsegv1" on the remote
        pfms server will be used to run inference. The return from this call is a NIfTI
        segmented volume saved in the <outputDir>.

        [--man]
        If specified, print this help page and quit.

        [--version]
        If specified, print the version and quit.

        [--logTransformVols]
        If specified, log a set of intermediary NIfTI volumes as used for training,
        validation, spacing, and inference.

        [--useModel <modelFile>]
        If specified, use <modelFile> for inference or continued training.

        [--trainImageDir <train> --trainLabelsDir <label>]
        In the <inputDir>, the name of the directory containing files for training
        with their corresponding label targets.

        [--testImageDir]
        In the <inputDir> the name of the directory containing images for inference.

        [--device <device>]
        The device to use, typically "cpu" or "cuda:0".

        [--determinismSeed <seed>]
        Set the training seed.

        [--maxEpochs <count>]
        The max number of training epochs.

        [--validateSize <size>]
        In the training space, the number of images that should be used for validation
        and not training.

    """
    )
